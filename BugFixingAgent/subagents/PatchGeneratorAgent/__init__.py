"""Patch Generator Agent: A subagent for generating patches to fix bugs in codebases.
This agent is responsible for creating patches based on bug locations and descriptions.
It uses a specialized LLM to generate precise code changes that address the identified issues.
"""

from .agent import patch_generator_agent
