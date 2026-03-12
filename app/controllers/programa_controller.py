from http.client import HTTPException
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
import psycopg2
from config.db_config import get_db_connection

class ProgramaController:

    def get_all_programa(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM programa")
            results = cursor.fetchall()
            payload = []
            content = {}
            
            for result in results:
                content={
                    'id_programa':int(result[0]),
                    'nombre_programa':result[1],
                    'facultad':result[2],
                    'descripcion':result[3]
                }
                payload.append(content)
                content={}
            
            return payload

        except Exception as e:
            return {"error": str(e)}

        finally:
            if conn:
                conn.close()
                
    def get_programa(self, id_programa: int):
      
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM programa WHERE id_programa = %s", (id_programa,))
            result = cursor.fetchone()
            payload = []
            content = {} 
            
            content={
                    'id_programa':int(result[0]), #type: ignore
                    'nombre_programa':result[1],#type: ignore
                    'facultad':result[2],#type: ignore
                    'descripcion':result[3]#type: ignore
                }
            
            payload.append(content)
            
            json_data = jsonable_encoder(content)            
            if result:
               return  json_data
            else:
                raise HTTPException(status_code=404, detail="Programa not found")
            
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()
    def create_programa(self, programa_data: dict):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO programa (nombre_programa, facultad, descripcion) VALUES (%s, %s, %s) RETURNING id_programa",
                (
                    programa_data['nombre_programa'],
                    programa_data['facultad'],
                    programa_data['descripcion']
                )
            )
            new_id = cursor.fetchone()[0] #type: ignore
            conn.commit()
            return {"id_programa": new_id}
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e)}
        finally:
            if conn:
                conn.close()   
    def update_programa(self, id_programa: int, programa_data: dict):   
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE programa SET nombre_programa = %s, facultad = %s, descripcion = %s WHERE id_programa = %s",
            (
                programa_data['nombre_programa'],
                programa_data['facultad'],
                programa_data['descripcion'],
                id_programa
            ))
            conn.commit()
            return {"message": "Programa updated successfully"}
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e)}
        finally:
            if conn:
                conn.close()
    
    def delete_programa(self, id_programa: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM programa WHERE id_programa = %s", (id_programa,))
            conn.commit()
            return {"message": "Programa deleted successfully"}
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e)}
        finally:
            if conn:
                conn.close()
         