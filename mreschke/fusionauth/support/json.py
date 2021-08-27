import json
from uvicore.support.dumper import dump, dd


def to(act: bool, models):
    """Convert List or Dict  JSON"""
    if not act: return models
    if not models: return '{}'
    return json.dumps(models)


def toOBSOLETE_NO_LONGER_USE_UVICORE_MODELS(act: bool, models):
    """Convert Uvicore Model or List[Model] to JSON"""
    # Uvicore models already have a pydantic .json() method
    # But if its a List of models, we must handle manually
    if not act: return models
    if not models: return '{}'
    if type(models) == list:
        results = []
        for model in models:
            results.append(model.json())
        json_results = '['
        for result in results:
            json_results += result + ','
        return json_results[0:-1] + ']'

    # A single uvicore model
    return models.json()


