from fastapi import HTTPException
from psycopg2.extras import RealDictCursor
from app.config.db_config import get_db_connection


class AuthController:

    @staticmethod
    def login(data):
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        try:
            query = """
                SELECT 
                    id_usuario,
                    nombre,
                    apellido,
                    correo,
                    id_rol
                FROM usuario
                WHERE correo = %s
                AND contrasena = %s
                AND active = true
                LIMIT 1
            """

            cursor.execute(query, (
                data["correo"],
                data["contrasena"]
            ))

            usuario = cursor.fetchone()

            if not usuario:
                raise HTTPException(
                    status_code=401,
                    detail="Correo o contraseña incorrectos"
                )

            # 🔥 respuesta estructurada para frontend
            return {
                "success": True,
                "user": usuario
            }

        finally:
            cursor.close()
            conn.close()