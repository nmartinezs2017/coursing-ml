import pandas as pd
import re
import numpy as np

def extract_time_range(x):
    x = x.rstrip()
    if len(str(x).split(' ')) > 1:
        time_range = str(x).split(' ')[-1]
        return time_range
    else:
        return 'Weeks'


def convert_ratings_coursera(x):
    if len(str(x).split(' ')) > 1:
        return float(str(x).split(' ')[0].replace(",", ""))
    else:
        return 1


def convert_enrolled_coursera(x):
    if 'complete' in str(x):
        return 0
    else:
        return float(str(x).replace(",", ""))


def convert_views_coursera(x):
    if len(str(x).split(',')) > 2:
        new_number = str(x).split(',')[0] + str(x).split(',')[1]
        return float(new_number)
    else:
        return float(str(x).replace(",", ""))


def process_difficulty_coursera(x):
    x = str(x)
    x = x.split(' ')[0]
    if x == 'Professional':
        x = 'Advanced'
    if x not in ['Beginner', 'Intermediate', 'Advanced']:
        x = 'Beginner'
    return x


def process_text(x):
    x = str(x)
    x = x.replace("\n", " ")
    return re.sub(",([\w]+)", r"\1", x)


def extract_n_element(x, n):
    x = str(x)
    if len(str(x).split(',')) > 1:
        return str(x).split(',')[n]
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


def extract_months_hours_coursera(x):
    try:
        if len(str(x).split(' ')) > 3:
            if str(x).split(' ')[1] in ['hour', 'hours', 'hr']:
                return float(str(x).split(' ')[0])
            return float(str(x).split(' ')[1])
        elif len(str(x).split(' ')) == 2:
            return float(str(x).split(' ')[0])
        else:
            return 0
    except ValueError:
        return None


def extract_hours_per_week_coursera(x):
    if len(str(x).split(' ')) > 3:
        return float(str(x).split(' ')[3])
    elif len(str(x).split(' ')) == 2:
        return float(str(x).split(' ')[0])
    else:
        return 0


def extract_duration_hours(x):
    if len(str(x).split(' ')) > 3:
        return float(str(x).split(' ')[3])
    elif len(str(x).split(' ')) == 2:
        return float(str(x).split(' ')[0])
    else:
        return 0


def map_boolean_to_int(df, field) -> pd.DataFrame:
    d = {'True': 1, 'False': 0}
    df[field] = df[field].map(d)
    return df


def preprocess_udacity(df: pd.DataFrame) -> pd.DataFrame:
    df['n_reviews'] = df['n_reviews'].apply(extract_n_element, n=0)
    df['free'] = df['free'].str.strip('[]')
    df['rating'] = df['rating'].apply(extract_n_element, n=0)
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


def preprocess_coursera(df: pd.DataFrame) -> pd.DataFrame:
    del df['characteristics']
    df['subcategory'] = df['category'].apply(extract_n_element, n=2)
    df['description'] = df['description'].apply(process_text)
    df['difficulty'] = df['difficulty'].apply(process_difficulty_coursera)
    df['hours_months'] = df['duration'].apply(extract_months_hours_coursera)
    df['hours_week'] = df['duration_week'].apply(extract_hours_per_week_coursera)
    df['enrolled'] = df['enrolled'].apply(convert_enrolled_coursera)
    df['n_ratings'] = df['n_ratings'].apply(convert_ratings_coursera)
    df['views'] = df['views'].apply(convert_views_coursera)
    values = df["hours_months"] * df["hours_week"] * 4
    df['aux'] = values
    df['total_hours'] = values.where(df.aux != 0, other=df['hours_months'])
    del df['aux']
    df.to_csv('data/03_primary/preprocessed_coursera.csv')


def feature_cleaning_udacity(df: pd.DataFrame) -> pd.DataFrame:
    # rellenar manualmente
    mask = df["title"] == 'Shell Workshop'
    df.loc[mask, "difficulty"] = 'beginner'
    mask = df["difficulty"].isnull()  # porque la mayoría de cursos con este parámetro a null son de nivel intermedio
    df.loc[mask, "difficulty"] = 'intermediate'
    mask = df["duration"].isnull()
    df.loc[mask, "duration"] = 10
    # arbitrary value imputation
    df["collaboration"].fillna("", inplace=True)
    df["description"].fillna("", inplace=True)
    df["skills"].fillna("", inplace=True)
    df["title"].fillna("", inplace=True)
    return df

