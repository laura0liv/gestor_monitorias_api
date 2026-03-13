from http.client import HTTPException
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
import psycopg2
from config.db_config import get_db_connection


class SeguimientoAcademicoController:

    def get_all_seguimiento_academico(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM seguimiento_academico")
            results = cursor.fetchall()
            payload = []
            content = {}
            
            for result in results:
                content={
                    'id_seguimiento':int(result[0]),
                    'id_estudiante':int(result[1]),
                    'id_monitor':int(result[2]),
                    'id_periodo':int(result[3]),
                    'fecha_inicio':result[4],
                    'nivel_riesgo':result[5],
                    'motivo':result[6],
                    'plan_acompanamiento':result[7],
                    'resultado':result[8],
                    'estado':result[9],
                    'fecha_cierre':result[10]
                }
                payload.append(content)
                content={}
            
            return payload

        except Exception as e:
            return {"error": str(e)}

        finally:
            if conn:
                conn.close()
    
    
    def get_seguimiento_academico(self, id_seguimiento: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM seguimiento_academico WHERE id_seguimiento = %s", (id_seguimiento,))
            result = cursor.fetchone()
            payload = []
            content = {} 
            
            content={
                    'id_seguimiento':int(result[0]),
                    'id_estudiante':int(result[1]),
                    'id_monitor':int(result[2]),
                    'id_periodo':int(result[3]),
                    'fecha_inicio':result[4],
                    'nivel_riesgo':result[5],
                    'motivo':result[6],
                    'plan_acompanamiento':result[7],
                    'resultado':result[8],
                    'estado':result[9],
                    'fecha_cierre':result[10]
            }
            payload.append(content)
            
            json_data = jsonable_encoder(content)            
            if result:
               return  json_data
            else:
                raise HTTPException(status_code=404, detail="seguimiento academico not found")  
                
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()

    def create_seguimiento_academico(self, seguimiento_academico_data: dict):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO seguimiento_academico (id_estudiante, id_monitor, id_periodo, fecha_inicio, nivel_riesgo, motivo, plan_acompanamiento, resultado, estado, fecha_cierre) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_seguimiento",
                (
                    seguimiento_academico_data['id_estudiante'],
                    seguimiento_academico_data['id_monitor'],
                    seguimiento_academico_data['id_periodo'],
                    seguimiento_academico_data['fecha_inicio'],
                    seguimiento_academico_data.get('nivel_riesgo'),
                    seguimiento_academico_data.get('motivo'),
                    seguimiento_academico_data['plan_acompanamiento'],
                    seguimiento_academico_data['resultado'],
                    seguimiento_academico_data['estado'],
                    seguimiento_academico_data.get('fecha_cierre')
                )
            )
            new_id = cursor.fetchone()[0] #type: ignore
            conn.commit()
            return {"id_seguimiento": new_id}
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e)}
        finally:
            if conn:
                conn.close()

    def update_seguimiento_academico(self, id_seguimiento: int, seguimiento_academico_data: dict):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE seguimiento_academico SET id_estudiante = %s, id_monitor = %s, id_periodo = %s, fecha_inicio = %s, nivel_riesgo = %s, motivo = %s, plan_acompanamiento = %s, resultado = %s, estado = %s, fecha_cierre = %s WHERE id_seguimiento = %s",
                (
                    seguimiento_academico_data['id_estudiante'],
                    seguimiento_academico_data['id_monitor'],
                    seguimiento_academico_data['id_periodo'],
                    seguimiento_academico_data['fecha_inicio'],
                    seguimiento_academico_data.get('nivel_riesgo'),
                    seguimiento_academico_data.get('motivo'),
                    seguimiento_academico_data['plan_acompanamiento'],
                    seguimiento_academico_data['resultado'],
                    seguimiento_academico_data['estado'],
                    seguimiento_academico_data.get('fecha_cierre'),
                    id_seguimiento
                )
            )
            conn.commit()
            return {"message": "Seguimiento Académico updated successfully"}
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e)}
        finally:
            if conn:
                conn.close()

    def delete_seguimiento_academico(self, id_seguimiento: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM seguimiento_academico WHERE id_seguimiento = %s", (id_seguimiento,))
            conn.commit()
            return {"message": "Seguimiento Académico deleted successfully"}
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e)}
        finally:
            if conn:
                conn.close()
        
