from enum import Enum
from dataclasses import fields, is_dataclass


def to_dict(instance, exclude=None) -> dict:
    if exclude is None:
        exclude = []

    class_exclude = getattr(instance, '_exclude', [])
    exclude.extend(class_exclude)

    result = {}
    for field_info in fields(instance):
        field_name = field_info.name
        if field_name in exclude:
            continue

        field_value = getattr(instance, field_name)

        if is_dataclass(field_value):
            nested_result = to_dict(field_value)
            if nested_result is not None:
                result[field_name] = nested_result
        elif isinstance(field_value, Enum):
            result[field_name] = field_value.value
        elif isinstance(field_value, list):
            list_result = [to_dict(item) if is_dataclass(
                item) else item for item in field_value]
            if any(item is not None for item in list_result):
                result[field_name] = list_result
        elif isinstance(field_value, dict):
            dict_result = {key: to_dict(value) if is_dataclass(
                value) else value for key, value in field_value.items()}
            if any(value is not None for value in dict_result.values()):
                result[field_name] = dict_result
        else:
            result[field_name] = field_value

    if not result:
        return None

    return result
