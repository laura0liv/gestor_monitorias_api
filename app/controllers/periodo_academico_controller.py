from fastapi import HTTPException
from psycopg2.extras import RealDictCursor
from app.config.db_config import get_db_connection


class PeriodoAcademicoController:

    def get_all_periodos(self):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT
                    id_periodo,
                    nombre_periodo,
                    fecha_inicio,
                    fecha_fin,
                    active,
                    created_at,
                    updated_at
                FROM periodo_academico
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

    def get_periodo(self, id_periodo: int):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT
                    id_periodo,
                    nombre_periodo,
                    fecha_inicio,
                    fecha_fin,
                    active,
                    created_at,
                    updated_at
                FROM periodo_academico
                WHERE id_periodo = %s
                AND active = true
            """, (id_periodo,))

            result = cursor.fetchone()

            if not result:
                raise HTTPException(
                    status_code=404,
                    detail="Periodo académico not found"
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

    def create_periodo(self, periodo_data: dict):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                INSERT INTO periodo_academico (
                    nombre_periodo,
                    fecha_inicio,
                    fecha_fin,
                    active
                )
                VALUES (%s, %s, %s, %s)
                RETURNING id_periodo
            """, (
                periodo_data['nombre_periodo'],
                periodo_data['fecha_inicio'],
                periodo_data['fecha_fin'],
                periodo_data.get('active', True)
            ))

            new_data = cursor.fetchone()

            conn.commit()

            return {
                "message": "Periodo académico created successfully",
                "id_periodo": new_data["id_periodo"]
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

    def update_periodo(self, id_periodo: int, periodo_data: dict):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE periodo_academico
                SET
                    nombre_periodo = %s,
                    fecha_inicio = %s,
                    fecha_fin = %s,
                    active = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id_periodo = %s
            """, (
                periodo_data['nombre_periodo'],
                periodo_data['fecha_inicio'],
                periodo_data['fecha_fin'],
                periodo_data['active'],
                id_periodo
            ))

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Periodo académico not found"
                )

            conn.commit()

            return {
                "message": "Periodo académico updated successfully"
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

    def delete_periodo(self, id_periodo: int):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE periodo_academico
                SET
                    active = false,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id_periodo = %s
            """, (id_periodo,))

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Periodo académico not found"
                )

            conn.commit()

            return {
                "message": "Periodo académico deleted successfully"
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

    def get_periodo_activo(self):
        """
        Retorna el periodo académico cuya fecha_inicio <= hoy <= fecha_fin
        y que esté active = true. Debe existir exactamente uno.
        """
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("""
                SELECT
                    id_periodo,
                    nombre_periodo,
                    fecha_inicio,
                    fecha_fin
                FROM periodo_academico
                WHERE active = true
                AND fecha_inicio <= CURRENT_DATE
                AND fecha_fin    >= CURRENT_DATE
                LIMIT 1
            """)
            result = cursor.fetchone()
            if not result:
                raise HTTPException(
                    status_code=404,
                    detail="No hay un periodo académico activo en este momento"
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