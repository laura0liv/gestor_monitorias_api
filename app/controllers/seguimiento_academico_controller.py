from fastapi import HTTPException
from psycopg2.extras import RealDictCursor
from app.config.db_config import get_db_connection


class SeguimientoAcademicoController:

    def get_all_seguimiento_academico(self):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT
                    id_seguimiento,
                    id_estudiante,
                    id_monitor,
                    id_periodo,
                    fecha_inicio,
                    nivel_riesgo,
                    motivo,
                    plan_acompanamiento,
                    resultado,
                    estado,
                    fecha_cierre,
                    active,
                    created_at,
                    updated_at
                FROM seguimiento_academico
                WHERE active = true
            """)

            return cursor.fetchall()

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        finally:
            if conn:
                cursor.close()
                conn.close()

    def get_seguimiento_academico(self, id_seguimiento: int):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT
                    id_seguimiento,
                    id_estudiante,
                    id_monitor,
                    id_periodo,
                    fecha_inicio,
                    nivel_riesgo,
                    motivo,
                    plan_acompanamiento,
                    resultado,
                    estado,
                    fecha_cierre,
                    active,
                    created_at,
                    updated_at
                FROM seguimiento_academico
                WHERE id_seguimiento = %s
                AND active = true
            """, (id_seguimiento,))

            result = cursor.fetchone()

            if not result:
                raise HTTPException(
                    status_code=404,
                    detail="Seguimiento académico not found"
                )

            return result

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        finally:
            if conn:
                cursor.close()
                conn.close()

    def create_seguimiento_academico(self, seguimiento_academico_data: dict):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                INSERT INTO seguimiento_academico (
                    id_estudiante,
                    id_monitor,
                    id_periodo,
                    fecha_inicio,
                    nivel_riesgo,
                    motivo,
                    plan_acompanamiento,
                    resultado,
                    estado,
                    fecha_cierre,
                    active
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id_seguimiento
            """, (
                seguimiento_academico_data['id_estudiante'],
                seguimiento_academico_data['id_monitor'],
                seguimiento_academico_data['id_periodo'],
                seguimiento_academico_data['fecha_inicio'],
                seguimiento_academico_data.get('nivel_riesgo'),
                seguimiento_academico_data.get('motivo'),
                seguimiento_academico_data['plan_acompanamiento'],
                seguimiento_academico_data['resultado'],
                seguimiento_academico_data['estado'],
                seguimiento_academico_data.get('fecha_cierre'),
                seguimiento_academico_data.get('active', True)
            ))

            new_data = cursor.fetchone()

            conn.commit()

            return {
                "message": "Seguimiento académico created successfully",
                "id_seguimiento": new_data["id_seguimiento"]
            }

        except Exception as e:
            if conn:
                conn.rollback()

            raise HTTPException(status_code=500, detail=str(e))

        finally:
            if conn:
                cursor.close()
                conn.close()

    def update_seguimiento_academico(
        self,
        id_seguimiento: int,
        seguimiento_academico_data: dict
    ):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE seguimiento_academico
                SET
                    id_estudiante = %s,
                    id_monitor = %s,
                    id_periodo = %s,
                    fecha_inicio = %s,
                    nivel_riesgo = %s,
                    motivo = %s,
                    plan_acompanamiento = %s,
                    resultado = %s,
                    estado = %s,
                    fecha_cierre = %s,
                    active = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id_seguimiento = %s
            """, (
                seguimiento_academico_data['id_estudiante'],
                seguimiento_academico_data['id_monitor'],
                seguimiento_academico_data['id_periodo'],
                seguimiento_academico_data['fecha_inicio'],
                seguimiento_academico_data.get('nivel_riesgo'),
                seguimiento_academico_data.get('motivo'),
                seguimiento_academico_data['plan_acompanamiento'],
                seguimiento_academico_data['resultado'],
                seguimiento_academico_data['estado'],
                seguimiento_academico_data.get('fecha_cierre'),
                seguimiento_academico_data['active'],
                id_seguimiento
            ))

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Seguimiento académico not found"
                )

            conn.commit()

            return {
                "message": "Seguimiento académico updated successfully"
            }

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

    def delete_seguimiento_academico(self, id_seguimiento: int):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE seguimiento_academico
                SET
                    active = false,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id_seguimiento = %s
            """, (id_seguimiento,))

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Seguimiento académico not found"
                )

            conn.commit()

            return {
                "message": "Seguimiento académico deleted successfully"
            }

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