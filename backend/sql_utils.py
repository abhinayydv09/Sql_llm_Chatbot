import re

def clean_sql(query: str) -> str:
    lines = query.strip().splitlines()
    cleaned_lines = [re.sub(r"\s+", " ", line.strip()) for line in lines if line.strip()]
    return "\n".join(cleaned_lines)
