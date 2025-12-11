# main.py
import asyncio
from aiohttp import web
from pyppeteer import launch

async def generate_pdf(html_content: str):
    # Remplace ce chemin par le chemin exact de ton Chrome
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    browser = await launch(
        executablePath=chrome_path,
        headless=True,
        args=['--no-sandbox', '--disable-dev-shm-usage']
    )
    page = await browser.newPage()
    await page.setContent(html_content)
    pdf_bytes = await page.pdf({'format': 'A4'})
    await browser.close()
    return pdf_bytes

async def handle_generate(request):
    data = await request.json()
    html = f"""
    <h1>Facture {data.get('numero')}</h1>
    <p>Client: {data.get('client')}</p>
    <p>Total: {data.get('total')}</p>
    """
    pdf_bytes = await generate_pdf(html)
    return web.Response(body=pdf_bytes, content_type='application/pdf')

app = web.Application()
app.router.add_post('/generate', handle_generate)

if __name__ == '__main__':
    web.run_app(app, port=5001)
