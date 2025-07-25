import pandas as pd

# Correct column order based on your HTML form
columns = ['Name', 'Email', 'Course', 'Year', 'Rating', 'Feedback', 'Suggestions', 'Timestamp']

# Create empty Excel with correct headers
df = pd.DataFrame(columns=columns)
df.to_excel('feedback_data.xlsx', index=False)

print("✅ Excel file created with correct column order.")
