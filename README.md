# ai_wf_capstone
 Coursera AI Workflow Project
 
   1. Running the application
 
 python app.py
 
 Navigate to http://localhost:8080
 
 2. Test application (Model, Logs, API)
 
 python run-tests.py
 
  3. To run just the API or Models or Logs. Run respective commands
 
 python unittests/ApiTests.py   (Make sure app.py is run, for the APIs to be available)
 
 python unittests/ModelTests.py
 
 python LoggerTests.py
 
 4. Train Models 
 
 python run-model-train
 
 5. Project Artefacts Summary (Has a list of code and descriptions)
 
 ai_wf_capstone_summary.pptx
 
  
The following questions are being evaluated as part of the peer review submission:

1. Are there unit tests for the API?
1. Are there unit tests for the model?
1. Are there unit tests for the logging?
1. Can all of the unit tests be run with a single script and do all of the unit 1. tests pass?
1. Was there an attempt to isolate the read/write unit tests from production 1. models and logs?
1. Does the API work as expected? For example, can you get predictions for a 1. specific country as well as for all countries combined?
1. Does the data ingestion exists as a function or script to facilitate 1. automation? 
1. Were multiple models compared?
1. Did the EDA investigation use visualizations?
1. Is everything containerized within a working Docker image?
1. Did they use a visualization to compare their model to the baseline model?
1. Is there a mechanism to monitor performance?
