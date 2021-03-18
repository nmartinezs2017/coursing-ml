# kedro run --pipeline=de

from kedro.pipeline import Pipeline, node

from .nodes import *

def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=preprocess_udacity,
                inputs="udacity_scrapped",
                outputs="preprocessed_udacity",
                name="preprocessing_udacity",
            ),
            node(
                lambda x: x,
                inputs="preprocessed_udacity",
                outputs="data_exp_report",
                name="data_exploration_report",
            ),
            node(
                func=feature_cleaning_udacity,
                inputs="preprocessed_udacity",
                outputs="cleaned_udacity",
                name="feature_cleaning_udacity",
            ),
            node(
                func=feature_engineering_udacity,
                inputs="cleaned_udacity",
                outputs="fe_udacity",
                name="feature_engineering_udacity",
            ),
            node(
                func=feature_selection_udacity,
                inputs="fe_udacity",
                outputs="features_udacity",
                name="feature_selection",
            ),
            node(
                func=preprocess_coursera,
                inputs="coursera_scrapped",
                outputs=None,
                name="preprocessing_coursera",
            ),
            node(
                func=feature_cleaning_coursera,
                inputs="preprocessed_coursera",
                outputs=None,
                name="feature_cleaning_coursera",
            ),
            node(
                func=feature_engineering_coursera,
                inputs="cleaned_coursera",
                outputs=None,
                name="feature_engineering_coursera",
            ),
            node(
                func=feature_selection_coursera,
                inputs="fe_coursera",
                outputs=None,
                name="feature_selection_coursera",
            ),
        ]
    )
