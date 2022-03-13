from fastapi import FastAPI, File, UploadFile, Query, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


from fastapi.responses import JSONResponse


import aiofiles
import asyncio

from datetime import datetime

app = FastAPI()

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/results", StaticFiles(directory="results"), name="results")


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import os
from pathlib import Path

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


import sys
stdout_backup = sys.stdout

import traceback

@app.post("/files/")
async def create_file(file: bytes = File(..., description="A file read as bytes")):
    return {"file_size": len(file)}

from deepdub import main 

@app.post("/uploadfile/")
async def create_upload_file(
    from_language: str = Form (...), 
    to_language: str = Form (...), 
    file: UploadFile = File(..., description="A file read as UploadFile"),
):
    sys.stdout = stdout_backup 
    
    print("Received a file...", file.filename)
    print("File extension:", file.content_type)

    print("From language:", from_language)
    print("To language:", to_language)

    runname = str(datetime.now()).replace(" ", "_").replace(":", "_").replace(".", "_") + "__" + file.filename
    
    filename = runname + ".webm"

    async with aiofiles.open("uploads/"+filename, 'wb') as out_file:
        content = await file.read()  # async read
        await out_file.write(content)  # async write


    uploads_folder_path = os.path.join(os.path.abspath(os.getcwd()), "uploads")
    results_folder_path = os.path.join(os.path.abspath(os.getcwd()), "results")    


    # Build the structure of results folder
    run_folder_path = os.path.join(results_folder_path, runname)
    os.mkdir(run_folder_path)

    extracted_folder_path = os.path.join(run_folder_path, "extracted")
    os.mkdir(extracted_folder_path)
    os.mkdir(os.path.join(extracted_folder_path, "audio"))
    os.mkdir(os.path.join(extracted_folder_path, "video"))
    
    translated_folder_path = os.path.join(run_folder_path, "translated")
    os.mkdir(translated_folder_path)
    os.mkdir(os.path.join(translated_folder_path, "audio"))
    os.mkdir(os.path.join(translated_folder_path, "video"))

    os.mkdir(os.path.join(run_folder_path, "metadata"))

    deepdub_path = "/home/saadbazaz/Projects/deepdub/deepdub_cli"
    #deepdub_path = "/Users/abdurrehmansubhani/Desktop/FYP/project_code.pptx/deepdub/deepdub_cli"

    deepdub_args = {
    "video": str(os.path.join(uploads_folder_path, filename)),
    "translation": None,
    "deepdubstart": "00:00:00",
    "deepdubend": None,
    "clipminlength": 0.1,
    "translation_language_source": from_language,
    "translation_language_target": to_language,
    "extracted_path": str(os.path.join(run_folder_path, "extracted")),
    "translated_path": str(os.path.join(run_folder_path, "translated")),
    "results_path": str(run_folder_path),
    "samples_path": str(os.path.join(deepdub_path, "samples")),
    "metadata_path": str(os.path.join(run_folder_path, "metadata")),
    "enc_model_fpath": Path(deepdub_path + "/deepdub/pipeline/audio/real_time_voice_cloning/encoder/saved_models/pretrained.pt"),
    "syn_model_fpath": Path(deepdub_path + "/deepdub/pipeline/audio/real_time_voice_cloning/synthesizer/saved_models/pretrained/pretrained.pt"),
    "voc_model_fpath": Path(deepdub_path + "/deepdub/pipeline/audio/real_time_voice_cloning/vocoder/saved_models/pretrained/pretrained.pt"),
    "cpu": False,
    "no_sound": False,
    "seed": None,
    "no_mp3_support": False,
    "checkpoint_path": Path(deepdub_path, "deepdub/pipeline/lipsync/wav2lip/checkpoints/wav2lip.pth"),
    "outfile": str(os.path.join(run_folder_path, "metadata")),
    "static": False,
    "fps": 25.0,
    "pads": [0, 10, 0, 0],
    "face_det_batch_size": 16,
    "wav2lip_batch_size": 128,
    "resize_factor": 1,
    "crop": [0, -1, 0, -1],
    "box": [-1, -1, -1, -1],
    "rotate": False,
    "nosmooth": False,
    "nthreads": 12,
    "output": None,
    "conservative": False,
    "disfluency": False,
}

    mydict = dotdict(deepdub_args)

    log_file_path = os.path.join(run_folder_path, 'Deepdub_run_Log.txt')
    relative_return_log_file = os.path.relpath(log_file_path, os.getcwd())

    try:
        with open(log_file_path, 'a') as f:
            sys.stdout = f
            return_file = main.main(mydict)
        sys.stdout = stdout_backup
    except Exception as e:
        sys.stdout = stdout_backup
        error_message = traceback.format_exc()
        print (error_message)
        with open(log_file_path, 'a') as f:
            f.write("---------------------------------------------ERROR---------------------------------------------\n")
            f.write(error_message)
        return JSONResponse(
        status_code=500,
        content={
        	"message": f"Deepdub crashed while trying to process the video.",
        	"logs": str(relative_return_log_file),
        	},
    )
    print("Return file is:", return_file)

    relative_return_file = os.path.relpath(return_file, os.getcwd())
    relative_return_folder = os.path.relpath(run_folder_path, os.getcwd())


    print("Relative Return file is:", relative_return_file)
    print("Relative Return folder is:", relative_return_folder)

    return {"filename": str(relative_return_file), "foldername": str(relative_return_folder), "logs": str(relative_return_log_file)}
