import json
from datetime import date, datetime
from decimal import Decimal

from dateutil import parser
from sqlalchemy.orm import InstanceState

DATETIME_AWARE = "%m/%d/%Y %I:%M:%S %p %z"
DATE_ONLY = "%m/%d/%Y"

ONE_HOUR_IN_SECONDS = 3600
ONE_DAY_IN_SECONDS = ONE_HOUR_IN_SECONDS * 24
ONE_WEEK_IN_SECONDS = ONE_DAY_IN_SECONDS * 7
ONE_MONTH_IN_SECONDS = ONE_DAY_IN_SECONDS * 30
ONE_YEAR_IN_SECONDS = ONE_DAY_IN_SECONDS * 365

SERIALIZE_OBJ_MAP = {
    str(datetime): parser.parse,
    str(date): parser.parse,
    str(Decimal): Decimal,
}


def default( obj ):
    result = {}
    if isinstance(obj , dict):
        for key , value in obj.items():
            if not isinstance(value , InstanceState):
                if isinstance(value , datetime):
                    # {f"val-{key}": value.strftime(DATETIME_AWARE) , "_spec_type": str(datetime)}
                    result[f"val-{key}"] = value.strftime(DATETIME_AWARE)
                else:
                    result[key] = value
        return result
    else:
        return None

class BetterJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        result = {}
        if isinstance(obj.dict , dict):
            for key, value in obj.dict.items():
                if not isinstance(value, InstanceState):
                    if isinstance(value, datetime):
                        # {f"val-{key}": value.strftime(DATETIME_AWARE) , "_spec_type": str(datetime)}
                        result[f"val-{key}"] = value.strftime(DATETIME_AWARE)
                    else:
                        result[key] = value
            return result
        else:
            return None
            # If it's a dictionary, apply serialization to each value
            # return {"val": value for key , value in obj.dict.items() if not isinstance(value, InstanceState)}


        # elif isinstance(obj , list):
        #     # If it's a list, apply serialization to each element
        #     return [self.default(element) for element in obj]
        # elif isinstance(obj, datetime):
        #     return {"val": obj.strftime(DATETIME_AWARE), "_spec_type": str(datetime)}
        # elif isinstance(obj, date):
        #     return {"val": obj.strftime(DATE_ONLY), "_spec_type": str(date)}
        # elif isinstance(obj, Decimal):
        #     return {"val": str(obj), "_spec_type": str(Decimal)}
        # elif isinstance(obj, BaseModel):
        #     return obj.dict()
        # elif isinstance(obj, UUID):
        #     return str(obj)
        # elif isinstance(obj, Enum):
        #     return str(obj.value)
        # else:  # pragma: no cover
        #     return super().default(obj)


def object_hook(obj):
    if "_spec_type" not in obj:
        return obj
    _spec_type = obj["_spec_type"]
    if _spec_type not in SERIALIZE_OBJ_MAP:  # pragma: no cover
        raise TypeError(f'"{obj["val"]}" (type: {_spec_type}) is not JSON serializable')
    return SERIALIZE_OBJ_MAP[_spec_type](obj["val"])


def serialize_json(json_dict):
    if isinstance(json_dict, dict):
        data = default(obj = json_dict)
        # return json.dumps(json_dict, cls=BetterJsonEncoder)
        return json.dumps(data)

    else:
        data_main= []
        for obj in json_dict:
            data = default(obj = obj.__dict__)
            data_main.append(data)

        return json.dumps(data_main)


def deserialize_json(json_str):
    return json.loads(json_str, object_hook=object_hook)
