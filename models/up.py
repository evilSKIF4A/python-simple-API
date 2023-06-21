from pydantic import BaseModel, root_validator
from uuid import UUID, uuid4
from typing import List
from faker import Faker
import random
import re as RegExp


Faker.seed(0)
fake = Faker(locale='ru_RU')


class Up(BaseModel):
    external_id: str
    title: str
    direction: str
    code_direction: str
    start_year: int
    end_year: int
    education_form: str
    educational_program: str

    @root_validator
    def validation(cls, values):
        external_id = values.get('external_id')
        title = values.get('title')
        direction = values.get('direction')
        code_direction = values.get('code_direction')
        start_year = values.get('start_year')
        end_year = values.get('end_year')
        education_form = values.get('education_form')
        educational_program = values.get('educational_program')
        if external_id == "":
            raise ValueError(
                "external_id не должен быть пустым")
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
        if education_form.upper() not in EDUCATION_FORM:
            raise ValueError(
                "Форма образования неверно ведена")
        if educational_program == "":
            raise ValueError(
                "educational_program не должен быть пустым")
        return values


class UpJson(BaseModel):
    organization_id: UUID
    up: List[Up]


EDUCATION_FORM = ['EXTRAMURAL', 'FULL_TIME', 'PART_TIME',
                  'SHORT_EXTRAMURAL', 'SHORT_FULL_TIME', 'EXTERNAL']


async def generate_fake_date_up():
    return eval(Up(
        external_id=str(uuid4()),
        title=fake.word(),
        direction=fake.word(),
        code_direction=fake.phone_number(),
        start_year=int(fake.date(pattern='%Y')),
        end_year=int(fake.date(pattern='%Y')),
        education_form=random.choice(EDUCATION_FORM),
        educational_program=str(uuid4())
    ).json(ensure_ascii=False))
