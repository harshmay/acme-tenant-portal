from docx import Document
import copy

def generate_welcome_pack(fields: dict, template_path: str, output_path: str):
    doc = Document(template_path)

    # Replace placeholders in paragraphs
    for para in doc.paragraphs:
        for key, value in fields.items():
            placeholder = f"{{{{{key}}}}}"
            if placeholder in para.text:
                for run in para.runs:
                    if placeholder in run.text:
                        run.text = run.text.replace(placeholder, str(value) if value else "")

    # Replace placeholders in tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    for key, value in fields.items():
                        placeholder = f"{{{{{key}}}}}"
                        if placeholder in para.text:
                            for run in para.runs:
                                if placeholder in run.text:
                                    run.text = run.text.replace(placeholder, str(value) if value else "")

    # Remove special conditions section if null
    if not fields.get("special_conditions"):
        remove_special_conditions_section(doc)

    doc.save(output_path)

def remove_special_conditions_section(doc):
    # Remove any paragraph that contains the special conditions heading or placeholder
    to_remove = []
    for i, para in enumerate(doc.paragraphs):
        if "special_conditions" in para.text.lower() or "special conditions" in para.text.lower():
            to_remove.append(para)
    for para in to_remove:
        p = para._element
        p.getparent().remove(p)