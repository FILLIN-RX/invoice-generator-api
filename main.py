from flask import Flask, request, send_file, jsonify
from weasyprint import HTML, CSS
import io

app = Flask(__name__)

# Version Tailwind compilé (mode production, v3.4)
TAILWIND_CSS = """
/* Exemple simplifié, tu peux remplacer par le CSS complet compilé de Tailwind */
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Exemple inline pour PDF */
body { font-family: 'Inter', sans-serif; margin: 0; padding: 0; }
h1 { @apply text-2xl font-bold text-blue-600; }
p { @apply text-base text-gray-800; }
table { @apply w-full border border-gray-300; border-collapse: collapse; }
th, td { @apply border border-gray-300 p-2 text-left; }
"""

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    data = request.get_json()
    html_content = data.get('html')

    if not html_content:
        return jsonify({'error': 'Le contenu HTML est requis'}), 400

    pdf_file = io.BytesIO()

    try:
        HTML(string=html_content).write_pdf(
            pdf_file,
            stylesheets=[CSS(string=TAILWIND_CSS)]
        )
        pdf_file.seek(0)
        return send_file(
            pdf_file,
            mimetype='application/pdf',
            download_name='facture.pdf'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
