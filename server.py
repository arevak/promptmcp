import os
import json
import inspect
import re
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

mcp = FastMCP("My App")

def get_prompt_directory():
    """Get the prompt directory from environment variable or default to ~/.promptmcp"""
    env_prompt_dir = os.environ.get("PROMPT_MCP_DIR")
    if env_prompt_dir and os.path.isdir(env_prompt_dir):
        return env_prompt_dir
    
    # Default to ~/.promptmcp
    default_dir = os.path.join(Path.home(), ".promptmcp")
    # Create the directory if it doesn't exist
    if not os.path.exists(default_dir):
        os.makedirs(default_dir)
    
    return default_dir

def generate_prompts_from_directory(directory_path=None):
    """Dynamically generate MCP prompts from text and JSON files in a directory."""
    if directory_path is None:
        directory_path = get_prompt_directory()
    
    print(f"Loading prompts from: {directory_path}")
    
    # Check if directory exists
    if not os.path.exists(directory_path):
        print(f"Warning: Prompt directory not found at {directory_path}")
        return
    
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        generate_prompt_from_text(file_path)

def generate_prompt_from_text(file_path):
    """Generate a simple prompt function from a text file."""
    # Create a function name from the filename (remove extension and replace spaces)
    func_name = os.path.splitext(os.path.basename(file_path))[0].replace(" ", "_").lower()
    
    # Read the content from the file
    with open(file_path, "r") as file:
        template_content = file.read().strip()
    
    # Keep original template to extract placeholders
    raw_template = template_content
    
    # Extract placeholder variable names
    var_names = sorted(set(re.findall(r"{(\w+)}", raw_template)))
    if var_names:
        params = ", ".join(f"{name}: str" for name in var_names)
    else:
        params = "input_text: str"
    
    # Define and register the prompt function directly in this module's namespace
    func_def = f"""
@mcp.prompt()
def {func_name}({params}) -> str:
    return f"{template_content}"
"""
    exec(func_def, globals())
    print(f"Created text-based prompt function: {func_name}")

generate_prompts_from_directory()

@mcp.prompt()
def test(a1: str, a2: str) -> str:
    return f"a1: {a1} a2: {a2}"