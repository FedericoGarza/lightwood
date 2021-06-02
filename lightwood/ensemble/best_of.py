from typing import List
from lightwood.model.base import BaseModel
import pandas as pd
from lightwood.data.encoded_ds import EncodedDs
from lightwood.ensemble.base import BaseEnsemble


class BestOf(BaseEnsemble):
    best_index: int

    def __init__(self, models: List[BaseModel], data: EncodedDs) -> None:
        super().__init__(models, data)
        # @TODO: Need some shared accuracy functionality to determine model selection here
        self.best_index = 0

    def __call__(self, ds: EncodedDs) -> pd.DataFrame:
        return self.models[self.best_index](ds)
