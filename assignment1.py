import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import skew, zscore
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN

#Making the plots prettier
plt.rcParams.update(**{'figure.dpi':150})
plt.style.use('ggplot')

# Read the CSV file
df = pd.read_csv('/app/data.csv')

##Question 1

# Remove columns with many missing values
threshold = len(df) * 0.6  # set a threshold for the percentage of missing values allowed
df = df.dropna(thresh=threshold, axis=1)

# Impute the missing values in the remaining columns
for col in df.columns:
    if df[col].isnull().sum() > 0:  # check if the column has missing values
        if df[col].dtype == 'object':  # check if the column contains categorical data
            df[col] = df[col].fillna(df[col].mode()[0])  # impute the missing values with the column mode
        else:
            df[col] = df[col].fillna(df[col].mean())  # impute the missing values with the column mean

#Making the days since _____ columns into positive values
df['DAYS_EMPLOYED'] = df['DAYS_EMPLOYED'].multiply(-1)
df['DAYS_BIRTH'] = df['DAYS_BIRTH'].multiply(-1)

## Question 2

# Plot histograms for each numeric feature
num_cols = df.select_dtypes(include=np.number).columns
for col in num_cols:
    plt.figure()
    plt.hist(df[col].dropna(), bins=20)
    plt.title(col)
    plt.show()

# Normalize numeric columns using z-score normalization
df2 = df.copy()
norm_cols = []
for col in num_cols:
    if abs(df2[col].skew()) > 1:  # check if the feature is highly skewed
        df2[col] = zscore(df2[col])
        norm_cols.append(col)

# Create a dataframe with normalized features
df_norm = df2[norm_cols].copy()

#save to csv
df_norm.to_csv('/tmp/transformed_data.csv', index=False)

#Make boxplots of normalized columns and remove outliers through clustering
for col in norm_cols:
    plt.figure(figsize=(12, 8))  # set the figure size
    sns.boxplot(x=df_norm[col])
    plt.title(col)
    plt.ylim(np.percentile(df_norm[col], 0.0001), np.percentile(df_norm[col], 99.9999))  # set the y-axis limits
    plt.show()

    # Identify and remove outliers using clustering using DBSCAN
    clustering = DBSCAN(eps=0.5, min_samples=10).fit(df_norm[[col]])
    outliers = df_norm[clustering.labels_ == -1]
    #print('Outliers:', outliers)

    df_norm = df_norm[clustering.labels_ != -1]

# Create a new dataframe with the original values for TARGET
df_norm_2 = df_norm.copy()
df_norm_2['TARGET'] = df_norm_2['TARGET'].apply(lambda x: 1 if x >= 0.5 else 0)

# Separate the data by target value
df_0 = df_norm_2[df_norm_2['TARGET'] == 0]
df_1 = df_norm_2[df_norm_2['TARGET'] == 1]

# Create a figure with two subplots
fig, axes = plt.subplots(nrows=1, ncols=len(df_norm_2.columns)-1, figsize=(20, 6))

# Generate boxplots for each column
for i, col in enumerate(df_norm_2.columns[:-1]):
    sns.boxplot(x='TARGET', y=col, data=df_norm_2, ax=axes[i])
    axes[i].set_title(col)

plt.show()

# Create a dataframe with normalized features
df_norm_3 = df[norm_cols].copy()

# Append 'NAME_EDUCATION_TYPE' column to df_norm
df_norm_3['NAME_EDUCATION_TYPE'] = df['NAME_EDUCATION_TYPE']

# Define the order of education levels
edu_order = ['Lower secondary', 'Secondary / secondary special', 'Incomplete higher', 'Higher education']

# Generate boxplots for each education level
sns.boxplot(x='NAME_EDUCATION_TYPE', y='AMT_INCOME_TOTAL', data=df_norm_3, order=edu_order)
plt.xticks(rotation=45, ha='right')
plt.title('Distribution of AMT_INCOME_TOTAL by Education Level')
plt.show()

# Plot the number of applicants by housing type
sns.countplot(data=df, x='NAME_HOUSING_TYPE')
plt.title('Counts by Housing Type')
plt.xlabel('Housing Type')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right', wrap=True)
plt.show()

# Creating the bar plot for housing types and family status
sns.countplot(data=df, x='NAME_HOUSING_TYPE', hue='NAME_FAMILY_STATUS')
plt.title('Counts by Housing Type and Family Status')
plt.xlabel('Housing Type')
plt.ylabel('Count')
plt.legend(title='Family Status')
plt.xticks(rotation=45, ha='right', wrap=True)
plt.show()

# Making a new copy just in case
df3 = df.copy()

# Making the new column for 'AGE
df3['AGE'] = df3['DAYS_BIRTH'] / 365

# Making a new column for 'AGE GROUP'
df3.loc[(df3['AGE'] >= 19) & (df3['AGE'] <= 25), 'AGE_GROUP'] = 'Very_Young'
df3.loc[(df3['AGE'] > 25) & (df3['AGE'] <= 35), 'AGE_GROUP'] = 'Young'
df3.loc[(df3['AGE'] > 35) & (df3['AGE'] <= 60), 'AGE_GROUP'] = 'Middle_Age'
df3.loc[df3['AGE'] > 60, 'AGE_GROUP'] = 'Senior_Citizen'
df3.head()

# Boxplots for different Totals of Anual Income by Age Group
plt.figure(figsize=(8,6))
sns.barplot(x='AGE_GROUP', y='TARGET', data=df3, estimator=lambda x: sum(x==1)/len(x))
plt.title('Proportion of applicants with "TARGET"=1 within each age group')
plt.xlabel('Age Group')
plt.ylabel('Proportion with "TARGET"=1')
plt.show()

# Boxplots for different levels of education and the feature 'AMT_INCOME_TOTAL'
plt.figure(figsize=(8,6))
sns.barplot(x='AGE_GROUP', y='TARGET', hue='CODE_GENDER', data=df3, estimator=lambda x: sum(x==1)/len(x))
plt.title('Proportion of applicants with "TARGET"=1 within each age group, by gender')
plt.xlabel('Age Group')
plt.ylabel('Proportion with "TARGET"=1')
plt.show()
