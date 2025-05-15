# REPAIR -- Real-time Error Patching using Agentic Intelligence & Retrieval

REPAIR is a **multi-agent** system designed to automatically identify and fix single-file, single-line bugs using large language models.

Built with the Google Agentic Development Kit (ADK) and powered by Gemini 2.0 Flash via the free Google AI Studio API, this project uses the **SWE-bench Lite** dataset as a benchmark for realistic software engineering bug-fixing tasks.

The system is composed of the following agents:

1. 🗂️ File Locator Agent
- Purpose: Identify and return the file(s) most relevant to a bug report.

- Inputs: 
  - `instance_id` (from the SWE-bench Lite dataset)
- Outputs:
  - `file_path`: the path to the relevant file
  - `file_contents`: the full contents of the file
  - `bug_descriptions`: a list of bug report descriptions

2. 🛠️ Patch Generator Agent
- Purpose: Generate a fix for the identified bug.

- Inputs:
  - `file_path`
  - `file_contents`
  - `bug_descriptions`

- Generate both:
  - `original`: the faulty code snippet
  - `replacement`: the fixed version

- Outputs:
  - `patch`: a unified diff string
  - `description`: a concise summary of the fix


## Environmental Setup
Create a `.env` file to include:
```
HF_TOKEN=<YOUR_HUGGINGFACE_TOKEN>
GOOGLE_API_KEY=<YOUR_GOOGLE_API_KEY>
```

And set up virtual environment to install required packages:
```
python3 -m venv repair-env     
source repair-env/bin/activate         
pip install -r requirements.txt
pip install -r agentless/requirements.txt    
```

## (Optional, already downloaded) Download SWE-Bench-Lite to csv
```
huggingface-cli login    
```
```
python SWE-Bench-Lite/get-dataset.py
```

## Run the pipeline of REPAIR:
1. Load the repo from **SWE-Bench-Lite** via `Agentless` file localization (it might take about 5~10 minutes depending on the wifi status):
```
python agentless/fl/localize.py --load_repo --num_threads 10 --skip_existing 
```
You would then pull the top 7 repos for simple demo. The number could be modified in the future.

2. (Optional, already implemented the top 7 dataset) Preprocess: Agentless

Please refer to 
[AGENTLESS README IN REPAIR](https://github.com/Unabashed0501/agdk-swe-fixer/tree/main/agentless#readme)

3. Run Bug Fixing Agent via Google Agentic Development Kit
```
adk web
```

You could access the web via [localhost:8080](http://0.0.0.0:8000/dev-ui?app=BugFixerAgent) by default, and please select **BugFixingAgent** to interact with the agent.

## 🚀 Project Demo

Here is a short demo of how the project works:

https://github.com/user-attachments/assets/2e66a0cc-a6cc-4e54-875f-010db96a50fd


## Reference
The `agentless` folder is referred to 
```bibtex
@article{agentless,
  author    = {Xia, Chunqiu Steven and Deng, Yinlin and Dunn, Soren and Zhang, Lingming},
  title     = {Agentless: Demystifying LLM-based Software Engineering Agents},
  year      = {2024},
  journal   = {arXiv preprint},

}
```

## Acknowledgement 

* [SWE-bench](https://www.swebench.com/)
* [Agentless](https://github.com/OpenAutoCoder/Agentless/tree/main)
