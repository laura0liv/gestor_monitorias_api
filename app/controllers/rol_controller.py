from fastapi import HTTPException
from psycopg2.extras import RealDictCursor
from config.db_config import get_db_connection


class RolController:

    def get_all_rol(self):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT
                    id_rol,
                    nombre_rol,
                    active,
                    created_at,
                    updated_at
                FROM rol
                WHERE active = true
            """)

            return cursor.fetchall()

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        finally:
            if conn:
                cursor.close()
                conn.close()

    def get_rol(self, id_rol: int):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT
                    id_rol,
                    nombre_rol,
                    active,
                    created_at,
                    updated_at
                FROM rol
                WHERE id_rol = %s
                AND active = true
            """, (id_rol,))

            result = cursor.fetchone()

            if not result:
                raise HTTPException(
                    status_code=404,
                    detail="Rol not found"
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

    def create_rol(self, rol_data: dict):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                INSERT INTO rol (
                    nombre_rol,
                    active
                )
                VALUES (%s, %s)
                RETURNING id_rol
            """, (
                rol_data['nombre_rol'],
                rol_data.get('active', True)
            ))

            new_data = cursor.fetchone()

            conn.commit()

            return {
                "message": "Rol created successfully",
                "id_rol": new_data["id_rol"]
            }

        except Exception as e:
            if conn:
                conn.rollback()

            raise HTTPException(status_code=500, detail=str(e))

        finally:
            if conn:
                cursor.close()
                conn.close()

    def update_rol(self, id_rol: int, rol_data: dict):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE rol
                SET
                    nombre_rol = %s,
                    active = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id_rol = %s
            """, (
                rol_data['nombre_rol'],
                rol_data['active'],
                id_rol
            ))

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Rol not found"
                )

            conn.commit()

            return {
                "message": "Rol updated successfully"
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

    def delete_rol(self, id_rol: int):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE rol
                SET
                    active = false,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id_rol = %s
            """, (id_rol,))

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Rol not found"
                )

            conn.commit()

            return {
                "message": "Rol deleted successfully"
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