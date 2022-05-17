
# Project
The main ideia of this project is build a data serve that will be accessed by  distributed servers, called business server, theses distributed server will be accessed by clients that will test the features of the business service.

```
├───business
│   ├───application
│   └───infra
├───client
│   └───infra
├───data
└───shared
```

the project is divided in 4 parts

* Data
* Business
* Client
* Shared

## Data
server used to control of data, here simule a database in memory.

```
├───data
│       data_server.py
```

To use a simple code only in one file simulating a low level programming for "high" performance

### EndPoints

* /getLock/{businessId}/{accountId} POST
    > responsible to lock one account by businessId 
* /unLock/{businessId}/{accountId} POST
    > responsible to unlock one account that the businessId is owner
* /setAmount/{businessId}/{accountId} POST
    > responsible to set amount value in a locked account by the businessId
* /getAmount/{businessId}/{accountId} GET
    > responsible to get informations one account that is not locked by another businessId


### Authentication

The authentication is by hardcode keys and is validated in a middleware in shared folder

### Settings config

To run this part of system is necessary a config file like this

/data/settings.py
```python
authKey = [
    'YOUR KEY HERE',
    'YOUR OTHER KEY HERE'
]
```

## Business

The business zone of code is used to access the data information to control balance of accounts 

```
├───business
│   │   business_server.py
│   │
│   ├───application
│   │       bank_service.py
│   │       queue_service.py
│   │
│   └───infra
            amount_repository.py
            lock_repository.py
```

The structure of code is designed similar a web service with layers dividing in 3 parts

* Presentation (root folder)
* Application (logical layer)
* Infrastrucure (data access layer)

### Presentation

EndPoint

* /deposit/{accountId}/{amount} POST
    > responsible to deposit one value in one account 
* /withdrawal/{accountId}/{amount} POST
    > responsible to withdrawal some value from account
* /balance/{accountId} GET
    > responsible to get the balance of one account
* /transfer/{originAccountId}/{targetAccountId}/{amount} POST
    > responsible to transfer a amount of origin account to a target account

### Application

This is the logical part of code, here is responsible to apply the business rule of deposit, withdrawal, the queue of 5 operations before save in data server

### Infrastrucure

This is the part of data access of the system, here was divided in 2 repositories, the amount and the lock repository each one with a differents settings, this choose was taken thinking in a modular code and microservices applications

### Authentication

The authentication is by hardcode keys and is validated in a middleware in shared folder

### Settings Config

To run this part of system is necessary a config file like this

/business/settings.py
```python
businessId = 2 #YOUR BUSINESSID HERE

authKey = [
    'YOUR KEY HERE',
    'YOUR OTHER KEY HERE'
]

amountApiSettings = {
    "URL" = "YOUR DATA SERVER URL",
    "AuthenticationKey" = "YOUR DATA SERVER AUTHENTICATION KEY"
}

lockApiSettings = {
    "URL" = "YOUR DATA SERVER URL",
    "AuthenticationKey" = "YOUR DATA SERVER AUTHENTICATION KEY"
}
```

## Client

```
├───client
│   │   client_script.py
│   │
│   └───infra
│           bank_repository.py
```

This part of code was designed to be a test script using a infra layer to access the business server. Here it will test

* Authentication necessity
* If queue works
* If deposits works
* If withdrawal works
* If transfer works
* Concurrent requests

### Settings config

To run this part of system is necessary a config file like this

/client/settings.py
```python
bankApiSettings = {
    "AuthenticationKey" = "YOUR BUSINESS SERVER AUTHENTICATION KEY"
}
```

## Shared

```
└───shared
        auth_middleware.py
        http_utils.py
```
Here has a shared utils files like a middleware to authentication by fixed keys (used by data server and business server) and a http requests and validation util file (used by client and business server)

# To Run

To run this code first of all, it is necessary to set a $PYTHONPATH with the command
```bash
export PYTHONPATH = $PYTHONPATH:/YOUR DIRECTORY PATH/DistributedComputing_DistributedDataServer/shared
```

And to run the web applications uses:
```bash
FLASK_APP={business/business_server OR data/business_server} flask run
```

or use this tutorial to ser up your visual studio code https://code.visualstudio.com/docs/python/tutorial-flask

And to run the client test uses:
```bash
python client/client_script.py
```

# Tests
the following videos show the system working

part 1: https://www.loom.com/share/0e6d1d92f0504bbd954d2c0d6c8cf13a 

part 2: https://www.loom.com/share/bd1d1b2d3eb1402ca3c37c868f4f0237

### Images of logs

