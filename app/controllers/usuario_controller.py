from http.client import HTTPException
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
import psycopg2
from config.db_config import get_db_connection


class UsuarioController:

    def get_all_usuario(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuario")
            results = cursor.fetchall()
            payload = []
            content = {}
            
            for result in results:
                content={
                    'id_usuario':int(result[0]),
                    'tipo_documento':result[1],
                    'numero_documento':result[2],
                    'nombre':result[3],
                    'apellido':result[4],
                    'correo':result[5],
                    'telefono':result[6],
                    'contrasena':result[7],
                    'estado':result[8],
                    'id_rol':result[9]
              
                }
                payload.append(content)
                content={}
            
            return payload

        except Exception as e:
            return {"error": str(e)}

        finally:
            if conn:
                conn.close()
    
    
    def get_usuario(self, id_usuario: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuario WHERE id_usuario = %s", (id_usuario,))
            result = cursor.fetchone()
            payload = []
            content = {} 
            
            content={
                    'id_usuario':int(result[0]), 
                    'tipo_documento':result[1],
                    'numero_documento':result[2],
                    'nombre':result[3],
                    'apellido':result[4],
                    'correo':result[5],
                    'telefono':result[6],
                    'contrasena':result[7],
                    'estado':result[8],
                    'id_rol':result[9]
            }
            payload.append(content)
            
            json_data = jsonable_encoder(content)            
            if result:
               return  json_data
            else:
                raise HTTPException(status_code=404, detail="User not found")  
                
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()

    def create_usuario(self, usuario_data: dict):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO usuario (tipo_documento, numero_documento, nombre, apellido, correo, telefono, contrasena, estado, id_rol) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_usuario",
                (
                    usuario_data['tipo_documento'],
                    usuario_data['numero_documento'],
                    usuario_data['nombre'],
                    usuario_data['apellido'],
                    usuario_data['correo'],
                    usuario_data['telefono'],
                    usuario_data['contrasena'],
                    usuario_data['estado'],
                    usuario_data['id_rol']
                )
            )
            new_id = cursor.fetchone()[0] #type: ignore
            conn.commit()
            return {"id_usuario": new_id}
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e)}
        finally:
            if conn:
                conn.close()

    def update_usuario(self, id_usuario: int, usuario_data: dict):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE usuario SET tipo_documento = %s, numero_documento = %s, nombre = %s, apellido = %s, correo = %s, telefono = %s, contrasena = %s, estado = %s, id_rol = %s WHERE id_usuario = %s",
                (
                    usuario_data['tipo_documento'],
                    usuario_data['numero_documento'],
                    usuario_data['nombre'],
                    usuario_data['apellido'],
                    usuario_data['correo'],
                    usuario_data['telefono'],
                    usuario_data['contrasena'],
                    usuario_data['estado'],
                    usuario_data['id_rol'],         
                    id_usuario
                )
            )
            conn.commit()
            return {"message": "Usuario updated successfully"}
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e)}
        finally:
            if conn:
                conn.close()

    def delete_usuario(self, id_usuario: int):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuario WHERE id_usuario = %s", (id_usuario,))
            conn.commit()
            return {"message": "Usuario deleted successfully"}
        except Exception as e:
            if conn:
                conn.rollback()
            return {"error": str(e)}
        finally:
            if conn:
                conn.close()
        
