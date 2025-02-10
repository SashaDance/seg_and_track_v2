from pydantic import BaseModel


class FileUploaderResponse(BaseModel):
    file_id: str
