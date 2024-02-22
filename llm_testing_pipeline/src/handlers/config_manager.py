import os
import json

class ConfigManager:
    def __init__(self, test_config_path:str, question_path:str) -> None:
        with open(test_config_path, encoding="utf-8") as f:
            self.__config = json.load(f)
            
        with open(question_path, encoding="utf-8") as f:
            self.__runnable_sets = json.load(f)
              
        # with open(output_path, encoding="utf-8") as f:
        #     output = json.load(f)
    
    @property
    def config(self):
        return self.__config
    
    @property
    def question_sets(self):
        return self.__runnable_sets["questions"]
    
    @property
    def function_sets(self):
        return self.__runnable_sets["functions"]
    
    def update_output(self, question_result: dict):
        output_path = self.__config["output"]
        with open(output_path, encoding="utf-8") as f:
            output = json.load(f)
        
        # write question_result
        # update performance scores
        