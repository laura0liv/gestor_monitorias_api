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
                    'nombre':result[1],
                    'apellido':result[2],
                    'correo':result[3],
                    'telefono':result[4],
                    'contraseña':result[5],
                    'tipo_documento':result[6],
                    'numero_documento':result[7],
                    'estado':result[8]
              
                }
                payload.append(content)
                content={}
            
            return payload

        except Exception as e:
            return {"error": str(e)}

        finally:
            if conn:
                conn.close()