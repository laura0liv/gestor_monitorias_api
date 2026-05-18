from fastapi import HTTPException
from psycopg2.extras import RealDictCursor
from app.config.db_config import get_db_connection


class HorarioMonitorController:

    def get_all_horario_monitors(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("""
                SELECT
                    id_horario,
                    id_monitor,
                    dia_semana,
                    TO_CHAR(hora_inicio, 'HH24:MI') AS hora_inicio,
                    TO_CHAR(hora_fin,    'HH24:MI') AS hora_fin,
                    active,
                    created_at,
                    updated_at
                FROM horario_monitor
                WHERE active = true
            """)
            return cursor.fetchall()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if conn:
                cursor.close()
                conn.close()

    def get_horario_monitor(self, id_horario: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("""
                SELECT
                    id_horario,
                    id_monitor,
                    dia_semana,
                    TO_CHAR(hora_inicio, 'HH24:MI') AS hora_inicio,
                    TO_CHAR(hora_fin,    'HH24:MI') AS hora_fin,
                    active,
                    created_at,
                    updated_at
                FROM horario_monitor
                WHERE id_horario = %s AND active = true
            """, (id_horario,))
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Horario Monitor not found")
            return result
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if conn:
                cursor.close()
                conn.close()

    def create_horario_monitor(self, horario_monitor_data: dict):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("""
                INSERT INTO horario_monitor (
                    id_monitor, dia_semana, hora_inicio, hora_fin, active
                )
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id_horario
            """, (
                horario_monitor_data['id_monitor'],
                horario_monitor_data['dia_semana'],
                horario_monitor_data['hora_inicio'],
                horario_monitor_data['hora_fin'],
                horario_monitor_data.get('active', True)
            ))
            new_data = cursor.fetchone()
            conn.commit()
            return {
                "message": "Horario Monitor created successfully",
                "id_horario": new_data["id_horario"]
            }
        except Exception as e:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if conn:
                cursor.close()
                conn.close()

    def update_horario_monitor(self, id_horario: int, horario_monitor_data: dict):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE horario_monitor
                SET
                    id_monitor  = %s,
                    dia_semana  = %s,
                    hora_inicio = %s,
                    hora_fin    = %s,
                    active      = %s,
                    updated_at  = CURRENT_TIMESTAMP
                WHERE id_horario = %s
            """, (
                horario_monitor_data['id_monitor'],
                horario_monitor_data['dia_semana'],
                horario_monitor_data['hora_inicio'],
                horario_monitor_data['hora_fin'],
                horario_monitor_data['active'],
                id_horario
            ))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Horario Monitor not found")
            conn.commit()
            return {"message": "Horario Monitor updated successfully"}
        except HTTPException:
            raise
        except Exception as e:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if conn:
                cursor.close()
                conn.close()

    def delete_horario_monitor(self, id_horario: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE horario_monitor
                SET active = false, updated_at = CURRENT_TIMESTAMP
                WHERE id_horario = %s
            """, (id_horario,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Horario Monitor not found")
            conn.commit()
            return {"message": "Horario Monitor deleted successfully"}
        except HTTPException:
            raise
        except Exception as e:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if conn:
                cursor.close()
                conn.close()

    def get_horarios_by_monitor(self, id_monitor: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("""
                SELECT
                    id_horario,
                    id_monitor,
                    dia_semana,
                    TO_CHAR(hora_inicio, 'HH24:MI') AS hora_inicio,
                    TO_CHAR(hora_fin,    'HH24:MI') AS hora_fin
                FROM horario_monitor
                WHERE id_monitor = %s AND active = true
            """, (id_monitor,))
            return cursor.fetchall()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if conn:
                cursor.close()
                conn.close()

    def delete_horarios_by_monitor(self, id_monitor: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE horario_monitor
                SET active = false, updated_at = CURRENT_TIMESTAMP
                WHERE id_monitor = %s AND active = true
            """, (id_monitor,))
            conn.commit()
            return {"message": "Horarios eliminados correctamente"}
        except Exception as e:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if conn:
                cursor.close()
                conn.close()

    # ─────────────────────────────────────────────────────────
    # NUEVO — consumido por SolicitarMonitoria.svelte (paso 3)
    # GET /disponibilidad/get_disponibilidad/{id_monitor}
    #
    # Retorna solo los slots que NO tienen monitoría activa
    # (Pendiente o Programada) en la próxima ocurrencia de ese día.
    # Campos: dia_semana, hora_inicio "HH:MM", hora_fin "HH:MM"
    # ─────────────────────────────────────────────────────────

    def get_disponibilidad_monitor(self, id_monitor: int):
        """
        Para cada bloque de horario_monitor del monitor verifica que
        no exista una monitoría activa (Pendiente | Programada) en la
        próxima fecha de ese día de la semana.
        Solo retorna los slots libres.
        """
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("""
                WITH proximas AS (
                    -- Calcula la próxima fecha de cada bloque registrado
                    SELECT
                        hm.id_horario,
                        hm.dia_semana,
                        TO_CHAR(hm.hora_inicio, 'HH24:MI') AS hora_inicio,
                        TO_CHAR(hm.hora_fin,    'HH24:MI') AS hora_fin,
                        hm.hora_inicio  AS hi_raw,
                        hm.hora_fin     AS hf_raw,
                        (
                            CURRENT_DATE + (
                                (
                                    CASE hm.dia_semana
                                        WHEN 'Lunes'      THEN 1
                                        WHEN 'Martes'     THEN 2
                                        WHEN 'Miércoles'  THEN 3
                                        WHEN 'Jueves'     THEN 4
                                        WHEN 'Viernes'    THEN 5
                                        WHEN 'Sábado'     THEN 6
                                        WHEN 'Domingo'    THEN 0
                                    END
                                    - EXTRACT(DOW FROM CURRENT_DATE)::int + 7
                                ) %% 7
                            )
                        )::date AS proxima_fecha
                    FROM horario_monitor hm
                    WHERE hm.id_monitor = %s
                      AND hm.active     = true
                )
                SELECT p.dia_semana, p.hora_inicio, p.hora_fin
                FROM proximas p
                WHERE NOT EXISTS (
                    SELECT 1
                    FROM monitoria m
                    WHERE m.id_monitor  = %s
                      AND m.fecha       = p.proxima_fecha
                      AND m.hora_inicio < p.hf_raw
                      AND m.hora_fin    > p.hi_raw
                      AND m.estado IN ('Pendiente', 'Programada')
                      AND m.active = true
                )
                ORDER BY
                    CASE p.dia_semana
                        WHEN 'Lunes'     THEN 1
                        WHEN 'Martes'    THEN 2
                        WHEN 'Miércoles' THEN 3
                        WHEN 'Jueves'    THEN 4
                        WHEN 'Viernes'   THEN 5
                        WHEN 'Sábado'    THEN 6
                        WHEN 'Domingo'   THEN 7
                    END,
                    p.hi_raw
            """, (id_monitor, id_monitor))
            return cursor.fetchall()
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Error obteniendo disponibilidad del monitor")
        finally:
            if conn:
                cursor.close()
                conn.close()