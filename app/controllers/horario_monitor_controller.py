from http.client import HTTPException
from fastapi.encoders import jsonable_encoder
import psycopg2
from config.db_config import get_db_connection


class HoriarioMonitorController:

    def get_all_horario_monitors(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM horario_monitor")
            results = cursor.fetchall()
            payload = []
            content = {}
            
            for result in results:
                content={
                    'id_horario_monitor':int(result[0]),
                    'id_monitor':int(result[1]),
                    'dia_semana':result[2],
                    'hora_inicio':str(result[3]),
                    'hora_fin':str(result[4])
                    
                }
                payload.append(content)
                content={}
            
            return payload

        except Exception as e:
            return {"error": str(e)}

        finally:
            if conn:
                conn.close()
    
    
    def get_horario_monitor(self, id_horario_monitor: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM horario_monitor WHERE id_horario_monitor = %s", (id_horario_monitor,))
            result = cursor.fetchone()
            payload = []
            content = {} 
            
            content={
                    'id_horario_monitor':int(result[0]),
                    'id_monitor':int(result[1]),
                    'dia_semana':result[2],
                    'hora_inicio':str(result[3]),
                    'hora_fin':str(result[4])
            }
            payload.append(content)
            
            json_data = jsonable_encoder(content)            
            if result:
               return  json_data
            else:
                raise HTTPException(status_code=404, detail="Horario Monitor not found")  
                
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()

    def create_horario_monitor(self, horario_monitor_data: dict):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO horario_monitor (id_monitor, dia_semana, hora_inicio, hora_fin) VALUES (%s, %s, %s, %s) RETURNING id_horario_monitor",
                (
                    horario_monitor_data['id_monitor'],
                    horario_monitor_data['dia_semana'],
                    horario_monitor_data['hora_inicio'],
                    horario_monitor_data['hora_fin']
                )
            )
            new_id = cursor.fetchone()[0]
            conn.commit()
            return {"id_horario_monitor": new_id}
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e)}
        finally:
            if conn:
                conn.close()


    def update_horario_monitor(self, id_horario_monitor: int, horario_monitor_data: dict):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE horario_monitor SET id_monitor = %s, dia_semana = %s, hora_inicio = %s, hora_fin = %s WHERE id_horario_monitor = %s",
                (
                    horario_monitor_data['id_monitor'],
                    horario_monitor_data['dia_semana'],
                    horario_monitor_data['hora_inicio'],
                    horario_monitor_data['hora_fin'],
                    id_horario_monitor
                )
            )
            conn.commit()
            return {"message": "Horario Monitor updated successfully"}
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e)}
        finally:
            if conn:
                conn.close()


    def delete_horario_monitor(self, id_horario_monitor: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM horario_monitor WHERE id_horario_monitor = %s", (id_horario_monitor,))
            conn.commit()
            return {"message": "Horario Monitor deleted successfully"}
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e)}
        finally:
            if conn:
                conn.close()
        
