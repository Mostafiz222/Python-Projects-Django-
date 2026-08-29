from fastapi import FastAPI, Request, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import shutil

from app.inference import count_coins


app = FastAPI()


app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)


app.mount(
    "/outputs",
    StaticFiles(directory="outputs"),
    name="outputs"
)


templates = Jinja2Templates(
    directory="templates"
)



@app.get("/")
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )



@app.post("/upload")
def upload_image(
    request: Request,
    file: UploadFile = File(...)
):

    file_location = f"uploads/{file.filename}"


    with open(file_location, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )


    result = count_coins(
        file_location
    )


    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={

            "image_path":
                f"/uploads/{file.filename}",

            "result_image":
                "/outputs/result.jpg",

            "filename":
                file.filename,

            "coin_count":
                result["count"]
        }
    )