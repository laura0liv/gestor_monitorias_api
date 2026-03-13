from http.client import HTTPException
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
import psycopg2
from config.db_config import get_db_connection


class SesionSeguimientoController:

    def get_all_sesion_seguimiento(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sesion_seguimiento")
            results = cursor.fetchall()
            payload = []
            content = {}
            
            for result in results:
                content={
                    'id_sesion':int(result[0]),
                    'id_seguimiento':int(result[1]),
                    'fecha':result[2],
                    'observaciones':result[3],
                    'avance':int(result[4])
              
                }
                payload.append(content)
                content={}
            
            return payload

        except Exception as e:
            return {"error": str(e)}

        finally:
            if conn:
                conn.close()
    
    
    def get_sesion_seguimiento(self, id_sesion: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sesion_seguimiento WHERE id_sesion = %s", (id_sesion,))
            result = cursor.fetchone()
            payload = []
            content = {} 
            
            content={
                    'id_sesion':int(result[0]), 
                    'id_seguimiento':int(result[1]),
                    'fecha':result[2],
                    'observaciones':result[3],
                    'avance':int(result[4])
            }
            payload.append(content)
            
            json_data = jsonable_encoder(content)            
            if result:
               return  json_data
            else:
                raise HTTPException(status_code=404, detail="SesionSeguimiento not found")  
                
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()

    def create_sesion_seguimiento(self, sesion_seguimiento_data: dict):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO sesion_seguimiento (id_sesion, id_seguimiento, fecha, observaciones, avance) VALUES (%s, %s, %s, %s, %s) RETURNING id_sesion",
                (
                    sesion_seguimiento_data['id_sesion'],
                    sesion_seguimiento_data['id_seguimiento'],
                    sesion_seguimiento_data['fecha'],
                    sesion_seguimiento_data['observaciones'],
                    sesion_seguimiento_data['avance']
                )
            )
            new_id = cursor.fetchone()[0] #type: ignore
            conn.commit()
            return {"id_sesion": new_id}
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e)}
        finally:
            if conn:
                conn.close()

    def update_sesion_seguimiento(self, id_sesion: int, sesion_seguimiento_data: dict):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE sesion_seguimiento SET id_seguimiento = %s, fecha = %s, observaciones = %s, avance = %s WHERE id_sesion = %s",
                (
                    sesion_seguimiento_data['id_seguimiento'],
                    sesion_seguimiento_data['fecha'],
                    sesion_seguimiento_data['observaciones'],
                    sesion_seguimiento_data['avance'],
                    id_sesion
                )
            )
            conn.commit()
            return {"message": "SesionSeguimiento updated successfully"}
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e)}
        finally:
            if conn:
                conn.close()

    def delete_sesion_seguimiento(self, id_sesion: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM sesion_seguimiento WHERE id_sesion = %s", (id_sesion,))
            conn.commit()
            return {"message": "SesionSeguimiento deleted successfully"}
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e)}
        finally:
            if conn:
                conn.close()
        
