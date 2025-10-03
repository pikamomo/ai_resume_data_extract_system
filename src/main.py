from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List

from langchain.prompts import PromptTemplate
from langchain.chat_models import init_chat_model
from langchain.output_parsers import PydanticOutputParser
from langchain_community.document_loaders import PyPDFLoader

from dotenv import load_dotenv, find_dotenv
import os
import json
from models.resume import Resume

def main():

    load_dotenv(find_dotenv())
    api_key = os.getenv("OPENAI_API_KEY")

    resume_template = """
    You are an AI assistant tasked with extracting structured information from a resume.

    Only extract information that's present in the Resume class.

    Resume Context:
    {resume_text}
    """

    prompt_template = PromptTemplate(
        template=resume_template,
        input_variables=["resume_text"]
    )

    parser = PydanticOutputParser(pydantic_object=Resume)

    modle = init_chat_model(model = 'gpt-4o-mini', model_provider='openai').with_structured_output(Resume, method="function_calling")

    file_path = os.path.join('resume', 'ResumeEx2.pdf')
    loader = PyPDFLoader(file_path)

    docs = loader.load()

    resume_text = "\n".join([doc.page_content for doc in docs])

    promp = prompt_template.invoke({'resume_text': resume_text})
    response = modle.invoke(promp)

    result = response.model_dump()
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
