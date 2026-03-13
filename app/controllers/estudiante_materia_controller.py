from http.client import HTTPException
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
import psycopg2
from config.db_config import get_db_connection

class EstudianteMateriaController:

    def get_all_estudiante_materias(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM estudiante_materia")
            results = cursor.fetchall()
            payload = []
            content = {}
            
            for result in results:
                content={
                    'id_estudiante':int(result[0]),
                    'id_materia':result[1],
                    'id_periodo':result[2]  
                }
                payload.append(content)
                content={}
            
            return payload

        except Exception as e:
            return {"error": str(e)}

        finally:
            if conn:
                conn.close()
                
    def get_estudiante_materia(self, id_estudiante: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM estudiante_materia WHERE id_estudiante = %s", (id_estudiante,))
            result = cursor.fetchone()
            payload = []
            content = {} 
            
            content={
                    'id_estudiante':int(result[0]), #type: ignore
                    'id_materia':result[1],#type: ignore
                    'id_periodo':result[2]#type: ignore
                }
            
            payload.append(content)
            
            json_data = jsonable_encoder(content)            
            if result:
               return  json_data
            else:
                raise HTTPException(status_code=404, detail="Estudiante Materia not found")

        except Exception as e:
            return {"error": str(e)}

        finally:
            if conn:
                conn.close()
                cursor.close()
                
    def create_estudiante_materia(self, estudiante_materia_data: dict):  
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO estudiante_materia (id_estudiante, id_materia, id_periodo) VALUES (%s, %s, %s) RETURNING id_estudiante",
                            (estudiante_materia_data['id_estudiante'],
                             estudiante_materia_data['id_materia'],
                             estudiante_materia_data['id_periodo']))
            new_id = cursor.fetchone()[0] #type: ignore
            conn.commit()
            return {"id_estudiante": new_id}
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e)}
        finally:
            if conn:
                conn.rollback()
            return {"error": str(e)}

                
    def update_estudiante_materia(self, id_estudiante: int, estudiante_materia_data: dict):           
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE estudiante_materia SET id_materia = %s, id_periodo = %s WHERE id_estudiante = %s",
                            (estudiante_materia_data['id_materia'],
                             estudiante_materia_data['id_periodo'],
                             id_estudiante))
            conn.commit()
            return {"message": "Estudiante Materia updated successfully"}
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e)}
        finally:
            if conn:
                conn.close()
                cursor.close()
                
    def delete_estudiante_materia(self, id_estudiante: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM estudiante_materia WHERE id_estudiante = %s", (id_estudiante,))
            conn.commit()
            return {"message": "Estudiante Materia deleted successfully"}
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e)}
        finally:
            if conn:
                conn.close()
                cursor.close()