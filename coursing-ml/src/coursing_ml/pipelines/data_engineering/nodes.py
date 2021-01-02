# Copyright 2020 QuantumBlack Visual Analytics Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND
# NONINFRINGEMENT. IN NO EVENT WILL THE LICENSOR OR OTHER CONTRIBUTORS
# BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF, OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# The QuantumBlack Visual Analytics Limited ("QuantumBlack") name and logo
# (either separately or in combination, "QuantumBlack Trademarks") are
# trademarks of QuantumBlack. The License does not grant you any right or
# license to the QuantumBlack Trademarks. You may not use the QuantumBlack
# Trademarks or any confusingly similar mark as a trademark for your product,
# or use the QuantumBlack Trademarks in any other manner that might cause
# confusion in the marketplace, including but not limited to in advertising,
# on websites, or on software.
#
# See the License for the specific language governing permissions and
# limitations under the License.
"""Example code for the nodes in the example pipeline. This code is meant
just for illustrating basic Kedro features.

PLEASE DELETE THIS FILE ONCE YOU START WORKING ON YOUR OWN PROJECT!
"""

from typing import Any, Dict
from sklearn import preprocessing
import pandas as pd

def extract_time_range(x):
    x = x.rstrip()
    if len(str(x).split(' ')) > 1:
        time_range = str(x).split(' ')[-1]
        return time_range
    else:
        return 'Weeks'

def extract_number_months(x):
        n_months = str(x).split(' ')[0]
        if n_months == 'Approx.,':
            return str(x).split(' ')[1].strip(',')
        else:
            return n_months

def extract_duration_hours(x):
    if len(str(x).split(' ')) > 1:
        range_hours = str(x).split(' ')[1]
        if '-' in range_hours:
            range_hours = range_hours.split('-')[1]
        return range_hours
    else:
        return 0

def calculate_total_hours(df: pd.DataFrame) -> pd.DataFrame:
    values = df["number_weeks_months"] * df["hours_per_week"]
    df['duration_total_hours'] = values.where(df.time_range == 'weeks')
    values = values * 4
    df['duration_total_hours'] = values.where(df.time_range == 'months', other=df['duration_total_hours'])
    return df


def label_difficulty(df: pd.DataFrame) -> pd.DataFrame:
    df['difficulty'] = df['difficulty'].apply(lambda _: str(_))
    le = preprocessing.LabelEncoder()
    df['difficulty'] = le.fit_transform(df['difficulty'])
    return df


def map_boolean_to_int(df, field) -> pd.DataFrame:
    d = {'True': 1, 'False': 0}
    df[field] = df[field].map(d)
    return df


def preprocess_udacity(df: pd.DataFrame) -> pd.DataFrame:
    df['n_reviews'] = df['n_reviews'].str.strip(' Reviews')
    df['n_reviews'] = pd.to_numeric(df['n_reviews'])
    df['new'] = df['new'].str.strip('[]')
    df['free'] = df['free'].str.strip('[]')
    df['rating'] = df['rating'].str.strip(' width:%;')
    df['rating'] = pd.to_numeric(df['rating'])
    df = label_difficulty(df)
    df['duration_hours'] = df['duration_hours'].apply(extract_duration_hours)
    df['n_reviews'].fillna(0, inplace=True)
    df['time_range'] = df['duration_weeks'].apply(extract_time_range)
    df['time_range'] = df['time_range'].str.lower()
    df['duration_weeks'] = df['duration_weeks'].apply(extract_number_months)
    df = map_boolean_to_int(df, 'new')
    df = map_boolean_to_int(df, 'free')
    df = df.rename(columns={"duration_hours": "hours_per_week", "duration_weeks": "number_weeks_months"})
    df['number_weeks_months'] = pd.to_numeric(df['number_weeks_months'])
    df['hours_per_week'] = pd.to_numeric(df['hours_per_week'])
    df = calculate_total_hours(df)
    return df

def split_data(data: pd.DataFrame, example_test_data_ratio: float) -> Dict[str, Any]:
    """Node for splitting the classical Iris data set into training and test
    sets, each split into features and labels.
    The split ratio parameter is taken from conf/project/parameters.yml.
    The data and the parameters will be loaded and provided to your function
    automatically when the pipeline is executed and it is time to run this node.
    """
    data.columns = [
        "sepal_length",
        "sepal_width",
        "petal_length",
        "petal_width",
        "target",
    ]
    classes = sorted(data["target"].unique())
    # One-hot encoding for the target variable
    data = pd.get_dummies(data, columns=["target"], prefix="", prefix_sep="")

    # Shuffle all the data
    data = data.sample(frac=1).reset_index(drop=True)

    # Split to training and testing data
    n = data.shape[0]
    n_test = int(n * example_test_data_ratio)
    training_data = data.iloc[n_test:, :].reset_index(drop=True)
    test_data = data.iloc[:n_test, :].reset_index(drop=True)

    # Split the data to features and labels
    train_data_x = training_data.loc[:, "sepal_length":"petal_width"]
    train_data_y = training_data[classes]
    test_data_x = test_data.loc[:, "sepal_length":"petal_width"]
    test_data_y = test_data[classes]

    # When returning many variables, it is a good practice to give them names:
    return dict(
        train_x=train_data_x,
        train_y=train_data_y,
        test_x=test_data_x,
        test_y=test_data_y,
    )
