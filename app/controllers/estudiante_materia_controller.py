
from fastapi import HTTPException
from psycopg2.extras import RealDictCursor
from config.db_config import get_db_connection


class EstudianteMateriaController:

    def get_all_estudiante_materias(self):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT
                    id_estudiante,
                    id_materia,
                    id_periodo,
                    active,
                    created_at,
                    updated_at
                FROM estudiante_materia
                WHERE active = true
            """)

            return cursor.fetchall()

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        finally:
            if conn:
                cursor.close()
                conn.close()

    def get_estudiante_materia(self, id_estudiante: int):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT
                    id_estudiante,
                    id_materia,
                    id_periodo,
                    active,
                    created_at,
                    updated_at
                FROM estudiante_materia
                WHERE id_estudiante = %s
                AND active = true
            """, (id_estudiante,))

            result = cursor.fetchone()

            if not result:
                raise HTTPException(
                    status_code=404,
                    detail="Estudiante Materia not found"
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

    def create_estudiante_materia(self, estudiante_materia_data: dict):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                INSERT INTO estudiante_materia (
                    id_estudiante,
                    id_materia,
                    id_periodo,
                    active
                )
                VALUES (%s, %s, %s, %s)
                RETURNING id_estudiante
            """, (
                estudiante_materia_data['id_estudiante'],
                estudiante_materia_data['id_materia'],
                estudiante_materia_data['id_periodo'],
                estudiante_materia_data.get('active', True)
            ))

            new_data = cursor.fetchone()

            conn.commit()

            return {
                "message": "Estudiante Materia created successfully",
                "id_estudiante": new_data["id_estudiante"]
            }

        except Exception as e:
            if conn:
                conn.rollback()

            raise HTTPException(status_code=500, detail=str(e))

        finally:
            if conn:
                cursor.close()
                conn.close()

    def update_estudiante_materia(self, id_estudiante: int, estudiante_materia_data: dict):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE estudiante_materia
                SET
                    id_materia = %s,
                    id_periodo = %s,
                    active = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id_estudiante = %s
            """, (
                estudiante_materia_data['id_materia'],
                estudiante_materia_data['id_periodo'],
                estudiante_materia_data['active'],
                id_estudiante
            ))

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Estudiante Materia not found"
                )

            conn.commit()

            return {
                "message": "Estudiante Materia updated successfully"
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

    def delete_estudiante_materia(self, id_estudiante: int):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE estudiante_materia
                SET
                    active = false,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id_estudiante = %s
            """, (id_estudiante,))

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Estudiante Materia not found"
                )

            conn.commit()

            return {
                "message": "Estudiante Materia deleted successfully"
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