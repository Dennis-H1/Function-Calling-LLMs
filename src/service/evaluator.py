import re
import json
from enum import Enum
from itertools import zip_longest
from dataclasses import dataclass, field

from src.service.llm_service import ModelSolution


class EvaluationCategory(Enum):
    CORRECT = "Correct"
    PARTIALLY_CORRECT = "Partially Correct"
    INCORRECT = "Incorrect"


@dataclass
class Path:
    functions: list[str]
    parameters: list[dict]
    n_gram: int = field(default=0)
    _exclude: tuple = ("functions", "parameters", "n_gram")

    def get_num_functions(self) -> int:
        return len(self.functions)

    def get_num_arguments(self) -> int:
        num_params = 0
        for params in self.parameters:
            num_params += len(params)
        return num_params


@dataclass
class Evaluation:
    function_eval: EvaluationCategory
    argument_eval: EvaluationCategory
    response_eval: EvaluationCategory
    num_correct_functions: int
    num_correct_arguments: int
    path: Path

    _exclude: tuple = ("_exclude", "num_correct_functions",
                       "num_correct_arguments", "path")

    def get_total_number_functions(self) -> int:
        return self.path.get_num_functions()

    def get_total_number_arguments(self) -> int:
        return self.path.get_num_arguments()

    def get_num_correct_functions(self) -> int:
        return self.num_correct_functions

    def get_num_correct_arguments(self) -> int:
        return self.num_correct_arguments

    def get_answer_correct(self) -> bool:
        return True if self.response_eval == EvaluationCategory.CORRECT else False

    def get_overall_match(self) -> bool:
        return (self.function_eval == EvaluationCategory.CORRECT and self.argument_eval ==
                EvaluationCategory.CORRECT and self.response_eval == EvaluationCategory.CORRECT)


