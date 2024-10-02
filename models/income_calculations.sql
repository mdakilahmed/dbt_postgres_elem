-- models/income_calculations.sql

{{ config(materialized='view') }}  -- Create this model as a view

with income_data as (
    select 
        Loan_ID,
        ApplicantIncome,
        CoapplicantIncome,
        CIBIL_Score,
        Credit_History,
        LoanAmount,
        (ApplicantIncome + CoapplicantIncome) as Total_Income  -- Calculate Total Income
    from {{ ref('raw_data') }}  -- Reference to the raw_data model
),

eligibility as (
    select 
        Loan_ID,
        CIBIL_Score,
        Credit_History,
        LoanAmount,
        Total_Income,
        case 
            when CIBIL_Score >= 650 and Credit_History = 1 and Total_Income > LoanAmount * 0.5 then 'Eligible' 
            else 'Not Eligible' 
        end as Loan_Eligibility,
        case 
            when CIBIL_Score >= 650 and Credit_History = 1 and Total_Income > LoanAmount * 0.5 then 'Low Risk'
            when CIBIL_Score < 650 and Credit_History = 1 then 'Medium Risk'
            else 'High Risk'
        end as Risk_Category
    from income_data
)

select 
    Loan_ID,
    Loan_Eligibility,
    Risk_Category,
    CIBIL_Score,
    Credit_History,
    LoanAmount,
    Total_Income  -- Ensure Total_Income is selected
from eligibility
