from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from supabase import create_client
import shutil
import os
from datetime import datetime
from dotenv import load_dotenv
from extractor import extract_fields
from document import generate_welcome_pack

load_dotenv()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
TEMPLATE_PATH = os.path.join(BASE_DIR, "templates", "Tenant Welcome Pack Template.docx")

# Supabase
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)


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
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"welcome_pack_{timestamp}.docx"
        output_path = os.path.join(UPLOAD_DIR, output_filename)
        generate_welcome_pack(fields, TEMPLATE_PATH, output_path)

        # Save to Supabase — lease upload record
        upload_record = supabase.table("lease_uploads").insert({
            "original_filename": file.filename,
            "tenant_name": fields.get("tenant_name"),
            "property_address": fields.get("property_address"),
            "lease_start_date": fields.get("lease_start_date"),
            "lease_end_date": fields.get("lease_end_date"),
            "rent_amount": fields.get("rent_amount"),
            "bond_amount": fields.get("bond_amount"),
            "num_occupants": fields.get("num_occupants"),
            "pet_permission": fields.get("pet_permission"),
            "parking_included": fields.get("parking_included"),
            "special_conditions": fields.get("special_conditions"),
            "landlord_name": fields.get("landlord_name"),
            "property_manager_name": fields.get("property_manager_name"),
            "property_manager_email": fields.get("property_manager_email"),
            "property_manager_phone": fields.get("property_manager_phone"),
            "status": "processed"
        }).execute()

        lease_id = upload_record.data[0]["id"]

        # Upload generated file to Supabase Storage
        with open(output_path, "rb") as f:
            supabase.storage.from_("documents").upload(
                path=output_filename,
                file=f,
                file_options={"content-type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"}
            )

        # Get public URL
        file_url = supabase.storage.from_("documents").get_public_url(output_filename)

        # Save generated document record
        supabase.table("generated_documents").insert({
            "lease_upload_id": lease_id,
            "output_filename": output_filename,
            "file_url": file_url
        }).execute()

        try:
            os.remove(output_path)
            os.remove(file_path)
        except OSError:
            pass

        return {
            "message": "Your Tenant Welcome Pack has been uploaded successfully.",
            "file_url": file_url,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount static frontend at root after API routes are declared.
app.mount("/", StaticFiles(directory="static", html=True), name="static")