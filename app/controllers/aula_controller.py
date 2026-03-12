from http.client import HTTPException
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
import psycopg2
from config.db_config import get_db_connection

class AulaController:

    def get_all_aula(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM aula")
            results = cursor.fetchall()
            payload = []
            content = {}
            
            for result in results:
                content={
                    'id_aula':int(result[0]),
                    'nombre_aula':result[1],
                    'bloque':result[2],
                    'capacidad':result[3]
                }
                payload.append(content)
                content={}
            
            return payload

        except Exception as e:
            return {"error": str(e)}

        finally:
            if conn:
                conn.close()
                
    def get_aula(self, id_aula: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM aula WHERE id_aula = %s", (id_aula,))
            result = cursor.fetchone()
            payload = []
            content = {} 
            
            content={
                    'id_aula':int(result[0]), #type: ignore
                    'nombre_aula':result[1],#type: ignore
                    'bloque':result[2],#type: ignore
                    'capacidad':result[3]#type: ignore
                }
            
            payload.append(content)
            
            json_data = jsonable_encoder(content)            
            if result:
               return  json_data
            else:
                raise HTTPException(status_code=404, detail="Aula not found")

        except Exception as e:
            return {"error": str(e)}

        finally:
            if conn:
                conn.close()
                cursor.close()
                
    def create_aula(self, aula_data: dict):  
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO aula (nombre_aula, bloque, capacidad) VALUES (%s, %s, %s) RETURNING id_aula",
                            (aula_data['nombre_aula'],
                             aula_data['bloque'], 
                             aula_data['capacidad']))
            new_id = cursor.fetchone()[0] #type: ignore
            conn.commit()
            return {"id_aula": new_id}
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e)}
        finally:
            if conn:
                conn.close()
                cursor.close()  
                
    def update_aula(self, id_aula: int, aula_data: dict):           
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE aula SET nombre_aula = %s, bloque = %s, capacidad = %s WHERE id_aula = %s",
                            (aula_data['nombre_aula'],
                             aula_data['bloque'], 
                             aula_data['capacidad'],
                             id_aula))
            conn.commit()
            return {"message": "Aula updated successfully"}
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e)}
        finally:
            if conn:
                conn.close()
                cursor.close()
                
    def delete_aula(self, id_aula: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM aula WHERE id_aula = %s", (id_aula,))
            conn.commit()
            return {"message": "Aula deleted successfully"}
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e)}
        finally:
            if conn:
                conn.close()
                cursor.close()