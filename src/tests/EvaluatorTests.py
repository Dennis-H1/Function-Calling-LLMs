import unittest
from src.service.evaluator import Evaluator, EvaluationCategory


class EvaluatorTests(unittest.TestCase):

    # Description of the eval_functions algorithm:
    # for each path:
    #   for each (function in called, function in path): do fcn by fcn check for both lists...
    #   if no match: Incorrect
    #   if any match: Partially Correct
    #   if all match: Correct
    # Among all processed paths: select the path that has the most matches

    def test_eval_functions_single_paths_different_lenghts(self):

        path1 = [
            {
                "path_id": 1,
                "functions": [],
                "parameters": []
            }
        ]

        path2 = [
            {
                "path_id": 1,
                "functions": ["top_rated_albums"],
                "parameters": [{}]
            }
        ]

        path3 = [
            {
                "path_id": 1,
                "functions": ["top_rated_albums", "albums_by_artist", "top_streamed_albums"],
                "parameters": [{}, {}, {}]
            }
        ]

        path4 = [
            {
                "path_id": 1,
                "functions": ["albums_by_release_date",
                              "albums_by_release_date"],
                "parameters": [{}, {}]
            }
        ]

        path5 = [
            {
                "path_id": 1,
                "functions": ["albums_by_release_date", "albums_by_artist", "top_streamed_songs", "songs_by_artist"],
                "parameters": [{}, {}, {}, {}]
            }
        ]

        called1 = []
        called2 = ["top_rated_albums"]
        called3 = ["top_rated_albums",
                   "albums_by_artist", "top_streamed_albums"]
        called4 = ["albums_by_release_date",
                   "albums_by_release_date"]
        called5 = ["albums_by_release_date", "albums_by_artist",
                   "top_streamed_songs", "songs_by_artist"]

        self.assertEqual((0, EvaluationCategory.INCORRECT),
                         Evaluator.eval_functions(called1, path1))  # Exception Case (never reached in production)
        self.assertEqual((1, EvaluationCategory.CORRECT),
                         Evaluator.eval_functions(called2, path2))
        self.assertEqual((3, EvaluationCategory.CORRECT),
                         Evaluator.eval_functions(called3, path3))
        self.assertEqual((2, EvaluationCategory.CORRECT),
                         Evaluator.eval_functions(called4, path4))
        self.assertEqual((4, EvaluationCategory.CORRECT),
                         Evaluator.eval_functions(called5, path5))

    def test_eval_functions_single_paths_different_order(self):
        path1 = [
            {
                "path_id": 1,
                "functions": ["top_rated_albums", "albums_by_artist"],
                "parameters": [{}, {}]
            }
        ]

        path2 = [
            {
                "path_id": 1,
                "functions": ["top_rated_albums", "albums_by_artist", "albums_by_artist"],
                "parameters": [{}, {}, {}]
            }
        ]

        path3 = [
            {
                "path_id": 1,
                "functions": ["top_rated_albums", "albums_by_artist", "albums_by_artist", "albums_by_artist", "albums_by_artist"],
                "parameters": [{}, {}, {}, {}, {}]
            }
        ]

        called1 = ["albums_by_artist", "top_rated_albums"]
        called2 = ["albums_by_artist", "top_rated_albums", "albums_by_artist"]
        called3 = ["albums_by_artist", "top_rated_albums",
                   "albums_by_artist", "albums_by_artist", "albums_by_artist"]

        self.assertEqual((0, EvaluationCategory.INCORRECT),
                         Evaluator.eval_functions(called1, path1))
        self.assertEqual((1, EvaluationCategory.PARTIALLY_CORRECT),
                         Evaluator.eval_functions(called2, path2))
        self.assertEqual((3, EvaluationCategory.PARTIALLY_CORRECT),
                         Evaluator.eval_functions(called3, path3))

    def test_eval_functions_multiple_paths_different_lengths(self):
        path1 = [
            {
                "path_id": 1,
                "functions": ["top_rated_albums", "top_rated_albums", "top_rated_albums", "top_rated_albums", "top_rated_albums"],
                "parameters": [{}]
            },
            {
                "path_id": 2,
                "functions": ["top_streamed_songs"],
                "parameters": [{}]
            }
        ]

        called1 = ["top_rated_albums"]

        self.assertEqual((1, EvaluationCategory.PARTIALLY_CORRECT),
                         Evaluator.eval_functions(called1, path1))

    def test_eval_functions_multiple_paths_different_order(self):

        path1 = [
            {
                "path_id": 1,
                "functions": ["top_rated_albums"],
                "parameters": [{}]
            },
            {
                "path_id": 2,
                "functions": ["top_streamed_songs"],
                "parameters": [{}]
            }
        ]

        path2 = [
            {
                "path_id": 1,
                "functions": ["top_rated_albums", "top_streamed_songs", "unique_songs", "albums_by_artist"],
                "parameters": [{}, {}, {}, {}]
            },
            {
                "path_id": 2,
                "functions": ["top_streamed_songs"],
                "parameters": [{}]
            }
        ]

        path3 = [
            {
                "path_id": 1,
                "functions": ["top_rated_albums", "top_streamed_songs", "unique_songs", "albums_by_artist"],
                "parameters": [{}, {}, {}, {}]
            },
            {
                "path_id": 2,
                "functions": ["songs_by_artist", "songs_by_artist", "songs_by_artist", "songs_by_artist"],
                "parameters": [{}]
            }
        ]

        called1 = ["top_rated_albums"]
        called2 = ["top_rated_albums", "top_streamed_songs",
                   "unique_songs", "albums_by_artist"]
        called3 = ["top_rated_albums", "songs_by_artist",
                   "songs_by_artist", "songs_by_artist"]

        self.assertEqual((1, EvaluationCategory.CORRECT),
                         Evaluator.eval_functions(called1, path1))
        self.assertEqual((4, EvaluationCategory.CORRECT),
                         Evaluator.eval_functions(called2, path2))
        self.assertEqual((3, EvaluationCategory.PARTIALLY_CORRECT),
                         Evaluator.eval_functions(called3, path3))

    # Description of the eval_arguments algorithm:
    # for each path:
    #   for each (paramterset in called, parameterset in path): compare their keys & values
    #   if no match: Incorrect (also if lists do not exactly contain all the items)
    #   if any match: Partially Correct if ANY key:value (parameter) pair matches
    #   if all match: Correct
    # Among all processed paths: select the path that has the most matches
    # If no matches at all for all paths: return the first path

    def test_eval_arguments_single_paths(self):
        path1 = [
            {
                "path_id": 1,
                "functions": ["top_rated_albums", "items_by_numbers"],
                "parameters": [{"n": 30}, {"items": [1, 2, 3, 4, 5], "k": 30}]
            }
        ]

        path2 = [
            {
                "path_id": 1,
                "functions": ["top_rated_albums"],
                "parameters": [{"items": [1, 2, 3, 4, 5, 6]}]
            }
        ]

        called1 = [{"n": 30}, {"items": [1, 2, 3, 4, 5], "k": 30}]
        called2 = [{"items": [1, 2, 3, 4, 5]}]

        self.assertEqual((3, EvaluationCategory.CORRECT),
                         Evaluator.eval_arguments(called1, path1))
        self.assertEqual((0, EvaluationCategory.INCORRECT),
                         Evaluator.eval_arguments(called2, path2))

    def test_eval_arguments_multiple_paths(self):
        path1 = [
            {
                "path_id": 1,
                "functions": ["top_rated_albums", "items_by_numbers"],
                "parameters": [{"items": [1, 2, 3, 4, 5]}, {"n": 30}]
            },
            {
                "path_id": 2,
                "functions": ["top_rated_albums", "items_by_numbers"],
                "parameters": [{"n": 30}, {"items": [1, 2, 3, 4, 5]}]
            }
        ]

        path2 = [
            {
                "path_id": 1,
                "functions": ["top_rated_albums", "items_by_numbers"],
                "parameters": [{"n": 30, "k": 999}]
            },
            {
                "path_id": 1,
                "functions": ["top_rated_albums", "items_by_numbers"],
                "parameters": [{"n": 30, "k": 1000}]
            }

        ]

        called1 = [{"n": 30}, {"items": [1, 2, 3, 4, 5]}]
        called2 = [{"n": 30, "k": 40}]

        self.assertEqual((2, EvaluationCategory.CORRECT),
                         Evaluator.eval_arguments(called1, path1))
        self.assertEqual((1, EvaluationCategory.PARTIALLY_CORRECT),
                         Evaluator.eval_arguments(called2, path2))

    def test_eval_functions(self):
        self.assertEqual()


if __name__ == "__main__":
    unittest.main()
