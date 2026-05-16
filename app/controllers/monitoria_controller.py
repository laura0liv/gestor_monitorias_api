from fastapi import HTTPException
from psycopg2.extras import RealDictCursor
from app.config.db_config import get_db_connection


class MonitoriaController:

    def get_all_monitorias(self):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT
                    id_monitoria,
                    nombre_monitoria,
                    fecha_inicio,
                    fecha_fin,
                    active,
                    created_at,
                    updated_at
                FROM monitoria
                WHERE active = true
            """)

            return cursor.fetchall()

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=str(e)
            )

        finally:
            if conn:
                cursor.close()
                conn.close()

    def get_monitoria(self, id_monitoria: int):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT
                    id_monitoria,
                    nombre_monitoria,
                    fecha_inicio,
                    fecha_fin,
                    active,
                    created_at,
                    updated_at
                FROM monitoria
                WHERE id_monitoria = %s
                AND active = true
            """, (id_monitoria,))

            result = cursor.fetchone()

            if not result:
                raise HTTPException(
                    status_code=404,
                    detail="Monitoria not found"
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

    def create_monitoria(self, monitoria_data: dict):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                INSERT INTO monitoria (
                    nombre_monitoria,
                    fecha_inicio,
                    fecha_fin,
                    active
                )
                VALUES (%s, %s, %s, %s)
                RETURNING id_monitoria
            """, (
                monitoria_data['nombre_monitoria'],
                monitoria_data['fecha_inicio'],
                monitoria_data['fecha_fin'],
                monitoria_data.get('active', True)
            ))

            new_data = cursor.fetchone()

            conn.commit()

            return {
                "message": "Monitoria created successfully",
                "id_monitoria": new_data["id_monitoria"]
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

    def update_monitoria(self, id_monitoria: int, monitoria_data: dict):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE monitoria
                SET
                    nombre_monitoria = %s,
                    fecha_inicio = %s,
                    fecha_fin = %s,
                    active = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id_monitoria = %s
            """, (
                monitoria_data['nombre_monitoria'],
                monitoria_data['fecha_inicio'],
                monitoria_data['fecha_fin'],
                monitoria_data['active'],
                id_monitoria
            ))

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Monitoria not found"
                )

            conn.commit()

            return {
                "message": "Monitoria updated successfully"
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

    def delete_monitoria(self, id_monitoria: int):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE monitoria
                SET
                    active = false,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id_monitoria = %s
            """, (id_monitoria,))

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Monitoria not found"
                )

            conn.commit()

            return {
                "message": "Monitoria deleted successfully"
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