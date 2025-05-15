from google.adk.agents import Agent, SequentialAgent

from .subagents.FileLocatorAgent import file_locator_agent
from .subagents.PatchGeneratorAgent import patch_generator_agent

# Create the agent -> Sequential agent
root_agent = SequentialAgent(
# root_agent = Agent(
    name="BugFixingAgent",
    description="A pipeline that coordinates the bug-fixing process by delegating tasks to specialized agents.",
    # model="gemini-2.0-flash",  # Match the model used in completion
    # instruction=("""You are a Main Coordination Agent responsible for managing the bug-fixing process by delegating tasks to specialized agents.
    #     Your objective is to fix a bug associated with a given instance ID by coordinating the following agents:

    #     1. File Locator Agent
    #     - Use this agent to retrieve:
    #         - The relevant file path
    #         - The full contents of the file
    #         - The bug description(s) related to the instance ID

    #     2. Patch Generator Agent 
    #     - Provide this agent with:
    #         - File path
    #         - File contents
    #         - Bug description(s)
    #     - This agent will:
    #         - Identify the buggy code snippet
    #         - Return a JSON object with:
    #         - `patch`: the diff showing the code change
    #         - `description`: a concise explanation of the fix

    #     Your responsibilities:

    #     - Begin by calling the **File Locator Agent** to retrieve:
    #         - `file_path`: the path to the relevant file
    #         - `file_contents`: the complete contents of the file
    #         - `bug_descriptions`: the description(s) of the bug from the report

    #     - Once you receive this data, pass it as input to the **Patch Generator Agent** (the bug-fixing agent). This agent will:
    #         - Identify the buggy code snippet
    #         - Generate a corrected version (`original` and `replacement`)
    #         - Use the `generate_patch` tool to create a unified diff

    #     - Wait for the response from the Patch Generator Agent.

    #     - Finally, return the output containing:
    #     - `patch`: the diff showing the code change
    #     - `description`: a concise explanation of the fix
        
    #     📝 Notes:
    #     - Be precise and efficient when delegating tasks.
    #     - Maintain this strict order of operations: **File Locator Agent → Patch Generator Agent**.
    #     - Do not proceed to patch generation until the necessary context has been retrieved.
    #     - Your final output should be the JSON object returned by the Bug-Fixing Agent.
        
    #     This coordination ensures a clear, step-by-step bug resolution process.
    # """
    #     # State: original, replacement, patch, description
    # ),
    sub_agents=[file_locator_agent, patch_generator_agent],
    # tools=[file_locator, get_problem_statement, generate_patch, save_to_json],
    # output_key="bug_fix_output",
)


# The Response I got:
# {
#   "original": "        cright = _coord_matrix(right, \'right\', noutp)\n    else:\n        cright = np.zeros((noutp, right.shape[1]))\n        cright[-right.shape[0]:, -right.shape[1]:] = 1",
#   "replacement": "        cright = _coord_matrix(right, \'right\', noutp)\n    else:\n        cright = np.zeros((noutp, right.shape[1]))\n        cright[-right.shape[0]:, -right.shape[1]:] = right",
#   "diff": "--- original\n+++ replacement\n@@ -1,4 +1,4 @@\n         cright = _coord_matrix(right, 'right', noutp)\n     else:\n         cright = np.zeros((noutp, right.shape[1]))\n-        cright[-right.shape[0]:, -right.shape[1]:] = 1\n+        cright[-right.shape[0]:, -right.shape[1]:] = right",
#   "description": "Fixed the `_cstack` function to correctly handle the `right` argument when it's a `Model` by assigning `right` instead of `1` to the corresponding slice of the `cright` matrix. This ensures that the separability matrix is correctly calculated for nested `CompoundModel` instances."
# }

# Pipeline:
# Agentless get all swe bench lite file structure
# Bug Fixer Agent to get the bug description and fix the code
# then save it to a json file or state

# Input (from SWE-bench Lite + Agentless):
# - Bug description
# - File path and buggy line
# - Line number
# - (Optional) File context

# Output:
# - Replacement line
# - Unified diff / patch
# - Explanation/rationale
# - (Optional) score from tests/validation


# [done] tool: file_locator to get the file path given the repo and issue information
# [done] agent: get the corrected code/function 
# [done] post_process: use the diff tool to get the diff and save/add as json

# [] combine file loc
# [] filter the found files and test files
# [] generate the test patch
# Save the reponse to a JSON file

# [] RAG to get the swe bench lite context from the csv
# instead of generating by one instance_id, generate by all instance_ids in the swe bench lite