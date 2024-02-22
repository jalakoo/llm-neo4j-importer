from gpt4all import GPT4All
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain_community.llms import GPT4All
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from .secrets_manager import OPENAI_API_KEY
import os

# Using GPT4All
# local_gpt4all_path = (
#     # "mistral-7b-instruct-v0.1.Q4_0.gguf"
#     "gpt4all-falcon-newbpe-q4_0.gguf"
# )
# # Callbacks support token-wise streaming
# CALLBACKS = [StreamingStdOutCallbackHandler()]
# # Verbose is required to pass to the callback manager
# LLM = GPT4All(model=local_gpt4all_path, callbacks=CALLBACKS, verbose=True)
# EMBEDDINGS = GPT4AllEmbeddings()


# Using OpenAI
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
LLM = ChatOpenAI(temperature=0)
EMBEDDINGS = OpenAIEmbeddings()