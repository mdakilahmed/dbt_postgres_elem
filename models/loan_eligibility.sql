-- models/final_transformation.sql

with final_data as (
    select 
        ic.Loan_ID,
        ic.Risk_Category,
        ic.Loan_Eligibility,
        ic.Application_Status,
        r.Gender,
        r.Married,
        r.Dependents,
        r.Education,
        r.Self_Employed,
        r.LoanAmount,
        r.Loan_Amount_Term,
        r.Credit_History,
        r.Property_Area,
        r.Loan_Status
    from {{ ref('income_classifications') }} ic
    join {{ ref('raw_data') }} r on ic.Loan_ID = r.Loan_ID
)

select 
    Loan_ID,
    Risk_Category,
    Loan_Eligibility,
    Application_Status,
    Gender,
    Married,
    Dependents,
    Education,
    Self_Employed,
    LoanAmount,
    Loan_Amount_Term,
    Credit_History,
    Property_Area,
    Loan_Status
from final_data
