import os
import json
import threading
from dotenv import load_dotenv

from src.controller.server import FunctionServer
from src.controller.pipeline import Pipeline
from src.util.config_manager import ConfigManager


load_dotenv()
API_KEY = os.environ.get("API_KEY")
HOST = os.environ.get("HOST")
PORT = int(os.environ.get("PORT"))


def main():
    config, question_set, function_set = ConfigManager.load_data()
    output_path = ConfigManager.output_path()
    use_case = ConfigManager.get_use_case()

    server = FunctionServer(HOST, PORT, use_case, function_set)
    pipeline = Pipeline(question_set, function_set, config,
                        mode="sequential", api_key=API_KEY)

    t_server = threading.Thread(target=server.start)
    t_server.daemon = True
    t_server.name = "Server"

    t_pipeline = threading.Thread(target=pipeline.run_tests)
    t_pipeline.name = "Pipeline"

    t_pipeline.start()
    t_server.start()
    t_pipeline.join()

    with open(output_path, "w") as f:
        json.dump(pipeline.result.to_dict(), f)


if __name__ == "__main__":
    main()
