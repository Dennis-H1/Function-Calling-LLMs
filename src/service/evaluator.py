import re
import json
from enum import Enum
from itertools import zip_longest
from dataclasses import dataclass, field

from src.service.llm_service import ModelSolution
from numbers import Number


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

    _exclude: tuple = (
        "_exclude",
        "num_correct_functions",
        "num_correct_arguments",
        "path",
    )

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
        return (
            self.function_eval == EvaluationCategory.CORRECT
            and self.argument_eval == EvaluationCategory.CORRECT
            and self.response_eval == EvaluationCategory.CORRECT
        )


class Evaluator:

    @staticmethod
    def eval_arguments(
        called_parameters: list[dict],
        target_parameters: list[dict],
    ):
        matches = 0
        for called_params, target_params in zip(called_parameters, target_parameters):
            for key, value in called_params.items():
                if key in target_params:
                    # lists: sort their content (strings)
                    if (
                        isinstance(value, list)
                        and isinstance(target_params[key], list)
                        and sorted(value) == sorted(target_params[key])
                    ):
                        matches += 1

                    # round numbers by 2 decimals
                    elif isinstance(value, Number) and isinstance(
                        target_params[key], Number
                    ):
                        if round(value, 2) == round(target_params[key], 2):
                            matches += 1

                    elif value == target_params[key]:
                        matches += 1

        len_target_parameters = sum([len(params)
                                     for params in target_parameters])

        if matches == len_target_parameters:
            evaluation_category = EvaluationCategory.CORRECT
        elif matches > 0:
            evaluation_category = EvaluationCategory.PARTIALLY_CORRECT
        else:
            evaluation_category = EvaluationCategory.INCORRECT

        return matches, evaluation_category

    @staticmethod
    def eval_functions(
        called_functions: list[str], correct_paths: list[Path]
    ) -> tuple[Path, int, EvaluationCategory]:

        def generate_n_gram(l: list[str], n: int):
            if n > len(l) or n <= 0:
                return []

            out = []
            for i in range(len(l)):
                if i + n > len(l):
                    break
                else:
                    out.append(l[i: i + n])
            return out

        def best_n_gram(called: list[str], paths: list[Path]):
            max_n = 0
            max_path = paths[0]

            max_range = min(len(called), max(
                [len(path.functions) for path in paths]))
            for n in range(1, max_range + 1):
                for path in paths:
                    n_grams_target = generate_n_gram(path.functions, n)
                    n_grams_called = generate_n_gram(called, n)
                    matched = any(
                        n_gram for n_gram in n_grams_called if n_gram in n_grams_target
                    )

                    if matched:
                        max_n += 1
                        max_path = path
                        break
            return max_path, max_n

        max_path, n = best_n_gram(called_functions, correct_paths)

        if n != 0 and n == len(max_path.functions) and len(max_path.functions) == len(called_functions):
            evaluation_category = EvaluationCategory.CORRECT
        elif n == 0:
            evaluation_category = EvaluationCategory.INCORRECT
        else:
            evaluation_category = EvaluationCategory.PARTIALLY_CORRECT

        return max_path, n, evaluation_category

    @staticmethod
    def eval_response(
        model_response: str, target_responses: dict
    ) -> EvaluationCategory:

        def eval_response(
            model_response: dict, target_response: dict, ordered_items: dict
        ):

            if sorted(model_response.keys()) != sorted(target_response.keys()):
                return False

            for key in model_response.keys():
                if key in ordered_items:
                    if model_response[key] != target_response[key]:
                        return False

                else:
                    if isinstance(model_response[key], list) and isinstance(
                        target_response[key], list
                    ):
                        if sorted(model_response[key]) != sorted(target_response[key]):
                            return False

                    # round numbers by 2 decimals
                    elif isinstance(model_response[key], Number) and isinstance(
                        target_response[key], Number
                    ):
                        if round(model_response[key], 2) != round(target_response[key], 2):
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
            r"\{(.|\n)*?\}", model_response, re.DOTALL)

        if model_response_raw:
            try:
                model_response = json.loads(model_response_raw.group())

                if eval_response(
                    model_response,
                    target_responses["answer"],
                    target_responses["ordered_items"],
                ):
                    return EvaluationCategory.CORRECT

            except json.JSONDecodeError:
                return EvaluationCategory.INCORRECT

        return EvaluationCategory.INCORRECT

    @staticmethod
    def get_overall_evaluation(
        model_solution: ModelSolution, correct_paths: list[Path], target_response: dict
    ) -> Evaluation:
        gold_path, num_correct_functions, function_eval = Evaluator.eval_functions(
            model_solution.functions, correct_paths
        )

        def generate_n_gram(l: list[str], n: int):
            if n > len(l) or n <= 0:
                return []

            out = []
            for i in range(len(l)):
                if i + n > len(l):
                    break
                else:
                    out.append(l[i: i + n])
            return out

        def find_n_gram(called, path, n: int):
            called_n_grams = generate_n_gram(called, n)
            target_n_grams = generate_n_gram(path.functions, n)

            i = 0
            for called, target in zip(called_n_grams, target_n_grams):
                if called == target:
                    return i, i + n
                i += 1
            return 0, 0

        start, end = find_n_gram(
            model_solution.functions, gold_path, num_correct_functions
        )

        num_correct_arguments, argument_eval = Evaluator.eval_arguments(
            model_solution.parameters,
            gold_path.parameters[start:end],
        )

        response_eval = Evaluator.eval_response(
            model_solution.answer, target_response)

        return Evaluation(
            function_eval,
            argument_eval,
            response_eval,
            num_correct_functions,
            num_correct_arguments,
            gold_path,
        )
