# -*- coding: utf-8 -*-
"""stock_reference.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/gist/priyathamtarak/616ad3a85a2f599b87cb6b557a0470a4/stock_reference.ipynb
"""

import pandas as pd
import numpy as np
import yfinance as yf
import warnings
from sklearn.exceptions import ConvergenceWarning

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=ConvergenceWarning)

symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN','TSLA']

data = yf.download(symbols,period='15y',interval='1d')

data

column = ['Open','High','Low']

"""# Visualizing Data and Relations btw data"""

import matplotlib.pyplot as plt
for col in column:
    plt.scatter(data[col],data['Close'],alpha=0.5)
    plt.title('Scatter plot of close')
    plt.xlabel('Open')
    plt.ylabel('Close')

    plt.show()

plt.figure(figsize=(15,5))
plt.plot(data['Close'],label=symbols)
plt.title('Historical Closing price', fontsize=15)
plt.xlabel('Year')
plt.ylabel('Value')
plt.legend()
plt.show()

"""# Data Cleaning"""

data = data.droplevel(level=1, axis=1)
data

data.drop('Volume',axis=1,inplace=True)
data.drop('Adj Close',axis=1,inplace=True)
data

new_close = []
new_high = []
new_low = []
new_open = []
tom_c = []
for symbol in symbols:
    # Append values to the list
    new_close.append(symbol+'_close')

for symbol in symbols:
    # Append values to the list
    new_high.append(symbol+'_high')

for symbol in symbols:
    # Append values to the list
    new_low.append(symbol+'_low')

for symbol in symbols:
    # Append values to the list
    new_open.append(symbol+'_open')
for symbol in symbols:
    # Append values to the list
    tom_c.append(symbol+'_Stock')
new_name=new_close+new_high+new_low+new_open
data.columns = new_name
data.columns

data.isnull().sum()

data = data.dropna()

data=data.reset_index()

data.isna().any()

data["AAPL_stock"] = data["AAPL_close"].shift(-1)
data["GOOGL_stock"] = data["GOOGL_close"].shift(-1)
data["MSFT_stock"] = data["MSFT_close"].shift(-1)
data["AMZN_stock"] = data["AMZN_close"].shift(-1)
data["TSLA_stock"] = data["TSLA_close"].shift(-1)

data

"""# Spliting Data and storing them into variables"""

X = data.iloc[:-1,6:21]
X

y= data.iloc[:-1,21:]
y

"""# Pipelining all the models to see best model to choose Using Bar Graph"""

import warnings
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import plotly.graph_objects as go
import plotly.io as pio


def regression_pipeline(X, y):
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    models = [
        LinearRegression(),
        Ridge(),
        Lasso(),
        RandomForestRegressor(),
        DecisionTreeRegressor(),
        KNeighborsRegressor()
    ]

    warnings.filterwarnings("ignore", category=FutureWarning)
    warnings.filterwarnings("ignore", category=ConvergenceWarning)

    model_names = []
    scores = []
    R2= []
    MSE=[]
    MAE=[]
    RMSE=[]

    for model in models:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        rmse = mean_squared_error(y_test, y_pred, squared=False)
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test,y_pred)
        accu = model.score(X_test,y_test)*100
        model_names.append(type(model).__name__)
        scores.append(accu * 100)
        R2.append(r2)
        MSE.append(mse)
        MAE.append(mae)
        RMSE.append(rmse)

        print('Model:', type(model).__name__)
        print('MSE:', mse)
        print('RMSE:', rmse)
        print('R-squared:', r2)
        print("MAE",mae)
        print("score:",accu)
        print('-----------------------------')
    fig = go.Figure(data=go.Bar(x=model_names, y=scores))
    fig.update_layout(title="Model Accuracy Comparison",
                  xaxis_title="Model",
                yaxis_title="Accuracy Score (%)")
    fr = go.Figure(data=go.Bar(x=model_names, y=R2))
    fig.update_layout(title="Model's R^2",
                  xaxis_title="Model",
                yaxis_title="R2")
    fr.show()
    fms = go.Figure(data=go.Bar(x=model_names, y=MSE))
    fig.update_layout(title="Model'S MSE,
                  xaxis_title="Model",
                yaxis_title="MSE")
    fma = go.Figure(data=go.Bar(x=model_names, y=MAE))
    fig.update_layout(title="Model's MAE",
                  xaxis_title="Model",
                yaxis_title="MAE")
    frm = go.Figure(data=go.Bar(x=model_names, y=RMSE))
    fig.update_layout(title="Model's RMSE",
                  xaxis_title="Model",
                yaxis_title="RMSE")
    fms.show()
    fma.show()
    frm.show()
regression_pipeline(X, y)

"""# The Lasso model is a favorable choice for predicting stock prices due to its key advantages:

Feature Selection: It automatically selects the most relevant features, reducing noise and improving interpretability.
Regularization: The Lasso model prevents overfitting by penalizing large coefficients, resulting in more robust predictions.
Interpretability: Its transparency aids in understanding the drivers of stock price movements.
Flexibility: It can handle various data structures and be extended as needed.
Balance: The Lasso model strikes a balance between bias and variance, capturing essential relationships without sacrificing generalization.

Even the accuracy is high
"""

les = Lasso()

X_train,X_test,y_train,y_test = train_test_split(X,y, test_size=0.2, random_state=0)

X.columns

les.fit(X_train,y_train)

pred = les.predict(X_test)
pred

les.score(X_test,y_test)*100

sc = go.Figure()
sc.add_trace(go.Scatter(x=y_test.index, y=y_test, mode='lines', name='Actual'))
sc.add_trace(go.Scatter(x=y_test.index, y=pred, mode='lines', name='Predicted'))
sc.update_layout(title="Actual vs. Predicted Values",
                          xaxis_title="Data Point",
                          yaxis_title="Value")

pr = pd.DataFrame(pred)
pr

pr.columns = ['AAPL_stock','GOOGL_stock','MSFT_stock','AMZN_stock','TSLA_stock']
pr

for symbol in symbols:
    plt.scatter(y_test[f'{symbol}_stock'], pr[f'{symbol}_stock'])
    plt.plot([min(y_test[f'{symbol}_stock']), max(y_test[f'{symbol}_stock'])], [min(y_test[f'{symbol}_stock']), max(y_test[f'{symbol}_stock'])], 'k--', lw=2)  # Diagonal line
    plt.xlabel('True Values')
    plt.ylabel('Predicted Values')
    plt.title('Scatter Plot of True vs. Predicted Values')
    plt.show()

"""# Predicting Tomorrows close price by using todays data"""

X_lat = data.iloc[-1,6:21]
X_lat_df = pd.DataFrame(X_lat)
X_lat_df = X_lat_df.transpose()
Tom_price = les.predict(X_lat_df)
print(data.iloc[-1,0])
print(f"Apples Tommorrows price: {Tom_price[0,0]}\nGoogles Tomorrows Price: {Tom_price[0,1]}\nMicrosofts Tomorrows Price: {Tom_price[0,2]}\nAmazons Tomorrows Price:{Tom_price[0,3]}\nTeslas Tomorrows price:{Tom_price[0,4]}\n")

"""# Model suggest best stock to invest in"""

model_scores = {}

for target_col in y.columns:
    # Extract the target variable
    a = data[target_col]


    # Get the model score (you can use any evaluation metric here)
    score = les.score(X, y)

    # Store the score in the dictionary
    model_scores[target_col] = score

# Recommend the stock with the highest score (model performance)
best_stock = max(model_scores, key=model_scores.get)

# Print the recommended stock
print("Recommended stock to invest: ", best_stock)

