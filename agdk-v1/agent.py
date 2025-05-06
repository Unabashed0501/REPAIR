import os
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from litellm import completion

# Define a tool to analyze and fix code
def analyze_and_fix_code(code_snippet: str, bug_description: str) -> dict:
    prompt = f"Given this code:\n{code_snippet}\nAnd this bug: {bug_description}\nSuggest a one-line fix."
    response = completion(
        model="gemini-2.0-flash",  # Use a supported model
        api_key=os.getenv("GOOGLE_API_KEY"),
        messages=[{"role": "user", "content": prompt}],
    )
    report = response.choices[0].message.content
    print(f"Response: {report}")
    return {"status": "success", "report": report}

# Define the tool schema explicitly
# fix_code_tool = FunctionTool(
    # name="fix_code",
    # description="Analyzes a code snippet and suggests a one-line fix for a described bug.",
    # func=analyze_and_fix_code,
    # schema={
    #     "type": "function",
    #     "function": {
    #         "name": "fix_code",
    #         "description": "Suggests a one-line fix for a bug in a code snippet.",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {
    #                 "code_snippet": {
    #                     "type": "string",
    #                     "description": "The code snippet containing the bug."
    #                 },
    #                 "bug_description": {
    #                     "type": "string",
    #                     "description": "A description of the bug in the code."
    #                 }
    #             },
    #             "required": ["code_snippet", "bug_description"]
    #         }
        # }
    # }
# )

# Example SWE-Bench Lite bug
code = "def add(a, b): return a - b"
bug_desc = "Function subtracts instead of adding."

# Create the agent
root_agent = Agent(
    name="BugFixer",
    model="gemini-2.0-flash",  # Match the model used in completion
    instruction=(
        "You are a code analysis and bug fixing agent. "
        "Analyze code snippets and suggest fixes for bugs. "
        f"Given this code:\n{code}\nAnd this bug: {bug_desc}\nSuggest a one-line fix."
    ),
    # tools=[analyze_and_fix_code],
    # api_key=os.getenv("GOOGLE_API_KEY"),
)

# Run the agent
# try:
#     fix = root_agent.run(f"Fix this bug:\nCode: {code}\nBug: {bug_desc}")
#     print(f"Proposed fix: {fix}")
# except Exception as e:
#     print(f"Error running agent: {e}")