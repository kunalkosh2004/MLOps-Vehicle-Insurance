# Project Overview
This project is a comprehensive workflow for setting up a Python-based application with MongoDB integration, data ingestion, processing, model training, deployment, and CI/CD pipeline using AWS services.

## Table of Contents
1. [Project Setup](#project-setup)
2. [MongoDB Setup](#mongodb-setup)
3. [Logging, Exception Handling, and Notebooks](#logging-exception-handling-and-notebooks)
4. [Data Ingestion](#data-ingestion)
5. [Data Validation, Transformation, and Model Training](#data-validation-transformation-and-model-training)
6. [AWS Services Setup](#aws-services-setup)
7. [Model Evaluation and Prediction Pipeline](#model-evaluation-and-prediction-pipeline)
8. [CI/CD Pipeline](#ci-cd-pipeline)

---

## Project Setup

1. **Create Project Template**
   - Execute `template.py` to initialize the project structure.

2. **Setup Local Package Imports**
   - Write code in `setup.py` and `pyproject.toml` to manage local package imports.
   - Refer to `crashcourse.txt` for detailed instructions.

3. **Environment and Dependencies**
   - Create and activate a virtual environment:
     ```bash
     conda create -n vehicle python=3.10 -y
     conda activate vehicle
     ```
   - Add required modules to `requirements.txt`.
   - Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```
   - Verify installed packages:
     ```bash
     pip list
     ```

---

## MongoDB Setup

1. **Create a MongoDB Atlas Account**
   - Sign up and create a new project.

2. **Set Up a Cluster**
   - Use M0 service (free tier) with default settings.

3. **User and Network Configuration**
   - Set up a DB user with a username and password.
   - Add IP address `0.0.0.0/0` to Network Access for global access.

4. **Connection String**
   - Retrieve the connection string (Driver: Python, Version: 3.6+), replace the password, and save it.

5. **Data Ingestion to MongoDB**
   - Create a folder `notebook` and add datasets.
   - Create a `mongoDB_demo.ipynb` file to upload data to MongoDB.

6. **Verify Data**
   - Browse MongoDB Atlas collections to see your data in key-value format.

---

## Logging, Exception Handling, and Notebooks

1. **Logging and Exception Handling**
   - Write logger and exception handling scripts.
   - Test these scripts in `demo.py`.

2. **Notebooks for EDA and Feature Engineering**
   - Add exploratory data analysis (EDA) and feature engineering notebooks.

---

## Data Ingestion

1. **Setup Configuration**
   - Define variables in `constants.__init__.py`.
   - Implement MongoDB connection in `configuration.mongo_db_connections.py`.

2. **Data Access and Transformation**
   - Write scripts in `data_access/proj1_data.py` to fetch data from MongoDB and transform it into a DataFrame.

3. **Define Data Ingestion Classes**
   - Implement `DataIngestionConfig` in `entity.config_entity.py`.
   - Implement `DataIngestionArtifact` in `entity.artifact_entity.py`.

4. **Run Data Ingestion**
   - Add and test ingestion logic in `components.data_ingestion.py`.
   - Set up MongoDB connection URL and test with `demo.py`.

---

## Data Validation, Transformation, and Model Training

1. **Data Validation**
   - Complete `utils.main_utils.py` and `config.schema.yaml` for validation.
   - Implement the validation component similar to Data Ingestion.

2. **Data Transformation**
   - Implement transformation logic in `components.data_transformation.py`.
   - Add `estimator.py` for transformation logic in the `entity` folder.

3. **Model Training**
   - Add training logic to `components.model_trainer.py`.
   - Update `estimator.py` with model training code.

---

## AWS Services Setup

1. **IAM Configuration**
   - Create a new IAM user with `AdministratorAccess`.
   - Generate and download access keys.

2. **Environment Variables**
   - Set up AWS access keys as environment variables.

3. **S3 Bucket**
   - Create an S3 bucket for model storage.

4. **AWS Configuration**
   - Implement S3 interactions in `src.configuration.aws_connection.py` and `src.aws_storage/s3_estimator.py`.

---

## Model Evaluation and Prediction Pipeline

1. **Model Evaluation**
   - Implement model evaluation logic in `components.model_evaluation.py`.

2. **Prediction Pipeline**
   - Set up `app.py` and the required routes for prediction.
   - Add `static` and `template` directories.

---

## CI/CD Pipeline

1. **Docker Setup**
   - Write a `Dockerfile` and `.dockerignore`.

2. **GitHub Actions**
   - Create workflows in `.github/workflows/aws.yaml`.

3. **EC2 and Runner Setup**
   - Launch an EC2 instance and install Docker.
   - Connect GitHub Actions to the EC2 instance using a self-hosted runner.

4. **ECR Repository**
   - Create an ECR repository for Docker images.

5. **Deploy Application**
   - Open port 5080 in the EC2 security group.
   - Access the application using the public IP and port.

---

**Happy Coding!**

