from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import shutil
import os
from extractor import extract_fields
from document import generate_welcome_pack

app = FastAPI()

UPLOAD_DIR = "uploads"
TEMPLATE_PATH = "templates/welcome_pack_template.docx"

@app.post("/process-lease")
async def process_lease(file: UploadFile = File(...)):
    # Save uploaded file
    file_path = os.path.join(UPLOAD_DIR, file.filename)
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

@app.get("/")
def root():
    return {"message": "Lease Processor API is running"}