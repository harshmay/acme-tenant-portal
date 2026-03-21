from extractor import extract_fields
import json

result = extract_fields("uploads/Lease_Agreement - Emma_Whitfield.docx")
print(json.dumps(result, indent=2))