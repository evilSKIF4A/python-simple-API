from pydantic import BaseModel, root_validator
from typing import List
from uuid import UUID
from faker import Faker
import re as RegExp

Faker.seed(0)
fake = Faker(locale='ru_RU')


class EduProg(BaseModel):
    external_id: str
    title: str
    direction: str
    code_direction: str
    start_year: int
    end_year: int

    @root_validator
    def validation(cls, values):
        external_id = values.get('external_id')
        title = values.get('title')
        direction = values.get('direction')
        code_direction = values.get('code_direction')
        start_year = values.get('start_year')
        end_year = values.get('end_year')
        if len(external_id) != 6:
            raise ValueError(
                "external_id не шестизначное число")
        if title == "":
            raise ValueError("title не должен быть пустым")
        if direction == "":
            raise ValueError(
                "direction не должен быть пустым")
        if not RegExp.match(r'\+?\d\s?\(?\d{3}\)?\s?\d{3}[\s|-]?\d{2}[\s|-]?\d{2}', code_direction):
            raise ValueError(
                'code_direction неверный формат телефона')
        if not str(start_year).isdigit():
            raise ValueError(
                "Начальный год должен быть числом")
        if not str(end_year).isdigit():
            raise ValueError(
                "Конечный год должен быть числом")
        return values


class EduProgJson(BaseModel):
    organization_id: UUID
    edu_prog: List[EduProg]


async def generate_fake_date_edu_prog():
    return eval(EduProg(
        external_id=str(fake.pyint(min_value=100_000, max_value=999_999)),
        title=fake.word(),
        direction=fake.word(),
        code_direction=fake.phone_number(),
        start_year=int(fake.date(pattern='%Y')),
        end_year=int(fake.date(pattern='%Y')),
    ).json(ensure_ascii=False))
