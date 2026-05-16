from fastapi import HTTPException
from psycopg2.extras import RealDictCursor
from app.config.db_config import get_db_connection


class SesionSeguimientoController:

    def get_all_sesion_seguimiento(self):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT
                    id_sesion,
                    id_seguimiento,
                    fecha,
                    observaciones,
                    avance,
                    active,
                    created_at,
                    updated_at
                FROM sesion_seguimiento
                WHERE active = true
            """)

            return cursor.fetchall()

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        finally:
            if conn:
                cursor.close()
                conn.close()

    def get_sesion_seguimiento(self, id_sesion: int):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT
                    id_sesion,
                    id_seguimiento,
                    fecha,
                    observaciones,
                    avance,
                    active,
                    created_at,
                    updated_at
                FROM sesion_seguimiento
                WHERE id_sesion = %s
                AND active = true
            """, (id_sesion,))

            result = cursor.fetchone()

            if not result:
                raise HTTPException(
                    status_code=404,
                    detail="SesionSeguimiento not found"
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

    def create_sesion_seguimiento(self, sesion_seguimiento_data: dict):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                INSERT INTO sesion_seguimiento (
                    id_seguimiento,
                    fecha,
                    observaciones,
                    avance,
                    active
                )
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id_sesion
            """, (
                sesion_seguimiento_data['id_seguimiento'],
                sesion_seguimiento_data['fecha'],
                sesion_seguimiento_data['observaciones'],
                sesion_seguimiento_data['avance'],
                sesion_seguimiento_data.get('active', True)
            ))

            new_data = cursor.fetchone()

            conn.commit()

            return {
                "message": "SesionSeguimiento created successfully",
                "id_sesion": new_data["id_sesion"]
            }

        except Exception as e:
            if conn:
                conn.rollback()

            raise HTTPException(status_code=500, detail=str(e))

        finally:
            if conn:
                cursor.close()
                conn.close()

    def update_sesion_seguimiento(
        self,
        id_sesion: int,
        sesion_seguimiento_data: dict
    ):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE sesion_seguimiento
                SET
                    id_seguimiento = %s,
                    fecha = %s,
                    observaciones = %s,
                    avance = %s,
                    active = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id_sesion = %s
            """, (
                sesion_seguimiento_data['id_seguimiento'],
                sesion_seguimiento_data['fecha'],
                sesion_seguimiento_data['observaciones'],
                sesion_seguimiento_data['avance'],
                sesion_seguimiento_data['active'],
                id_sesion
            ))

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="SesionSeguimiento not found"
                )

            conn.commit()

            return {
                "message": "SesionSeguimiento updated successfully"
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

    def delete_sesion_seguimiento(self, id_sesion: int):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE sesion_seguimiento
                SET
                    active = false,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id_sesion = %s
            """, (id_sesion,))

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="SesionSeguimiento not found"
                )

            conn.commit()

            return {
                "message": "SesionSeguimiento deleted successfully"
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