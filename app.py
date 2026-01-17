import logging
from fastapi import FastAPI, Response
from pydantic import BaseModel
from weasyprint import HTML

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class PdfPayload(BaseModel):
    html: str

@app.post("/pdf")
def generate_pdf(payload: PdfPayload):
    try:
        logger.info(f"Received PDF generation request. HTML size: {len(payload.html)} chars")
        pdf_bytes = HTML(
            string=payload.html,
            base_url="."
        ).write_pdf()
        logger.info(f"PDF generated successfully. Size: {len(pdf_bytes)} bytes")
        return Response(
            pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": "inline; filename=facture.pdf"}
        )
    except Exception as e:
        logger.error("PDF generation failed", exc_info=e)
        return Response(
            f"PDF generation failed: {str(e)}",
            status_code=500
        )

@app.get("/healthz")
def healthcheck():
    return {"status": "ok"}
