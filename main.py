from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import shutil
import os
from extractor import extract_fields
from document import generate_welcome_pack

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
TEMPLATE_PATH = "templates\Tenant Welcome Pack Template.docx"

@app.post("/process-lease")
async def process_lease(file: UploadFile = File(...)):
    # Save uploaded file
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract fields
        fields = extract_fields(file_path)

        # Generate welcome pack
        output_path = os.path.join(UPLOAD_DIR, f"welcome_pack_{file.filename}.docx")
        generate_welcome_pack(fields, TEMPLATE_PATH, output_path)

        return FileResponse(
            output_path,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename="Tenant_Welcome_Pack.docx"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount static frontend at root after API routes are declared.
app.mount("/", StaticFiles(directory="static", html=True), name="static")