from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
import psycopg2
from config.db_config import get_db_connection

class RolController():

    def get_all_rol(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM rol")
            results = cursor.fetchall()
            payload = []
            content = {}
            
            for result in results:
                content={
                    'id_rol':int(result[0]),
                    'nombre_rol':result[1]
                }
                payload.append(content)
                content={}
            
            return payload

        except Exception as e:
            return {"error": str(e)}

        finally:
            if conn:
                conn.close()
    

    def get_rol(self, id_rol: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM rol WHERE id_rol = %s", (id_rol,))
            result = cursor.fetchone()
            payload = []
            content = {} 
            
            content={
                    'id_rol':int(result[0]),
                    'nombre_rol':result[1]
            }
            payload.append(content)
            
            json_data = jsonable_encoder(content)            
            if result:
               return  json_data
            else:
                raise HTTPException(status_code=404, detail="Rol not found")  
                
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()

    def create_rol(self, rol_data: dict):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO rol (nombre_rol) VALUES (%s) RETURNING id_rol",
                (rol_data['nombre_rol'],)
            )
            new_id = cursor.fetchone()[0]
            conn.commit()
            return {"id_rol": new_id, "nombre_rol": rol_data['nombre_rol']}
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e)}
        finally:
            if conn:
                conn.close()
    

    def update_rol(self, id_rol: int, rol_data: dict):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE rol SET nombre_rol = %s WHERE id_rol = %s",
                (rol_data['nombre_rol'], id_rol)
            )
            conn.commit()
            return {"id_rol": id_rol, "nombre_rol": rol_data['nombre_rol']}
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e)}
        finally:
            if conn:
                conn.close()


    def delete_rol(self, id_rol: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM rol WHERE id_rol = %s", (id_rol,))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Rol not found")
            return {"message": "Rol deleted successfully"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
            raise HTTPException(status_code=500, detail="Error deleting rol")
        finally:
            conn.close()