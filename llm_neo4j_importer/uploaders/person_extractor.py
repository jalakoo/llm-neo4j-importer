# from langchain_community.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from .llm_manager import LLM
import logging

def get_entities(text: str) -> list[str]:

    # Using langchain GPT4All example
    template = """
            Given a prompt, extrapolate the most important Relationships.

            Each Relationship must connect 2 Entities represented as an item list like ["ENTITY 1", "RELATIONSHIP", "ENTITY 2"]. The Relationship is directed, so the order matters.

            Use singular nouns for Entities.

            For example; the prompt: `All birds like to eat seeds` should return: ["Bird", "EATS", "Seed"]

            Limit the list to a maximum of 12 relationships. Prioritize item lists with Entities in multiple item lists. Remove duplicate entries.

            prompt: {question}
            """
    prompt = PromptTemplate.from_template(template)
    llm_chain = LLMChain(prompt=prompt, llm=LLM)
    result = llm_chain.invoke(text)

    # final_text = f"""
    #         Given a prompt, extrapolate the most important Relationships.

    #         Each Relationship must connect 2 Entities represented as an item list like ["ENTITY 1", "RELATIONSHIP", "ENTITY 2"]. The Relationship is directed, so the order matters.

    #         Use singular nouns for Entities.

    #         For example; the prompt: `All birds like to eat seeds` should return: ["Bird", "EATS", "Seed"]

    #         Limit the list to a maximum of 12 relationships. Prioritize item lists with Entities in multiple item lists. Remove duplicate entries.

    #         prompt: {text}
    #         """
    
    # result = LLM.generate(text)

    print(f'Entity triples generated: {result}')
    logging.info(f'Entity triples generated: {result}')
    
    # Process strings if result was as expected - removing topics: header if not
    # tags = [x.strip().replace("topics: ","").replace("topics:","").lower() for x in result.content.split(",")]

    cleaned = result

    # Process strings if result came back as a numbered list
    # cleaned = []
    # for tag in tags:
    #     for item in tag.split("."):
    #         cleaned.append(item.strip().lstrip("0123456789"))

    return cleaned

