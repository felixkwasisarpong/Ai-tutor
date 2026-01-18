from typing import TypedDict, Literal, Optional

class RagMetadata(TypedDict,total=False):
    course: str
    documents:str
    topic: Optional[str]
    source: Optional[str]

class RadChunk(TypedDict):
    text: str
    metadata: RagMetadata