from http.client import HTTPException
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
import psycopg2
from config.db_config import get_db_connection

class MonitoriaController:

    def get_all_monitorias(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM monitoria")
            results = cursor.fetchall()
            payload = []
            content = {}
            
            for result in results:
                content={
                    'id_monitoria':int(result[0]),
                    'nombre_monitoria':result[1],
                    'fecha_inicio':result[2],
                    'fecha_fin':result[3]
                }
                payload.append(content)
                content={}
            
            return payload

        except Exception as e:
            return {"error": str(e)}

        finally:
            if conn:
                conn.close()
                
                
    def get_monitoria(self, id_monitoria: int):
      
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM monitoria WHERE id_monitoria = %s", (id_monitoria,))
            result = cursor.fetchone()
            payload = []
            content = {} 
            
            content={
                    'id_monitoria':int(result[0]), #type: ignore
                    'nombre_monitoria':result[1],#type: ignore
                    'fecha_inicio':result[2],#type: ignore
                    'fecha_fin':result[3]#type: ignore
                }
            
            payload.append(content)
            
            json_data = jsonable_encoder(content)            
            if result:
               return  json_data
            else:
                raise HTTPException(status_code=404, detail="Monitoria not found")
            
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()

            
    def create_monitoria(self, monitoria_data: dict):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO monitoria (nombre_monitoria, fecha_inicio, fecha_fin) VALUES (%s, %s, %s) RETURNING id_monitoria",
                (
                    monitoria_data['nombre_monitoria'],
                    monitoria_data['fecha_inicio'],
                    monitoria_data['fecha_fin']
                )
            )
            new_id = cursor.fetchone()[0] #type: ignore
            conn.commit()
            return {"id_monitoria": new_id}
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e)}
        finally:
            if conn:
                conn.close()   


    def update_monitoria(self, id_monitoria: int, monitoria_data: dict):   
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE monitoria SET nombre_monitoria = %s, fecha_inicio = %s, fecha_fin = %s WHERE id_monitoria = %s",
            (
                monitoria_data['nombre_monitoria'],
                monitoria_data['fecha_inicio'],
                monitoria_data['fecha_fin'],
                id_monitoria
            ))
            conn.commit()
            return {"message": "Monitoria updated successfully"}
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e)}
        finally:
            if conn:
                conn.close()
    

    def delete_monitoria(self, id_monitoria: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM monitoria WHERE id_monitoria = %s", (id_monitoria,))
            conn.commit()
            return {"message": "Monitoria deleted successfully"}
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e)}
        finally:
            if conn:
                conn.close()
         