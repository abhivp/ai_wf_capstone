# ai_wf_capstone
 Coursera AI Workflow Project
 
 Note - Setup Python environment with required packages and folder structure by clone repository
 
 ## 1. Running the application
 
 python app.py
 
 Navigate to http://localhost:8080
 
 ## 2. Test application (Model, Logs, API)
 
 python run-tests.py
 
 ## 3. To run just the API or Models or Logs. Run respective commands
 
 python unittests/ApiTests.py   (Make sure app.py is run, for the APIs to be available)
 
 python unittests/ModelTests.py
 
 python unittests/LoggerTests.py
 
 ## 4. Train Models 
 
 python run-model-train
 
 ## 5. Project Artefacts Summary (Has a list of code and descriptions)
 
 ai_wf_capstone_summary.pptx
 
  
The following questions are being evaluated as part of the peer review submission:

## Are there unit tests for the API?

To test api (run api server), then run - python unittests/ApiTests.py

## Are there unit tests for the model?

Run - python unittests/ModelTests.py 

## Are there unit tests for the logging?

Run - python unittests/LoggerTests.py

## Can all of the unit tests be run with a single script and do all of the unit 1. tests pass?

Run - python run-tests.py

(Remember to run api server before using app.py, otherwise API tests will be skipped)

## Was there an attempt to isolate the read/write unit tests from production 1. models and logs?

Controlled by passing prefix. Testing produces log files as train-test.log, predict-test.log and production/training produces train-{YYYY}-{MM}.log, predict--{YYYY}-{MM}.log. Also, in logfiles the lineitems have the prefix to differentiate

## Does the API work as expected? For example, can you get predictions for a 1. specific country as well as for all countries combined?

start api by running: $ python app.py

open following url in browser: (Firstime may took a minute or two to load models)

http://localhost:8080/predict?country=united_kingdom&date=2019-05-05

http://localhost:8080/predict?country=all&date=2019-05-05


## Does the data ingestion exists as a function or script to facilitate 1. automation? 

data_ingestion.py is the data ingestion script to extract and load json input files. This can be developed further as required

## Were multiple models compared?

Please refer to compare_model_performance.ipynb notebook where different models are compared

## Did the EDA investigation use visualizations?

Please refer to ai_wf_eda_visuals.ipynb for visuals, as well as ai_wf_eda.py for EDA

## Is everything containerized within a working Docker image?

Build image from Dockerfile, requirements.txt

docker build -t ai_wf_ml_app .

docker image ls

run docker

docker run -d -p 8080:8080 ai_wf_ml_app

Issue below URL in the browser to test API

http://localhost:8080/predict?country=united_kingdom&date=2019-05-05


## Did they use a visualization to compare their model to the baseline model?

## Is there a mechanism to monitor performance?
