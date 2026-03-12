from http.client import HTTPException
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
import psycopg2
from config.db_config import get_db_connection

class CalificacionController:

    def get_all_calificacions(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM calificacion")
            results = cursor.fetchall()
            payload = []
            content = {}
            
            for result in results:
                content={
                    'id_calificacion':int(result[0]),
                    'id_monitoria':result[1],
                    'puntuacion':result[2],
                    'comentario':result[3],
                    'fecha_calificacion':result[4]
                }
                payload.append(content)
                content={}
            
            return payload

        except Exception as e:
            return {"error": str(e)}

        finally:
            if conn:
                conn.close()
                
    def get_calificacion(self, id_calificacion: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM calificacion WHERE id_calificacion = %s", (id_calificacion,))
            result = cursor.fetchone()
            payload = []
            content = {} 
            
            content={
                    'id_calificacion':int(result[0]), #type: ignore
                    'id_monitoria':result[1],#type: ignore
                    'puntuacion':result[2],#type: ignore
                    'comentario':result[3],#type: ignore
                    'fecha_calificacion':result[4]#type: ignore
                }
            
            payload.append(content)
            
            json_data = jsonable_encoder(content)            
            if result:
               return  json_data
            else:
                raise HTTPException(status_code=404, detail="Calificacion not found")

        except Exception as e:
            return {"error": str(e)}

        finally:
            if conn:
                conn.close()
                cursor.close()
                
    def create_calificacion(self, calificacion_data: dict):  
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO calificacion (id_monitoria, puntuacion, comentario, fecha_calificacion) VALUES (%s, %s, %s, %s) RETURNING id_calificacion ",
                            (calificacion_data['id_monitoria'],
                             calificacion_data['puntuacion'],
                             calificacion_data['comentario'],
                             calificacion_data['fecha_calificacion']))
            new_id = cursor.fetchone()[0] #type: ignore
            conn.commit()
            return {"id_calificacion": new_id}
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e)}
        finally:
            if conn:
                conn.close()
                cursor.close()  
                
    def update_calificacion(self, id_calificacion: int, calificacion_data: dict):           
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE calificacion SET id_monitoria = %s, puntuacion = %s, comentario = %s, fecha_calificacion = %s WHERE id_calificacion = %s",
                            (calificacion_data['id_monitoria'],
                             calificacion_data['puntuacion'],
                             calificacion_data['comentario'],
                             calificacion_data['fecha_calificacion'],
                             id_calificacion))
            conn.commit()
            return {"message": "Calificacion updated successfully"}
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e)}
        finally:
            if conn:
                conn.close()
                cursor.close()
                
    def delete_calificacion(self, id_calificacion: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM calificacion WHERE id_calificacion = %s", (id_calificacion,))
            conn.commit()
            return {"message": "Calificacion deleted successfully"}
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e)}
        finally:
            if conn:
                conn.close()
                cursor.close()