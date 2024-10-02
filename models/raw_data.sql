-- models/raw_data.sql

with source_data as (
    select 
        Loan_ID,
        Gender,
        Married,
        Dependents,
        Education,
        Self_Employed,
        ApplicantIncome,
        CoapplicantIncome,
        LoanAmount,
        Loan_Amount_Term,
        Credit_History,
        Property_Area,
        Loan_Status,
        CIBIL_Score
    from {{ source('loan_data', 'loanee_details') }} -- reference to your raw table
)

select *
from source_data