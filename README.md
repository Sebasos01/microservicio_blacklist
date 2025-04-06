# Blacklists Microservice

## Table of Contents
1. [Overview](#overview)  
2. [Part 1: Local Setup & Testing](#part-1-local-setup--testing)  
   - [Prerequisites](#prerequisites)  
   - [Installation Steps](#installation-steps)  
   - [Local Environment Variables](#local-environment-variables)  
   - [Running the Application Locally](#running-the-application-locally)  
   - [Testing with Postman](#testing-with-postman)  
   - [Available Endpoints (Local)](#available-endpoints-local)  
3. [Part 2: AWS Elastic Beanstalk Deployment](#part-2-aws-elastic-beanstalk-deployment)  
    - [Setting Up the RDS PostgreSQL Instance](#1-setting-up-the-rds-postgresql-instance)  
    - [Creating the Database Schema](#2-creating-the-database-schema)  
    - [Configuring Elastic Beanstalk](#3-configuring-elastic-beanstalk)  
    - [Deploying the Application to EB (Manual Zip Upload)](#4-deploying-the-application-to-eb-manual-zip-upload)  
    - [Postman Testing on the EB Environment](#5-postman-testing-on-the-eb-environment)  

---

## Overview
This **Blacklists Microservice** allows you to blacklist emails for a given application (`app_uuid`) and optionally record the reason for blacklisting along with the IP address that performed the request.  

The microservice provides:
- An endpoint to **add** an email to the blacklist.
- An endpoint to **check** if an email is already blacklisted.
- A **health check** endpoint to confirm the service is up and running.  

For now, this document **only covers local setup and testing**. You will find a placeholder for part 2 which will detail the **AWS Elastic Beanstalk** deployment and **PostgreSQL RDS** configuration at a later time.

---

## Part 1: Local Setup & Testing

### Prerequisites
1. **Python 3.7+** (make sure `python --version` matches or exceeds 3.7).
2. **pip** (comes bundled with most Python installations).
3. **Virtualenv** or the ability to create Python virtual environments.

### Installation Steps

1. **Clone or Download** this repository. Inside the project root, you should see the following structure (shortened for clarity):

   ```
   .
   ├── app/
   │   ├── __init__.py
   │   ├── auth.py
   │   ├── extensions.py
   │   ├── models.py
   │   ├── routes.py
   │   └── schemas.py
   ├── application.py
   ├── config.py
   ├── requirements.txt
   └── Blacklists Microservice Local Testing.postman_collection.json
   ```

2. **Create a virtual environment** (recommended) and activate it.

   ```bash
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   
   # On Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install the dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

### Local Environment Variables
By default, the application uses `DevelopmentConfig` from `config.py`. This means:
- A local SQLite database (`dev.db`) is used unless overridden by an environment variable `DATABASE_URL`.  
- A static JWT token is used for authorization, defaulting to `mi_token_jwt_estatico`, but you can change it by setting `JWT_STATIC_TOKEN` in your environment.

If you want to customize any environment variables locally, you can create a `.env` file in the project root or export them directly in your shell before running:

```bash
export FLASK_CONFIG="config.DevelopmentConfig"
export JWT_STATIC_TOKEN="my_custom_jwt_token_here"
export DATABASE_URL="sqlite:///my_dev_database.db"
```

> **Note**: For local testing, you typically won't need to modify these unless you have specific requirements.

### Running the Application Locally
After installing dependencies and (optionally) setting your local environment variables, you can run:

```bash
python application.py
```

This will start the Flask development server at [http://0.0.0.0:8000](http://0.0.0.0:8000).  
Feel free to open your browser or use a tool like Postman to hit the endpoints.

### Testing with Postman
A Postman collection is provided in the repo: **`Blacklists Microservice Local Testing.postman_collection.json`**. You can import this collection into Postman to test all the endpoints quickly.

1. **Import** the collection into Postman:
   - Open Postman, go to **File** -> **Import**.
   - Select the JSON file named `Blacklists Microservice Local Testing.postman_collection.json`.

2. **Set up JWT token in Postman Environment**:
   - In Postman, create (or use an existing) environment and add a variable, e.g. `jwt_token`.
   - Set its **Initial Value** and **Current Value** to your JWT token. By default, the microservice expects `mi_token_jwt_estatico` if you haven't changed `JWT_STATIC_TOKEN`.
   - The requests in the Postman collection will use `Bearer {{auth_token}}` in the **Authorization** header to pass your token.

3. **Send requests** to the endpoints; the collection has examples for:
   - **POST** to create a new blacklist entry.
   - **GET** to check if an email is blacklisted.
   - **GET** to check health status.

### Available Endpoints (Local)

1. **Health Check**  
   - **Endpoint**: `GET /blacklists/health`  
   - **Description**: Simple check to ensure the service is running.  
   - **Response**:  
     ```json
     {
       "status": "OK"
     }
     ```

2. **Add to Blacklist**  
   - **Endpoint**: `POST /blacklists/`  
   - **Authorization**: `Bearer {jwt_token}` (Header)  
   - **JSON Body**:
     ```json
     {
       "email": "test@example.com",
       "app_uuid": "some-unique-app-id",
       "reason": "Optional reason"
     }
     ```
   - **Response**:  
     ```json
     {
       "message": "Email agregado a la lista negra",
       "data": {
         "id": 1,
         "email": "test@example.com",
         "app_uuid": "some-unique-app-id",
         "reason": "Optional reason",
         "ip_address": "127.0.0.1",
         "created_at": "2025-04-06T12:34:56.789Z"
       }
     }
     ```
     (Status code: `201 Created`)

3. **Check Blacklist**  
   - **Endpoint**: `GET /blacklists/<string:email>`  
   - **Authorization**: `Bearer {jwt_token}` (Header)  
   - **Response (if blacklisted)**:  
     ```json
     {
       "blacklisted": true,
       "email": "test@example.com",
       "reason": "Optional reason",
       "app_uuid": "some-unique-app-id",
       "created_at": "2025-04-06T12:34:56.789Z"
     }
     ```
   - **Response (if not blacklisted)**:  
     ```json
     {
       "blacklisted": false,
       "email": "test@example.com"
     }
     ```

---

## Part 2: AWS Elastic Beanstalk Deployment

This section describes how to deploy the **Blacklists Microservice** to an Amazon EC2 instance via Elastic Beanstalk (EB), using a PostgreSQL instance in Amazon RDS. It covers:

---

### 1. Setting Up the RDS PostgreSQL Instance
1. **Go to the RDS console** in your AWS account.
2. **Create a new database** (Select **PostgreSQL** as the engine).
3. **Specify the DB instance details**, such as instance class, storage, and username/password.  
   - **DB name**: This **must match** the environment variable you will configure in Elastic Beanstalk (e.g., `RDS_DB_NAME`).
   - **Master username**: Will match `RDS_USERNAME`.
   - **Master password**: Will match `RDS_PASSWORD`.

4. After the instance is created, note the following RDS information (you will need these for EB environment variables):
   - **Endpoint** (e.g. `mydb.xxxxx.us-east-1.rds.amazonaws.com`)
   - **Port** (default PostgreSQL port is 5432, unless you customized it)

5. **Configure inbound rules** in the **RDS security group** to allow the Elastic Beanstalk instance to connect to the PostgreSQL port (5432). Typically, you will:
   - Add the EC2 security group (the one associated with the EB environment) as an inbound rule for your RDS security group on port 5432.

### 2. Creating the Database Schema
Once the RDS is up and running, you need to create the schema (i.e., the tables) used by the microservice.

1. **Connect to your RDS** using a PostgreSQL client (e.g., `psql` from a local machine or EC2).
   ```bash
   psql --host=YOUR_RDS_ENDPOINT --port=5432 --username=YOUR_RDS_USERNAME --password --dbname=YOUR_RDS_DB_NAME
   ```
2. **Verify the database** is accessible:
   ```sql
   SELECT version();
   ```
3. **(Optional) Create the database** if you have not already done so. If you used the AWS console to specify the DB name, it should already exist. However, if needed:
   ```sql
   CREATE DATABASE your_db_name;
   ```
4. **Tables will be created automatically** by this microservice on the first run (thanks to `db.create_all()` in the code). You do not need to manually create the `blacklist` table. Once the service runs in your EB environment, it will handle table creation.

### 3. Configuring Elastic Beanstalk

1. **Go to the Elastic Beanstalk console** in your AWS account.
2. **Create a new Application** (or use an existing one).
3. **Create a new Environment** of type **Web server environment**.  
   - During creation, EB will provision an EC2 instance running a platform (e.g., Python 3.8).
4. **Set the environment variables** in the EB Configuration:
   - `FLASK_CONFIG`: `config.ProductionConfig`
   - `RDS_HOSTNAME`: (Your RDS endpoint, e.g. `mydb.xxxxx.us-east-1.rds.amazonaws.com`)
   - `RDS_PORT`: `5432` (or your custom port)
   - `RDS_DB_NAME`: (Your DB name, e.g. `my_eb_db`)
   - `RDS_USERNAME`: (Your RDS username)
   - `RDS_PASSWORD`: (Your RDS password)
   - `JWT_STATIC_TOKEN`: (Your preferred static token, e.g. `my_production_jwt_token`)
   - Optionally, set any other environment variables such as `SECRET_KEY`.

### 4. Deploying the Application to EB (Manual Zip Upload)

1. **In your local project**, ensure you have a **`Procfile`** at the root (which you already do).  
   - It typically contains something like:  
     ```
     web: gunicorn application:application
     ```
2. **Zip the application** contents from the root. Include:
   - All Python code (`app/`, `application.py`, `config.py`).
   - `requirements.txt`
   - `Procfile`
   - (Optionally) `.ebextensions/` if you have additional configurations.
3. **Upload the zip** to your EB environment:
   - In the EB console, go to **Actions** > **Upload and Deploy**.
   - Select your zipped file, then **Deploy**.
4. **Wait for the deployment** to finish. EB will:
   - Install dependencies.
   - Start the gunicorn server using your `Procfile`.
5. **Verify** the environment status is **Healthy** on the EB dashboard.

### 5. Postman Testing on the EB Environment
Once your EB environment is healthy and running, you can test the endpoints from Postman:

1. **Replace the localhost base URL** in your Postman requests with your EB environment domain.  
   - For example, if your environment URL is `http://my-blacklists-env.us-east-1.elasticbeanstalk.com`, then:  
     - `POST /blacklists/` becomes `http://my-blacklists-env.us-east-1.elasticbeanstalk.com/blacklists/`.
     - `GET /blacklists/<email>` becomes `http://my-blacklists-env.us-east-1.elasticbeanstalk.com/blacklists/test@example.com`.
2. **Keep using your `Bearer {{jwt_token}}`** in the Authorization header. Make sure the `jwt_token` variable in your Postman environment still matches the `JWT_STATIC_TOKEN` you set on EB.
3. **Send requests** just like you did locally to confirm everything works with the RDS PostgreSQL backend.
