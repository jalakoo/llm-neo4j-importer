
from .langchain_youtube import is_youtube_url, upload_url

def extract_urls(text:str)->list[str]:
    x = text.split()
    res = []
    for i in x:
        if i.startswith("https:") or i.startswith("http:"):
            res.append(i)
    return res

# def webpage_description(url) -> str:

# TODO: Take any url string and either pull down a .pdf or summarize a given webpage content
def dynamic_summary(url:str)->str:
    # TODO: File download?
    # TODO: Webpage summary?
    # TODO: Youtube video?
    # TODO: Image file?

    pass