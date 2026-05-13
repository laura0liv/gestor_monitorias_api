from fastapi import HTTPException
from psycopg2.extras import RealDictCursor
from config.db_config import get_db_connection


class HorarioMonitorController:

    def get_all_horario_monitors(self):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT
                    id_horario_monitor,
                    id_monitor,
                    dia_semana,
                    hora_inicio,
                    hora_fin,
                    active,
                    created_at,
                    updated_at
                FROM horario_monitor
                WHERE active = true
            """)

            return cursor.fetchall()

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        finally:
            if conn:
                cursor.close()
                conn.close()

    def get_horario_monitor(self, id_horario_monitor: int):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT
                    id_horario_monitor,
                    id_monitor,
                    dia_semana,
                    hora_inicio,
                    hora_fin,
                    active,
                    created_at,
                    updated_at
                FROM horario_monitor
                WHERE id_horario_monitor = %s
                AND active = true
            """, (id_horario_monitor,))

            result = cursor.fetchone()

            if not result:
                raise HTTPException(
                    status_code=404,
                    detail="Horario Monitor not found"
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

    def create_horario_monitor(self, horario_monitor_data: dict):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                INSERT INTO horario_monitor (
                    id_monitor,
                    dia_semana,
                    hora_inicio,
                    hora_fin,
                    active
                )
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id_horario_monitor
            """, (
                horario_monitor_data['id_monitor'],
                horario_monitor_data['dia_semana'],
                horario_monitor_data['hora_inicio'],
                horario_monitor_data['hora_fin'],
                horario_monitor_data.get('active', True)
            ))

            new_data = cursor.fetchone()

            conn.commit()

            return {
                "message": "Horario Monitor created successfully",
                "id_horario_monitor": new_data["id_horario_monitor"]
            }

        except Exception as e:
            if conn:
                conn.rollback()

            raise HTTPException(status_code=500, detail=str(e))

        finally:
            if conn:
                cursor.close()
                conn.close()

    def update_horario_monitor(self, id_horario_monitor: int, horario_monitor_data: dict):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE horario_monitor
                SET
                    id_monitor = %s,
                    dia_semana = %s,
                    hora_inicio = %s,
                    hora_fin = %s,
                    active = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id_horario_monitor = %s
            """, (
                horario_monitor_data['id_monitor'],
                horario_monitor_data['dia_semana'],
                horario_monitor_data['hora_inicio'],
                horario_monitor_data['hora_fin'],
                horario_monitor_data['active'],
                id_horario_monitor
            ))

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Horario Monitor not found"
                )

            conn.commit()

            return {
                "message": "Horario Monitor updated successfully"
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

    def delete_horario_monitor(self, id_horario_monitor: int):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE horario_monitor
                SET
                    active = false,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id_horario_monitor = %s
            """, (id_horario_monitor,))

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Horario Monitor not found"
                )

            conn.commit()

            return {
                "message": "Horario Monitor deleted successfully"
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