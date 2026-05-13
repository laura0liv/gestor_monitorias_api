from fastapi import HTTPException
from psycopg2.extras import RealDictCursor
from config.db_config import get_db_connection


class ProgramaController:

    def get_all_programa(self):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT
                    id_programa,
                    nombre_programa,
                    facultad,
                    descripcion,
                    active,
                    created_at,
                    updated_at
                FROM programa
                WHERE active = true
            """)

            return cursor.fetchall()

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        finally:
            if conn:
                cursor.close()
                conn.close()

    def get_programa(self, id_programa: int):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT
                    id_programa,
                    nombre_programa,
                    facultad,
                    descripcion,
                    active,
                    created_at,
                    updated_at
                FROM programa
                WHERE id_programa = %s
                AND active = true
            """, (id_programa,))

            result = cursor.fetchone()

            if not result:
                raise HTTPException(
                    status_code=404,
                    detail="Programa not found"
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

    def create_programa(self, programa_data: dict):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                INSERT INTO programa (
                    nombre_programa,
                    facultad,
                    descripcion,
                    active
                )
                VALUES (%s, %s, %s, %s)
                RETURNING id_programa
            """, (
                programa_data['nombre_programa'],
                programa_data['facultad'],
                programa_data['descripcion'],
                programa_data.get('active', True)
            ))

            new_data = cursor.fetchone()

            conn.commit()

            return {
                "message": "Programa created successfully",
                "id_programa": new_data["id_programa"]
            }

        except Exception as e:
            if conn:
                conn.rollback()

            raise HTTPException(status_code=500, detail=str(e))

        finally:
            if conn:
                cursor.close()
                conn.close()

    def update_programa(self, id_programa: int, programa_data: dict):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE programa
                SET
                    nombre_programa = %s,
                    facultad = %s,
                    descripcion = %s,
                    active = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id_programa = %s
            """, (
                programa_data['nombre_programa'],
                programa_data['facultad'],
                programa_data['descripcion'],
                programa_data['active'],
                id_programa
            ))

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Programa not found"
                )

            conn.commit()

            return {
                "message": "Programa updated successfully"
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

    def delete_programa(self, id_programa: int):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE programa
                SET
                    active = false,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id_programa = %s
            """, (id_programa,))

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Programa not found"
                )

            conn.commit()

            return {
                "message": "Programa deleted successfully"
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