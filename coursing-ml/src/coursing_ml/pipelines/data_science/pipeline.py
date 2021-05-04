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

from kedro.pipeline import Pipeline, node

from .nodes import *

def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                clustering_udacity,
                ["numerical_features_udacity", "numerical_data_udacity"],
                ["clustering_output_udacity", "data_labeled_udacity", "clustering_model_udacity"],
            ),
            node(
                clustering_coursera,
                ["numerical_features_coursera", "numerical_data_coursera"],
                ["clustering_output_coursera", "data_labeled_coursera", "clustering_model_coursera"],
            ),
            node(
                generate_embeddings_udacity,
                "categorical_features_udacity",
                ["corpus_embeddings_udacity", "nlp_model_udacity"]
            ),
            node(
                generate_embeddings_coursera,
                "categorical_features_coursera",
                ["corpus_embeddings_coursera", "nlp_model_coursera"]
            ),
        ]
    )
