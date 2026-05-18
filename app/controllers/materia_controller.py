from fastapi import HTTPException
from psycopg2.extras import RealDictCursor
from app.config.db_config import get_db_connection


class MateriaController:

    def get_all_materia(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("""
                SELECT 
                    mat.id_materia,
                    mat.nombre_materia,
                    mat.codigo_materia,
                    mat.creditos,
                    mat.id_programa,
                    prog.nombre_programa,
                    mat.active,
                    mat.created_at,
                    mat.updated_at
                FROM materia mat
                LEFT JOIN programa prog ON prog.id_programa = mat.id_programa
                WHERE mat.active = true
                ORDER BY mat.nombre_materia
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
                    mat.id_materia,
                    mat.nombre_materia,
                    mat.codigo_materia,
                    mat.creditos,
                    mat.id_programa,
                    prog.nombre_programa,
                    prog.facultad,
                    mat.active,
                    mat.created_at,
                    mat.updated_at
                FROM materia mat
                LEFT JOIN programa prog 
                    ON prog.id_programa = mat.id_programa 
                    AND prog.active = true
                WHERE mat.id_materia = %s 
                  AND mat.active = true
            """, (id_materia,))
            
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Materia not found")
            return result
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if conn:
                cursor.close()
                conn.close()

    def create_materia(self, data: dict):
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
                data["nombre_materia"],
                data["codigo_materia"],
                data["creditos"],
                data["id_programa"],
                data.get("active", True)
            ))

            new_id = cursor.fetchone()
            conn.commit()

            return {
                "id_materia": new_id["id_materia"],
                "message": "Materia creada correctamente"
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
                raise HTTPException(status_code=404, detail="Materia not found")
            conn.commit()
            return {"message": "Materia updated successfully"}
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
                raise HTTPException(status_code=404, detail="Materia not found")
            conn.commit()
            return {"message": "Materia deleted successfully"}
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

    # ─────────────────────────────────────────────
    # NUEVO — consumido por MateriasEstudiante.svelte
    # GET /materia/disponibles
    # ─────────────────────────────────────────────

    def get_materias_disponibles(self):
        """
        Retorna las materias que tienen al menos un monitor activo asignado.
        Campos: id_materia, nombre_materia, creditos, nombre_programa,
                monitores_disponibles.
        """
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("""
                SELECT
                    mat.id_materia,
                    mat.nombre_materia,
                    mat.creditos,
                    prog.nombre_programa,
                    COUNT(mm.id_monitor)  AS monitores_disponibles
                FROM materia mat
                LEFT JOIN programa prog
                    ON prog.id_programa = mat.id_programa
                    AND prog.active     = true
                INNER JOIN monitor_materia mm
                    ON mm.id_materia = mat.id_materia
                    AND mm.active    = true
                INNER JOIN usuario u
                    ON u.id_usuario = mm.id_monitor
                    AND u.active    = true
                WHERE mat.active = true
                GROUP BY
                    mat.id_materia,
                    mat.nombre_materia,
                    mat.creditos,
                    prog.nombre_programa
                HAVING COUNT(mm.id_monitor) > 0
                ORDER BY mat.nombre_materia
            """)
            return cursor.fetchall()
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Error obteniendo materias disponibles")
        finally:
            if conn:
                cursor.close()
                conn.close()