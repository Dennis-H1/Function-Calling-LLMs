from src.config import ConfigManager
# from .src.config import ...
from src.api.function_server import FunctionServer

def start_pipeline():
    pass



if __name__ == "__main__":
    # read config data
    
    config = ConfigReader.read_config(CONFIG_F)
    # config stuff
    MODE = "parallel" #  "sequential"
    
    
    # start server
    server = FunctionServer.start()
    
    # start pipeline
    # pipeline = start_pipeline()