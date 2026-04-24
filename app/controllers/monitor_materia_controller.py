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

            cursor.execute("""
                INSERT INTO monitor_materia (id_monitor, id_materia)
                VALUES (%s, %s)
                ON CONFLICT (id_monitor, id_materia) DO NOTHING
                RETURNING id_monitor, id_materia
            """, (
                monitor_materia_data['id_monitor'],
                monitor_materia_data['id_materia']
            ))

            result = cursor.fetchone()

            if result is None:
                return {"message": "Ya existe la asignación"}

            conn.commit()

            return {
                "id_monitor": result[0],
                "id_materia": result[1]
            }

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

    def get_monitors_and_subjects(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            # ✅ Se agrega m.id_materia al SELECT
            cursor.execute("""
                SELECT u.id_usuario, u.nombre, u.apellido, m.id_materia, m.nombre_materia
                FROM usuario u
                JOIN monitor_materia mm ON u.id_usuario = mm.id_monitor
                JOIN materia m ON mm.id_materia = m.id_materia
                WHERE u.id_rol = 2
                ORDER BY u.id_usuario
            """)
            results = cursor.fetchall()
            monitors = {}
            for result in results:
                id_usuario = int(result[0])
                if id_usuario not in monitors:
                    monitors[id_usuario] = {
                        'id_usuario': id_usuario,  # ✅ clave correcta
                        'nombre': result[1],
                        'apellido': result[2],
                        'materias': []
                    }
                # ✅ Materia como objeto, no string
                monitors[id_usuario]['materias'].append({
                    'id_materia': int(result[3]),
                    'nombre_materia': result[4]
                })
            return list(monitors.values())
        except Exception as e:
            return {"error": str(e)}
        finally:
            if conn:
                conn.close()

    def delete_subject_from_monitor_if_admin(self, current_user_role: int, id_monitor: int, id_materia: int):
        if current_user_role != 1:  # Assuming 1 is admin role
            return {"error": "Unauthorized: Only admins can delete monitor-subject assignments"}
        
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM monitor_materia WHERE id_monitor = %s AND id_materia = %s", (id_monitor, id_materia))
            conn.commit()
            return {"message": "Subject removed from monitor successfully"}
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e)}
        finally:
            if conn:
                conn.close()
         