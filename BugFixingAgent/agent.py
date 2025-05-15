from google.adk.agents import SequentialAgent

from .subagents.FileLocatorAgent import file_locator_agent
from .subagents.PatchGeneratorAgent import patch_generator_agent

# Create the Sequential agent
root_agent = SequentialAgent(
    name="BugFixingAgent",
    description="A pipeline that coordinates the bug-fixing process by delegating tasks to specialized agents.",
    sub_agents=[file_locator_agent, patch_generator_agent],
)
