from agent.agent import run_agent

# Example input: read issue
print(run_agent("openai/gpt-2 1"))

# Example: read README
print(run_agent("read GitHub README openai/gpt-2"))

# Example: Generate code
issue = "Fix the bug in training.py where loading data fails."
context = "This repo uses PyTorch and loads data with DataLoader."
print(run_agent(f"{issue} ||| {context}"))
