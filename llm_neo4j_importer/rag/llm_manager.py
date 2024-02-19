from gpt4all import GPT4All
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain_community.llms import GPT4All
from langchain.embeddings import GPT4AllEmbeddings
from langchain.prompts import PromptTemplate

local_gpt4all_path = (
    "mistral-7b-instruct-v0.1.Q4_0.gguf"  # replace with your desired local file path
)

# Callbacks support token-wise streaming
CALLBACKS = [StreamingStdOutCallbackHandler()]

# Verbose is required to pass to the callback manager
LLM = GPT4All(model=local_gpt4all_path, callbacks=CALLBACKS, verbose=True)

EMBEDDINGS = GPT4AllEmbeddings()