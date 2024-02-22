class FunctionHandler:
    def __init__(self) -> None:
        self.__functions = []
        self.__functions_metadata = None
        
    def register_function(self, fcn:function) -> function:
        self.__functions.append(fcn)
        return fcn
    
    @property
    def available_functions(self):
        return self.__functions
    
    @property
    def available_functions_metadata(self):
        # 1. read in metadata if not done yet
        if self.__functions_metadata is None:
            ...
        
        # filter registered functions w.r.t. metadata
        self.__functions_metadata = ... 
        
        # return error message if some function was not found? 
        
        return self.__functions_metadata
        


# what about function execution error? => Pass to pipeline back & Define errors 

class FunctionNotFoundError(Exception):
    pass

class ArgumentNotFoundError(Exception):
    pass

class FunctionExecutionError(Exception):
    pass

