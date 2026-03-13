from http.client import HTTPException
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
import psycopg2
from config.db_config import get_db_connection

class MonitorMateriaController:

    def get_all_monitor_materias(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM monitor_materia")
            results = cursor.fetchall()
            payload = []
            content = {}
            
            for result in results:
                content={
                    'id_monitor':int(result[0]),
                    'id_materia':int(result[1])
                }
                payload.append(content)
                content={}
            
            return payload

        except Exception as e:
            return {"error": str(e)}

        finally:
            if conn:
                conn.close()
                
                
    def get_monitor_materia(self, id_monitor: int, id_materia: int):
      
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM monitor_materia WHERE id_monitor = %s AND id_materia = %s", (id_monitor, id_materia))
            result = cursor.fetchone()
            payload = []
            content = {} 
            
            content={
                    'id_monitor':int(result[0]), #type: ignore
                    'id_materia':int(result[1]) #type: ignore
                }
            
            payload.append(content)
            
            json_data = jsonable_encoder(content)            
            if result:
               return  json_data
            else:
                raise HTTPException(status_code=404, detail="Monitor Materia not found")
            
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()

            
    def create_monitor_materia(self, monitor_materia_data: dict):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO monitor_materia (id_monitor, id_materia) VALUES (%s, %s) RETURNING id_monitor, id_materia",
                (
                    monitor_materia_data['id_monitor'],
                    monitor_materia_data['id_materia']
                )
            )
            new_id = cursor.fetchone()[0] #type: ignore
            conn.commit()
            return {"id_monitor": new_id[0], "id_materia": new_id[1]}
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e)}
        finally:
            if conn:
                conn.close()   


    def update_monitor_materia(self, id_monitor: int, id_materia: int, monitor_materia_data: dict):   
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE monitor_materia SET id_monitor = %s, id_materia = %s WHERE id_monitor = %s AND id_materia = %s",
            (
                monitor_materia_data['id_monitor'],
                monitor_materia_data['id_materia'],
                id_monitor,
                id_materia
            ))
            conn.commit()
            return {"message": "Monitor Materia updated successfully"}
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e)}
        finally:
            if conn:
                conn.close()
    

    def delete_monitor_materia(self, id_monitor: int, id_materia: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM monitor_materia WHERE id_monitor = %s AND id_materia = %s", (id_monitor, id_materia))
            conn.commit()
            return {"message": "Monitor Materia deleted successfully"}
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e)}
        finally:
            if conn:
                conn.close()
         