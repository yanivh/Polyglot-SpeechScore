from langchain.document_loaders import google_speech_to_text

def get_open_ai():

    set_api_key("OPENAI_API_KEY")
    llm = OpenAI(model='gpt-3.5-turbo-instruct', temperature=0)
    # llm = ChatOpenAI(model='gpt-4', temperature=0)
    embedding = OpenAIEmbeddings()

    return llm, embedding
