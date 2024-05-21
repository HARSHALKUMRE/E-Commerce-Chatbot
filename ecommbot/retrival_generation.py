from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.llms.bedrock import Bedrock
from ecommbot.ingest import ingestdata
import boto3

## bedrock client
bedrock = boto3.client(service_name="bedrock-runtime", region_name = "us-east-1")

def generation(vstore):
    retriever = vstore.as_retriever(search_kwargs={"k": 3})
    
    PRODUCT_BOT_TEMPLATE = """
    Your ecommercebot bot is an expert in product recommendations and customer queries.
    It analyzes product titles and reviews to provide accurate and helpful responses.
    Ensure your answers are relevant to the product context and refrain from straying off-topic.
    Your responses should be concise and informative.

    CONTEXT:
    {context}

    QUESTION: {question}

    YOUR ANSWER:
    
    """
    
    prompt = ChatPromptTemplate.from_template(PRODUCT_BOT_TEMPLATE)
    
    llm = Bedrock(model_id="meta.llama2-70b-chat-v1", client=bedrock,
                  model_kwargs={'max_gen_len':512})
    
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain


if __name__ == "__main__":
    vstore = ingestdata("done")
    chain = generation(vstore)
    print(chain.invoke("can you tell me the best bluetooth buds?"))