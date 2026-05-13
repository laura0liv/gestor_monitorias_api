from fastapi import HTTPException
from psycopg2.extras import RealDictCursor
from config.db_config import get_db_connection


class MateriaController:

    def get_all_materia(self):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT
                    id_materia,
                    nombre_materia,
                    codigo_materia,
                    creditos,
                    id_programa,
                    active,
                    created_at,
                    updated_at
                FROM materia
                WHERE active = true
            """)

            return cursor.fetchall()

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        finally:
            if conn:
                cursor.close()
                conn.close()

    def get_materia(self, id_materia: int):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT
                    id_materia,
                    nombre_materia,
                    codigo_materia,
                    creditos,
                    id_programa,
                    active,
                    created_at,
                    updated_at
                FROM materia
                WHERE id_materia = %s
                AND active = true
            """, (id_materia,))

            result = cursor.fetchone()

            if not result:
                raise HTTPException(
                    status_code=404,
                    detail="Materia not found"
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

    def create_materia(self, materia_data: dict):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                INSERT INTO materia (
                    nombre_materia,
                    codigo_materia,
                    creditos,
                    id_programa,
                    active
                )
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id_materia
            """, (
                materia_data['nombre_materia'],
                materia_data['codigo_materia'],
                materia_data['creditos'],
                materia_data['id_programa'],
                materia_data.get('active', True)
            ))

            new_data = cursor.fetchone()

            conn.commit()

            return {
                "message": "Materia created successfully",
                "id_materia": new_data["id_materia"]
            }

        except Exception as e:
            if conn:
                conn.rollback()

            raise HTTPException(status_code=500, detail=str(e))

        finally:
            if conn:
                cursor.close()
                conn.close()

    def update_materia(self, id_materia: int, materia_data: dict):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE materia
                SET
                    nombre_materia = %s,
                    codigo_materia = %s,
                    creditos = %s,
                    id_programa = %s,
                    active = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id_materia = %s
            """, (
                materia_data['nombre_materia'],
                materia_data['codigo_materia'],
                materia_data['creditos'],
                materia_data['id_programa'],
                materia_data['active'],
                id_materia
            ))

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Materia not found"
                )

            conn.commit()

            return {
                "message": "Materia updated successfully"
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

    def delete_materia(self, id_materia: int):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE materia
                SET
                    active = false,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id_materia = %s
            """, (id_materia,))

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Materia not found"
                )

            conn.commit()

            return {
                "message": "Materia deleted successfully"
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