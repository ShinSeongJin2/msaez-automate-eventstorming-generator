from pydantic import BaseModel

class BaseModelWithItem(BaseModel):
    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)
    
    def keys(self):
        return self.model_dump().keys()

    def items(self):
        return self.model_dump().items()