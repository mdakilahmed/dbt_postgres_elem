-- models/income_classification.sql

{{ config(materialized='view') }}  -- Create this model as a view

with classified_data as (
    select 
        Loan_ID,
        Total_Income,
        CIBIL_Score,
        Risk_Category,
        Loan_Eligibility,
        case
            when Loan_Eligibility = 'Eligible' then 'Approved'
            when Loan_Eligibility = 'Not Eligible' then 'Rejected'
            else 'Under Review'
        end as Application_Status
    from {{ ref('income_calculations') }}
)

select 
    Loan_ID,
    Total_Income,
    CIBIL_Score,
    Risk_Category,
    Loan_Eligibility,
    Application_Status
from classified_data
