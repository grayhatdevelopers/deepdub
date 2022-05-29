from fastapi import FastAPI, File, UploadFile, Query, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from fastapi.responses import JSONResponse

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import os

@app.post("/files/")
async def create_file(file: bytes = File(..., description="A file read as bytes")):
    return {"file_size": len(file)}

## Import your model's inference function
# from <YOUR_MODEL_FOLDER> import <YOUR_MODELS_INFERENCE_FUNCTION> 

@app.post("/uploadfile/")
async def create_upload_file(
    file: UploadFile = File(..., description="A file sent by the frontend."),
):
    
    print("Received a file...", file.filename)
    print("File extension:", file.content_type)

    # Just adjusting the filename a bit so that it is easy to understand.
    runname = str(datetime.now()).replace(" ", "_").replace(":", "_").replace(".", "_") + "__" + file.filename
    filename = os.path.join("uploads", runname + ".webm")

    # Save uploaded file in server, just in case you want to check it out later
    async with aiofiles.open(filename, 'wb') as out_file:
        content = await file.read()  # async read
        await out_file.write(content)  # async write

    ## Pass the filename (or the raw file) to your model's inference function. return_data contains the
    ## data which your model would have generated.
    
    #return_data = <YOUR_MODELS_INFERENCE_FUNCTION>.(filename)
     
    # Just checking :)
    print("Return data is:", return_data)

    # Now prettify the data and send back
    return {
        "uploaded_filename": str(filename), 
        "return_data": str(return_data),
        }
