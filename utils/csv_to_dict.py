import csv
import os


def csv_to_dict(filename):
    """Lee el CSV y devuelve un diccionario de columnas con los valores exactos"""
    path = f'database/{filename}.csv'

    if not os.path.exists(path):
        raise FileNotFoundError(f"Archivo no encontrado: {path}")

    data = {}

    with open(path, mode='r', encoding='utf-8') as file:
        # Leer todas las líneas no vacías
        lines = [line.strip() for line in file if line.strip()]

        if not lines:
            raise ValueError("El archivo CSV está vacío")

        # Reiniciar el cursor para volver a leer
        file.seek(0)

        # Leer como DictReader para manejar correctamente las comillas
        reader = csv.DictReader(file)

        # Inicializar estructura de datos
        headers = reader.fieldnames
        for header in headers:
            data[header.strip()] = []

        # Procesar cada fila
        for row in reader:
            for header in headers:
                data[header.strip()].append(row[header].strip() if row[header] else None)

    return data


def get_record_by_id(filename, id_value, id_field='id_producto'):
    data = csv_to_dict(filename)

    if id_field not in data:
        raise ValueError(f'Campo {id_field} no existe en el CSV')

    # Convertir a string y limpiar el valor buscado
    search_id = str(id_value).strip()

    # Buscar coincidencia exacta
    try:
        index = data[id_field].index(search_id)
        return {key: data[key][index] for key in data.keys()}
    except ValueError:
        return None


def add_record(filename, new_data, id_field='id_producto'):
    path = f'database/{filename}.csv'

    try:
        # Leer datos existentes desde el CSV
        existing_data = csv_to_dict(filename)
        headers = list(existing_data.keys())

        # Calcular el nuevo ID (generar si no existe)
        if id_field in existing_data and existing_data[id_field]:
            last_id = max(int(id_) for id_ in existing_data[id_field] if id_.isdigit())
            new_id = str(last_id + 1)
        else:
            new_id = '1'

    except (FileNotFoundError, ValueError):
        headers = list(new_data.keys())  # Si el archivo no existe o está vacío, usar las claves del nuevo dato
        existing_data = {header: [] for header in headers}
        new_id = '1'  # Generar el primer ID

    # Verificar que los campos necesarios estén presentes (sin contar id_producto ni fecha_creacion)
    required_fields = ['nombre', 'descripcion', 'precio', 'categoria', 'stock', 'marca']
    missing_fields = [field for field in required_fields if field not in new_data]
    if missing_fields:
        raise ValueError(f"Campos faltantes: {', '.join(missing_fields)}")

    # Si no hay fecha_creacion, agregarla
    if 'fecha_creacion' not in new_data:
        from datetime import datetime
        new_data['fecha_creacion'] = datetime.now().strftime('%Y-%m-%d')

    # Asignar el nuevo ID
    new_data[id_field] = new_id

    # Asegurarse de que todos los datos estén en las columnas correctas
    for header in headers:
        if header not in new_data:
            new_data[header] = ''  # Si falta algún campo, agregarlo como vacío

    # Agregar el nuevo registro a los datos existentes
    for header in headers:
        existing_data[header].append(str(new_data.get(header, '')))

    # Escribir los datos actualizados al archivo CSV
    with open(path, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()

        records = []
        for i in range(len(existing_data[headers[0]])):
            record = {header: existing_data[header][i] for header in headers}
            records.append(record)

        writer.writerows(records)

    return new_data



def update_record(filename, id_value, updated_data, id_field='id_producto'):
    path = f'database/{filename}.csv'
    data = csv_to_dict(filename)

    if id_field not in data:
        raise ValueError(f'Campo ID {id_field} no existe')

    try:
        index = data[id_field].index(str(id_value))
    except ValueError:
        raise ValueError(f'ID {id_value} no encontrado')

    # Actualizar solo campos existentes
    headers = list(data.keys())
    for key in updated_data:
        if key in headers and key != id_field:  # No permitir actualizar el ID
            data[key][index] = str(updated_data[key])

    # Escribir archivo
    with open(path, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(
            [{header: data[header][i] for header in headers}
             for i in range(len(data[headers[0]]))]
        )

    return get_record_by_id(filename, id_value, id_field)


def delete_record(filename, id_value, id_field='id_producto'):
    path = f'database/{filename}.csv'
    data = csv_to_dict(filename)

    if id_field not in data:
        raise ValueError(f'Campo ID {id_field} no existe')

    try:
        index = data[id_field].index(str(id_value))
    except ValueError:
        raise ValueError(f'ID {id_value} no encontrado')

    # Eliminar registro
    headers = list(data.keys())
    for header in headers:
        del data[header][index]

    # Escribir archivo
    with open(path, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(
            [{header: data[header][i] for header in headers}
             for i in range(len(data[headers[0]]))]
        )

    return True


def search_by_name(filename, name, name_field='nombre'):
    data = csv_to_dict(filename)

    if name_field not in data:
        raise ValueError(f'Campo {name_field} no existe')

    search_term = name.lower().strip()
    headers = list(data.keys())

    return [
        {header: data[header][i] for header in headers}
        for i in range(len(data[name_field]))
        if search_term in data[name_field][i].lower()
    ]