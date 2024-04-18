# Team Project: Benchmark for Function Calling LLMs

### Introduction

Our project goal was to create a testing pipeline for benchmarking the accuracy of function-calling enabled Large Language Models (LLMs), such as GPT, across two key use cases: Music, and Travel (Airbnb & Restaurants). We focused on evaluating the models' performance in handling complex user queries involving multi-call functions, testing them with diverse prompts of varying complexity, and benchmarking their ability to execute function calls accurately, both sequentially and in parallel. This project aims to shed light on the strengths and limitations of these LLMs in real-world scenarios.

## Installation

1. Clone the repo
```console
git clone https://github.com/Dennis-H1/Function-Calling-LLMs.git
```

2. Switch into the _master_ branch
```console
git checkout master
```

3. _Optional_: Create python virtual environment & activate it

```console
python -m virtualenv .venv
.venv\Scripts\activate
```

4. Install dependencies
```console
pip install -r requirements.txt
```

5. Set up the .env file
```python
API_KEY=...
PORT=...
HOST=...
```

## Usage

### Configuration

Before running any tests, we have to configure our benchmark pipeline. For that, navigate to the src > config folder. There, you can see three JSON files. 
The question_sets JSON contains all the questions and expected solutions for both use cases. The function_sets JSON contains all available functions grouped 
into function groups that provide all available functions and their descriptions to test the run. Finally, the test_config JSON contains the run configuration. 
We expect you to make changes here. You can specify the model or hyperparameters to use, or the function and question set that we are interested in testing.

#### config.json
Configure this file **before** running the benchmark to the appropriate function_set, question_set, hyperparameters, model, and much more.

- **ID**: Unique identifier for the configuration. __Important__: Must contain either 'music', 'travel', or 'restaurant' keyword to automatically detect the functions to be loaded.
- **Name**: Descriptive name of the benchmark configuration.
- **Description**: Provides a brief overview of the benchmark's purpose and scope.
- **Authors**: Lists the individuals who developed and authored the benchmark configuration.
- **License**: Indicates the type of license under which this benchmark configuration is released.
- **Model**: Specifies the version of the LLM that the benchmark is designed to test.
- **Hyperparameters**: Specifies the LLM hyperparameters.
- **Prompt**: Instructions that are fed to the LLM to guide its responses during the benchmark.
- **Function Set**: Identifies the set of functions used in the benchmark.
- **Question Set**: Denotes the specific set of questions that the benchmark will address.
- **Output File**: Specifies the file path where the results of the benchmark are stored.


#### question_set.jsom
The question set contains the questions that the LLM is tested on.

- **ID**: Serves as a unique identifier for the question set.
- **Name**: Provides a descriptive name.
- **Domain**: Indicates the domain of interest. Either music or travel/restaurants.
- **Description**: Describes the scope of the questions, which include challenges like record selection, interpretation, and reasoning, among others.
- **Authors**: Lists the creators of the question set.
- **License**: Specifies the licensing under which the question set is released.
- **Function Sets**: Identifies the specific function sets used to support the questions.
- **Questions**: Lists the individual questions.

#### function_set.json
The function set contains the functions that the LLM is allowed to call.

- **ID**: Uniquely identifies this function set within the broader benchmark.
- **Name**: Describes the function set as tailored to a specific use case e.g., Music with complex descriptions.
- **Domain**: Specifies the domain like Music and Travel/Restaurants.
- **Categories**: Classifies the functions under themes like handling all parameters, lacking examples, and simplicity in description.
- **Number of Functions**: States the total count of functions included.
- **Functions**: Lists the individual functions.

### Run

To run the project:
```console
python main.py
```

https://github.com/Dennis-H1/Function-Calling-LLMs/assets/108003634/a3129cd3-0357-451f-870d-b5c1bf5e640e

## Extend Benchmark with other LLMs

![image](https://github.com/Dennis-H1/Function-Calling-LLMs/assets/108003634/087fe12a-8668-4652-b4f1-beead6e28f6e)

## Features

- Evaluate the LLM on: 1. correctness of API calls, and 2. quality of LLM responses
- For two use cases: 1. Music and 2. Travel & Restaurants


## License

This project is licensed under the MIT License.
