from openai import OpenAI
import json
import logging

def get_entities(text: str) -> list[str]:

    # Using langchain GPT4All example
    template = """
    Given a prompt, extrapolate the most important Relationships. 

    Each Relationship must connect 2 Entities represented as an item list like ["ENTITY 1", "RELATIONSHIP", "ENTITY 2"]. The Relationship is directed, so the order matters.

    Use singular nouns for Entities.

    For example; the prompt: `All birds like to eat seeds` should return: ["Bird", "EATS", "Seed"]

    Prioritize item lists with Entities in multiple item lists. Remove duplicates.

    prompt:
            """
    input = template + text

    client = OpenAI()

    # Official chat completion doc: https://platform.openai.com/docs/api-reference/chat/create

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        # model="gpt-4",
        response_format={"type":"json_object"},
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to output JSON"},
            {"role": "user", "content": input}
            ]
    )

    # Print does a better job pretty printing outputs!
    # print(f'Completion: {completion}, type: {type(completion)}')

    try:
        result_string = completion.choices[0].message.content
        json_object = json.loads(result_string)
        # print(f'JSON parsed: {json_object}. type: {type(json_object)}')
        cleaned = json_object["relationships"]
    except Exception as e:
        logging.error(f"Error processing entity extraction from completion:{completion}")
        cleaned = []

    return cleaned

# Using new JSON response - this doesn't work well, always adds \n and whitespace at end
# def get_entities(text: str) -> list[str]:

#     # Using langchain GPT4All example
#     template = """
#             Given a prompt, extrapolate the most important Relationships.

#             Each Relationship must connect 2 Entities represented as a JSON object like 
#             {"from": "ENTITY 1", "type": "RELATIONSHIP", "to": "ENTITY 2"}
            
#             The Relationship is directed, so the order matters.
            
#             Use only singular nouns for Entities.

#             For example; the prompt: `All birds like to eat seeds` should return: {"from":"Bird", "type":"EATS", "to":"Seed}

#             Prioritize item lists with Entities in multiple item lists. Remove duplicate entries. Remove newlines, tabs and whitespaces from the answer.

#             prompt: 
#             """
#     input = template + text

#     client = OpenAI()

#     # Official chat completion doc: https://platform.openai.com/docs/api-reference/chat/create

#     completion = client.chat.completions.create(
#         model="gpt-3.5-turbo-1106", #json compatible model
#         response_format = { "type": "json_object" },
#         messages=[
#             {"role": "system", "content": "You are a data entity extraction expert"},
#             {"role": "user", "content": input}
#         ]
#     )

#     logging.debug(f'(l) Entity triples generated: {completion}')
#     try:
#         result = completion["choices"][0]["message"]["content"]
#         print(f'(p) Entity triples generated: {result}')
#         json_response = json.loads(result)
#         print(f'(p) json parsed: {json_response}')
#         cleaned = result
#     except Exception as e:
#         logging.error(f"Error processing entity extraction from completion:{completion}")
#         print(f'Error processing entity extraction from completion:{completion}')
#         return []

#     return cleaned