def feature_cleaning_coursera(df: pd.DataFrame) -> pd.DataFrame:
    del df['Unnamed: 0']
    del df['hours_months']
    del df['hours_week']
    del df['duration']
    del df['url']
    del df['id_course']
    del df['duration_week']
    del df['skills']
    del df['views']
    del df['n_ratings']
    del df['category']
    from feature_engine.imputation import DropMissingData
    from feature_engine.imputation import CategoricalImputer
    from feature_engine.imputation import ArbitraryNumberImputer
    from feature_engine.imputation import MeanMedianImputer
    # subcategory
    missingdata_imputer = DropMissingData(variables=['subcategory'])
    missingdata_imputer.fit(df)
    df = missingdata_imputer.transform(df)
    # description
    imputer = CategoricalImputer(variables=['description'], fill_value='')
    imputer.fit(df)
    df = imputer.transform(df)
    # enrolled
    arbitrary_imputer = ArbitraryNumberImputer(arbitrary_number=0, variables=['enrolled'])
    arbitrary_imputer.fit(df)
    df = arbitrary_imputer.transform(df)
    # institution & instructor
    imputer = CategoricalImputer(variables=['institution', 'instructor'], fill_value='')
    imputer.fit(df)
    df = imputer.transform(df)
    # rating
    median_imputer = MeanMedianImputer(imputation_method='median', variables=['rating'])
    median_imputer.fit(df)
    df = median_imputer.transform(df)
    # total_hours
    missingdata_imputer = DropMissingData(variables=['total_hours'])
    missingdata_imputer.fit(df)
    df = missingdata_imputer.transform(df)
    df.reset_index(inplace=True)
    del df['index']
    df.to_csv('data/03_primary/cleaned_coursera.csv')


def feature_engineering_udacity(df: pd.DataFrame) -> pd.DataFrame:
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
    df = pd.concat([df, pd.get_dummies(df['school'], prefix='school')], axis=1)
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


def feature_engineering_coursera(df: pd.DataFrame) -> pd.DataFrame:
    from feature_engine.encoding import CountFrequencyEncoder
    from feature_engine.encoding import OneHotEncoder
    from feature_engine.discretisation import ArbitraryDiscretiser
    df['institution'].fillna("", inplace=True)
    df['instructor'].fillna("", inplace=True)
    encoder_ins = CountFrequencyEncoder(encoding_method='frequency',
                                    variables=['instructor', 'institution'])
    encoder_ins.fit(df)
    df = encoder_ins.transform(df)
    df['difficulty'].fillna("Beginner", inplace=True)
    df['difficulty'] = df['difficulty'].map({'Beginner': 0, 'Intermediate': 1, 'Advanced': 2})
    df['subcategory'].fillna("", inplace=True)
    df['section'].fillna("", inplace=True)
    df['language'].fillna("", inplace=True)
    encoder = OneHotEncoder(variables=['subcategory', 'section', 'language'], drop_last=False)
    encoder.fit(df)
    df = encoder.transform(df)
    user_dict = {'rating': [3.0, 4.1, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, np.Inf]}
    transformer = ArbitraryDiscretiser(
        binning_dict=user_dict, return_object=False, return_boundaries=False)
    df = transformer.fit_transform(df)
    df.to_csv('data/03_primary/fe_coursera.csv')


def feature_selection_udacity(df: pd.DataFrame) -> pd.DataFrame:
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

def feature_selection_coursera(df: pd.DataFrame) -> pd.DataFrame:
    numerics = ['enrolled', 'rating', 'total_hours']
    aux_df = df[numerics]
    from sklearn.preprocessing import PowerTransformer
    pt = PowerTransformer()
    pt.fit(aux_df)
    print(pt.lambdas_)
    df[numerics] = pt.transform(aux_df)
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    num_df = df.select_dtypes(include=numerics)
    num_df.to_csv('data/04_feature/features_coursera.csv')
    text = ['object']
    text_df = df.select_dtypes(include=text)
    text_df.to_csv('data/04_feature/coursera_text.csv')