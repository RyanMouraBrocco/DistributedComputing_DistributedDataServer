
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

To use a simple code only in one file simulating a low level programming for "high" processing

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

### Settings config

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

### Infrastrucure

### Authentication

### Settings Config

## Client

## Shared

# Tests
the following videos show the system working

part 1: https://www.loom.com/share/0e6d1d92f0504bbd954d2c0d6c8cf13a 

part 2: https://www.loom.com/share/bd1d1b2d3eb1402ca3c37c868f4f0237

### Images of logs

