import requests
import argparse
from uuid import uuid4
from models.edu_prog import generate_fake_date_edu_prog, EduProg, EduProgJson
from models.up import generate_fake_date_up, Up, UpJson
from pydantic import ValidationError
import os
import glob

parse = argparse.ArgumentParser()
parse.add_argument('-schema', type=str, help="Выбор модели")
parse.add_argument('--size', type=int,
                   help="Количество объектов")

args = parse.parse_args()

if args.schema == "up":
    up_json = requests.get(f'http://localhost:8000/up?size={args.size}').json()
    uuid = uuid4()
    FOLDER = "ups"
    try:
        for up in up_json:
            Up.parse_obj(up)
        if not glob.glob(os.path.join(FOLDER, f'{uuid}*.json')):
            print("validation success")
            with open(os.path.join(FOLDER, f'{uuid}_up.json'), 'w') as f:
                f.write(UpJson(organization_id=uuid,
                        up=up_json).json(ensure_ascii=False))
        else:
            print(
                f"Файл с organization_id: {uuid} уже существует")
    except ValidationError as e:
        print(e.json())
        with open("logs.log", 'a') as f:
            f.write("\n" + e.json())

if args.schema == "edu_prog":
    edu_prog_json = requests.get(
        f'http://localhost:8000/edu_prog?size={args.size}').json()
    uuid = uuid4()
    FOLDER = "edu_progs"
    try:
        for ep in edu_prog_json:
            EduProg.parse_obj(ep)
        if not glob.glob(os.path.join(FOLDER, f'{uuid}*.json')):
            print("validation success")
            with open(os.path.join(FOLDER, f'{uuid}_edu_prog.json'), 'w') as f:
                f.write(EduProgJson(organization_id=uuid,
                        edu_prog=edu_prog_json).json(ensure_ascii=False))
        else:
            print(
                f"Файл с organization_id: {uuid} уже существует")

    except ValidationError as e:
        print(e.json())
        with open("logs.log", 'a') as f:
            f.write("\n" + e.json())
