import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.estudiante_model import Estudiante
from fastapi.encoders import jsonable_encoder

class EstudianteController :

    def create_estudiante(self, estudiante: Estudiante):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            query = """
              INSERT INTO estudiante (
                id_persona,
                id_programa,
                semestre_actual,
                estado_academico
              ) VALUES (%s, %s, %s, %s)
              RETURNING id_estudiante
            """

            values = (
                estudiante.id_persona,
                estudiante.id_programa,
                estudiante.semestre_actual,
                estudiante.estado_academico
            )

            cursor.execute(query, values)

            nuevo_id = cursor.fetchone()[0]
            conn.commit()

            return {
                "mensaje": "Estudiante creado correctamente",
                "id_estudiante": nuevo_id
            }

        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e)}

        finally:
            if conn:
                conn.close()


    def get_estudiante(self, id_estudiante: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM estudiante WHERE id_estudiante = %s", (id_estudiante,))
            result = cursor.fetchone()
            payload = []
            content = {} 
            
            content={
                    'id_estudiante':int(result[0]),
                    'id_persona':result[1],
                    'id_programa':result[2],    
                    'semestre_actual':result[3],
                    'estado_academico':result[4]
            }
            payload.append(content)
            
            json_data = jsonable_encoder(content)            
            if result:
               return  json_data
            else:
                raise HTTPException(status_code=404, detail="User not found")  
                
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()
       
    def get_estudiantes(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM estudiante")
            result = cursor.fetchall()
            payload = []
            content = {} 
            for data in result:
                content={
                    'id_estudiante':data[0],
                    'id_persona':data[1],
                    'id_programa':data[2],  
                    'semestre_actual':data[3],
                    'estado_academico':data[4]
                }
                payload.append(content)
                content = {}
            json_data = jsonable_encoder(payload)        
            if result:
               return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="User not found")  
                
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()
    


    def update_estudiante(self, id_estudiante: int, estudiante: Estudiante):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            query = """
                UPDATE estudiante
                SET id_persona = %s,
                    id_programa = %s,
                    semestre_actual = %s,
                    estado_academico = %s
                WHERE id_estudiante = %s
                RETURNING *
            """

            values = (
                estudiante.id_persona,
                estudiante.id_programa,
                estudiante.semestre_actual,
                estudiante.estado_academico,
                id_estudiante
            )

            cursor.execute(query, values)

            updated = cursor.fetchone()

            if not updated:
                raise HTTPException(status_code=404, detail="Estudiante no encontrado")

            conn.commit()

            estudiante_actualizado = {
                "id_estudiante": updated[0],
                "id_persona": updated[1],
                "id_programa": updated[2],
                "semestre_actual": updated[3],
                "estado_academico": updated[4]
            }

            return jsonable_encoder(estudiante_actualizado)

        except Exception as e:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(e))

        finally:
            if conn:
                conn.close()

    
    def delete_estudiante(self, id_estudiante: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM estudiante WHERE id_estudiante = %s", (id_estudiante,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Estudiante no encontrado")
            conn.commit()
            return {"mensaje": "Estudiante eliminado correctamente"}
        except Exception as e:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(e))

        finally:
            if conn:
                conn.close()