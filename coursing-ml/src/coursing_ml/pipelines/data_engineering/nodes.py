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
