from extractor import extract_fields
import json

result = extract_fields("uploads/Lease Agreement - Sarah Chen.docx")
print(json.dumps(result, indent=2))