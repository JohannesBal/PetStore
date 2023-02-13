from flask import Blueprint, jsonify, request
import json
from functions import getData, postData, importData, deleteData

routes = Blueprint('routes', __name__)

### GETTERS ###
@routes.route('/owners', methods = ['GET'])
def getOwners():
    return getData('select * from owners')

@routes.route('/ownerswithpets', methods = ['GET'])
def getOwnersAndPets():
    return getData('select owners.owner_id, owners.first_name, owners.last_name, owners.email, group_concat(pets.pet_id) as pets from owners left join pets on owners.owner_id = pets.fk_owned_by group by owners.owner_id;')

@routes.route('/owners/<int:ownerId>', methods = ['GET'])
def getOwner(ownerId: int):
    return getData('select * from owners where owner_id=%s' % (ownerId))

@routes.route('/ownerswithpets/<int:ownerId>', methods = ['GET'])
def getOwnerAndPets(ownerId: int):
    return getData('select owners.owner_id, owners.first_name, owners.last_name, owners.email, group_concat(pets.pet_id) as pets from owners left join pets on owners.owner_id = pets.fk_owned_by where owners.owner_id=%s group by owners.owner_id;' % (ownerId))

@routes.route('/owners/<int:ownerId>/pets', methods = ['GET'])
def getPetsOfOwner(ownerId: int):
    return getData('select * from pets where fk_owned_by=%s' % (ownerId))

@routes.route('/pets', methods = ['GET'])
def getPets():
    return getData('select * from pets')

@routes.route('/pets/<int:petId>', methods = ['GET'])
def getPet(petId: int):
    return getData('select * from pets where pet_id=%s' % (petId))
### END ###

### POSTS ####
@routes.route('/owners', methods = ['POST'])
def postOwner():
    data = request.get_json()
    return postData('owners', data)

@routes.route('/pets', methods = ['POST'])
def postPet():
    data = request.get_json()
    return postData('pets', data)


@routes.route('/customers', methods = ['POST'])
def postCustomer():
    data = request.get_json()
    return importData(data)
### END ###

### DELETES ###
@routes.route('/owners/<int:ownerId>', methods = ['DELETE'])
def deleteOwner(ownerId: int):
    return deleteData('owners', ownerId)

@routes.route('/pets/<int:petId>', methods = ['DELETE'])
def deletePet(petId: int):
    return deleteData('pets', petId)


### END ###
