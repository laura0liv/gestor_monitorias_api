from http.client import HTTPException
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
import psycopg2
from config.db_config import get_db_connection

class PeriodoAcademicoController:

    def get_all_periodos(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM periodo_academico")
            results = cursor.fetchall()
            payload = []
            content = {}
            
            for result in results:
                content={
                    'id_periodo':int(result[0]),
                    'nombre_periodo':result[1],
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
                
                
    def get_periodo(self, id_periodo: int):
      
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM periodo_academico WHERE id_periodo = %s", (id_periodo,))
            result = cursor.fetchone()
            payload = []
            content = {} 
            
            content={
                    'id_periodo':int(result[0]), #type: ignore
                    'nombre_periodo':result[1],#type: ignore
                    'fecha_inicio':result[2],#type: ignore
                    'fecha_fin':result[3]#type: ignore
                }
            
            payload.append(content)
            
            json_data = jsonable_encoder(content)            
            if result:
               return  json_data
            else:
                raise HTTPException(status_code=404, detail="Periodo académico not found")
            
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()

            
    def create_periodo(self, periodo_data: dict):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO periodo_academico (nombre_periodo, fecha_inicio, fecha_fin) VALUES (%s, %s, %s) RETURNING id_periodo",
                (
                    periodo_data['nombre_periodo'],
                    periodo_data['fecha_inicio'],
                    periodo_data['fecha_fin']
                )
            )
            new_id = cursor.fetchone()[0] #type: ignore
            conn.commit()
            return {"id_periodo": new_id}
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e)}
        finally:
            if conn:
                conn.close()   


    def update_periodo(self, id_periodo: int, periodo_data: dict):   
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE periodo_academico SET nombre_periodo = %s, fecha_inicio = %s, fecha_fin = %s WHERE id_periodo = %s",
            (
                periodo_data['nombre_periodo'],
                periodo_data['fecha_inicio'],
                periodo_data['fecha_fin'],
                id_periodo
            ))
            conn.commit()
            return {"message": "Periodo académico updated successfully"}
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e)}
        finally:
            if conn:
                conn.close()
    

    def delete_periodo(self, id_periodo: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM periodo_academico WHERE id_periodo = %s", (id_periodo,))
            conn.commit()
            return {"message": "Periodo académico deleted successfully"}
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e)}
        finally:
            if conn:
                conn.close()
         