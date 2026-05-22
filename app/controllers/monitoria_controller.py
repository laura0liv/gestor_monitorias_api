from fastapi import HTTPException
from psycopg2.extras import RealDictCursor
from app.config.db_config import get_db_connection


class MonitoriaController:

    # ─────────────────────────────────────────────
    # CONSULTAS GENERALES
    # ─────────────────────────────────────────────

    def get_all_monitorias(self):
        """Lista todas las monitorías activas (vista administrativa)."""
        try:
            with get_db_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute("""
                        SELECT
                            m.id_monitoria,
                            m.fecha,
                            m.hora_inicio,
                            m.hora_fin,
                            m.modalidad,
                            m.estado,
                            m.asistencia,
                            m.observaciones,
                            monitor.id_usuario   AS id_monitor,
                            monitor.nombre || ' ' || monitor.apellido AS monitor,
                            estudiante.id_usuario AS id_estudiante,
                            estudiante.nombre || ' ' || estudiante.apellido AS estudiante,
                            mat.id_materia,
                            mat.nombre_materia,
                            a.id_aula,
                            a.nombre_aula,
                            p.nombre_periodo
                        FROM monitoria m
                        INNER JOIN usuario monitor   ON monitor.id_usuario   = m.id_monitor
                        INNER JOIN usuario estudiante ON estudiante.id_usuario = m.id_estudiante
                        INNER JOIN materia mat        ON mat.id_materia       = m.id_materia
                        LEFT  JOIN aula a             ON a.id_aula            = m.id_aula
                        LEFT  JOIN periodo_academico p ON p.id_periodo        = m.id_periodo
                        WHERE m.active = true
                        ORDER BY m.fecha DESC, m.hora_inicio
                    """)
                    return cursor.fetchall()

        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Error obteniendo monitorías")

    # ─────────────────────────────────────────────
    # MÓDULO ESTUDIANTE
    # ─────────────────────────────────────────────

    def get_tutores_disponibles(self, id_materia: int, fecha: str, hora_inicio: str, hora_fin: str):
        """
        Devuelve los tutores que:
          1. Están asignados a la materia solicitada.
          2. Tienen un horario registrado que cubre el bloque pedido en ese día de la semana.
          3. NO tienen otra monitoría activa (Pendiente o Programada) que se solape en esa fecha/hora.
        """
        try:
            with get_db_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute("""
                        SELECT
                            u.id_usuario  AS id_monitor,
                            u.nombre || ' ' || u.apellido AS nombre_monitor,
                            u.correo,
                            u.telefono,
                            hm.dia_semana,
                            hm.hora_inicio AS disponible_desde,
                            hm.hora_fin    AS disponible_hasta
                        FROM monitor_materia mm
                        INNER JOIN usuario u ON u.id_usuario = mm.id_monitor
                        INNER JOIN horario_monitor hm ON hm.id_monitor = mm.id_monitor
                        WHERE mm.id_materia = %s
                          AND mm.active     = true
                          AND u.active      = true
                          AND hm.active     = true
                          -- El día de la semana del horario coincide con la fecha pedida
                          AND hm.dia_semana = TO_CHAR(DATE %s, 'TMDay')
                          -- El horario del tutor cubre completamente el bloque pedido
                          AND hm.hora_inicio <= %s::time
                          AND hm.hora_fin    >= %s::time
                          -- El tutor NO tiene conflicto de monitoría en esa fecha/hora
                          AND NOT EXISTS (
                              SELECT 1
                              FROM monitoria conf
                              WHERE conf.id_monitor = u.id_usuario
                                AND conf.fecha      = DATE %s
                                AND conf.hora_inicio < %s::time
                                AND conf.hora_fin   > %s::time
                                AND conf.estado IN ('Pendiente', 'Programada')
                                AND conf.active = true
                          )
                        ORDER BY u.nombre
                    """, (
                        id_materia,
                        fecha,
                        hora_inicio, hora_fin,   # cubre el bloque
                        fecha,
                        hora_fin, hora_inicio    # sin conflicto
                    ))
                    tutores = cursor.fetchall()

                    if not tutores:
                        raise HTTPException(
                            status_code=404,
                            detail="No hay tutores disponibles para esa materia en el horario solicitado"
                        )

                    return tutores

        except HTTPException:
            raise
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Error consultando tutores disponibles")

    def get_monitorias_estudiante(self, id_estudiante: int):
        """Devuelve todas las monitorías del estudiante con detalle completo."""
        try:
            with get_db_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute("""
                        SELECT
                            m.id_monitoria,
                            m.fecha,
                            m.hora_inicio,
                            m.hora_fin,
                            m.modalidad,
                            m.estado,
                            m.asistencia,
                            m.observaciones,
                            monitor.id_usuario  AS id_monitor,
                            monitor.nombre || ' ' || monitor.apellido AS monitor,
                            monitor.correo      AS correo_monitor,
                            monitor.telefono    AS telefono_monitor,
                            mat.nombre_materia,
                            a.nombre_aula,
                            a.bloque,
                            p.nombre_periodo
                        FROM monitoria m
                        INNER JOIN usuario monitor  ON monitor.id_usuario = m.id_monitor
                        INNER JOIN materia mat       ON mat.id_materia     = m.id_materia
                        LEFT  JOIN aula a            ON a.id_aula          = m.id_aula
                        LEFT  JOIN periodo_academico p ON p.id_periodo     = m.id_periodo
                        WHERE m.id_estudiante = %s
                          AND m.active = true
                        ORDER BY m.fecha DESC, m.hora_inicio
                    """, (id_estudiante,))
                    return cursor.fetchall()

        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Error obteniendo monitorías del estudiante")

    def solicitar_monitoria(self, monitoria_data: dict):
        try:
            with get_db_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:

                    # 1. Tutor asignado a la materia
                    cursor.execute("""
                        SELECT 1
                        FROM monitor_materia
                        WHERE id_monitor = %s
                        AND id_materia = %s
                        AND active     = true
                    """, (monitoria_data["id_monitor"], monitoria_data["id_materia"]))

                    if not cursor.fetchone():
                        raise HTTPException(
                            status_code=400,
                            detail="El tutor no está asignado a esa materia"
                        )

                    # 2. Tutor tiene horario disponible ese día/hora
                    cursor.execute("""
                        SELECT 1
                        FROM horario_monitor
                        WHERE id_monitor = %s
                        AND dia_semana = (
                            CASE EXTRACT(DOW FROM DATE %s)::int
                                WHEN 0 THEN 'Domingo'
                                WHEN 1 THEN 'Lunes'
                                WHEN 2 THEN 'Martes'
                                WHEN 3 THEN 'Miércoles'
                                WHEN 4 THEN 'Jueves'
                                WHEN 5 THEN 'Viernes'
                                WHEN 6 THEN 'Sábado'
                            END
                        )
                        AND hora_inicio <= %s::time
                        AND hora_fin    >= %s::time
                        AND active      = true
                    """, (
                        monitoria_data["id_monitor"],
                        monitoria_data["fecha"],
                        monitoria_data["hora_inicio"],
                        monitoria_data["hora_fin"]
                    ))

                    if not cursor.fetchone():          # ← faltaba esto
                        raise HTTPException(
                            status_code=400,
                            detail="El tutor no tiene disponibilidad en ese horario"
                        )

                    # 3. Sin conflicto para el TUTOR
                    cursor.execute("""
                        SELECT 1
                        FROM monitoria
                        WHERE id_monitor  = %s
                        AND fecha       = DATE %s
                        AND hora_inicio < %s::time
                        AND hora_fin    > %s::time
                        AND estado IN ('Pendiente', 'Programada')
                        AND active = true
                    """, (
                        monitoria_data["id_monitor"],
                        monitoria_data["fecha"],
                        monitoria_data["hora_fin"],
                        monitoria_data["hora_inicio"]
                    ))

                    if cursor.fetchone():
                        raise HTTPException(
                            status_code=400,
                            detail="El tutor ya tiene una monitoría en ese horario"
                        )

                    # 4. Sin conflicto para el ESTUDIANTE
                    cursor.execute("""
                        SELECT 1
                        FROM monitoria
                        WHERE id_estudiante = %s
                        AND fecha         = DATE %s
                        AND hora_inicio   < %s::time
                        AND hora_fin      > %s::time
                        AND estado IN ('Pendiente', 'Programada')
                        AND active = true
                    """, (
                        monitoria_data["id_estudiante"],
                        monitoria_data["fecha"],
                        monitoria_data["hora_fin"],
                        monitoria_data["hora_inicio"]
                    ))

                    if cursor.fetchone():
                        raise HTTPException(
                            status_code=400,
                            detail="Ya tienes una monitoría registrada en ese horario"
                        )

                    # 5. Insertar
                    cursor.execute("""
                        INSERT INTO monitoria (
                            id_monitor, id_estudiante, id_materia, id_aula,
                            fecha, hora_inicio, hora_fin,
                            modalidad, estado, id_periodo,
                            asistencia, observaciones, active
                        ) VALUES (
                            %s, %s, %s, %s,
                            %s, %s, %s,
                            %s, 'Pendiente', %s,
                            false, %s, true
                        )
                        RETURNING id_monitoria
                    """, (
                        monitoria_data["id_monitor"],
                        monitoria_data["id_estudiante"],
                        monitoria_data["id_materia"],
                        monitoria_data.get("id_aula"),
                        monitoria_data["fecha"],
                        monitoria_data["hora_inicio"],
                        monitoria_data["hora_fin"],
                        monitoria_data["modalidad"],
                        monitoria_data["id_periodo"],
                        monitoria_data.get("observaciones")
                    ))

                    new = cursor.fetchone()
                    conn.commit()

                    return {
                        "message": "Monitoría solicitada correctamente. Queda pendiente de aceptación del tutor.",
                        "id_monitoria": new["id_monitoria"]
                    }

        except HTTPException:
            raise
        except Exception as e:
            import traceback
            traceback.print_exc()  # ← esto en los logs de Render te dirá la línea exacta
            raise HTTPException(status_code=500, detail=str(e))  # ← muestra el error real

    def cancelar_monitoria_estudiante(self, id_monitoria: int, id_estudiante: int):
        """El estudiante cancela una monitoría propia que aún esté Pendiente."""
        try:
            with get_db_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:

                    cursor.execute("""
                        SELECT estado, id_estudiante
                        FROM monitoria
                        WHERE id_monitoria = %s AND active = true
                    """, (id_monitoria,))

                    monitoria = cursor.fetchone()

                    if not monitoria:
                        raise HTTPException(status_code=404, detail="Monitoría no encontrada")

                    if monitoria["id_estudiante"] != id_estudiante:
                        raise HTTPException(status_code=403, detail="No tienes permiso para cancelar esta monitoría")

                    if monitoria["estado"] not in ("Pendiente",):
                        raise HTTPException(
                            status_code=400,
                            detail=f"No se puede cancelar una monitoría en estado '{monitoria['estado']}'"
                        )

                    cursor.execute("""
                        UPDATE monitoria
                        SET estado = 'Cancelada', updated_at = CURRENT_TIMESTAMP
                        WHERE id_monitoria = %s
                    """, (id_monitoria,))

                    conn.commit()
                    return {"message": "Monitoría cancelada correctamente"}

        except HTTPException:
            raise
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Error al cancelar la monitoría")

    # ─────────────────────────────────────────────
    # MÓDULO TUTOR
    # ─────────────────────────────────────────────

    def get_monitorias_tutor(self, id_monitor: int):
        """Devuelve todas las monitorías asignadas al tutor con detalle completo."""
        try:
            with get_db_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute("""
                        SELECT
                            m.id_monitoria,
                            m.fecha,
                            m.hora_inicio,
                            m.hora_fin,
                            m.modalidad,
                            m.estado,
                            m.asistencia,
                            m.observaciones,
                            estudiante.id_usuario   AS id_estudiante,
                            estudiante.nombre || ' ' || estudiante.apellido AS estudiante,
                            estudiante.correo        AS correo_estudiante,
                            estudiante.telefono      AS telefono_estudiante,
                            mat.nombre_materia,
                            a.nombre_aula,
                            a.bloque,
                            p.nombre_periodo
                        FROM monitoria m
                        INNER JOIN usuario estudiante ON estudiante.id_usuario = m.id_estudiante
                        INNER JOIN materia mat         ON mat.id_materia       = m.id_materia
                        LEFT  JOIN aula a              ON a.id_aula            = m.id_aula
                        LEFT  JOIN periodo_academico p ON p.id_periodo         = m.id_periodo
                        WHERE m.id_monitor = %s
                          AND m.active     = true
                        ORDER BY m.fecha DESC, m.hora_inicio
                    """, (id_monitor,))
                    return cursor.fetchall()

        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Error obteniendo monitorías del tutor")

    def get_monitorias_tutor_pendientes(self, id_monitor: int):
        """Monitorías pendientes de aceptación para el tutor."""
        try:
            with get_db_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute("""
                        SELECT
                            m.id_monitoria,
                            m.fecha,
                            m.hora_inicio,
                            m.hora_fin,
                            m.modalidad,
                            m.observaciones,
                            estudiante.nombre || ' ' || estudiante.apellido AS estudiante,
                            estudiante.correo   AS correo_estudiante,
                            mat.nombre_materia
                        FROM monitoria m
                        INNER JOIN usuario estudiante ON estudiante.id_usuario = m.id_estudiante
                        INNER JOIN materia mat         ON mat.id_materia       = m.id_materia
                        WHERE m.id_monitor = %s
                          AND m.estado     = 'Pendiente'
                          AND m.active     = true
                        ORDER BY m.fecha, m.hora_inicio
                    """, (id_monitor,))
                    return cursor.fetchall()

        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Error obteniendo monitorías pendientes")

    def responder_monitoria(self, id_monitoria: int, id_monitor: int, accion: str, observaciones: str = None):
        """
        El tutor acepta o rechaza una monitoría pendiente.
        accion: 'Programada' | 'Rechazada'
        """
        if accion not in ("Programada", "Rechazada"):
            raise HTTPException(status_code=400, detail="Acción inválida. Use 'Programada' o 'Rechazada'")

        try:
            with get_db_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:

                    cursor.execute("""
                        SELECT estado, id_monitor
                        FROM monitoria
                        WHERE id_monitoria = %s AND active = true
                    """, (id_monitoria,))

                    monitoria = cursor.fetchone()

                    if not monitoria:
                        raise HTTPException(status_code=404, detail="Monitoría no encontrada")

                    if monitoria["id_monitor"] != id_monitor:
                        raise HTTPException(status_code=403, detail="No tienes permiso para responder esta monitoría")

                    if monitoria["estado"] != "Pendiente":
                        raise HTTPException(
                            status_code=400,
                            detail=f"Solo se pueden responder monitorías Pendientes. Estado actual: '{monitoria['estado']}'"
                        )

                    cursor.execute("""
                        UPDATE monitoria
                        SET estado       = %s,
                            observaciones = COALESCE(%s, observaciones),
                            updated_at   = CURRENT_TIMESTAMP
                        WHERE id_monitoria = %s
                    """, (accion, observaciones, id_monitoria))

                    conn.commit()

                    mensaje = "Monitoría Programada correctamente" if accion == "Programada" else "Monitoría rechazada"
                    return {"message": mensaje}

        except HTTPException:
            raise
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Error al responder la monitoría")

    def registrar_asistencia(self, id_monitoria: int, id_monitor: int, asistencia: bool, observaciones: str = None):
        """El tutor registra si el estudiante asistió a la monitoría (estado debe ser 'Programada')."""
        try:
            with get_db_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:

                    cursor.execute("""
                        SELECT estado, id_monitor
                        FROM monitoria
                        WHERE id_monitoria = %s AND active = true
                    """, (id_monitoria,))

                    monitoria = cursor.fetchone()

                    if not monitoria:
                        raise HTTPException(status_code=404, detail="Monitoría no encontrada")

                    if monitoria["id_monitor"] != id_monitor:
                        raise HTTPException(status_code=403, detail="No tienes permiso para registrar asistencia en esta monitoría")

                    if monitoria["estado"] != "Programada":
                        raise HTTPException(
                            status_code=400,
                            detail="Solo se puede registrar asistencia en monitorías Programadas"
                        )

                    cursor.execute("""
                        UPDATE monitoria
                        SET asistencia    = %s,
                            estado        = 'Completada',
                            observaciones = COALESCE(%s, observaciones),
                            updated_at    = CURRENT_TIMESTAMP
                        WHERE id_monitoria = %s
                    """, (asistencia, observaciones, id_monitoria))

                    conn.commit()
                    return {"message": "Asistencia registrada y monitoría marcada como Completada"}

        except HTTPException:
            raise
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Error al registrar asistencia")

    # ─────────────────────────────────────────────
    # CRUD GENERAL (admin)
    # ─────────────────────────────────────────────

    def get_monitoria(self, id_monitoria: int):
        try:
            with get_db_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute("""
                        SELECT
                            m.*,
                            monitor.nombre || ' ' || monitor.apellido AS monitor,
                            estudiante.nombre || ' ' || estudiante.apellido AS estudiante,
                            mat.nombre_materia,
                            a.nombre_aula,
                            p.nombre_periodo
                        FROM monitoria m
                        INNER JOIN usuario monitor   ON monitor.id_usuario   = m.id_monitor
                        INNER JOIN usuario estudiante ON estudiante.id_usuario = m.id_estudiante
                        INNER JOIN materia mat        ON mat.id_materia       = m.id_materia
                        LEFT  JOIN aula a             ON a.id_aula            = m.id_aula
                        LEFT  JOIN periodo_academico p ON p.id_periodo        = m.id_periodo
                        WHERE m.id_monitoria = %s AND m.active = true
                    """, (id_monitoria,))

                    result = cursor.fetchone()

                    if not result:
                        raise HTTPException(status_code=404, detail="Monitoría no encontrada")

                    return result

        except HTTPException:
            raise
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Error obteniendo monitoría")

    def update_monitoria(self, id_monitoria: int, monitoria_data: dict):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        UPDATE monitoria
                        SET
                            id_monitor    = %s,
                            id_estudiante = %s,
                            id_materia    = %s,
                            id_aula       = %s,
                            fecha         = %s,
                            hora_inicio   = %s,
                            hora_fin      = %s,
                            modalidad     = %s,
                            estado        = %s,
                            id_periodo    = %s,
                            asistencia    = %s,
                            observaciones = %s,
                            updated_at    = CURRENT_TIMESTAMP
                        WHERE id_monitoria = %s AND active = true
                    """, (
                        monitoria_data["id_monitor"],
                        monitoria_data["id_estudiante"],
                        monitoria_data["id_materia"],
                        monitoria_data.get("id_aula"),
                        monitoria_data["fecha"],
                        monitoria_data["hora_inicio"],
                        monitoria_data["hora_fin"],
                        monitoria_data["modalidad"],
                        monitoria_data["estado"],
                        monitoria_data["id_periodo"],
                        monitoria_data.get("asistencia"),
                        monitoria_data.get("observaciones"),
                        id_monitoria
                    ))

                    if cursor.rowcount == 0:
                        raise HTTPException(status_code=404, detail="Monitoría no encontrada")

                    conn.commit()
                    return {"message": "Monitoría actualizada correctamente"}

        except HTTPException:
            raise
        except Exception as e:
            if conn:
                conn.rollback()
            print(e)
            raise HTTPException(status_code=500, detail="Error actualizando monitoría")

    def delete_monitoria(self, id_monitoria: int):
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        UPDATE monitoria
                        SET active = false, updated_at = CURRENT_TIMESTAMP
                        WHERE id_monitoria = %s AND active = true
                    """, (id_monitoria,))

                    if cursor.rowcount == 0:
                        raise HTTPException(status_code=404, detail="Monitoría no encontrada")

                    conn.commit()
                    return {"message": "Monitoría eliminada correctamente"}

        except HTTPException:
            raise
        except Exception as e:
            if conn:
                conn.rollback()
            print(e)
            raise HTTPException(status_code=500, detail="Error eliminando monitoría")