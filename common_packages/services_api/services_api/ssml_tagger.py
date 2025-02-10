from pydantic.v1 import BaseModel, Field
from langserve import RemoteRunnable
from langchain.output_parsers import PydanticOutputParser


class SSMLTaggerRequest(BaseModel):
    text: str = Field(None, alias="text")


class SSMLTaggerResponse(BaseModel):
    text: str = Field(None, alias="text")


model = RemoteRunnable("http://ssml_tagger:8000")
chain = model | PydanticOutputParser(pydantic_object=SSMLTaggerResponse)
