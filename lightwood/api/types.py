from typing import Dict, List, Union
from dataclasses import dataclass
from lightwood.helpers.log import log
from dataclasses_json import dataclass_json
from dataclasses_json.core import _asdict, Json


@dataclass_json
@dataclass
class Feature:
    name: str
    data_dtype: str
    dependency: List[str] = None
    encoder: str = None


@dataclass_json
@dataclass
class Output:
    name: str
    data_dtype: str
    encoder: str = None
    models: List[str] = None
    ensemble: str = None


@dataclass_json
@dataclass
class TypeInformation:
    dtypes: Dict[str, str]
    additional_info: Dict[str, object]
    identifiers: Dict[str, str]

    def __init__(self):
        self.dtypes = dict()
        self.additional_info = dict()
        self.identifiers = dict()


@dataclass_json
@dataclass
class StatisticalAnalysis:
    nr_rows: int
    train_std_dev: float
    train_observed_classes: Union[None, List[str]]
    target_class_distribution: Dict[str, float]
    histograms: Dict[str, Dict[str, List[object]]]


@dataclass_json
@dataclass
class DataAnalysis:
    statistical_analysis: StatisticalAnalysis
    type_information: TypeInformation


@dataclass
class TimeseriesSettings:
    is_timeseries: bool
    order_by: List[str] = None
    window: int = None
    group_by: List[str] = None
    use_previous_target: bool = False
    nr_predictions: int = None
    historical_columns: List[str] = None

    @staticmethod
    def from_dict(obj: Dict):
        if len(obj) > 0:
            for mandatory_setting in ['order_by', 'window']:
                err = f'Missing mandatory timeseries setting: {mandatory_setting}'
                log.error(err)
                raise Exception(err)

            timeseries_settings = TimeseriesSettings(
                is_timeseries=True,
                historical_columns=[],
                order_by=obj['order_by'],
                window=obj['window']

            )
            for setting in obj:
                timeseries_settings.__setattr__(setting, obj['setting'])

        else:
            timeseries_settings = TimeseriesSettings(is_timeseries=False)

        return timeseries_settings

    def to_dict(self, encode_json=False) -> Dict[str, Json]:
        return _asdict(self, encode_json=encode_json)


@dataclass
class ProblemDefinition:
    target: str
    nfolds: int
    pct_invalid: float
    seconds_per_model: int
    target_weights: List[float]
    positive_domain: bool
    fixed_confidence: Union[int, float, None]
    timeseries_settings: TimeseriesSettings
    anomaly_detection: bool
    anomaly_error_rate: Union[float, None]
    anomaly_cooldown: int
    ignore_features: List[str]

    @staticmethod
    def from_dict(obj: Dict) -> None:
        target = obj['target']
        nfolds = obj.get('nfolds', 10)
        pct_invalid = obj.get('pct_invalid', 1)
        seconds_per_model = obj.get('seconds_per_model', None)
        target_weights = obj.get('target_weights', None)
        positive_domain = obj.get('positive_domain', False)
        fixed_confidence = obj.get('fixed_confidence', None)
        timeseries_settings = TimeseriesSettings.from_dict(obj.get('timeseries_settings', {}))
        anomaly_detection = obj.get('anomaly_detection', True)
        anomaly_error_rate = obj.get('anomaly_error_rate', None)
        anomaly_cooldown = obj.get('anomaly_detection', 1)
        ignore_features = obj.get('ignore_features', [])

        problem_definition = ProblemDefinition(
            target=target,
            nfolds=nfolds,
            pct_invalid=pct_invalid,
            seconds_per_model=seconds_per_model,
            target_weights=target_weights,
            positive_domain=positive_domain,
            fixed_confidence=fixed_confidence,
            timeseries_settings=timeseries_settings,
            anomaly_detection=anomaly_detection,
            anomaly_error_rate=anomaly_error_rate,
            anomaly_cooldown=anomaly_cooldown,
            ignore_features=ignore_features
        )

        return problem_definition

    def to_dict(self, encode_json=False) -> Dict[str, Json]:
        return _asdict(self, encode_json=encode_json)


@dataclass_json
@dataclass
class LightwoodConfig:
    features: Dict[str, Feature]
    output: Output
    problem_definition: ProblemDefinition
    statistical_analysis: StatisticalAnalysis
    identifiers: Dict[str, str]
    cleaner: object = None
    splitter: object = None
    analyzer: object = None
    explainer: object = None
    imports: object = None
    timeseries_transformer: object = None
    accuracy_functions: List[str] = None


@dataclass_json
@dataclass
class ModelAnalysis:
    accuracies: Dict[str,float]
    train_sample_size: int
    test_sample_size: int
    column_importances: Dict[str, float]
    confusion_matrix: object = None