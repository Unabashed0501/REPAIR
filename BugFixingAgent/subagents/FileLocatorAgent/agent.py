"""
File Locator Agent

This agent is responsible for locating files that contain bugs in the codebase.
"""

import csv
import json
import os
import subprocess
from google.adk.agents import LlmAgent

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

def file_locator(instance_id: str) -> str:
    """
    Locate the file path given the repository and issue information.
    
    Args:
        instance_id (str): The instance ID.
        
    Returns:
        file_path (str): The path of the found file.
        file_content (str): The content of the found file.
    """
    # repo = "astropy/astropy"
    # instance_id = "astropy__astropy-12907"
    # base_commit = "d16bfe05a744909de4b27f5875fe0d4ed41ce607"
    
    repo_name = instance_id.split("__")[0]
    found_edit_loc_files = {}
    found_files = []
    most_related_edit_file = ""
    most_related_edit_loc = ""
    
    found_edit_loc_file_outputs = "results/swe-bench-lite/edit_location_individual/loc_merged_0-0_outputs.jsonl"

    with open(found_edit_loc_file_outputs, "r", encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            if record.get("instance_id") == instance_id:
                found_edit_loc_files = record.get("found_edit_locs")
                found_files = list(found_edit_loc_files.keys())
                most_related_edit_file = next(iter(found_edit_loc_files))
                most_related_edit_loc = found_edit_loc_files[most_related_edit_file]
                break
            
    print(f"Most related edit file: {most_related_edit_file}")
    print(f"Most related edit loc: {most_related_edit_loc}")
                
    repo_path = f"playground/{instance_id}/{repo_name.split('/')[0]}/"
    
    file_contents = {}
    relative_path = most_related_edit_file

    if relative_path:
        full_path = os.path.join(repo_path, relative_path)
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                file_contents[relative_path] = f.read()
        except FileNotFoundError:
            print(f"File not found: {full_path}")
        except Exception as e:
            print(f"Error reading {full_path}: {e}")
       
    return {"file_path": most_related_edit_file, "file_contents": file_contents}

# file_locator_output = file_locator("astropy__astropy-14182")
# print(file_locator_output)

def get_bug_descriptions(instance_id: str) -> str:
    """
    Retrieve the bug descriptions for a given instance ID.
    
    Args:
        instance_id (str): The instance ID.
        
    Returns:
        str: The bug descriptions.
    """
    bug_descriptions = ""
    with open("SWE-Bench-Lite/swe_bench_lite_test.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("instance_id") == instance_id:
                bug_descriptions = row.get("problem_statement")
                break
        else:
            # If no matching instance_id is found, set bug_descriptions to an empty string
            print(f"No matching instance_id found for {instance_id}")
    return {"bug_descriptions": bug_descriptions}


def run_agentless(instance_id: str) -> str:
    """
    Run the agentless function to test the agent.
    """
    # Run python agentless/fl/localize.py --file_level \
        # --output_folder results/swe-bench-lite/file_level \
        # --num_threads 10 \
        # --skip_existing  --target_id astropy__astropy-12907
    try:
        print(
            f"Locating files for instance ID: {instance_id} via Agentless..."
        )
        subprocess.run(
            [
                "python",
                "agentless/fl/localize.py",
                "--file_level",
                "--output_folder",
                "results/swe-bench-lite/file_level",
                "--num_threads",
                "10",
                "--skip_existing",
                "--target_id",
                instance_id,
            ],
            check=True,
        )
        return {"status": "success", "message": "File localization completed successfully."}
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the agentless command: {e}")
        return {"status": "error", "message": str(e)}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


# Create the scorer agent
file_locator_agent = LlmAgent(
    name="FileLocatorAgent",
    model=GEMINI_MODEL,
    instruction="""You are a File Locator AI Agent.

        Your task is to identify and return the file(s) in the codebase that are relevant to a given bug report.

        You will be provided with an `instance ID` corresponding to a specific bug report.

        Follow these steps:

        1. Use the `file_locator` tool to retrieve the relevant file path and its contents.
        2. Use the `get_bug_descriptions` tool to retrieve the bug description(s) for the instance.
        3. Determine which file and it corresponding contents that most likely contain the reported bug.
        4. Return the file information in the following format:

        Format:
        "Here is the most relevant file that contains the bug:\n"
        "  File Path: <file_path>\n"
        "  Content: <file_contents>\n"
        "  Bug Descriptions: <bug_descriptions>\n"

        📝 Notes:
        - You may return more than one file if needed, but prioritize the most relevant one.
        - Ensure the file content is complete and not truncated.
        - Do not include explanations or commentary—only structured file and bug data.

        Your output will be passed to a patch generator agent, so it must be machine-readable and consistent.
    """,
    description="Locates files that contain bugs in the codebase.",
    tools=[file_locator, get_bug_descriptions],
    output_key="file_locator_output",
)
