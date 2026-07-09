# Basic Python For Data Handling
#%%
# Basic Syntax of Python
print("Hello World!")
#%%
# Basic Data Type in Python
# int = integer
x = 10
print("x: ",x)
y = -5
print("y: ",y)

#%%
# float = Floating‑point number
pi = 3.14
print("pi: ", pi)
salary = 1250.50
print("salary: ",salary)

#%%
# str = String
user_name = "Alice"
print("User Name: ",user_name)
message = "Hello, World"
print("Message: ",message)

#%%
#bool = Boolean
is_active = True
print("Boolean Test: ",is_active)
is_senior = False
print("Status Test: ",is_senior)

#%%
# Collection Data Type
#List Data type
numbers = [10, 20, 30, 20]
numbers.append(40)
print(numbers)
#%%
# Tuple data type
coordinates = (10, 20, 30)
print(coordinates[0])

#%%
# Set data type
unique_numbers = {1, 2, 3, 3, 4}
print(unique_numbers)

#%%
# Dictionary data type
student = {
    "name": "Sok",
    "age": 20,
    "grade": "A"
}
print(student["name"])

#%%
# Basics Operations in Python 
# Arithmatic Operations In Python
a = 10
b = 3

print(a + b)   # Addition
print(a - b)   # Subtraction
print(a * b)   # Multiplication
print(a / b)   # Division
print(a % b)   # Modulus (remainder)
print(a ** b)  # Power
print(a // b)  # Floor division

#%%
# Comparison Operations in Python
a = 5
b = 10

print(a == b)   # Equal
print(a != b)   # Not equal
print(a > b)    # Greater than
print(a < b)    # Less than
print(a >= b)   # Greater or equal
print(a <= b)   # Less or equal

#%%
# Logical Operation in Python 
x = True
y = False

print(x and y)   
print(x or y)    
print(not x) 

#%%
# Membership Operations Examples
print("a" in "apple")     
print(2 not in [1, 3, 5])

#%%
# Identity Operations Examples
a = [1, 2]
b = a

print(a is b)      
print(a is not b)

#%%
# if Statement
age = 18
if age >= 18:
    print("You are an adult")
#%% 
#if-else Statement   
age = 16
if age >= 18:
    print("Adult")
else:
    print("Minor")
#%%
#if-elif-else Statement
score = 75
if score >= 90:
    print("Grade A")
elif score >= 70:
    print("Grade B")
else:
    print("Grade C")
#%%
#Nested if Statement
age = 20
has_id = True
if age >= 18:
    if has_id:
        print("Access")
#%%
# Function example
def add(a, b):
    return a + b

result = add(5, 3)
print(result)

#%%
# Merging (Join)
import pandas as pd
df1 = pd.DataFrame({"id": [1, 2], "name": ["A", "B"]})
df2 = pd.DataFrame({"id": [1, 2], "score": [80, 90]})
result = pd.merge(df1, df2, on="id")

#%%
#Concatenation
df1 = pd.DataFrame({"A": [1, 2]})
df2 = pd.DataFrame({"A": [3, 4]})

result = pd.concat([df1, df2])

#%%
# Data Aggregation

import pandas as pd

data = {
    "Category": ["A", "A", "B", "B", "C"],
    "Sales": [100, 150, 200, 250, 300]
}

df = pd.DataFrame(data)
total_sales = df.groupby("Category")["Sales"].sum()
print(total_sales)
#%%
# Data Transformation
import pandas as pd

data = {
    "Name": ["Sokha", "Dara", "Vanna"],
    "Age": ["20", "21", "19"],   # stored as text (string)
    "Score": [70, 85, 90]
}

df = pd.DataFrame(data)
print(df)
# Convert data type
df["Age"] = df["Age"].astype(int)
# Create New Column
df["Passed"] = df["Score"] >= 80
# Modify Values
df["Score"] = df["Score"] + 5

#%%
# Read Multiple data sources
# Set up working 
import os
import pandas as pd
os.chdir("D:\CADT\Automata")

# Read data from CSV file
df1 = pd.read_csv("bank_transaction_part_1.csv")
df2 = pd.read_csv("bank_transaction_part_2.csv")

# Read data from XLSX file
df3 = pd.read_excel("bank_transaction_part_3.xlsx", sheet_name="sheet1")

# Read data from XLSB file
df4 = pd.read_excel(
    "bank_transaction_part_4.xlsb",
    engine="pyxlsb"
)

# Dataset combination 
df = pd.concat([df1,df2,df3,df4], ignore_index=True)
del df1, df2, df3, df4

#%%
# Exploratory Data Analysis 
print(df.head(5))
print(df.describe())
print(df.info()) 
print("\nMISSING VALUES:")
print(df.isnull().sum())
print("\nDUPLICATES:", df.duplicated().sum())

#%%
# Process of Data treatment
import pandas as pd
import numpy as np

# Step1: Standardize Column Name
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
print(df.columns)

#%%

#Step2: Cleaning for text column
text_cols = ['transactiontype', 'profession', 'location', 'channel', 'loanpurpose']

for col in text_cols:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip().str.lower()

# Fix inconsistent labels
df['transactiontype'] = df['transactiontype'].replace({
    'withdraw': 'withdrawal',
    'withdrew': 'withdrawal'
})

df['channel'] = df['channel'].replace({
    'mobile_app': 'mobile',
    'app': 'mobile'
})

df['profession'] = df['profession'].replace({
    'salaried_employee': 'salaried'
})

#%% 
#  Step 3: Missing value treatment 
# Missing Value treatment / Invalid Value
df.replace(['unknown', 'error', 'nan', 'none'], np.nan, inplace=True)

# Drop rows with missing key columns
df.dropna(subset=['transactiontype', 'amount'], inplace=True)


#%%
#Step 4: Fixing Date format data 
#Fix Date format data
df['transactiondate'] = pd.to_datetime(df['transactiondate'], errors='coerce')

# Remove invalid dates
df = df[df['transactiondate'].notna()]

#%%
# Step 5: Fixing numeric column
# fix numeric column
numeric_cols = ['amount', 'currentbalance']

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Remove invalid numeric rows
df.dropna(subset=numeric_cols, inplace=True)

#%%
# Step 6: Handle with outlier
# Remove extreme values
df = df[(df['amount'] > 0) & (df['amount'] < 100000)]

# Optional: IQR method
Q1 = df['amount'].quantile(0.25)
Q3 = df['amount'].quantile(0.75)
IQR = Q3 - Q1

df = df[
    (df['amount'] >= Q1 - 1.5 * IQR) & 
    (df['amount'] <= Q3 + 1.5 * IQR)
]

print("Cleaned Shape:", df.shape)

#%%
#  Step 1: Visualization on Channel 
# Data visulization
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Channel Usage
if 'channel' in df.columns:
    plt.figure(figsize=(6,4))
    sns.countplot(data=df, x='channel')
    plt.title("Channel Distribution")
    plt.xticks(rotation=45)
    plt.show()


#%%
# Step 2: Visualization on Amount Distribution 
# Amount Distribution 
plt.figure(figsize=(6,4))
sns.histplot(df['amount'], bins=30, kde=True)
plt.title("Transaction Amount Distribution")
plt.show()

#%%
# Step 3: Visualization on Profession
if 'profession' in df.columns:
    plt.figure(figsize=(8,5))
    sns.boxplot(data=df, x='profession', y='amount')
    plt.xticks(rotation=45)
    plt.title("Amount by Profession")
    plt.show()

#%%
#  Step 4: data trend 
# Trends Over Time 
df['month'] = df['transactiondate'].dt.to_period('M')
monthly_trend = df.groupby('month')['amount'].sum()
monthly_trend.plot(figsize=(8,4), title="Monthly Transaction Trend")
plt.show()


#%%
# Step 5:Correlation Analysis
# Correlation Analysis
plt.figure(figsize=(5,4))
sns.heatmap(df[['amount', 'currentbalance']].corr(), annot=True, cmap='coolwarm')
plt.title("Correlation Matrix")
plt.show()

