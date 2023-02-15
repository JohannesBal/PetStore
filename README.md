# Customer Environment PetStore

## Introduction

This is an application for the PetStore. It is an API based on flask that fetches data from a mariadb. Its built to easily manage the data of customers (owners and pets).

The application environment itself is created on Kubernetes and is using Helm the Kubernetes Package Manager.

## Quickstart
 
 The setup itself is really easy. 
 
You would need to have kubectl and helm installed already. Then just clone the repository, and give it a try.

To customize the application, you would only need to edit the values.yaml file(s). You could also easily do this via kubectl command line. We'll have some examples for that in the following.

## Configuration

**What you should configure** is the certificate for the ingress, by default there is one set up - enough for testing it locally, but you should definitely change that. You should also modify the database credentials and maybe the size of the volume if needed.

**TLS Certificate** 

> Stored in the petstore-app/values.yaml

    host: hostname
    tlsCert: base64 encoded cert
    tlsKey: base64 encoded key

Just create a certificate and encode the key and cert in base64 to be used in the secret. Paste the encoded values in the "tls.crt"/"tls.key".

You could also change the hostname if you want to.

**Access via hostname**

To access the ingress via hostname, you would need to modify your hosts-file by adding the ip of the ingress with the hostname you selected. Also make sure, you add another hostname for the api to the /etc/hosts. For example:

    # $ sudo vi /etc/hosts
    10.2.0.5 hostname
    10.2.0.5 api.hostname

**Database configs**

> Stored in mariadb/values.yaml

    # Database credentials
    dbUser: base64 encoded database user
    dbPassword: base64 encoded user password
    dbRootPassword: base 64 encoded root password
    dbName: name of the database
    dbPort: port of the database

    # Volume configs
    volume:
      enabled: true 
      capacity: 1Gi
      # some more

Just insert your values. If you dont want a volume included, just change `enabled: false`.


### Command line configuration samples

#### Changing certificate data

	cert=$(cat certfile.cert | base64 | grep '\t' '\0')
	key=$(cat certfile.key | base64 | grep '\t' '\0')
	
	helm install petstore petstore-app --set tls.crt=$cert --set tls.key=$key 

#### Disabling volume for database

	helm install petstore petstore-app --set mariadb.volume.enabled=false

#### Modifying credentials on database

> Note that it could cause issues when database volume already exists and you modify the user credentials as the user you apply would not be recognized by the database

	dbUser=$(echo -n sampleUser | base64)
	dbPassword=$(echo -n samplePass | base64)
	#dbRootPassword= ...
	
	helm install petstore petstore-app --set mariadb.dbUser=$dbUser --set mariadb.dbPassword=$dbPassword



## API Structure / Endpoints

### Owners

    # GET "/owners"
    -> result: All owners
    
    # GET "/ownerswithpets"
    -> result: All owners included with owners pets
    
    # GET "/owners/{ownerId}"
    -> result: Owner with owner_id ownerId
    
    # GET "/ownerswithpets/{ownerId}"
    -> result: Owner with owner_id ownerId included with owners pets
    
    # POST "/owners"
    -> requests: owner model in json
				
	# DELETE "/owners/{ownerId}"


### Pets

    # GET "/pets"
    -> result: All pets
    
    # GET "/pets/{petId}"
    -> result: Pet with pet_id petId
    
    # POST "/pets"
    -> requests: pet model in json
    
    # DELETE "/pets/{petId}"

### Importing legacy data

    # POST "/customers"
    -> requests: model with owner model data (and pet model data)


### Responses

	# GET-RESPONSE
		{'status': '200', 'description': 'Success', 'data': result}
	    
	# POST-RESPONSE
		{'status': '201', 'description': 'Success', 'inserted_id': inserted_id}
		{'status': '400', 'description': 'Bad Request'}
		
	# DELETE-RESPONSE
		{'status': '200', 'description': 'Success', 'removed_id': id}
		{'status': '400', 'description': 'Bad Request'}
		{'status': '404', 'description': 'Data not found'}
		
	# IMPORT
		{'status': '201', 'description': 'Success', 'inserted': { 'owners': owner_count, 'pets': pet_count }}


### Models

    # OWNER
		owner_id int NOT NULL AUTO_INCREMENT,
		first_name varchar(64) NOT NULL,
		last_name varchar(64) NOT NULL,
		email varchar(64) NOT NULL,
		PRIMARY KEY (owner_id)


    # PET
		pet_id int NOT NULL AUTO_INCREMENT,
		fk_owned_by int,
		pet_name varchar(64) NOT NULL,
		species varchar(64) NOT NULL,
		PRIMARY KEY (pet_id),
		FOREIGN KEY (fk_owned_by)
			REFERENCES owners(owner_id)
			ON DELETE CASCADE

