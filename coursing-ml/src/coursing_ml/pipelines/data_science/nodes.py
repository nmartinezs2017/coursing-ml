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

Delete this when you start working on your own Kedro project.
"""
# pylint: disable=invalid-name

import logging
from typing import Any, Dict

import hdbscan
from feature_engine.imputation import ArbitraryNumberImputer
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer, util
from sklearn.cluster import DBSCAN

def clustering_udacity(df: pd.DataFrame, data: pd.DataFrame):
    km7 = KMeans(n_clusters=7).fit(df)
    df['Label'] = km7.labels_
    data['Label'] = km7.labels_
    return [df, data, km7]

def clustering_coursera(df: pd.DataFrame, data: pd.DataFrame):
    # set up the imputer
    arbitrary_imputer = ArbitraryNumberImputer(arbitrary_number=0)
    # fit the imputer
    arbitrary_imputer.fit(df)
    # transform the data
    df = arbitrary_imputer.transform(df)
    clustering_model = hdbscan.HDBSCAN(min_samples=10, min_cluster_size=100, prediction_data=True)
    cluster_labels = clustering_model.fit_predict(df)
    df['Label'] = cluster_labels
    data['Label'] = cluster_labels
    return [df, data, clustering_model]


def clustering_udemy(df: pd.DataFrame, data: pd.DataFrame):
    clustering_model = hdbscan.HDBSCAN(min_samples=1, min_cluster_size=500, prediction_data=True)
    cluster_labels = clustering_model.fit_predict(df)
    df['Label'] = cluster_labels
    data['Label'] = cluster_labels
    return [df, data, clustering_model]


def generate_embeddings_udacity(df: pd.DataFrame):
    df['description'] = df.description.replace(np.nan, '', regex=True)
    result = [x + '. ' + y for x, y in zip(df['title'], df['description'])]
    model = SentenceTransformer('allenai-specter')
    corpus_embeddings = model.encode(result, convert_to_tensor=True)
    return [corpus_embeddings, model]


def generate_embeddings_coursera(df: pd.DataFrame):
    df['description'] = df.description.replace(np.nan, '', regex=True)
    df['title'] = df.title.replace(np.nan, '', regex=True)
    model = SentenceTransformer('distiluse-base-multilingual-cased-v2')
    result = [x + '. ' + y for x, y in zip(df['title'], df['description'])]
    corpus_embeddings = model.encode(result, convert_to_tensor=True)
    return [corpus_embeddings, model]


def generate_embeddings_udemy(df: pd.DataFrame):
    df['description'] = df.description.replace(np.nan, '', regex=True)
    df['title'] = df.title.replace(np.nan, '', regex=True)
    df['description_extend'] = df.description_extend.replace(np.nan, '', regex=True)
    model = SentenceTransformer('distiluse-base-multilingual-cased-v2')
    result = [x + '. ' + y + '. ' + z for x, y, z in zip(df['title'], df['description'], df['description_extend'])]
    corpus_embeddings = model.encode(result, convert_to_tensor=True)
    return [corpus_embeddings, model]