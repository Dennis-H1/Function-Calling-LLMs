from tqdm import tqdm
from datetime import datetime
from typing import Dict, List
from dataclasses import dataclass, field

from src.service.evaluator import Evaluator, Evaluation, Path
from src.service.llm_service import LLMService, ModelSolution
from src.util.to_dict import to_dict


@dataclass
class Metadata:
    run_id: str
    run_name: str
    question_set_id: str
    function_set_id: str
    prompt: str
    model: str
    hyperparameters: Dict[str, str]
    run_start_timestamp: str = field(
        default_factory=lambda: str(datetime.now()))
    run_end_timestamp: str = None
    test_driver_version: str = field(default_factory=lambda: "1.0.0")

    def update_endtime(self):
        self.run_end_timestamp = str(datetime.now())


@dataclass
class Statistics:
    number_of_functions: dict = field(
        default_factory=lambda: {"total": 0, "correct": 0, "accuracy": 0.0})
    number_of_parameters: dict = field(
        default_factory=lambda: {"total": 0, "correct": 0, "accuracy": 0.0})
    number_of_answers: dict = field(
        default_factory=lambda: {"total": 0, "correct": 0, "accuracy": 0.0})
    number_of_tokens: dict = field(
        default_factory=lambda: {"input": 0, "output": 0})

    def update_functions(self, correct: int, total: int):
        self.number_of_functions["total"] += total
        self.number_of_functions["correct"] += correct
        self.number_of_functions["accuracy"] = self.calculate_accuracy(
            self.number_of_functions["correct"], self.number_of_functions["total"])

    def update_parameters(self, correct: int, total: int):
        self.number_of_parameters["total"] += total
        self.number_of_parameters["correct"] += correct
        self.number_of_parameters["accuracy"] = self.calculate_accuracy(
            self.number_of_parameters["correct"], self.number_of_parameters["total"])

    def update_answers(self, correct: int):
        self.number_of_answers["total"] += 1
        self.number_of_answers["correct"] += correct
        self.number_of_answers["accuracy"] = self.calculate_accuracy(
            self.number_of_answers["correct"], self.number_of_answers["total"])

    def update_tokens(self, input_tokens: int, output_tokens: int):
        self.number_of_tokens["input"] += input_tokens
        self.number_of_tokens["output"] += output_tokens

    @staticmethod
    def calculate_accuracy(correct: int, total: int) -> float:
        return round(correct / total, 3) if total > 0 else 0.0


@dataclass
class QuestionResult:

    question_id: str
    category: str
    question: str
    motivation: str
    overall_match: bool
    correct_paths: List[Dict[str, Dict]]
    model_solution: ModelSolution
    correct_answer: str
    evaluation: Evaluation


@dataclass
class Run:
    metadata: Metadata
    statistics: Statistics
    question_result: List[QuestionResult]

    def to_dict(self):
        return to_dict(self)


class Pipeline:
    def __init__(self, question_set: dict, function_set: dict, config: dict, mode: str, api_key: str) -> None:

        self.question_set = question_set
        self.function_set = function_set
        self.config = config
        self.mode = mode

        self.llm_service = LLMService(
            function_set, config["prompt"], self.config["model"], config["hyperparameters"], mode, api_key)

        self.run: Run = None  # is readable from main

    @property
    def result(self) -> Run:
        return self.run

    def run_tests(self) -> None:
        metadata = Metadata(self.config["id"],
                            self.config["name"],
                            self.config["question_set"],
                            self.config["function_set"],
                            self.config["prompt"],
                            self.config["model"],
                            self.config["hyperparameters"])
        statistics = Statistics()
        results: List[QuestionResult] = []

        for question in tqdm(self.question_set["questions"], desc="Test Run", unit="Question"):

            # llm response
            model_solution, conversation = self.llm_service.process_question(
                question["question"])

            tokens_in, tokens_out = self.llm_service.get_tokens_from_conversation(
                conversation)

            # evaluation
            evaluation = Evaluator.get_overall_evaluation(model_solution, [Path(
                path["functions"], path["parameters"]) for path in question["target"]["solution_paths"]], question["target"]["expected_answer"])

            # statistics
            total_functions = evaluation.get_total_number_functions()
            total_parameters = evaluation.get_total_number_arguments()
            correct_functions = evaluation.get_num_correct_functions()
            correct_parameters = evaluation.get_num_correct_arguments()
            answer_correct = evaluation.get_answer_correct()

            statistics.update_functions(correct_functions, total_functions)
            statistics.update_parameters(correct_parameters, total_parameters)
            statistics.update_answers(int(answer_correct))
            statistics.update_tokens(tokens_in, tokens_out)

            # result
            result = QuestionResult(question["id"],
                                    question["category"],
                                    question["question"],
                                    question["motivation"],
                                    evaluation.get_overall_match(),
                                    question["target"]["solution_paths"],
                                    model_solution,
                                    question["target"]["expected_answer"],
                                    evaluation)
            results.append(result)

        metadata.update_endtime()
        self.run = Run(metadata, statistics, results)
