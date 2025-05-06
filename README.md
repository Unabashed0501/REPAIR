# agdk-swe-fixer
A bug-fixing agent using the Google Agentic Development Kit (AGDK) and the SWE-bench Lite dataset, focused on single-file, single-line bugs. This example builds a single-agent system that leverages the Google AI Studio free API Key for calling Gemini.

## Environmental Setup
```
python3 -m venv agdk-env     
source agdk-env/bin/activate         
pip install -r requirements.txt
```

## Download SWE-Bench-Lite to csv
```
huggingface-cli login    
```
```
python SWE-Bench-Lite/get-dataset.py
```

## Run agdk-swe-fixer
```
```