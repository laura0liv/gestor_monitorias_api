from fastapi import HTTPException
from psycopg2.extras import RealDictCursor
from app.config.db_config import get_db_connection


class MonitorMateriaController:

    def get_all_monitor_materias(self):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT
                    id_monitor,
                    id_materia
                FROM monitor_materia
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

    def get_monitor_materia(self, id_monitor: int, id_materia: int):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT
                    id_monitor,
                    id_materia
                FROM monitor_materia
                WHERE id_monitor = %s
                AND id_materia = %s
            """, (id_monitor, id_materia))

            result = cursor.fetchone()

            if not result:
                raise HTTPException(
                    status_code=404,
                    detail="Monitor Materia not found"
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

    def create_monitor_materia(self, monitor_materia_data: dict):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                INSERT INTO monitor_materia (
                    id_monitor,
                    id_materia
                )
                VALUES (%s, %s)
                ON CONFLICT (id_monitor, id_materia)
                DO NOTHING
                RETURNING id_monitor, id_materia
            """, (
                monitor_materia_data['id_monitor'],
                monitor_materia_data['id_materia']
            ))

            result = cursor.fetchone()

            if result is None:
                return {
                    "message": "La asignación ya existe"
                }

            conn.commit()

            return {
                "message": "Monitor Materia created successfully",
                "id_monitor": result["id_monitor"],
                "id_materia": result["id_materia"]
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

    def update_monitor_materia(
        self,
        id_monitor: int,
        id_materia: int,
        monitor_materia_data: dict
    ):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE monitor_materia
                SET
                    id_monitor = %s,
                    id_materia = %s
                WHERE id_monitor = %s
                AND id_materia = %s
            """, (
                monitor_materia_data['id_monitor'],
                monitor_materia_data['id_materia'],
                id_monitor,
                id_materia
            ))

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Monitor Materia not found"
                )

            conn.commit()

            return {
                "message": "Monitor Materia updated successfully"
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

    def delete_monitor_materia(self, id_monitor: int, id_materia: int):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM monitor_materia
                WHERE id_monitor = %s
                AND id_materia = %s
            """, (id_monitor, id_materia))

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Monitor Materia not found"
                )

            conn.commit()

            return {
                "message": "Monitor Materia deleted successfully"
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

    def get_monitors_and_subjects(self):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    u.id_usuario,
                    u.nombre,
                    u.apellido,
                    m.id_materia,
                    m.nombre_materia
                FROM usuario u
                JOIN monitor_materia mm
                    ON u.id_usuario = mm.id_monitor
                JOIN materia m
                    ON mm.id_materia = m.id_materia
                WHERE u.id_rol = 2
                ORDER BY u.id_usuario
            """)

            results = cursor.fetchall()

            monitors = {}

            for result in results:

                id_usuario = int(result[0])

                if id_usuario not in monitors:
                    monitors[id_usuario] = {
                        "id_usuario": id_usuario,
                        "nombre": result[1],
                        "apellido": result[2],
                        "materias": []
                    }

                monitors[id_usuario]["materias"].append({
                    "id_materia": int(result[3]),
                    "nombre_materia": result[4]
                })

            return list(monitors.values())

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        finally:
            if conn:
                cursor.close()
                conn.close()


    def get_materias_by_monitor(self, id_monitor: int):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT
                    m.id_materia,
                    m.nombre_materia
                FROM monitor_materia mm
                JOIN materia m
                    ON mm.id_materia = m.id_materia
                WHERE mm.id_monitor = %s
                ORDER BY m.nombre_materia
            """, (id_monitor,))

            results = cursor.fetchall()

            if not results:
                raise HTTPException(
                    status_code=404,
                    detail="No se encontraron materias para este monitor"
                )

            return {
                "id_monitor": id_monitor,
                "materias": results
            }

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