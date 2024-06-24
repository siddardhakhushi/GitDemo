import pandas as pd

def extract_construction_keywords(text):
    keywords = ["remodeling", "construction", "builder", "contractor", "concrete", "siding", "windows", "gutters",
                "plumbing", "flooring", "carpentry", "carpet", "roofing", "painting", "drywall", "electrician",
                "HVAC", "insulation", "landscaping", "foundation", "home", "service", "steel", "residential", "real",
                "estate", "filtration", "metal", "boilers", "sewer", "engineering", "survey", "lawn", "hvac", "cleaning",
                "wood"]
    extracted_keywords = [keyword for keyword in keywords if keyword in text.lower()]
    return ', '.join(extracted_keywords)

# Read Excel file
df = pd.read_excel('descriptions.xlsx')

# Apply function to 'text' column
df['construction_keywords'] = df['description'].apply(extract_construction_keywords)

# Save the modified DataFrame to a new Excel file
df.to_excel('output.xlsx', index=False)

