from fastapi import HTTPException
from psycopg2.extras import RealDictCursor
from app.config.db_config import get_db_connection


class AulaController:

    def get_all_aula(self):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT 
                    id_aula,
                    nombre_aula,
                    bloque,
                    capacidad,
                    active,
                    created_at,
                    updated_at
                FROM aula
                WHERE active = true;
            """)

            results = cursor.fetchall()

            return results

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        finally:
            if conn:
                cursor.close()
                conn.close()

    def get_aula(self, id_aula: int):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT 
                    id_aula,
                    nombre_aula,
                    bloque,
                    capacidad,
                    active,
                    created_at,
                    updated_at
                FROM aula
                WHERE id_aula = %s AND active = true
            """, (id_aula,))

            result = cursor.fetchone()

            if not result:
                raise HTTPException(
                    status_code=404,
                    detail="Aula not found"
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

    def create_aula(self, aula_data: dict):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                INSERT INTO aula (
                    nombre_aula,
                    bloque,
                    capacidad,
                    active
                )
                VALUES (%s, %s, %s, %s)
                RETURNING id_aula
            """, (
                aula_data['nombre_aula'],
                aula_data['bloque'],
                aula_data['capacidad'],
                aula_data.get('active', True)
            ))

            new_aula = cursor.fetchone()

            conn.commit()

            return {
                "message": "Aula created successfully",
                "id_aula": new_aula["id_aula"]
            }

        except Exception as e:
            if conn:
                conn.rollback()

            raise HTTPException(status_code=500, detail=str(e))

        finally:
            if conn:
                cursor.close()
                conn.close()

    def update_aula(self, id_aula: int, aula_data: dict):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE aula
                SET
                    nombre_aula = %s,
                    bloque = %s,
                    capacidad = %s,
                    active = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id_aula = %s
            """, (
                aula_data['nombre_aula'],
                aula_data['bloque'],
                aula_data['capacidad'],
                aula_data['active'],
                id_aula
            ))

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Aula not found"
                )

            conn.commit()

            return {
                "message": "Aula updated successfully"
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

    def delete_aula(self, id_aula: int):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE aula
                SET 
                    active = false,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id_aula = %s
            """, (id_aula,))

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Aula not found"
                )

            conn.commit()

            return {
                "message": "Aula deleted successfully"
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