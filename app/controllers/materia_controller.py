from http.client import HTTPException
from fastapi.encoders import jsonable_encoder
import psycopg2
from config.db_config import get_db_connection


class MateriaController:

    def get_all_materia(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM materia")
            results = cursor.fetchall()
            payload = []
            content = {}
            
            for result in results:
                content={
                    'id_materia':int(result[0]),
                    'nombre_materia':result[1],
                    'codigo_materia':result[2],
                    'creditos':result[3],
                    'id_programa':result[4]
                }
                payload.append(content)
                content={}
            
            return payload

        except Exception as e:
            return {"error": str(e)}

        finally:
            if conn:
                conn.close()
    
    
    def get_materia(self, id_materia: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM materia WHERE id_materia = %s", (id_materia,))
            result = cursor.fetchone()
            payload = []
            content = {} 
            
            content={
                    'id_materia':int(result[0]),
                    'nombre_materia':result[1],
                    'codigo_materia':result[2],
                    'creditos':result[3],
                    'id_programa':result[4]
            }
            payload.append(content)
            
            json_data = jsonable_encoder(content)            
            if result:
               return  json_data
            else:
                raise HTTPException(status_code=404, detail="Materia not found")  
                
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()

    def create_materia(self, materia_data: dict):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO materia (nombre_materia, codigo_materia, creditos, id_programa) VALUES (%s, %s, %s, %s) RETURNING id_materia",
                (
                    materia_data['nombre_materia'],
                    materia_data['codigo_materia'],
                    materia_data['creditos'],
                    materia_data['id_programa']
                )
            )
            new_id = cursor.fetchone()[0]
            conn.commit()
            return {"id_materia": new_id}
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e)}
        finally:
            if conn:
                conn.close()


    def update_materia(self, id_materia: int, materia_data: dict):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE materia SET nombre_materia = %s, codigo_materia = %s, creditos = %s, id_programa = %s WHERE id_materia = %s",
                (
                    materia_data['nombre_materia'],
                    materia_data['codigo_materia'],
                    materia_data['creditos'],
                    materia_data['id_programa'],
                    id_materia
                )
            )
            conn.commit()
            return {"message": "Materia updated successfully"}
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e)}
        finally:
            if conn:
                conn.close()


    def delete_materia(self, id_materia: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM materia WHERE id_materia = %s", (id_materia,))
            conn.commit()
            return {"message": "Materia deleted successfully"}
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e)}
        finally:
            if conn:
                conn.close()
        
