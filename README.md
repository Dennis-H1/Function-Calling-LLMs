# Team Project: Function Calling LLMs

### Introduction

Our project goal was to create a testing pipeline for benchmarking the accuracy of function-calling enabled Large Language Models (LLMs), such as GPT, across two key use cases: Music, and Travel (Airbnb & Restaurants). We focused on evaluating the models' performance in handling complex user queries involving multi-call functions, testing them with diverse prompts of varying complexity, and benchmarking their ability to execute function calls accurately, both sequentially and in parallel. This project aims to shed light on the strengths and limitations of these LLMs in real-world scenarios.

### Installation

1. Clone the repo: git clone https://github.com/Dennis-H1/Function-Calling-LLMs.git

2. Switch into the _master_ branch

3. Optional: Create python virtual environment & activate it

4. Install dependencies: pip install requirements.txt

5. Set up the .env file with API_KEY=...

### Usage

##### Configuration

Before running any tests, we have to configure our benchmark pipeline. For that, navigate to the src > config folder.
There, you can see three JSON files. The question_sets JSON contains all the questions and expected solutions for both use cases.
The function_sets JSON contains all available functions grouped into function groups that provide all available functions and their descriptions to the test run.
Finally, the test_config JSON contains the run configuration. We expect you to make changes here. You can specify the model or hyperparameters to use, or
the function and question set that we are interested in testing.

Do not forget to configure your config.json file before starting the run.

##### Run

To run the project, execute: python main.py

https://github.com/Dennis-H1/Function-Calling-LLMs/assets/108003634/a3129cd3-0357-451f-870d-b5c1bf5e640e

### Features

- Evaluate the LLM on: 1. correctness of API calls, and 2. quality of LLM responses
- For two use cases: 1. Music and 2. Travel & Restaurants
- Automatic classification of question errors using a selection of empirically identified error categories

### License

This project is licensed under the MIT License.
