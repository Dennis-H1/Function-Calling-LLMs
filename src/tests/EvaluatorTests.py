import unittest
from src.service.evaluator import Evaluator, EvaluationCategory, Path


class EvaluatorTests(unittest.TestCase):
    def test_eval(self):

        model_solution_1 = ["top_streamed_songs", "songs_by_release_date"]
        model_solution_2 = ["top_streamed_songs"]
        model_solution_3 = []
        model_solution_4 = ["incorrect_function"]

        correct_paths_1 = [
            {
                "path_id": 1,
                "functions": ["top_streamed_songs", "songs_by_release_date"],
                "parameters": [
                    {"n": 5}, {"release_date": "2010"}
                ]
            }
        ]

        _, num_correct_functions, function_eval = Evaluator.eval_functions(
            model_solution_1, [Path(
                path["functions"], path["parameters"]) for path in correct_paths_1]
        )
        self.assertEqual(num_correct_functions, 2)
        self.assertEqual(function_eval,
                         EvaluationCategory.CORRECT)

        _, num_correct_functions, function_eval = Evaluator.eval_functions(
            model_solution_2, [Path(
                path["functions"], path["parameters"]) for path in correct_paths_1]
        )
        self.assertEqual(num_correct_functions, 1)
        self.assertEqual(function_eval,
                         EvaluationCategory.PARTIALLY_CORRECT)

        _, num_correct_functions, function_eval = Evaluator.eval_functions(
            model_solution_3, [Path(
                path["functions"], path["parameters"]) for path in correct_paths_1]
        )
        self.assertEqual(num_correct_functions, 0)
        self.assertEqual(function_eval,
                         EvaluationCategory.INCORRECT)

        _, num_correct_functions, function_eval = Evaluator.eval_functions(
            model_solution_4, [Path(
                path["functions"], path["parameters"]) for path in correct_paths_1]
        )
        self.assertEqual(num_correct_functions, 0)
        self.assertEqual(function_eval,
                         EvaluationCategory.INCORRECT)

    def test_eval2(self):

        model_solution_1 = ["top_streamed_songs", "songs_by_release_date"]
        model_solution_2 = ["top_streamed_songs"]
        model_solution_4 = ["incorrect_function"]

        correct_paths_2 = [
            {
                "path_id": 2,
                "functions": ["top_streamed_songs"],
                "parameters": [
                    {"n": 5}, {"release_date": "2010"}
                ]
            }
        ]

        _, num_correct_functions, function_eval = Evaluator.eval_functions(
            model_solution_1, [Path(
                path["functions"], path["parameters"]) for path in correct_paths_2]
        )
        self.assertEqual(num_correct_functions, 1)
        self.assertEqual(function_eval,
                         EvaluationCategory.PARTIALLY_CORRECT)

        _, num_correct_functions, function_eval = Evaluator.eval_functions(
            model_solution_2, [Path(
                path["functions"], path["parameters"]) for path in correct_paths_2]
        )
        self.assertEqual(num_correct_functions, 1)
        self.assertEqual(function_eval,
                         EvaluationCategory.CORRECT)

        _, num_correct_functions, function_eval = Evaluator.eval_functions(
            model_solution_4, [Path(
                path["functions"], path["parameters"]) for path in correct_paths_2]
        )
        self.assertEqual(num_correct_functions, 0)
        self.assertEqual(function_eval,
                         EvaluationCategory.INCORRECT)

    def test_eval3(self):

        model_solution_1 = ["top_streamed_songs", "songs_by_release_date"]
        model_solution_2 = ["top_streamed_songs"]
        model_solution_4 = ["incorrect_function"]
        correct_paths_3 = [
            {
                "path_id": 3,
                "functions": [],
                "parameters": [
                    {"n": 5}, {"release_date": "2010"}
                ]
            }
        ]

        _, num_correct_functions, function_eval = Evaluator.eval_functions(
            model_solution_1, [Path(
                path["functions"], path["parameters"]) for path in correct_paths_3]
        )
        self.assertEqual(num_correct_functions, 0)
        self.assertEqual(function_eval,
                         EvaluationCategory.INCORRECT)

        _, num_correct_functions, function_eval = Evaluator.eval_functions(
            model_solution_2, [Path(
                path["functions"], path["parameters"]) for path in correct_paths_3]
        )
        self.assertEqual(num_correct_functions, 0)
        self.assertEqual(function_eval,
                         EvaluationCategory.INCORRECT)

        _, num_correct_functions, function_eval = Evaluator.eval_functions(
            model_solution_4, [Path(
                path["functions"], path["parameters"]) for path in correct_paths_3]
        )
        self.assertEqual(num_correct_functions, 0)
        self.assertEqual(function_eval,
                         EvaluationCategory.INCORRECT)

    def test_eval4(self):
        model_solution_1 = ["top_streamed_songs", "songs_by_release_date"]
        model_solution_2 = ["top_streamed_songs"]
        model_solution_4 = ["incorrect_function"]
        correct_paths_5 = [
            {
                "path_id": 3,
                "functions": ["other_function_not_in_called"],
                "parameters": [
                    {"n": 5}, {"release_date": "2010"}
                ]
            }
        ]

        _, num_correct_functions, function_eval = Evaluator.eval_functions(
            model_solution_1, [Path(
                path["functions"], path["parameters"]) for path in correct_paths_5]
        )
        self.assertEqual(num_correct_functions, 0)
        self.assertEqual(function_eval,
                         EvaluationCategory.INCORRECT)

        _, num_correct_functions, function_eval = Evaluator.eval_functions(
            model_solution_2, [Path(
                path["functions"], path["parameters"]) for path in correct_paths_5]
        )
        self.assertEqual(num_correct_functions, 0)
        self.assertEqual(function_eval,
                         EvaluationCategory.INCORRECT)

        _, num_correct_functions, function_eval = Evaluator.eval_functions(
            model_solution_4, [Path(
                path["functions"], path["parameters"]) for path in correct_paths_5]
        )
        self.assertEqual(num_correct_functions, 0)
        self.assertEqual(function_eval,
                         EvaluationCategory.INCORRECT)

    def test_eval4(self):
        model_solution_1 = ["top_streamed_songs", "songs_by_release_date"]
        model_solution_4 = ["incorrect_function", "called"]
        correct_paths_5 = [
            {
                "path_id": 3,
                "functions": ["called"],
                "parameters": [
                    {"n": 5}, {"release_date": "2010"}
                ]
            }
        ]

        _, num_correct_functions, function_eval = Evaluator.eval_functions(
            model_solution_1, [Path(
                path["functions"], path["parameters"]) for path in correct_paths_5]
        )
        self.assertEqual(num_correct_functions, 0)
        self.assertEqual(function_eval,
                         EvaluationCategory.INCORRECT)

        _, num_correct_functions, function_eval = Evaluator.eval_functions(
            model_solution_4, [Path(
                path["functions"], path["parameters"]) for path in correct_paths_5]
        )
        self.assertEqual(num_correct_functions, 1)
        self.assertEqual(function_eval,
                         EvaluationCategory.PARTIALLY_CORRECT)

    def test_eval5(self):
        model_solution_1 = ["f1", "f2"]
        correct_paths_5 = [
            {
                "path_id": 3,
                "functions": ["called"],
                "parameters": [
                    {"n": 5}, {"release_date": "2010"}
                ]
            },
            {
                "path_id": 4,
                "functions": ["f1", "other"],
                "parameters": [
                    {"n": 5}, {"release_date": "2010"}
                ]
            }
        ]

        _, num_correct_functions, function_eval = Evaluator.eval_functions(
            model_solution_1, [Path(
                path["functions"], path["parameters"]) for path in correct_paths_5]
        )
        self.assertEqual(num_correct_functions, 1)
        self.assertEqual(function_eval,
                         EvaluationCategory.PARTIALLY_CORRECT)

    def test_eval6(self):
        model_solution_1 = ["f1", "f2"]
        correct_paths_5 = [
            {
                "path_id": 3,
                "functions": ["called"],
                "parameters": [
                    {"n": 5}
                ]
            },
            {
                "path_id": 4,
                "functions": ["called", "called"],
                "parameters": [
                    {"n": 5}, {"release_date": "2010"}
                ]
            }
        ]

        _, num_correct_functions, function_eval = Evaluator.eval_functions(
            model_solution_1, [Path(
                path["functions"], path["parameters"]) for path in correct_paths_5]
        )
        self.assertEqual(num_correct_functions, 0)
        self.assertEqual(function_eval,
                         EvaluationCategory.INCORRECT)

    def test_param(self):

        model_solution = {
            "parameters": [{"n": 10}]
        }

        gold_path = Path(functions=[], parameters=[
            {"n": 10},
            {"n": 20}
        ])
        start, end = 0, 1

        num_correct_arguments, argument_eval = Evaluator.eval_arguments(
            model_solution["parameters"],
            gold_path.parameters[start:end],
        )

        self.assertEqual(num_correct_arguments, 1)
        self.assertEqual(argument_eval, EvaluationCategory.CORRECT)

    def test_param2(self):
        model_solution = {
            "parameters": [{"test_param": [1, 2, 3, 4, 5]}]
        }

        gold_path = Path(functions=[], parameters=[
            {"n": [1, 2, 3, 4, 5]},
        ])

        gold_path2 = Path(functions=[], parameters=[
            {"test_param": [1, 2, 3, 4, 5]},
        ])

        gold_path3 = Path(functions=[], parameters=[
            {"test_param": [5, 4, 3, 2, 1]},
        ])

        start, end = 0, 1

        num_correct_arguments, argument_eval = Evaluator.eval_arguments(
            model_solution["parameters"],
            gold_path.parameters[start:end],
        )

        self.assertEqual(num_correct_arguments, 0)
        self.assertEqual(argument_eval, EvaluationCategory.INCORRECT)

        num_correct_arguments, argument_eval = Evaluator.eval_arguments(
            model_solution["parameters"],
            gold_path2.parameters[start:end],
        )

        self.assertEqual(num_correct_arguments, 1)
        self.assertEqual(argument_eval, EvaluationCategory.CORRECT)

        num_correct_arguments, argument_eval = Evaluator.eval_arguments(
            model_solution["parameters"],
            gold_path3.parameters[start:end],
        )

        self.assertEqual(num_correct_arguments, 1)
        self.assertEqual(argument_eval, EvaluationCategory.CORRECT)

    def test_param3(self):
        model_solution = {
            "parameters": [{"n": 1, "m": 2}]
        }

        gold_path = Path(functions=[], parameters=[
            {"n": 1, "m": 2},
        ])

        gold_path2 = Path(functions=[], parameters=[
            {"n": 1, "p": 2},
        ])

        gold_path3 = Path(functions=[], parameters=[
            {"n": 1, "m": 100},
        ])

        start, end = 0, 2

        num_correct_arguments, argument_eval = Evaluator.eval_arguments(
            model_solution["parameters"],
            gold_path.parameters[start:end],
        )
        self.assertEqual(num_correct_arguments, 2)
        self.assertEqual(argument_eval, EvaluationCategory.CORRECT)

        num_correct_arguments, argument_eval = Evaluator.eval_arguments(
            model_solution["parameters"],
            gold_path2.parameters[start:end],
        )
        self.assertEqual(num_correct_arguments, 1)
        self.assertEqual(argument_eval, EvaluationCategory.PARTIALLY_CORRECT)

        num_correct_arguments, argument_eval = Evaluator.eval_arguments(
            model_solution["parameters"],
            gold_path3.parameters[start:end],
        )
        self.assertEqual(num_correct_arguments, 1)
        self.assertEqual(argument_eval, EvaluationCategory.PARTIALLY_CORRECT)

    def test_param4(self):
        model_solution = {
            "parameters": [{"release_date": "2010"}]
        }

        gold_path = Path(
            functions=["top_streamed_songs", "songs_by_release_date"],
            parameters=[{"n": 5}, {"release_date": "2010"}],
        )

        start, end = 1, 2

        num_correct_arguments, argument_eval = Evaluator.eval_arguments(
            model_solution["parameters"],
            gold_path.parameters[start:end],
        )
        self.assertEqual(num_correct_arguments, 1)
        self.assertEqual(argument_eval, EvaluationCategory.CORRECT)


if __name__ == "__main__":
    unittest.main()
