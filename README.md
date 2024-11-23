# e-comm

### What is this about

This project contains a Django-based e-commerce application with a PostgreSQL database running on the local machine. The Django application is containerized using Docker, while PostgreSQL runs natively on your host machine.

This setup is ideal for development purposes, allowing you to leverage your local database while isolating the application environment within a Docker container.

### Tell me more about the features

* Dockerized Django application.
* Uses local PostgreSQL for database management.
* Syncs code changes between the host and the container for seamless development.
* Ready-to-run development environment.

### What all do I need to get the application running

* Docker and Docker Compose installed.
* PostgreSQL installed and running on the local machine.
* Python dependencies listed in requirements.txt

### Tell me Step by Step process ot start the application

#### Step 1 - Cloning
First things First - get the project --> Clone the Repository

#### Step 2 - Setting up Postgres on local 
#### (Steps included are for MAC user - this can be looked up for the OS you are using)

Install postgres - `brew install postgresql`

Setting up the DB
```
➜  ~ brew services start postgresql
➜  ~ psql postgres

postgres=# CREATE DATABASE ecommerce;
CREATE DATABASE
postgres=# CREATE USER ecommerce_user WITH PASSWORD 'securepassword';
CREATE ROLE
postgres=# ALTER ROLE ecommerce_user SET client_encoding TO 'utf8';
ALTER ROLE
postgres=# GRANT ALL PRIVILEGES ON DATABASE ecommerce TO ecommerce_user;
GRANT
postgres=# ALTER USER ecommerce_user CREATEDB;
ALTER ROLE
```

#### Step 3 - Build and Run the Docker Container 

Go to the project dir and start the docker container -  `docker-compose up --build`

#### Step 4 - Access the Application
Open your browser and navigate to http://localhost:8000.
The Django development server should now be running and connected to your local PostgreSQL database.