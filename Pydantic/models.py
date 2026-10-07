from pydantic import BaseModel, Field, field_validator, model_validator, computed_field, ConfigDict, EmailStr, AnyUrl
from datetime import date 
from typing import Optional, Literal

class Category(BaseModel):
    name : Literal["starter", "main course", "dessert", "beverage"]

class Model(BaseModel):
    model_config = ConfigDict(extra="allow",
                              frozen=True,
                              strict=True,  # when strict is True, it will not raise error, if False it passes the value like taking id = '9' as string
                              validate_assignment=True)

    id           : int
    name         : str = Field(..., min_length=3, max_length=50, description="Name of the item")
    price        : float = Field(..., gt=0, description="Price of the item")
    category     : Category
    is_available : bool = Field(default=True)
    description  : Optional[str] = None
    # email        : EmailStr
    # url          : AnyUrl
    # Date         : date


    # Field Validator
    @field_validator("name")
    @classmethod
    def title_name(cls, value):
        return value.title()

    # Model Validator
    @model_validator(mode="after")
    def check_available(self):
        if self.is_available and self.price <= 0:
            raise ("Available items must have a price greater than 0")
        return self

    # Computed Fields
    @computed_field
    @property
    def price_tax(self) -> float:
        return round(self.price * 1.05, 2)


item = Model(id=9, name="sAMOsa", price=10, category=Category(name='dessert'), spicy = "bohot zyada")

# Converts object into dictionary
print(item.model_dump())
print("\n")

# Converts object into JSON
print(item.model_dump_json(indent=4))


