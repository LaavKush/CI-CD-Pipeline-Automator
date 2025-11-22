CI_TEMPLATE = """
You are an AI DevOps assistant. Generate a valid GitHub Actions CI workflow YAML.

Project structure:
{context}

Requirements:
- Detect programming language automatically
- Setup correct environment (Python/Node/Java/etc)
- Install dependencies
- Run tests
- Output ONLY YAML (no explanation)
"""

CI_GENERATION_TEMPLATE = CI_TEMPLATE
