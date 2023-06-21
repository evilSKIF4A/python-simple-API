from fastapi import FastAPI, Response
import requests
from models.edu_prog import generate_fake_date_edu_prog, EduProg, EduProgJson
from models.up import generate_fake_date_up, Up, UpJson
from pydantic import ValidationError
import os
import glob


app = FastAPI()


@app.get('/edu_prog')
async def get_edu_prog(size: int):
    res = []
    for i in range(size):
        res.append(await generate_fake_date_edu_prog())
    return res


@app.get('/up')
async def get_up(size: int):
    res = []
    for i in range(size):
        res.append(await generate_fake_date_up())
    return res


@app.post('/edu_prog')
async def post_edu_prog(edu_prog_json: EduProgJson):
    # res = requests.get("http://localhost:8000/edu_prog?size=5")
    FOLDER = "edu_progs"
    try:
        for ep in edu_prog_json.edu_prog:
            EduProg.parse_obj(ep)
        if not glob.glob(os.path.join(FOLDER, f'{edu_prog_json.organization_id}*.json')):
            print("validation success")
            with open(os.path.join(FOLDER, f'{edu_prog_json.organization_id}_edu_prog.json'), 'w') as f:
                f.write(edu_prog_json.json(ensure_ascii=False))
            return Response(content=f'{edu_prog_json.organization_id}_edu_prog.json')
        else:
            return f"Файл с organization_id: {edu_prog_json.organization_id} уже существует"
    except ValidationError as e:
        print(e.json())
        with open("logs.log", 'a') as f:
            f.write("\n" + e.json())


@app.post('/up')
async def post_up(up_json: UpJson):
    FOLDER = "ups"
    try:
        for up in up_json.up:
            Up.parse_obj(up)
        if not glob.glob(os.path.join(FOLDER, f'{up_json.organization_id}*.json')):
            print("validation success")
            with open(os.path.join(FOLDER, f'{up_json.organization_id}_up.json'), 'w') as f:
                f.write(up_json.json(ensure_ascii=False))
            return Response(content=f'{up_json.organization_id}_up.json')
        else:
            return f"Файл с organization_id: {up_json.organization_id} уже существует"
    except ValidationError as e:
        print(e.json())
        with open("logs.log", 'a') as f:
            f.write("\n" + e.json())


@app.get('/is_alive')
async def is_alive():
    return True
