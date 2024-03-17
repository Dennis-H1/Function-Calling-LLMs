import re
import json
from enum import Enum
from itertools import zip_longest


class EvaluationCategory(Enum):
    CORRECT = "Correct"
    PARTIALLY_CORRECT = "Partially Correct"
    INCORRECT = "Incorrect"


class Evaluator:

    @staticmethod
    def eval_arguments(called_path: list[dict], correct_paths: list[dict]) -> tuple[int, EvaluationCategory]:

        def compare_params(called_params: dict, target_params: dict):
            matches = 0
            matching_status = EvaluationCategory.INCORRECT

            if called_params is None or target_params is None:
                pass  # "Incorrect", 0
            elif called_params == target_params:
                matches = len(called_params)
                matching_status = EvaluationCategory.CORRECT
            else:
                matching_keys = called_params.keys() & target_params.keys()
                if len(matching_keys) > 0:
                    matches = len(
                        [True for key in matching_keys if called_params[key] == target_params[key]])
                    if matches > 0:
                        matching_status = EvaluationCategory.PARTIALLY_CORRECT

            return matching_status, matches

        def compare_paths(called_path: list[dict], correct_path: list[dict]):
            matches = 0
            best_status = None
            for called_params, target_params in zip_longest(called_path, correct_path["parameters"]):

                s, m = compare_params(called_params, target_params)
                matches += m

                if best_status is None:
                    best_status = s

                elif best_status == EvaluationCategory.CORRECT and (s == EvaluationCategory.PARTIALLY_CORRECT or s == EvaluationCategory.INCORRECT):
                    best_status = EvaluationCategory.PARTIALLY_CORRECT

                elif best_status == EvaluationCategory.INCORRECT and (s == EvaluationCategory.PARTIALLY_CORRECT or EvaluationCategory.CORRECT):
                    best_status = EvaluationCategory.PARTIALLY_CORRECT

            return best_status, matches

        # Edge Case: target is no function call (and model calls none)
        if len(called_path) == 0 and len(correct_paths) == 1 and len(correct_paths[0]["parameters"]) == 0:
            return 0, EvaluationCategory.CORRECT

        best_matches = 0
        best_status = EvaluationCategory.INCORRECT
        for correct_path in correct_paths:

            matching_status, matches = compare_paths(called_path, correct_path)

            if matches > best_matches:
                best_matches = matches
                best_status = matching_status

            if matching_status == EvaluationCategory.CORRECT:
                break

        return best_matches, best_status

    @staticmethod
    def eval_functions(called_functions: list[str], correct_paths: list[dict]) -> tuple[int, EvaluationCategory]:
        best_status = EvaluationCategory.INCORRECT
        best_match_count = 0

        for path in correct_paths:
            correct_functions = path["functions"]
            match_count = sum(1 for a, b in zip(
                called_functions, correct_functions) if a == b)

            if match_count > best_match_count:
                best_match_count = match_count
                if match_count == len(called_functions) == len(correct_functions):
                    best_status = EvaluationCategory.CORRECT
                elif match_count > 0:
                    best_status = EvaluationCategory.PARTIALLY_CORRECT

        return best_match_count, best_status

    @staticmethod
    def eval_response(model_response: dict, target_responses: dict) -> EvaluationCategory:

        def eval_response(model_response: dict, target_response: dict, ordered_items: dict):

            if model_response.keys() != target_response.keys():
                return False

            for key in model_response.keys():
                if key in ordered_items:
                    print("OKK SORTED!!")
                    print(key, model_response[key], target_response[key])
                    if model_response[key] != target_response[key]:
                        return False

                else:
                    if (isinstance(model_response[key], list) and isinstance(target_response[key], list)):
                        if sorted(model_response[key]) != sorted(target_response[key]):
                            return False
                    else:
                        if model_response[key] != target_response[key]:
                            return False

            return True

        model_response = re.sub("'", '"', model_response)
        model_response = re.sub(r"{\s*", "{", model_response)
        model_response = re.sub(r"\s}*}", "}", model_response)
        model_response = re.sub(r"\[\s*", "[", model_response)
        model_response = re.sub(r"\s*]", "]", model_response)
        model_response = re.sub(r",\s*(?!\s*\w)", ",", model_response)
        model_response = re.sub(r"/s*,", ",", model_response)
        model_response = re.sub(r":\s*", ":", model_response)
        model_response = re.sub(r"\s*:", ":", model_response)
        model_response = re.sub('(?<=[\s\w])"(?![:,}\]])', "'", model_response)

        model_response_raw = re.search(
            r'\{(.|\n)*?\}', model_response, re.DOTALL)

        if model_response_raw:
            try:
                model_response = json.loads(model_response_raw.group())

                if eval_response(model_response, target_responses["answer"], target_responses["ordered_items"]):
                    return EvaluationCategory.CORRECT

            except json.JSONDecodeError:
                return EvaluationCategory.INCORRECT

        return EvaluationCategory.INCORRECT
