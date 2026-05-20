import numpy as np 
import pandas as pd 
import random as rd 

Num_Students = 500
Num_Companies = 40  # Total number of companies visiting campus.
Grad_Year = 2026

Shortlist_Rate = 0.35        
Interview_Rate = 0.60        
Offer_Rate = 0.45

branch_factor = {
    "CSE": 0.10,
    "IT": 0.07,
    "ECE": 0.03,
    "Mechanical": -0.03,
    "Civil": -0.07
}

#now we create a dictionary where in we will write the acceptance probability of
#each tier of the company by student i.e tier a more students accept

Accept_Prob = {
    "Tier A" : 0.88,
    "Tier B" : 0.75,
    "Tier C" : 0.65
}

rd.seed(42)
np.random.seed(42)

#GENERATE STUDENTS 

#branches & their weights(how many% of students in each branch )
branches = ["CSE","IT","ECE","Mechanical","Civil"] 
branch_weights = [0.35, 0.20, 0.20, 0.15, 0.10]

#we create an empty list of students where in we will store the student records, each element will become a new row in the dataset
students = []

for i in range(1, Num_Students+1 ):
    branch = np.random.choice(branches , p = branch_weights) #we randomly assign branches from the list and then branch_Weight ensures realistic distribution 
    #so now we decide what type of performer that student is , we need 30 % high performers and 40 % mid and low 
    cgpa_group = np.random.choice(
        ["high", "mid", "low"],
        p =[0.2,0.4,0.4]
    )
#based on cgpa_group we assign the cgpa 
    if cgpa_group == "high":
        cgpa = round(np.random.uniform(8.5,9.8),2)
    elif cgpa_group == "mid":
        cgpa = round(np.random.uniform(7.0,8.5),2)
    else :
        cgpa = round(np.random.uniform(5.5,7.0),2)
    
    # Now create the student record as a list
    # f"STU{i:04d}" creates IDs like STU0001, STU0002
    # 04d ensures 4-digit zero padding (professional formatting)
    students.append([
        f"STU{i:04d}",
        branch,
        cgpa,
        Grad_Year
    ])

students_df = pd.DataFrame(
    students,
    columns = ["student_id","branch","cgpa","graduation_year"]
)

#GENERATE COMPANIES

industries = [
    "Technology",
    "Consulting",
    "Finance",
    "Analytics",
    "Core Engineering"
]

role_types = {
    "Technology": ["SDE", "Data Scientist", "DevOps"],
    "Consulting": ["Business Analyst", "Strategy Analyst"],
    "Finance": ["Financial Analyst", "Risk Analyst"],
    "Analytics": ["Data Analyst", "BI Analyst"],
    "Core Engineering": ["Mechanical Engineer", "Electrical Engineer"]
}

# Name components for realism
name_prefixes = [
    "Nova", "Vertex", "Quantum", "BluePeak", "Core", "Nexa",
    "Infini", "Alpha", "Zenith", "Orbit", "Stratos", "Fusion",
    "Apex", "Prime", "Data", "Cloud", "NextGen", "Micro",
    "Hyper", "Bright"
]

industry_suffix_map = {
    "Technology": ["Tech", "Systems", "Labs", "Technologies", "Software"],
    "Consulting": ["Consulting", "Advisors", "Strategy", "Partners"],
    "Finance": ["Capital", "Finance", "Holdings", "Investments"],
    "Analytics": ["Analytics", "Insights", "Data Labs", "Intelligence"],
    "Core Engineering": ["Engineering", "Industries", "Infra", "Dynamics"]
}

tiers = ["Tier A", "Tier B", "Tier C"]
tier_weights = [0.30, 0.40, 0.30]

companies = []

for i in range(1, Num_Companies + 1):

    company_id = f"COMP{i:03d}"

    # Select industry
    industry = rd.choice(industries)

    # Select role aligned to industry
    role_type = rd.choice(role_types[industry])

    # Generate realistic company name
    prefix = rd.choice(name_prefixes)
    suffix = rd.choice(industry_suffix_map[industry])
    company_name = f"{prefix} {suffix}"

    # Assign tier
    tier = np.random.choice(tiers, p=tier_weights)

    # Assign package based on tier
    if tier == "Tier A":
        package = round(np.random.uniform(18, 30), 2)
    elif tier == "Tier B":
        package = round(np.random.uniform(10, 18), 2)
    else:
        package = round(np.random.uniform(5, 10), 2)

    companies.append([
        company_id,
        company_name,
        industry,
        role_type,
        tier,
        package
    ])

companies_df = pd.DataFrame(
    companies,
    columns=[
        "company_id",
        "company_name",
        "industry",
        "role_type",
        "tier",
        "package_lpa"
    ]
)


#GENERATE APPLICATIONS

applications = []
#Start application ID counter
# This ensures every application gets a unique ID
application_id = 1

for _, student_row in students_df.iterrows():

    student_id = student_row["student_id"]
    student_cgpa = student_row["cgpa"] #each student will apply to multiple companies we loop through all of them

