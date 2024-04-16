import json
from enum import Enum
from pathlib import Path
from jsonschema import validate, ValidationError

from src.util.use_case import UseCase

current_script_dir = Path(__file__).parent.parent.parent.resolve()


class ConfigManager:

    config = None
    question_set = None
    function_set = None

    __use_case_mappings = {
        "music": UseCase.MUSIC,
        "travel": UseCase.TRAVEL_AND_RESTAURANTS,
        "restaurant": UseCase.TRAVEL_AND_RESTAURANTS
    }

    class QuestionSetNotFoundException(Exception):
        def __init__(self, question_set_id: str) -> None:
            self.question_set_id = question_set_id

        def __str__(self):
            return f"The question set {self.question_set_id} that is provided in the test_config.json does not exist in the question_sets.json. You can find the files here: {ConfigManager.ConfigPath.QUESTION_SET_FILE_PATH.value}"

    class FunctionSetNotFoundException(Exception):
        def __init__(self, function_set_id: str) -> None:
            self.function_set_id = function_set_id

        def __str__(self):
            return f"The function set {self.function_set_id} that is provided in the test_config.json does not exist in the function_sets.json. You can find the files here: {ConfigManager.ConfigPath.FUNCTION_SET_FILE_PATH.value}"

    class UseCaseNotFoundException(Exception):
        def __init__(self, id: str) -> None:
            self.id = id

        def __str__(self):
            return f"The config id value of >>>{self.id}<<< does not contain any of the keywords: 'music', 'travel' or 'restaurant'. We cannot assign a usecase."

    class ConfigPath(Enum):
        BASE_DIR = current_script_dir/"src"/"config"
        TEST_CONFIG_FILE_PATH = BASE_DIR / "test_config.json"
        QUESTION_SET_FILE_PATH = BASE_DIR / "question_sets.json"
        FUNCTION_SET_FILE_PATH = BASE_DIR / "function_sets.json"
        DEFAULT_OUTPUT_FILE_PATH = BASE_DIR / "out"/"output.json"

    class Schema(Enum):
        TEST_CONFIG_SCHEMA = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "id": {
                    "type": "string"
                },
                "name": {
                    "type": "string"
                },
                "description": {
                    "type": "string"
                },
                "authors": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                },
                "use_case": {
                    "type": "string"
                },
                "license": {
                    "type": "string"
                },
                "model": {
                    "type": "string"
                },
                "hyperparameters": {
                    "type": "object",
                    "properties": {
                        "temperature": {
                            "type": "number"
                        }
                    },
                    "required": ["temperature"]
                },
                "prompt": {
                    "type": "string"
                },
                "function_set": {
                    "type": "string"
                },
                "question_set": {
                    "type": "string"
                },
                "output_file": {
                    "type": "string",
                    "pattern": "[\w\.\\\/]*?\.json"
                }
            },
            "required": ["id", "name", "description", "authors", "license", "model", "prompt", "function_set", "question_set", "output_file"]
        }

        QUESTION_SET_SCHEMA = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "question_sets": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "type": "string"
                            },
                            "name": {
                                "type": "string"
                            },
                            "domain": {
                                "type": "string"
                            },
                            "date": {
                                "type": "string",
                                "format": "date"
                            },
                            "description": {
                                "type": "string"
                            },
                            "authors": {
                                "type": "array",
                                "items": {
                                    "type": "string"
                                }
                            },
                            "license": {
                                "type": "string"
                            },
                            "function_sets": {
                                "type": "array",
                                "items": {
                                    "type": "string"
                                }
                            },
                            "questions": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "id": {
                                            "type": "string"
                                        },
                                        "category": {
                                            "type": "string"
                                        },
                                        "question": {
                                            "type": "string"
                                        },
                                        "motivation": {
                                            "type": "string"
                                        },
                                        "target": {
                                            "type": "object",
                                            "properties": {
                                                "chained": {
                                                    "type": "boolean"
                                                },
                                                "solution_paths": {
                                                    "type": "array",
                                                    "items": {
                                                        "type": "object",
                                                        "properties": {
                                                            "path_id": {
                                                                "type": "integer"
                                                            },
                                                            "functions": {
                                                                "type": "array",
                                                                "items": {
                                                                    "type": "string"
                                                                }
                                                            },
                                                            "parameters": {
                                                                "type": "array",
                                                                "items": {
                                                                    "type": "object",
                                                                    "additionalProperties": True
                                                                }
                                                            }
                                                        },
                                                        "required": ["path_id", "functions", "parameters"]
                                                    }
                                                },
                                                "expected_answer": {
                                                    "type": "object",
                                                    "properties": {
                                                        "ordered_items": {
                                                            "type": "array",
                                                            "items": {
                                                                "type": "string"
                                                            }
                                                        },
                                                        "answer": {
                                                            "type": "object",
                                                            "additionalProperties": True
                                                        }
                                                    },
                                                    "required": ["answer"]
                                                }
                                            },
                                            "required": ["chained", "solution_paths", "expected_answer"]
                                        }
                                    },
                                    "required": ["id", "category", "question", "motivation", "target"]
                                }
                            }
                        },
                        "required": ["id", "name", "domain", "date", "description", "authors", "license", "function_sets", "questions"]
                    }
                }
            },
            "required": ["question_sets"]
        }

        FUNCTION_SET_SCHEMA = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "function_sets": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "type": "string"
                            },
                            "name": {
                                "type": "string"
                            },
                            "domain": {
                                "type": "string"
                            },
                            "categories": {
                                "type": "array",
                                "items": {
                                    "type": "string"
                                }
                            },
                            "num_functions": {
                                "type": "integer"
                            },
                            "functions": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {
                                            "type": "string"
                                        },
                                        "description": {
                                            "type": "string"
                                        },
                                        "parameters": {
                                            "type": "object",
                                        }
                                    },
                                    "required": ["name", "description", "parameters"]
                                }
                            }
                        },
                        "required": ["id", "name", "domain", "categories", "num_functions", "functions"]
                    }
                }
            },
            "required": ["function_sets"]
        }

    @classmethod
    def load_data(cls) -> tuple[dict, dict, dict]:
        cls.config = cls._load_data(
            cls.ConfigPath.TEST_CONFIG_FILE_PATH.value, cls.Schema.TEST_CONFIG_SCHEMA.value)
        all_question_sets = cls._load_data(
            cls.ConfigPath.QUESTION_SET_FILE_PATH.value, cls.Schema.QUESTION_SET_SCHEMA.value)
        all_function_sets = cls._load_data(
            cls.ConfigPath.FUNCTION_SET_FILE_PATH.value, cls.Schema.FUNCTION_SET_SCHEMA.value)

        cls.question_set = cls._get_question_set(all_question_sets)
        cls.function_set = cls._get_function_set(all_function_sets)

        return cls.config, cls.question_set, cls.function_set

    @classmethod
    def output_path(cls) -> str:
        if cls.config is None:
            return cls.ConfigPath.DEFAULT_OUTPUT_FILE_PATH.value
        else:
            return cls.config.get("output_file") or cls.ConfigPath.DEFAULT_OUTPUT_FILE_PATH.value

    @classmethod
    def get_use_case(cls) -> UseCase:
        for keyword, use_case in cls.__use_case_mappings.items():
            if keyword in cls.config["id"].lower():
                return use_case

        raise cls.UseCaseNotFoundException(cls.config["id"])

    @classmethod
    def _load_data(cls, file_path: str, json_schema: dict) -> dict:
        try:
            with open(file_path, encoding="utf-8") as f:
                json_data = json.load(f)
        except json.JSONDecodeError:
            raise json.JSONDecodeError(
                f"There is a JSON formatting error with the {file_path} file.")

        cls._validate_json(json_data, json_schema, file_path)

        return json_data

    @classmethod
    def _get_question_set(cls, question_sets: list[dict]):
        question_set = None
        for q_set in question_sets["question_sets"]:
            if q_set["id"] == cls.config["question_set"]:
                question_set = q_set
                break
        if question_set is None:
            raise ConfigManager.QuestionSetNotFoundException(
                cls.config["question_set"])

        return question_set

    @classmethod
    def _get_function_set(cls, function_sets: list[dict]):
        function_set = None
        for f_set in function_sets["function_sets"]:
            if f_set["id"] == cls.config["function_set"]:
                function_set = f_set
                break
        if function_set is None:
            raise ConfigManager.FunctionSetNotFoundException(
                cls.config["function_set"])

        return function_set

    @classmethod
    def _validate_json(cls, json_data: dict, json_schema: dict, file_path: str) -> None:
        try:
            validate(json_data, schema=json_schema)
        except ValidationError as e:
            raise ValidationError(
                f"There is a JSON validation error with the {file_path} file. Some keys or values are not correctly specified: {e.message}.")
        return json_data
