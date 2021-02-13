from kedro.io import AbstractDataSet, DataSetError
from pandas_profiling import ProfileReport
from typing import Dict, Any

class ProfileReportDataSet(AbstractDataSet):

    def __init__(self, filepath: str, save_args: Dict[str, Any] = None):
        self._filepath = filepath
        self._save_args = save_args or {}

    def _load(self):
        raise DataSetError("Write-Only Dataset")

    def _save(self, df):
        pr = ProfileReport(df)
        pr.to_file(self._filepath)

    def _describe(self):
        return dict(
            filepath=self._filepath
        )