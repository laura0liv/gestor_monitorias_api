from fastapi import HTTPException
from psycopg2.extras import RealDictCursor
from app.config.db_config import get_db_connection


class CalificacionController:

    def get_all_calificacions(self):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT
                    id_calificacion,
                    id_monitoria,
                    puntuacion,
                    comentario,
                    fecha_calificacion,
                    active,
                    created_at,
                    updated_at
                FROM calificacion
                WHERE active = true
            """)

            results = cursor.fetchall()

            return results

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=str(e)
            )

        finally:
            if conn:
                cursor.close()
                conn.close()

    def get_calificacion(self, id_calificacion: int):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT
                    id_calificacion,
                    id_monitoria,
                    puntuacion,
                    comentario,
                    fecha_calificacion,
                    active,
                    created_at,
                    updated_at
                FROM calificacion
                WHERE id_calificacion = %s
                AND active = true
            """, (id_calificacion,))

            result = cursor.fetchone()

            if not result:
                raise HTTPException(
                    status_code=404,
                    detail="Calificacion not found"
                )

            return result

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=str(e)
            )

        finally:
            if conn:
                cursor.close()
                conn.close()

    def create_calificacion(self, calificacion_data: dict):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                INSERT INTO calificacion (
                    id_monitoria,
                    puntuacion,
                    comentario,
                    fecha_calificacion,
                    active
                )
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id_calificacion
            """, (
                calificacion_data['id_monitoria'],
                calificacion_data['puntuacion'],
                calificacion_data['comentario'],
                calificacion_data['fecha_calificacion'],
                calificacion_data.get('active', True)
            ))

            new_calificacion = cursor.fetchone()

            conn.commit()

            return {
                "message": "Calificacion created successfully",
                "id_calificacion": new_calificacion["id_calificacion"]
            }

        except Exception as e:
            if conn:
                conn.rollback()

            raise HTTPException(
                status_code=500,
                detail=str(e)
            )

        finally:
            if conn:
                cursor.close()
                conn.close()

    def update_calificacion(self, id_calificacion: int, calificacion_data: dict):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE calificacion
                SET
                    id_monitoria = %s,
                    puntuacion = %s,
                    comentario = %s,
                    fecha_calificacion = %s,
                    active = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id_calificacion = %s
            """, (
                calificacion_data['id_monitoria'],
                calificacion_data['puntuacion'],
                calificacion_data['comentario'],
                calificacion_data['fecha_calificacion'],
                calificacion_data['active'],
                id_calificacion
            ))

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Calificacion not found"
                )

            conn.commit()

            return {
                "message": "Calificacion updated successfully"
            }

        except HTTPException:
            raise

        except Exception as e:
            if conn:
                conn.rollback()

            raise HTTPException(
                status_code=500,
                detail=str(e)
            )

        finally:
            if conn:
                cursor.close()
                conn.close()

    def delete_calificacion(self, id_calificacion: int):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE calificacion
                SET
                    active = false,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id_calificacion = %s
            """, (id_calificacion,))

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Calificacion not found"
                )

            conn.commit()

            return {
                "message": "Calificacion deleted successfully"
            }

        except HTTPException:
            raise

        except Exception as e:
            if conn:
                conn.rollback()

            raise HTTPException(
                status_code=500,
                detail=str(e)
            )

        finally:
            if conn:
                cursor.close()
                conn.close()