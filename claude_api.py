import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

def query_to_claude(
        system_prompt, 
        message_contexts,
        max_tokens=1000,
        temperature=0,
        model_name="claude-3-sonnet-20240229",
):  
    message = client.messages.create(
        model=model_name,
        max_tokens=max_tokens,
        temperature=temperature,
        system=system_prompt,
        messages=message_contexts
    )  
    return message
