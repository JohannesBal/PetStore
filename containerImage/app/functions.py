from flask import Flask, jsonify
import json, mariadb

from configs import db_config

def getData(query: str):
    connection = mariadb.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute(query)

    row_headers=[i[0] for i in cursor.description]
    rv = cursor.fetchall()

    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))

    result = {'status': '200', 'description': 'Success', 'data': json_data}
    return jsonify(result)


def postData(dest: str, jsonData: str):
    connection = mariadb.connect(**db_config)
    cursor = connection.cursor()
    
    if dest == 'owners':
        query = 'insert into owners (first_name, last_name, email) values (%s, %s, %s)'
        values = (jsonData['first_name'], jsonData['last_name'], jsonData['email'])
    elif dest == 'pets':
        query = 'insert into pets (fk_owned_by, pet_name, species) values (%s, %s, %s)'
        values = (jsonData['fk_owned_by'], jsonData['pet_name'], jsonData['species'])
    else:
        return jsonify({'status': '400', 'description': 'Bad Request'})

    cursor.execute(query, values)
    inserted_id = cursor.lastrowid

    connection.commit()

    result = {'status': '201', 'description': 'Success', 'inserted_id': inserted_id}
    return jsonify(result)


def importData(jsonData: list):
    connection = mariadb.connect(**db_config)
    cursor = connection.cursor()

    owner_count = 0
    pet_count = 0

    for data in jsonData:
        pets = data.pop('pets', [])

        queryOwners = 'insert into owners (first_name, last_name, email) values (%s, %s, %s)'
        valueOwners = (data['first_name'], data['last_name'], data['email'])

        cursor.execute(queryOwners, valueOwners)
        last_inserted = cursor.lastrowid
        
        owner_count += 1
        pet_count += len(pets)

        queryPets = 'insert into pets (fk_owned_by, pet_name, species) values (%s, %s, %s)'
        cursor.executemany(queryPets, [(last_inserted, pet['name'], pet['species']) for pet in pets])

    connection.commit()

    result = {'status': '201', 'description': 'Success', 'inserted': { 'owners': owner_count, 'pets': pet_count }}
    return jsonify(result)

def deleteData(dest: str, id: int):
    connection = mariadb.connect(**db_config)
    cursor = connection.cursor()

    if dest == 'owners':
        check = getData('select * from owners where owner_id=%s' % (id)) 
        if check:
            query = 'delete from owners where owner_id=%s' % (id)

    elif dest == 'pets':
        check = getData('select * from pets where pet_id=%s' % (id))
        if check:
            query = 'delete from pets where pet_id=%s' % (id)

    else:
        return jsonify({'status': '400', 'description': 'Bad Request'})
    
    if not query:
        return jsonify({'status': '404', 'description': 'Data not found'})

    cursor.execute(query)
    connection.commit()

    result = {'status': '200', 'description': 'Success', 'removed_id': id}
    return jsonify(result)
