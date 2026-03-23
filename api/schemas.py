from pydantic import create_model, BaseModel, Field
import json
from typing import Literal

with open(r'/mlflow/model_artifacts/1/models/m-c9b8782d85e94044a200b6e9095e3238/artifacts/schemas.json', 'r') as f:
    schemas = json.load(f)

fields = {}

def find_dtype(dtype: str):
    if 'int' in dtype:
        return int
    elif 'float' in dtype:
        return float
    else:
        return str

for col, meta in schemas.items():
    dtype = find_dtype(meta['dtype'])

    if 'allowed_values' in meta and meta['allowed_values']:
        fields[col] = (Literal[tuple(meta['allowed_values'])], Field(...))
    elif dtype in [int, float]:
        fields[col] = (dtype, Field(..., ge=meta.get('min'), le=meta.get('max')))
    else:
        fields[col] = (dtype, Field(...))
RequestModel = create_model('RequestModel',**fields)

class ResponseModel(BaseModel):
    salePrice: float