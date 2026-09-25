from datetime import date
from pydantic import BaseModel, ConfigDict, model_validator

class BookingCreateSchema(BaseModel):
    room_id: int
    date_from: date
    date_to: date

    @model_validator(mode="after")
    def validate_dates(self):
        if self.date_from >= self.date_to:
            raise ValueError("Дата начала должна быть strictly раньше даты выезда")
        if self.date_from < date.today():
            raise ValueError("Нельзя забронировать дату в прошлом")
        return self

class BookingReadSchema(BaseModel):

    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int       # Цена за 1 ночь на момент брони
    total_cost: int  # Итоговая стоимость за все дни

    model_config = ConfigDict(from_attributes=True)



class BookingUpdateSchema(BaseModel):
    
    room_id: int
    date_from: date
    date_to: date

    @model_validator(mode="after")
    def validate_dates(self):
        if self.date_from >= self.date_to:
            raise ValueError("Дата начала должна быть strictly раньше даты выезда")
        if self.date_from < date.today():
            raise ValueError("Нельзя забронировать дату в прошлом")
        return self