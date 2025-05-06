# ---------------------- Libraries ----------------------
import pandas as pd
import requests
from bs4 import BeautifulSoup
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from io import StringIO
# ---------------------- Libraries ----------------------


def get_qb_projections_with_predictions(threshold=18.0):
    #   URL to scrape the projections data from FantasyPros
    url = 'https://www.fantasypros.com/nfl/projections/qb.php?week=draft&scoring=PPR&week=draft'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    #   Find the table with the data
    table = soup.find('table', {'id': 'data'})
    # Parses the table of stats into a DataFrame.
    df = pd.read_html(StringIO(str(table)))[0].dropna()

    #   Flatten the MultiIndex columns
    df.columns = ['_'.join(col).strip() for col in df.columns.values]

    print(df.columns)

    #   Converts relevant columns to numeric (e.g., passing yards, TDs).
    for col in ['PASSING_ATT', 'PASSING_CMP', 'PASSING_YDS', 'PASSING_TDS', 'PASSING_INTS',
                'RUSHING_ATT', 'RUSHING_YDS', 'RUSHING_TDS', 'MISC_FL', 'MISC_FPTS']:
        df[col] = df[col].astype(str).str.replace(',', '').astype(float)

    #   Select relevant features for regression model
    features = ['PASSING_YDS', 'PASSING_TDS', 'PASSING_INTS', 'RUSHING_ATT', 'RUSHING_YDS', 'RUSHING_TDS']
    X = df[features]
    y_reg = df['MISC_FPTS']

    # Fit the regression model to predict Fantasy Points (FPTS)
    reg_model = RandomForestRegressor()
    reg_model.fit(X, y_reg)
    df['Predicted FPTS'] = reg_model.predict(X)

    # Classification model predicts if a QB is a high performer based on a fantasy point threshold (default: 18 points).
    y_class = (y_reg >= threshold).astype(int)
    clf_model = RandomForestClassifier()
    clf_model.fit(X, y_class)
    df['High Performer'] = clf_model.predict(X)
    df['High Performer'] = df['High Performer'].replace({1: 'High', 0: 'Low'})

    #   Add player name, team, and position columns
    df['name'] = df['Unnamed: 0_level_0_Player']

    # Returns a simplified DataFrame - includes: name, Predicted FPTS, and High Performer.
    return df[['name', 'Predicted FPTS', 'High Performer']]