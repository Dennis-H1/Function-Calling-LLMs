import os
import threading

from dotenv import load_dotenv

from src.controller.server import FunctionServer
from src.controller.pipeline import Pipeline
from src.service.llm_service import GPTService
from src.util.protocols import LLMService
from src.util.config_manager import ConfigManager


load_dotenv()
API_KEY = os.environ.get("API_KEY")
HOST = os.environ.get("HOST") or "127.0.0.1"
PORT = os.environ.get("PORT") or 5000


def main():
    config, question_set, function_set = ConfigManager.load_data()
    output_path = ConfigManager.output_path()
    use_case = ConfigManager.get_use_case()

    print(
        f">> The Benchmark will be run on the {use_case.value} functions. <<")

    prompt = config["prompt"]
    model = config["model"]
    hp = config["hyperparameters"]

    # >>> UPDATE YOUR OWN LLM SERVICE HERE <<<
    llm_service: LLMService = GPTService(
        API_KEY, function_set, prompt, model, hp)
    # ----------------------------------------

    server = FunctionServer(HOST, PORT, use_case, function_set)
    pipeline = Pipeline(question_set, function_set,
                        config, llm_service, output_path)

    t_server = threading.Thread(target=server.start)
    t_server.daemon = True
    t_server.name = "Server"

    t_pipeline = threading.Thread(target=pipeline.run_tests)
    t_pipeline.name = "Pipeline"

    t_pipeline.start()
    t_server.start()
    t_pipeline.join()


if __name__ == "__main__":
    main()
