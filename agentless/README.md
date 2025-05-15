## 🐈 Setup

First create the environment 

```shell
git clone https://github.com/OpenAutoCoder/Agentless.git
cd Agentless

conda create -n agentless python=3.11 
conda activate agentless
pip install -r requirements.txt
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

Then export your OpenAI API key 
```shell
export OPENAI_API_KEY={key_here}
```

Create the folder to save our results
```shell
mkdir results # where we will save our results
```

> [!TIP]
> 
> We currently support SWE-Bench Lite and SWE-Bench Verified benchmarks, you can use `--dataset` to select the benchmark (by default it will be SWE-Bench Lite)
> 
> For example `--dataset=princeton-nlp/SWE-bench_Verified`

> [!TIP]
> 
> Since for each issue in the benchmark (both SWE-Bench Lite and SWE-Bench Verified) we need to checkout the repository and process the files, you might want to save some time by downloading the preprocessed data here: [swebench_lite_repo_structure.zip](https://github.com/OpenAutoCoder/Agentless/releases/tag/v1.5.0)
>
> After downloading, please unzip and export the location as such `export PROJECT_FILE_LOC={folder which you saved}`

> [!TIP]
> 
> You can use `--target_id` to specific a particular bug you want to target. 
> 
> For example `--target_id=django__django-10914`

> [!TIP]
> 
> We use multiple threads (controllable via `--num_threads`) to speed up the Agentless process 

## 🙀 Localization 

In localization, the goal is to find the locations in source code where we need to edit to fix the issues. 
At a high-level, **Agentless** uses a 3-stage localization step to first localize to specific files, then to relevant code elements, and finally to fine-grained edit locations. 
We will now take you through the step-by-step procedure of Agentless in each of the localization steps.

#### 1. Localize to suspicious files

First, we localize to suspicious files. This is done in a multi-step process where we combine both LLM localized files with retrieval files.

Run the following command to generate the LLM-predicted suspicious files:

```shell
python agentless/fl/localize.py --file_level \
                                --output_folder results/swe-bench-lite/file_level \
                                --num_threads 10 \
                                --skip_existing 
```

This will save all the LLM-predicted suspicious file locations in  `results/swe-bench-lite/file_level/loc_outputs.jsonl` with the logs saved in `results/swe-bench-lite/file_level/localization_logs`

We then complement the previous suspicious files with a simple embedding-based retrieval method to identify additional suspicious files.

This is done by first filtering out irrelevant folders by using LLM to produce a list of irrelevant folders that do not need to be retrieved from with the following command:

```shell
python agentless/fl/localize.py --file_level \
                                --irrelevant \
                                --output_folder results/swe-bench-lite/file_level_irrelevant \
                                --num_threads 10 \
                                --skip_existing 
```

This will save the identified irrelevant folders in `results/swe-bench-lite/file_level_irrelevant/loc_outputs.jsonl` with the logs saved in `results/swe-bench-lite/file_level_irrelevant/localization_logs`

We then perform the retrieval (note the embedding is done with OpenAI `text-embedding-3-small` model) by passing in the irrelevant folders and running the following command: 

```shell
python agentless/fl/retrieve.py --index_type simple \
                                --filter_type given_files \
                                --filter_file results/swe-bench-lite/file_level_irrelevant/loc_outputs.jsonl \
                                --output_folder results/swe-bench-lite/retrievel_embedding \
                                --persist_dir agentless/embedding/swe-bench_simple \
                                --num_threads 10 
```

This will save the retrieved files in `results/swe-bench-lite/retrievel_embedding/retrieve_locs.jsonl` with the logs saved in `results/swe-bench-lite/retrievel_embedding/retrieval_logs`

Finally we merge the LLM-predicted suspicious file locations with the embedding-based retrieved files to obtain a final list of relevant files:

```shell
python agentless/fl/combine.py  --retrieval_loc_file results/swe-bench-lite/retrievel_embedding/retrieve_locs.jsonl \
                                --model_loc_file results/swe-bench-lite/file_level/loc_outputs.jsonl \
                                --top_n 3 \
                                --output_folder results/swe-bench-lite/file_level_combined 
```

`results/swe-bench-lite/file_level_combined/combined_locs.jsonl` contains the final list of suspicious files identified by Agentless.

#### 2. localize to related elements

Next, we move on to localizing the related elements.

Run the following command to provide the suspicious files from the first stage as input:

```shell
python agentless/fl/localize.py --related_level \
                                --output_folder results/swe-bench-lite/related_elements \
                                --top_n 3 \
                                --compress_assign \
                                --compress \
                                --start_file results/swe-bench-lite/file_level_combined/combined_locs.jsonl \
                                --num_threads 10 \
                                --skip_existing 
```

This will save the related elements in `results/swe-bench-lite/related_elements/loc_outputs.jsonl` with the logs saved in `results/swe-bench-lite/related_elements/localization_logs`

#### 3. localize to edit locations

Finally, using the related elements, we then localize to the edit locations. This is done via sampling to obtain multiple different sets of edit locations:


```shell
python agentless/fl/localize.py --fine_grain_line_level \
                                --output_folder results/swe-bench-lite/edit_location_samples \
                                --top_n 3 \
                                --compress \
                                --temperature 0.8 \
                                --num_samples 4 \
                                --start_file results/swe-bench-lite/related_elements/loc_outputs.jsonl \
                                --num_threads 10 \
                                --skip_existing 
```

This will save the edit locations in `results/swe-bench-lite/edit_location_samples/loc_outputs.jsonl` with the logs saved in `results/swe-bench-lite/edit_location_samples/localization_logs`

<details><summary>⏬ Structure of `loc_outputs.jsonl` <i>:: click to expand ::</i> </summary>
<div>

- `instance_id`: task ID of the issue
- `found_files`: list of files localized by the model
- `additional_artifact_loc_file`: raw output of the model during file-level localization
- `file_traj`: trajectory of the model during file-level localization (e.g., \# of tokens)
- `found_related_locs`: dict of relevant code elements localized by the model
- `additional_artifact_loc_related`: raw output of the model during relevant-code-level localization 
- `related_loc_traj`: trajectory of the model during relevant-code-level localization
- `found_edit_locs`: dict of edit locations localized by the model
- `additional_artifact_loc_edit_location`: raw output of the model during edit-location-level localization 
- `edit_loc_traj`: trajectory of the model during edit-location-level localization

</div>
</details>

Run the following command to separate the individual sets of edit locations:

```shell
python agentless/fl/localize.py --merge \
                                --output_folder results/swe-bench-lite/edit_location_individual \
                                --top_n 3 \
                                --num_samples 4 \
                                --start_file results/swe-bench-lite/edit_location_samples/loc_outputs.jsonl 
```

The separate sets of edit locations can be found in `results/swe-bench-lite/edit_location_individual`. The location files will be named `loc_merged_{x}-{x}_outputs.jsonl` where `x` indicates the individual samples. For our experiments on SWE-bench, we will use all 4 sets of edit locations and perform repairs on them individually to generate 4 different repair runs.
