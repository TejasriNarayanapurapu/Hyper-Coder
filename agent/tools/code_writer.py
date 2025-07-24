import openai
from agent.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generate_code_from_issue(issue_text: str, context_text: str) -> str:
    """
    Sends issue + context to OpenAI GPT-4 and returns generated code snippet.
    """
    prompt = f"""
You are an expert software engineer. Given the following GitHub issue and repository context, write or fix the code to solve the issue.

GitHub Issue:
{issue_text}

Repository Context:
{context_text}

Provide only the relevant code snippet or solution.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful coding assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=800,
        n=1
    )
    
    return response['choices'][0]['message']['content'].strip()

if __name__ == "__main__":
    example_issue = "The training script throws an error when loading data. Fix the bug."
    example_context = "The repo uses PyTorch and loads data using DataLoader from dataset.py."
    
    code = generate_code_from_issue(example_issue, example_context)
    print("Generated code:\n", code)
