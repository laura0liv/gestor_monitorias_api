from fastapi import HTTPException
from psycopg2.extras import RealDictCursor
from app.config.db_config import get_db_connection


class UsuarioController:

    def get_all_usuario(self):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT
                    id_usuario,
                    tipo_documento,
                    numero_documento,
                    nombre,
                    apellido,
                    correo,
                    telefono,
                    contrasena,
                    estado,
                    id_rol,
                    active,
                    created_at,
                    updated_at
                FROM usuario
                WHERE active = true
            """)

            return cursor.fetchall()

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        finally:
            if conn:
                cursor.close()
                conn.close()

    def get_usuario(self, id_usuario: int):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                SELECT
                    id_usuario,
                    tipo_documento,
                    numero_documento,
                    nombre,
                    apellido,
                    correo,
                    telefono,
                    contrasena,
                    estado,
                    id_rol,
                    active,
                    created_at,
                    updated_at
                FROM usuario
                WHERE id_usuario = %s
                AND active = true
            """, (id_usuario,))

            result = cursor.fetchone()

            if not result:
                raise HTTPException(
                    status_code=404,
                    detail="Usuario not found"
                )

            return result

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        finally:
            if conn:
                cursor.close()
                conn.close()

    def create_usuario(self, usuario_data: dict):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute("""
                INSERT INTO usuario (
                    tipo_documento,
                    numero_documento,
                    nombre,
                    apellido,
                    correo,
                    telefono,
                    contrasena,
                    estado,
                    id_rol,
                    active
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id_usuario
            """, (
                usuario_data['tipo_documento'],
                usuario_data['numero_documento'],
                usuario_data['nombre'],
                usuario_data['apellido'],
                usuario_data['correo'],
                usuario_data['telefono'],
                usuario_data['contrasena'],
                usuario_data['estado'],
                usuario_data['id_rol'],
                usuario_data.get('active', True)
            ))

            new_data = cursor.fetchone()

            conn.commit()

            return {
                "message": "Usuario created successfully",
                "id_usuario": new_data["id_usuario"]
            }

        except Exception as e:
            if conn:
                conn.rollback()

            raise HTTPException(status_code=500, detail=str(e))

        finally:
            if conn:
                cursor.close()
                conn.close()

    def update_usuario(self, id_usuario: int, usuario_data: dict):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE usuario
                SET
                    tipo_documento = %s,
                    numero_documento = %s,
                    nombre = %s,
                    apellido = %s,
                    correo = %s,
                    telefono = %s,
                    contrasena = %s,
                    estado = %s,
                    id_rol = %s,
                    active = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id_usuario = %s
            """, (
                usuario_data['tipo_documento'],
                usuario_data['numero_documento'],
                usuario_data['nombre'],
                usuario_data['apellido'],
                usuario_data['correo'],
                usuario_data['telefono'],
                usuario_data['contrasena'],
                usuario_data['estado'],
                usuario_data['id_rol'],
                usuario_data['active'],
                id_usuario
            ))

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Usuario not found"
                )

            conn.commit()

            return {
                "message": "Usuario updated successfully"
            }

        except HTTPException:
            raise

        except Exception as e:
            if conn:
                conn.rollback()

            raise HTTPException(status_code=500, detail=str(e))

        finally:
            if conn:
                cursor.close()
                conn.close()

    def delete_usuario(self, id_usuario: int):
        conn = None

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE usuario
                SET
                    active = false,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id_usuario = %s
            """, (id_usuario,))

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Usuario not found"
                )

            conn.commit()

            return {
                "message": "Usuario deleted successfully"
            }

        except HTTPException:
            raise

        except Exception as e:
            if conn:
                conn.rollback()

            raise HTTPException(status_code=500, detail=str(e))

        finally:
            if conn:
                cursor.close()
                conn.close()