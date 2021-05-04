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
                outputs="pre_report_udacity",
                name="report_udacity",
            ),
            node(
                func=feature_cleaning_udacity,
                inputs="preprocessed_udacity",
                outputs="cleaned_udacity",
                name="feature_cleaning_udacity",
            ),
            node(
                func=feature_selection_udacity,
                inputs="cleaned_udacity",
                outputs=["categorical_data_udacity", "numerical_data_udacity"],
                name="feature_selection_udacity",
            ),
            node(
                func=f_engineering_categorical_features_udacity,
                inputs="categorical_data_udacity",
                outputs="categorical_features_udacity",
                name="categorical_features_udacity",
            ),
            node(
                func=f_engineering_numerical_features_udacity,
                inputs="numerical_data_udacity",
                outputs="numerical_features_udacity",
                name="numerical_features_udacity",
            ),
            node(
                func=preprocess_coursera,
                inputs="coursera_scrapped",
                outputs="preprocessed_coursera",
                name="preprocessing_coursera",
            ),
            node(
                lambda x: x,
                inputs="preprocessed_coursera",
                outputs="pre_report_coursera",
                name="report_coursera",
            ),
            node(
                func=feature_cleaning_coursera,
                inputs="preprocessed_coursera",
                outputs="cleaned_coursera",
                name="feature_cleaning_coursera",
            ),
            node(
                func=feature_selection_coursera,
                inputs="cleaned_coursera",
                outputs=["categorical_data_coursera", "numerical_data_coursera"],
                name="feature_selection_coursera",
            ),
            node(
                func=f_engineering_categorical_features_coursera,
                inputs="categorical_data_coursera",
                outputs="categorical_features_coursera",
                name="categorical_features_coursera",
            ),
            node(
                func=f_engineering_numerical_features_coursera,
                inputs="numerical_data_coursera",
                outputs="numerical_features_coursera",
                name="numerical_features_coursera",
            ),
        ]
    )
