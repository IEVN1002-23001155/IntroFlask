
from flask import Blueprint, jsonify, request
from database import mysql

maestros_bp = Blueprint(
    'maestros',
    __name__,
    url_prefix='/api/maestros'
)


def fila_a_diccionario(cursor, fila):
    columnas = [columna[0] for columna in cursor.description]
    return dict(zip(columnas, fila))


# GET: Listar todos los maestros
@maestros_bp.route("/", methods=['GET'])
def listar_maestros():
    cursor = None

    try:
        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT
                idmaestro,
                nombre,
                Apaterno AS apaterno,
                Amaterno AS amaterno,
                Correo AS correo
            FROM maestros
        """)

        datos = cursor.fetchall()

        maestros = [
            fila_a_diccionario(cursor, fila)
            for fila in datos
        ]

        return jsonify({
            'maestros': maestros,
            'mensaje': 'Lista de maestros',
            'exito': True
        }), 200

    except Exception as ex:
        return jsonify({
            'mensaje': 'Error al consultar los datos',
            'error': str(ex),
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()


# GET: Consultar un maestro por ID
@maestros_bp.route("/<int:idmaestro>", methods=['GET'])
def leer_maestro(idmaestro):
    cursor = None

    try:
        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT
                idmaestro,
                nombre,
                Apaterno AS apaterno,
                Amaterno AS amaterno,
                Correo AS correo
            FROM maestros
            WHERE idmaestro = %s
        """, (idmaestro,))

        fila = cursor.fetchone()

        if fila is None:
            return jsonify({
                'mensaje': 'Maestro no encontrado',
                'exito': False
            }), 404

        maestro = fila_a_diccionario(cursor, fila)

        return jsonify({
            'maestro': maestro,
            'exito': True
        }), 200

    except Exception as ex:
        return jsonify({
            'mensaje': 'Error al consultar el maestro',
            'error': str(ex),
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()


# POST: Registrar un maestro
@maestros_bp.route('/', methods=['POST'])
def registrar_maestro():

    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({
            'mensaje': 'Se requiere un objeto JSON',
            'exito': False
        }), 400

    # Validar ID Maestro
    idmaestro = datos.get('idmaestro')

    if type(idmaestro) is not int or idmaestro <= 0:
        return jsonify({
            'mensaje': 'El ID del maestro es inválido',
            'exito': False
        }), 400

    # Campos obligatorios
    campos = [
        'nombre',
        'apaterno',
        'amaterno',
        'correo'
    ]

    if any(
        campo not in datos
        or not isinstance(datos[campo], str)
        or not datos[campo].strip()
        for campo in campos
    ):
        return jsonify({
            'mensaje': 'Faltan campos obligatorios o son inválidos',
            'exito': False
        }), 400

    cursor = None

    try:
        cursor = mysql.connection.cursor()

        # Comprobar si el ID ya existe
        cursor.execute(
            """
            SELECT idmaestro
            FROM maestros
            WHERE idmaestro = %s
            """,
            (idmaestro,)
        )

        if cursor.fetchone() is not None:
            return jsonify({
                'mensaje': 'El ID del maestro ya existe',
                'exito': False
            }), 409

        # Insertar maestro
        cursor.execute("""
            INSERT INTO maestros
                (idmaestro, nombre, Apaterno, Amaterno, Correo)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            idmaestro,
            datos['nombre'].strip(),
            datos['apaterno'].strip(),
            datos['amaterno'].strip(),
            datos['correo'].strip()
        ))

        mysql.connection.commit()

        return jsonify({
            'mensaje': 'Maestro registrado correctamente',
            'exito': True
        }), 201

    except Exception as ex:
        mysql.connection.rollback()

        return jsonify({
            'mensaje': 'Error al registrar el maestro',
            'error': str(ex),
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()


# PUT: Modificar un maestro
@maestros_bp.route("/<int:idmaestro>", methods=['PUT'])
def modificar_maestro(idmaestro):

    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({
            'mensaje': 'No se recibieron datos válidos',
            'exito': False
        }), 400

    nombre = datos.get('nombre')
    apaterno = datos.get('apaterno')
    amaterno = datos.get('amaterno', '')
    correo = datos.get('correo')

    if (
        not isinstance(nombre, str)
        or not nombre.strip()
        or not isinstance(apaterno, str)
        or not apaterno.strip()
        or not isinstance(amaterno, str)
        or not isinstance(correo, str)
        or not correo.strip()
    ):
        return jsonify({
            'mensaje': 'Nombre, apellido paterno y correo son obligatorios',
            'exito': False
        }), 400

    cursor = None

    try:
        cursor = mysql.connection.cursor()

        cursor.execute(
            """
            SELECT idmaestro
            FROM maestros
            WHERE idmaestro = %s
            """,
            (idmaestro,)
        )

        maestro = cursor.fetchone()

        if not maestro:
            return jsonify({
                'mensaje': 'No existe un maestro con ese ID',
                'exito': False
            }), 404

        sql = """
            UPDATE maestros
            SET nombre = %s,
                Apaterno = %s,
                Amaterno = %s,
                Correo = %s
            WHERE idmaestro = %s
        """

        cursor.execute(sql, (
            nombre.strip(),
            apaterno.strip(),
            amaterno.strip(),
            correo.strip(),
            idmaestro
        ))

        mysql.connection.commit()

        return jsonify({
            'mensaje': 'Maestro modificado correctamente',
            'idmaestro': idmaestro,
            'exito': True
        }), 200

    except Exception as ex:
        mysql.connection.rollback()

        return jsonify({
            'mensaje': 'Error al modificar el maestro',
            'error': str(ex),
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()


# DELETE: Eliminar un maestro
@maestros_bp.route("/<int:idmaestro>", methods=['DELETE'])
def eliminar_maestro(idmaestro):

    cursor = None

    try:
        cursor = mysql.connection.cursor()

        cursor.execute(
            """
            SELECT idmaestro
            FROM maestros
            WHERE idmaestro = %s
            """,
            (idmaestro,)
        )

        maestro = cursor.fetchone()

        if not maestro:
            return jsonify({
                'mensaje': 'No existe un maestro con ese ID',
                'exito': False
            }), 404

        cursor.execute(
            """
            DELETE FROM maestros
            WHERE idmaestro = %s
            """,
            (idmaestro,)
        )

        mysql.connection.commit()

        return jsonify({
            'mensaje': 'Maestro eliminado correctamente',
            'idmaestro': idmaestro,
            'exito': True
        }), 200

    except Exception as ex:
        mysql.connection.rollback()

        return jsonify({
            'mensaje': 'Error al eliminar el maestro',
            'error': str(ex),
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()
