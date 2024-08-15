from openai import OpenAI

def prompt(cortellis, inxight):
    return f"You are an expert on disease names, return yes if these two refer to the same disease, no otherwise: {cortellis}, {inxight}"

client = OpenAI()

def response(cortellis, inxight):
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt(cortellis, inxight)}],
        stream=True,
    )

    response_content = []

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            response_content.append(chunk.choices[0].delta.content)

    return ''.join(response_content)
