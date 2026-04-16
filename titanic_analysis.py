# ============================================
# Titanic Survival Statistical Analysis Project
# ============================================

import  pandas as pd
import random
from functools import reduce

# --------------------------------------------
# 1. LOAD DATA WITH ERROR HANDLING
# --------------------------------------------
def load_data(file_path):
    try:
        df = pd.read_csv("titanic.csv")
        print("File loaded successfully!\n")
        return df
    except FileNotFoundError:
        print("Error::: File not found. Please check the file path.")
    except PermissionError:
        print("Error: Permission denied.")
    except Exception as e:
        print("Error:", e)

# --------------------------------------------
# 2. DISPLAY DATA
# --------------------------------------------
def display_data(df):
    print("\nFirst 10 rows:\n", df.head(10))
    print("\nLast 5 rows:\n", df.tail(5))
    print("\nDataFrame Info:\n")
    print(df.info())

    print("\nPassengers older than 60 or in First Class:")
    for i in range(len(df)):
        if (df.loc[i, 'Age'] > 60) or (df.loc[i, 'Pclass'] == 1):
            print(df.loc[i])

# --------------------------------------------
# 3. HANDLE MISSING VALUES
# --------------------------------------------
def fill_missing_values(df):
    print("\nMissing values:\n", df.isnull().sum())

    # Fill Age manually using median of Pclass
    for pclass in [1, 2, 3]:
        ages = []
        for i in range(len(df)):
            if df.loc[i, 'Pclass'] == pclass and pd.notnull(df.loc[i, 'Age']):
                ages.append(df.loc[i, 'Age'])

        ages.sort()
        median_age = ages[len(ages)//2] if ages else 0

        for i in range(len(df)):
            if df.loc[i, 'Pclass'] == pclass and pd.isnull(df.loc[i, 'Age']):
                df.loc[i, 'Age'] = median_age

    # Treat zero fare as missing
    for i in range(len(df)):
        if df.loc[i, 'Fare'] == 0:
            df.loc[i, 'Fare'] = df['Fare'].median()

    return df

# --------------------------------------------
# 4. CREATE NEW COLUMNS
# --------------------------------------------
def create_columns(df):
    df['FamilySize'] = df['SibSp'] + df['Parch'] + 1

    fare_per_person = []
    for i in range(len(df)):
        try:
            value = df.loc[i, 'Fare'] / df.loc[i, 'FamilySize']
        except ZeroDivisionError:
            value = 0
        fare_per_person.append(value)

    df['FarePerPerson'] = fare_per_person

    df['IsChild'] = df['Age'] < 12

    return df

# --------------------------------------------
# 5. WOMEN & CHILDREN ANALYSIS
# --------------------------------------------
def women_children_analysis(df):
    group1 = df[(df['Sex'] == 'female') | (df['Age'] < 12)]
    group2 = df[~((df['Sex'] == 'female') | (df['Age'] < 12))]

    print("\nWomen & Children Survival Rate:",
          group1['Survived'].mean())
    print("Others Survival Rate:",
          group2['Survived'].mean())

    # Manual check
    wc_survive = 0
    wc_total = 0

    for i in range(len(df)):
        if (df.loc[i, 'Sex'] == 'female') or (df.loc[i, 'Age'] < 12):
            wc_total += 1
            if df.loc[i, 'Survived'] == 1:
                wc_survive += 1

    print("Manual WC Survival Rate:", wc_survive / wc_total)

# --------------------------------------------
# 6. RANDOM SAMPLING
# --------------------------------------------
def random_sampling(df):
    survivors = df[df['Survived'] == 1].index.tolist()
    nonsurvivors = df[df['Survived'] == 0].index.tolist()

    sample_surv = random.sample(survivors, 50)
    sample_non = random.sample(nonsurvivors, 50)

    print("\nSample Survivors:")
    for i in sample_surv[:5]:
        print(df.loc[i])

    print("\nSample Non-Survivors:")
    for i in sample_non[:5]:
        print(df.loc[i])

    def avg(column, indices):
        return sum([df.loc[i, column] for i in indices]) / len(indices)

    print("\nAvg Age (Survivors):", avg('Age', sample_surv))
    print("Avg Age (Non-Survivors):", avg('Age', sample_non))

# --------------------------------------------
# 7. STATISTICS (MANUAL + PANDAS)
# --------------------------------------------
def recursive_sum(lst):
    if len(lst) == 0:
        return 0
    return lst[0] + recursive_sum(lst[1:])

def statistics(df):
    cols = ['Age', 'Fare', 'FamilySize']

    for col in cols:
        data = df[col].tolist()

        mean = recursive_sum(data) / len(data)
        data.sort()
        median = data[len(data)//2]
        mode = max(set(data), key=data.count)

        print(f"\n{col} Statistics:")
        print("Manual Mean:", mean)
        print("Manual Median:", median)
        print("Manual Mode:", mode)

        print("Pandas Mean:", df[col].mean())
        print("Pandas Median:", df[col].median())

    # Group stats
    group_dict = {}
    for i in range(len(df)):
        key = (df.loc[i, 'Sex'], df.loc[i, 'Pclass'])
        if key not in group_dict:
            group_dict[key] = []
        group_dict[key].append(df.loc[i, 'Fare'])

    print("\nGrouped Fare Statistics:")
    for key in group_dict:
        print(key, "Avg Fare:", sum(group_dict[key])/len(group_dict[key]))

# --------------------------------------------
# 8. FUNCTIONAL PROGRAMMING
# --------------------------------------------
def functional_programming(df):
    fares = df['Fare'].tolist()
    median_fare = df['Fare'].median()

    high_fares = list(filter(lambda x: x > median_fare, fares))
    doubled_fares = list(map(lambda x: x * 2, fares))
    total_fare = reduce(lambda x, y: x + y, fares)

    print("\nFunctional Programming:")
    print("High fares count:", len(high_fares))
    print("Total fare:", total_fare)

# --------------------------------------------
# 9. GENERATE REPORT
# --------------------------------------------
def generate_report(df):
    try:
        with open("titanic_analysis_report.txt", "w") as f:
            f.write("Titanic Analysis Report\n")
            f.write("========================\n")
            f.write(f"Total Passengers: {len(df)}\n")
            f.write(f"Survival Rate: {df['Survived'].mean()}\n")
            f.write(f"Average Age: {df['Age'].mean()}\n")
            f.write(f"Average Fare: {df['Fare'].mean()}\n")

        print("\nReport generated successfully!")
    except Exception as e:
        print("Error writing file:", e)

# --------------------------------------------
# MAIN FUNCTION
# --------------------------------------------
def main():
    file_path = "titanic.csv"

    df = load_data(file_path)
    if df is None:
        return

    display_data(df)
    df = fill_missing_values(df)
    df = create_columns(df)

    women_children_analysis(df)
    random_sampling(df)
    statistics(df)
    functional_programming(df)
    generate_report(df)

# Run the program
if __name__ == "__main__":
    main()