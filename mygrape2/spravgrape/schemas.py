from pydantic import BaseModel

class GrapeView(BaseModel):
    name: str
    alias: str
    naznach: str
    br_color: str
    frozen_re: str
    type_fl: str
    srok: str
    img_url: str

