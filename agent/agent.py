from langchain.agents import Tool, initialize_agent
from langchain.llms import OpenAI
from agent.tools.github_reader import get_github_issue, get_readme
from agent.tools.code_writer import generate_code_from_issue
from agent.config import OPENAI_API_KEY

# Initialize OpenAI LLM wrapper for LangChain
llm = OpenAI(openai_api_key=OPENAI_API_KEY, model_name="gpt-4", temperature=0)

# Define tool wrappers for LangChain

def read_issue_tool(input_text: str) -> str:
    """
    Expected input format: "owner/repo issue_number"
    Example: "openai/gpt-2 1"
    """
    try:
        repo_str, issue_number_str = input_text.strip().split()
        owner, repo = repo_str.split("/")
        issue_number = int(issue_number_str)
    except Exception as e:
        return f"Input format error: {e}. Use 'owner/repo issue_number'"

    issue = get_github_issue(owner, repo, issue_number)
    if "message" in issue and issue["message"] == "Not Found":
        return "Issue or repo not found."
    return issue.get("body", "No issue body found.")

def read_readme_tool(input_text: str) -> str:
    try:
        owner, repo = input_text.strip().split("/")
    except Exception as e:
        return f"Input format error: {e}. Use 'owner/repo'"

    readme_text = get_readme(owner, repo)
    return readme_text if readme_text else "README not found."

def write_code_tool(input_text: str) -> str:
    """
    Expects input as: issue_text ||| context_text
    """
    try:
        issue_text, context_text = input_text.split("|||")
    except Exception as e:
        return f"Input format error: {e}. Use 'issue_text ||| context_text'"

    return generate_code_from_issue(issue_text.strip(), context_text.strip())

# Define LangChain Tools

tools = [
    Tool(
        name="GitHub Issue Reader",
        func=read_issue_tool,
        description="Reads a GitHub issue body given 'owner/repo issue_number'"
    ),
    Tool(
        name="GitHub README Reader",
        func=read_readme_tool,
        description="Reads the README file given 'owner/repo'"
    ),
    Tool(
        name="Code Generator",
        func=write_code_tool,
        description="Generates code given issue text and repo context separated by '|||'"
    ),
]

# Initialize the agent

agent = initialize_agent(
    tools,
    llm,
    agent="zero-shot-react-description",
    verbose=True
)

# Function to run agent on input query

def run_agent(query: str):
    return agent.run(query)