# we assume each student supposedly applies to 5-12 firms
    num_apps = rd.randint(3,7)
# we select 5- 12 companies randomly , rd.sample ensures that no duplicate company for each student 
    applied_companies = rd.sample(
        list(companies_df["company_id"]),
        num_apps
    )

# now we show the application stage funel 
    for comp in applied_companies:
        stage = "Applied" #every application starts off with applied stage

        # Slight CGPA influence (controlled)
        shortlist_chance = Shortlist_Rate

# Branch impact based on market trend
        shortlist_chance += branch_factor[student_row["branch"]]

# CGPA impact
        if student_cgpa >= 8.5:
            shortlist_chance += 0.05
        elif student_cgpa < 6.5:
            shortlist_chance -= 0.05

# Keep probability valid
        shortlist_chance = max(0, min(1, shortlist_chance))
        
# random.random() gives a number between 0 and 1
# If it's below SHORTLIST_RATE (e.g., 0.55),
# we randomly select company from applied company if probability is less then shortlisted rate that means student/application is shortlisted
        if rd.random() < shortlist_chance:
            stage = "Shortlisted"

            if rd.random() < Interview_Rate:
                stage = "Interviewed" # only shortlisted students are eligible to be interviewed that is why nested if

                if rd.random() < Offer_Rate:
                    stage = "Offered"

 # Store the application record
# Format application ID like APP00001, APP00002 etc.

        applications.append([
            f"APP{application_id:05d}",
            student_id,
            comp,
            stage
        ])
        application_id += 1

applications_df = pd.DataFrame(
    applications , 
    columns = ["application_id","student_id","company_id", "stage"]
)


#GENERATE OFFERS 

# Each row = one official job offer issued to a student
offers = []
offer_id = 1

#Firstly we filter out only those applications that have reached "Offer" Stage
offered_apps = applications_df[
    applications_df["stage"] == "Offered"
]

# Loop through each offered application
# iterrows() lets us access each row as a dictionary-like object
for _, row in offered_apps.iterrows():
    # Find the company details for this offer
    # We match company_id from applications with companies table
    company_info = companies_df[
        companies_df["company_id"] == row["company_id"]
    ].iloc[0]

    # Extract company tier (Tier A / B / C)
    # This determines acceptance behavior
    tier = company_info["tier"]

    # Lookup acceptance probability based on company tier
    # Example:
    # Tier A = 88% acceptance
    # Tier B = 75%
    # Tier C = 65%
    acceptance_probability = Accept_Prob[tier]    

    # Now simulate student decision
    # random.random() generates number between 0 and 1
    # If less than acceptance_probability → Accepted
    # Otherwise → Declined
    outcome = (
        "Accepted"
        if rd.random() < acceptance_probability
        else "Declined"
    )

    # Append the offer record
    # f"OFF{offer_id:05d}" ensures formatted ID like OFF00001
    offers.append([
        f"OFF{offer_id:05d}",
        row["student_id"],
        row["company_id"],
        company_info["package_lpa"],
        outcome
    ])

    # Increment offer ID for next record
    offer_id += 1


# Convert list into structured DataFrame
# This becomes your offers_raw dataset
offers_df = pd.DataFrame(
    offers,
    columns=[
        "offer_id",
        "student_id",
        "company_id",
        "package_lpa",
        "offer_outcome"
    ]
)

# -------------------------------------------------------
# FIX MULTIPLE ACCEPTANCES (REAL PLACEMENT LOGIC)
# -------------------------------------------------------

# If a student has accepted multiple offers,
# keep only the highest package and decline others

accepted_offers = offers_df[
    offers_df["offer_outcome"] == "Accepted"
]

# Sort so highest package appears first per student
accepted_offers = accepted_offers.sort_values(
    ["student_id", "package_lpa"],
    ascending=[True, False]
)

# Keep only first (highest package) per student
accepted_offers = accepted_offers.drop_duplicates(
    subset=["student_id"],
    keep="first"
)

# Mark all offers as Declined initially
offers_df["offer_outcome"] = "Declined"

# Update only the final accepted ones
offers_df.loc[
    offers_df["offer_id"].isin(accepted_offers["offer_id"]),
    "offer_outcome"
] = "Accepted"

# EXPORT CSV FILES

students_df.to_csv("students_cleaned_scaled.csv", index=False)
companies_df.to_csv("companies_cleaned_scaled.csv", index=False)
applications_df.to_csv("applications_cleaned_scaled.csv", index=False)
offers_df.to_csv("offers_raw_scaled.csv", index=False)

print("Dataset Generated Successfully!")
print("Students:", len(students_df))
print("Applications:", len(applications_df))
print("Offers:", len(offers_df))
print("Total Offers:", len(offers_df))
print("Total Accepted Offers:", len(offers_df[offers_df["offer_outcome"] == "Accepted"]))
print("Distinct Placed Students:",
      offers_df[offers_df["offer_outcome"] == "Accepted"]["student_id"].nunique())