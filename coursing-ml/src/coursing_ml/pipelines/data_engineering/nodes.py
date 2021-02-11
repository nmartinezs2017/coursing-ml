import pandas as pd


def extract_time_range(x):
    x = x.rstrip()
    if len(str(x).split(' ')) > 1:
        time_range = str(x).split(' ')[-1]
        return time_range
    else:
        return 'Weeks'


def extract_first_element(x):
    x = str(x)
    if len(str(x).split(',')) > 1:
        return str(x).split(',')[0]
    else:
        return 0


def extract_number_hours(x):
    number = float(str(x).split(' ')[0])
    time_range = str(x).split(' ')[-1].lower()
    if (time_range == 'months') or (time_range == 'month'):
        return 4 * number * 10  # 4 semanas/mes * N meses * 10 horas/semana
    elif time_range == 'weeks' or time_range == 'week':
        return number * 10  # N semanas * 10 horas/semana
    elif time_range == 'day' or time_range == 'days':
        return number * 5  # N semanas * 5 horas/dia
    else:
        return number


def map_boolean_to_int(df, field) -> pd.DataFrame:
    d = {'True': 1, 'False': 0}
    df[field] = df[field].map(d)
    return df


def preprocess_udacity(df: pd.DataFrame) -> pd.DataFrame:
    df['n_reviews'] = df['n_reviews'].apply(extract_first_element)
    df['free'] = df['free'].str.strip('[]')
    df['rating'] = df['rating'].apply(extract_first_element)
    df['rating'] = df['rating'].str.strip(' width:')
    df['rating'] = df['rating'].str.strip('%')
    df['rating'] = pd.to_numeric(df['rating'])
    df['duration'] = df['duration'].apply(lambda _: str(_))
    df['n_reviews'].fillna(0, inplace=True)
    df['time_range'] = df['duration'].apply(extract_time_range)
    df['time_range'] = df['time_range'].str.lower()
    df['duration'] = df['duration'].apply(extract_number_hours)
    df = map_boolean_to_int(df, 'free')
    return df


def feature_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    # rellenar manualmente
    mask = df["title"] == 'Shell Workshop'
    df.loc[mask, "difficulty"] = 'beginner'
    mask = df["difficulty"].isnull() # porque la mayoría de cursos con este parámetro a null son de nivel intermedio
    df.loc[mask, "difficulty"] = 'intermediate'
    mask = df["duration"].isnull()
    df.loc[mask, "duration"] = 10
    # arbitrary value imputation
    df["collaboration"].fillna("", inplace=True)
    df["description"].fillna("", inplace=True)
    df["skills"].fillna("", inplace=True)
    df["title"].fillna("", inplace=True)
    return df

def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    # duration - normalization
    from sklearn.preprocessing import StandardScaler
    ss = StandardScaler().fit(df[['duration']])
    df['duration'] = ss.transform(df[['duration']])
    # rating - minmax scaling
    from sklearn.preprocessing import MinMaxScaler
    mms = MinMaxScaler().fit(df[['rating']])
    df['rating'] = mms.transform(df[['rating']])
    # difficulty and school - feature encoding
    from sklearn import preprocessing
    enc = preprocessing.OrdinalEncoder()
    X = df[['difficulty']]
    enc.fit(X)
    df['difficulty'] = enc.transform(X)
    # use pd.concat to join the new columns with your original dataframe
    df = pd.concat([df, pd.get_dummies(df['school'], prefix='difficulty')], axis=1)
    # now drop the original 'country' column (you don't need it anymore)
    df.drop(['school'], axis=1, inplace=True)
    # n_reviews - feature transformation
    import numpy as np
    from sklearn.preprocessing import QuantileTransformer
    X = df[['n_reviews']]
    qt = preprocessing.QuantileTransformer(random_state=0)
    qt.fit(X)
    df['n_reviews'] = qt.transform(X)
    return df

def feature_selection(df: pd.DataFrame) -> pd.DataFrame:
    # borrar columnas innecesarias
    del df['collaboration']
    del df['id_course']
    del df['description']
    del df['url']
    del df['title']
    del df['skills']
    del df['time_range']

    mask = df["rating"].isnull()
    df.loc[mask, "rating"] = 0
    return df

    return df