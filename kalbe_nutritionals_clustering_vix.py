# -*- coding: utf-8 -*-
"""Kalbe_Nutritionals_Clustering_VIX.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Cq36JT-Z3SFaYbIAnA5wafoYkb0Qgwqj

##**Machine Learning for Kalbe Nutritionals**

Objective : Customer Segmentation with K-Means Clustering

###**Attribute information:**

1. Customer

- CustomerID : No Unik Customer
- Age : Usia Customer
- Gender : 0 Wanita, 1 Pria
- Marital Status : Married, Single (Blm menikah/Pernah menikah)
- Income : Pendapatan per bulan dalam jutaan rupiah


2. Store

- StoreID : Kode Unik Store
- StoreName : Nama Toko
- GroupStore : Nama group
- Type : Modern Trade, General Trade
- Latitude : Kode Latitude
- Longitude : Kode Longitude


3. Product

- ProductID : Kode Unik Product
- Product Name : Nama Product
- Price : Harga dlm rupiah


4. Transaction

- TransactionID : Kode Unik Transaksi
- Date : Tanggal transaksi
- Qty : Jumlah item yang dibeli
- Total Amount : Price x Qty

### Import Library
"""

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.metrics import silhouette_score

import warnings
warnings.filterwarnings('ignore')

"""### Load Dataset"""

df_cus = pd.read_csv('Customer.csv')
df_str = pd.read_csv('Store.csv')
df_prod = pd.read_csv('Product.csv')
df_trans = pd.read_csv('Transaction.csv')

"""### Data Preprocessing

#### Customer
"""

df_cus = df_cus.drop_duplicates()

#Looking at the first 5 rows of the dataset
df_cus.head()

#Looking at the last 5 rows of the dataset
df_cus.tail()

#How many rows and columns in the dataset?
df_cus.shape

#Labeling categorical data
status = {
    "Single": 0,
    "Married": 1
}

df_cus['MaritalStatus'] = df_cus['MaritalStatus'].map(status)

df_cus.head()

#General information of the dataset
df_cus.info()

"""##### Handling Missing Values"""

#Checking for missing values
df_cus.isnull().sum()

#filling missing data
from sklearn.impute import SimpleImputer
imputer = SimpleImputer(strategy='mean', missing_values=np.nan)
imputer = imputer.fit(df_cus[['MaritalStatus']])
df_cus['MaritalStatus'] = imputer.transform(df_cus[['MaritalStatus']])

#Checking if the data is still missing
df_cus.isnull().sum()

"""#### Store"""

df_str = df_str.drop_duplicates()

#Looking at the first 5 rows of the dataset
df_str.head()

#Looking at the last 5 rows of the dataset
df_str.tail()

#How many rows and columns in the dataset?
df_str.shape

#General information of the dataset
df_str.info()

"""##### Handling Missing Values"""

#Checking for missing values
df_str.isnull().sum()

"""#### Product"""

df_prod = df_prod.drop_duplicates()

#Looking at the first 5 rows of the dataset
df_prod.head()

#Looking at the last 5 rows of the dataset
df_str.tail()

#How many rows and columns in the dataset?
df_prod.shape

#General information of the dataset
df_prod.info()

"""##### Handling Missing Values"""

#Checking for missing values
df_prod.isnull().sum()

"""#### Transaction"""

df_trans = df_trans.drop_duplicates()

#Looking at the first 5 rows of the dataset
df_trans.head()

#Looking at the last 5 rows of the dataset
df_trans.tail()

#How many rows and columns in the dataset?
df_trans.shape

#General information of the dataset
df_trans.info()

"""##### Handling Missing Values"""

#Checking for missing values
df_trans.isnull().sum()

"""### Merging Dataset"""

df1 = df_trans.merge(df_cus, on='CustomerID', how='inner')
df2 = df1.merge(df_str, on='StoreID', how='inner')
df = df2.merge(df_prod, on='ProductID', how='inner')

df.head()

df_clus = df.groupby('CustomerID').agg({'TransactionID': 'count', 'Qty': 'sum', 'TotalAmount': 'sum'}).reset_index()

# Display the first 10 rows of the new_data DataFrame
df_clus.head()

#Describing the dataset
df_clus.describe()

"""## Exploratory Data Analysis"""

#Describing the dataset
df.describe()

data_plot  = df['Gender'].value_counts().to_list()
label_plot = df['Gender'].value_counts().index.to_list()

title = 'Gender Distribution'

plot       = sns.barplot(data = df, x = label_plot, y = data_plot, palette = 'CMRmap')
plot_title = plt.title(title)

plt.show()

column_name_list_num = ['Age', 'Income']

num_cols = len(column_name_list_num)
num_rows = (num_cols + 2) // 3
fig, axs = plt.subplots(nrows=num_rows, ncols=3, figsize=(15,5*num_rows))
axs = axs.flatten()

#Barplot for each variables
for i, var in enumerate (column_name_list_num):
  sns.histplot(x=var, data=df, palette = 'CMRmap', ax=axs[i])
  axs[i].set_title(var + " " + "Distribution")
  axs[i].tick_params(axis='x', rotation=90)

#Removes extra empty subplots
if num_cols < len(axs):
  for i in range(num_cols, len(axs)):
    fig.delaxes(axs[i])

fig.tight_layout()
plt.show()

"""## Modelling"""

#Used feature
feature = ['TransactionID', 'Qty', 'TotalAmount']
x = df_clus[feature].values

#Scaling the data
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
x_sc = pd.DataFrame(sc.fit_transform(x))

#Elbow method
wcss = []
for n in range(1,11):
  kmeans = KMeans(n_clusters = n, init = 'k-means++')
  kmeans.fit(x_sc)
  wcss.append(kmeans.inertia_)

print(wcss)

plt.plot(range(1,11), wcss)
plt.xticks(range(1,11))
plt.title('Elbow Method for Number of Clusters')
plt.xlabel('Number of Clusters')
plt.ylabel('WCSS')
plt.show()

#Creating K-Means Clustering model
kmeans = KMeans(n_clusters = 4, init = 'k-means++')
kmeans.fit(x_sc)

Cluster = kmeans.fit_predict(x_sc)

df_clus['Cluster'] = kmeans.labels_
df_clus.head()

title = 'Customer Segmentation'
plot = sns.scatterplot(data=df_clus, x='Qty', y='TotalAmount', hue='Cluster', palette='viridis')
plot_title = plt.title(title)

data_plot  = df_clus['Cluster'].value_counts().to_list()
label_plot = df_clus['Cluster'].value_counts().index.to_list()

title = 'Customer Clusters'

plot       = sns.barplot(x = label_plot, y = data_plot, palette = 'CMRmap')
plot_title = plt.title(title)

plt.show()

df_clus['Cluster'].value_counts()

display(df_clus.groupby('Cluster').agg(['mean']))

column_name_list_num = ['TransactionID', 'Qty']

num_cols = len(column_name_list_num)
num_rows = (num_cols + 2) // 3
fig, axs = plt.subplots(nrows=num_rows, ncols=3, figsize=(15,5*num_rows))
axs = axs.flatten()

#Barplot for each variables
for i, var in enumerate (column_name_list_num):
  sns.histplot(x=var, hue = 'Cluster', data=df_clus, palette = 'CMRmap', ax=axs[i])
  axs[i].set_title(var + " " + "by Cluster")
  axs[i].tick_params(axis='x', rotation=90)

#Removes extra empty subplots
if num_cols < len(axs):
  for i in range(num_cols, len(axs)):
    fig.delaxes(axs[i])

fig.tight_layout()
plt.show()