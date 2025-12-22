from fastapi import FastAPI, Response
from pydantic import BaseModel
from weasyprint import HTML

app = FastAPI()

class PdfPayload(BaseModel):
    html: str

@app.post("/pdf")
def generate_pdf(payload: PdfPayload):
    pdf_bytes = HTML(
        string=payload.html,
        base_url="."
    ).write_pdf()

    return Response(
        pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "inline; filename=facture.pdf"
        }
    )
@app.get("/healthz")
def healthcheck():
    return {"status": "ok"}
