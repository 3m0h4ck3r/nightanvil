import os
def generate_gig_description(title, bullets=3):
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        return f"{title}\n\nI will craft an elite {title}. Key points:\n- Fast delivery\n- High-quality\n- Revisions included"
    return "[AI placeholder — enable OPENAI_API_KEY for real completions]"
