# DBT_Postgres_Elementary Project

### This project sets up a **DBT** (Data Build Tool) environment with a local or Docker-based PostgreSQL database and integrates **Elementary** for data monitoring and reporting.

## Project Setup

### 1. Create a Virtual Environment

1. Create and activate a virtual environment:

   On Linux/MacOS:
   ```bash
   python -m venv your_venv
   source your_venv/bin/activate
   ```

   On Windows:
   ```bash
   python -m venv your_venv
   your_venv\Scripts\activate
   ```

### 2. Upgrade PIP and Install Required Packages

Upgrade `pip` to the latest version:
   ```bash
   python -m pip install --upgrade pip
   ```

Install the required packages for DBT and PostgreSQL:
   ```bash
   pip install dbt-core dbt-postgres pandas setuptools
   ```

### 3. Create and Connect to PostgreSQL Database

You have two options for setting up a PostgreSQL server:

#### Option 1: Local PostgreSQL Setup

Create a PostgreSQL server with the following credentials:

- **Username**: `<your_username>`
- **Password**: `<your_password>`
- **Database**: `<your_db>`
- **Schema**: `<your_schema_name>`
- **Port**: `5432`
- **Host**: `localhost`

#### Option 2: Using Docker

A `docker-compose.yml` file is included in this project for easily setting up a PostgreSQL database using Docker.

1. Copy the `docker-compose.yml` file to your desired project folder.
2. Modify the connection string in `docker-compose.yml` as per your requirements.
3. Spin up the Docker container:
   ```bash
   docker-compose up -d
   ```
4. Verify that the Docker container is running:
   ```bash
   docker ps
   ```

### 4. Initialize DBT Project

1. Run the following command to initialize your DBT project:
   ```bash
   dbt init dbt_project
   cd dbt_project
   ```

2. Provide the following inputs during initialization:
   - **Project Name**: `dbt_project`
   - **Enter a number**: `1`
   - **Host**: `<host_id or IP address of the Docker container or local server>`
   - **Port**: `5432`
   - **User**: `<your_username>`
   - **Password**: `<your_password>`
   - **DB Name**: `<your_db>`
   - **Schema**: `<your_schema_name>`
   - **Threads**: `1`

This will generate a `profiles.yml` file in your home directory (e.g., `~/.dbt/profiles.yml`).

3. Verify the DBT project setup and PostgreSQL connection:
   ```bash
   dbt debug
   ```

## Loading Data into PostgreSQL

1. Place the `loan_data.csv` file in the root directory of your DBT project.

2. The project includes a `data_loader.py` script to load this data into PostgreSQL. You can run the script using the following command:
   ```bash
   python data_loader.py
   ```

## Setting Up Elementary for Data Monitoring

### 1. Add Elementary Package

1. Create a `packages.yml` file in the root of your DBT project and add the following content:
   ```
   packages:
     - package: elementary-data/elementary
       version: 0.16.1
   ```

2. Update the `dbt_project.yml` file to set a schema for Elementary models:
   ```
   models:
     elementary:
       +schema: "elementary"
   ```

### 2. Install Elementary and Run Models

1. Install dependencies:
   ```bash
   dbt deps
   ```

2. Run the Elementary models:
   ```bash
   dbt run --select elementary
   ```

3. Generate the Elementary CLI profile:
   ```bash
   dbt run-operation elementary.generate_elementary_cli_profile
   ```

4. Add the generated CLI profile in your `~/.dbt/profiles.yml` file.

5. Install the Elementary Data library for generating reports:
   ```bash
   pip install elementary-data[postgres]
   ```

6. Verify the installation:
   ```bash
   edr --version
   ```

## Running DBT Models and Generating Elementary Reports

1. Create your DBT models in the `models/` directory and run them:
   ```bash
   dbt run
   dbt test
   ```

2. Generate an Elementary report:
   ```bash
   edr report
   ```

## Project Structure

Once everything is set up, your project structure should resemble the following:

```
dbt_project/
│
├── your_venv/                # Virtual environment folder
├── dbt_project/              # DBT project folder
│   ├── analyses/
│   ├── dbt_packages/
│   ├── edr_target/
│   ├── logs/
│   ├── macros/
│   ├── models/
│   ├── seeds/
│   ├── snapshots/
│   ├── targets/
│   ├── tests/
│   └── dbt_project.yml       # DBT project configuration
├── loan_data.csv             # CSV data to load into PostgreSQL
├── data_loader.py            # Python script to load data into PostgreSQL
├── packages.yml              # DBT packages (Elementary configuration)
└── README.md                 # Project documentation
```

### Comments:
- The `data_loader.py` script is pre-configured to load data from `loan_data.csv` into your PostgreSQL database.
- Ensure that your `dbt_project.yml` and `profiles.yml` are correctly configured for DBT and Elementary to work smoothly.

This project provides a comprehensive environment to work with DBT and PostgreSQL, with integrated data quality monitoring and reporting through Elementary.