class Evaluator:

    # @staticmethod
    # def eval_arguments(called_path: list[dict], correct_path: Path) -> tuple[int, EvaluationCategory]:
    #     def compare_params(called_params: dict, target_params: dict):
    #         matches = 0
    #         matching_status = EvaluationCategory.INCORRECT
    #         if called_params is None or target_params is None:
    #             pass  # "Incorrect", 0
    #         elif called_params == target_params:
    #             matches = len(called_params)
    #             matching_status = EvaluationCategory.CORRECT
    #         else:
    #             matching_keys = called_params.keys() & target_params.keys()
    #             if len(matching_keys) > 0:
    #                 matches = len(
    #                     [True for key in matching_keys if called_params[key] == target_params[key]])
    #                 if matches > 0:
    #                     matching_status = EvaluationCategory.PARTIALLY_CORRECT
    #         return matching_status, matches
    #     def compare_paths(called_path: list[dict], correct_path: Path):
    #         matches = 0
    #         best_status = None
    #         for called_params, target_params in zip_longest(called_path, correct_path.parameters):
    #             s, m = compare_params(called_params, target_params)
    #             matches += m
    #             if best_status is None:
    #                 best_status = s
    #             elif best_status == EvaluationCategory.CORRECT and (s == EvaluationCategory.PARTIALLY_CORRECT or s == EvaluationCategory.INCORRECT):
    #                 best_status = EvaluationCategory.PARTIALLY_CORRECT
    #             elif best_status == EvaluationCategory.INCORRECT and (s == EvaluationCategory.PARTIALLY_CORRECT or EvaluationCategory.CORRECT):
    #                 best_status = EvaluationCategory.PARTIALLY_CORRECT
    #         return best_status, matches
    #     # Edge Case: target is no function call (and model calls none)
    #     if len(called_path) == 0 and len(correct_path.parameters) == 0:
    #         return 0, EvaluationCategory.CORRECT
    #     return compare_paths(called_path, correct_path)

    @staticmethod
    def eval_arguments(called_parameters: list[dict], target_parameters: list[dict], target_all_parameters: list[dict]):
        matches = 0
        for called_params, target_params in zip(called_parameters, target_parameters):
            for key, value in called_params.items():
                if isinstance(value, list) and isinstance(target_params[key], list) and sorted(value) == sorted(target_params[key]):
                    matches += 1

                elif key in target_params and value == target_params[key]:
                    matches += 1

        len_total_parameters = sum([len(params)
                                   for params in target_all_parameters])

        print(len_total_parameters)

        if matches == len_total_parameters:
            evaluation_category = EvaluationCategory.CORRECT
        elif matches > len_total_parameters:
            evaluation_category = EvaluationCategory.PARTIALLY_CORRECT
        else:
            evaluation_category = EvaluationCategory.INCORRECT

        return matches, evaluation_category

    @staticmethod
    def eval_functions(called_functions: list[str], correct_paths: list[Path]) -> tuple[int, EvaluationCategory]:

        def generate_n_gram(l: list[str], n: int):
            if n > len(l) or n <= 0:
                return []

            out = []
            for i in range(len(l)):
                if i + n > len(l):
                    break
                else:
                    out.append(l[i:i+n])
            return out

        def best_n_gram(called, paths):
            max_n = 0
            max_path = paths[0]

            max_range = min(len(called), max(
                [len(path.functions) for path in paths]))
            for n in range(1, max_range+1):
                for path in paths:
                    n_grams_target = generate_n_gram(path.functions, n)
                    n_grams_called = generate_n_gram(called, n)
                    matched = any(
                        n_gram for n_gram in n_grams_called if n_gram in n_grams_target)

                    if matched:
                        max_n += 1
                        max_path = path
                        break
            return max_path, n

        max_path, n = best_n_gram(called_functions, correct_paths)
        num_functions = max_path.get_num_functions()

        if num_functions == len(called_functions):
            evaluation_category = EvaluationCategory.CORRECT
        elif num_functions > len(called_functions):
            evaluation_category = EvaluationCategory.PARTIALLY_CORRECT
        else:
            evaluation_category = EvaluationCategory.INCORRECT

        return max_path, n, evaluation_category

    @staticmethod
    def eval_response(model_response: str, target_responses: dict) -> EvaluationCategory:

        def eval_response(model_response: dict, target_response: dict, ordered_items: dict):

            if model_response.keys() != target_response.keys():
                return False

            for key in model_response.keys():
                if key in ordered_items:
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

    @staticmethod
    def get_overall_evaluation(model_solution: ModelSolution, correct_paths: list[Path], target_response: dict) -> Evaluation:
        gold_path, num_correct_functions, function_eval = Evaluator.eval_functions(
            model_solution.functions, correct_paths)

        def generate_n_gram(l: list[str], n: int):
            if n > len(l) or n <= 0:
                return []

            out = []
            for i in range(len(l)):
                if i + n > len(l):
                    break
                else:
                    out.append(l[i:i+n])
            return out

        def find_n_gram(called, path, n: int):
            called_n_grams = generate_n_gram(called, n)
            target_n_grams = generate_n_gram(path.functions, n)

            i = 0
            for called, target in zip(called_n_grams, target_n_grams):
                if called == target:
                    return i, i+n
                i += 1
            return 0, 0

        start, end = find_n_gram(
            model_solution.functions, gold_path, num_correct_functions)

        num_correct_arguments, argument_eval = Evaluator.eval_arguments(
            model_solution.parameters, gold_path.parameters[start:end], gold_path.parameters)

        print(f"Start: {start}, End: {end}")

        print(model_solution.parameters,
              gold_path.parameters[start:end])
        print(
            f"Num correct:  {num_correct_arguments} Eval: {argument_eval.value}")

        response_eval = Evaluator.eval_response(
            model_solution.answer, target_response)

        return Evaluation(function_eval,
                          argument_eval,
                          response_eval,
                          num_correct_functions,
                          num_correct_arguments,
                          gold_path)
