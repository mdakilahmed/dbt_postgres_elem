import pandas as pd
import psycopg2
import numpy as np

# Load CSV into DataFrame
csv_file = './loan_eligibility_data.csv'
df = pd.read_csv(csv_file)  # Load the CSV file into a pandas DataFrame

# Data Cleaning/Transformation: Handling potential NaN values and large numbers
# Fill missing Loan_Amount_Term values with 360 (as a default assumption)
df['Loan_Amount_Term'] = df['Loan_Amount_Term'].fillna(360)

# Fill missing LoanAmount values with 0, as 0 could represent no loan amount
df['LoanAmount'] = df['LoanAmount'].fillna(0)

# Convert ApplicantIncome and CoapplicantIncome to numeric values, handle any non-numeric issues (NaN)
df['ApplicantIncome'] = pd.to_numeric(df['ApplicantIncome'], errors='coerce').fillna(0).astype(float)

# Similarly, handle CoapplicantIncome to ensure numeric type
df['CoapplicantIncome'] = pd.to_numeric(df['CoapplicantIncome'], errors='coerce').fillna(0).astype(float)

# Ensure LoanAmount is numeric, and any non-numeric values are coerced to NaN and filled with 0
df['LoanAmount'] = pd.to_numeric(df['LoanAmount'], errors='coerce').fillna(0).astype(float)

# Fill missing Credit_History values with 1 (default assumption)
df['Credit_History'] = df['Credit_History'].fillna(1)

# Replace '3+' in the Dependents column with 3 and fill any missing values with 0, then convert to integer
df['Dependents'] = df['Dependents'].replace('3+', 3).fillna(0).astype(int)

# Add a new column 'CIBIL_Score' with random integer values between 350 and 900
# Randomly set about 10% of the scores to -1 to represent NULL in the database
np.random.seed(42)  # For reproducibility
cibil_scores = np.random.randint(350, 901, size=len(df))  # Random scores as integers

# Randomly set about 10% of the scores to -1 to represent irregularity
mask = np.random.rand(len(df)) < 0.1  # 10% chance
cibil_scores[mask] = -1  # Assign -1 for irregularity
df['CIBIL_Score'] = cibil_scores

# Connect to Postgres Database
try:
    conn = psycopg2.connect(
        host="localhost",  # Postgres host, replace with actual IP/hostname
        database="loan_db",  # Name of your Postgres database
        user="postgres",  # Username for the Postgres database
        password="akil"  # Password for the Postgres database
    )
    cur = conn.cursor()
    print("Connection to database established successfully.")
except Exception as e:
    print(f"Error connecting to the database: {e}")
    exit(1)  # Exit the script if the connection fails

# Define the schema and table where the data will be inserted
schema = 'raw'  # Name of the schema in Postgres
table_name = 'loanee_details'  # Name of the table

# SQL query to create the table in Postgres if it does not already exist
create_table_query = f'''
CREATE TABLE IF NOT EXISTS {schema}.{table_name} (
    Loan_ID VARCHAR(20),  -- Loan ID (varchar of length 20)
    Gender VARCHAR(10),   -- Gender (varchar of length 10)
    Married VARCHAR(5),   -- Married status (varchar of length 5)
    Dependents INTEGER,   -- Number of dependents (integer)
    Education VARCHAR(20),  -- Education status (varchar of length 20)
    Self_Employed VARCHAR(5),  -- Self-employed status (varchar of length 5)
    ApplicantIncome NUMERIC,  -- Applicant income (numeric type to handle larger values)
    CoapplicantIncome NUMERIC,  -- Coapplicant income (numeric type)
    LoanAmount NUMERIC,   -- Loan amount (numeric type to handle larger values)
    Loan_Amount_Term INTEGER,  -- Loan term in months (integer)
    Credit_History INTEGER,  -- Credit history (1 for yes, 0 for no)
    Property_Area VARCHAR(20),  -- Property area (Urban, Rural, Semiurban)
    Loan_Status VARCHAR(5),   -- Loan status (Y/N)
    CIBIL_Score INTEGER  -- New CIBIL Score column (integer type)
);
'''
# Execute the table creation query
cur.execute(create_table_query)

# Commit the transaction to the database (this applies the table creation)
conn.commit()
print(f"Table {schema}.{table_name} created or already exists.")

# Loop through each row of the DataFrame and insert data into the table
try:
    for _, row in df.iterrows():
        insert_query = f'''
        INSERT INTO {schema}.{table_name} (
            Loan_ID, Gender, Married, Dependents, Education, Self_Employed,
            ApplicantIncome, CoapplicantIncome, LoanAmount, Loan_Amount_Term,
            Credit_History, Property_Area, Loan_Status, CIBIL_Score
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        '''
        
        # Prepare row values and handle any values that are -1 by replacing with None for NULL
        values = tuple(None if v == -1 else v for v in row)
        
        # Execute the insert query with the current row's values
        cur.execute(insert_query, values)

    # Commit all the inserted data to the database
    conn.commit()
    print("Data loaded successfully into the database.")

except Exception as e:
    print(f"Error occurred while inserting data: {e}")
    conn.rollback()  # Rollback the transaction on error

# Close the cursor and the connection to the database
cur.close()
conn.close()
print("Database connection closed.")
