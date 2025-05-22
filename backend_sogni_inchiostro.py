
import os
import datetime
from flask import Flask, request, send_file, jsonify
from fpdf import FPDF
import openai
import requests

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_image(prompt, path):
    try:
        r = openai.images.generate(prompt=prompt, n=1, size="512x512")
        image_url = r.data[0].url
        response = requests.get(image_url)
        with open(path, 'wb') as f:
            f.write(response.content)
        return path
    except Exception as e:
        return None

def generate_pdf(poem, image_path, output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in poem.split("\n"):
        pdf.multi_cell(0, 10, line)
    if image_path and os.path.exists(image_path):
        pdf.image(image_path, x=40, w=120)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    pdf.output(output_path)

@app.route("/genera", methods=["POST"])
def genera():
    data = request.json
    testo = data.get("testo", "")
    stile = data.get("stile", "matita")
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    image_path = f"output/image_{timestamp}.png"
    image_result = generate_image(f"{stile} illustration of {testo}", image_path)
    return jsonify({"status": "ok", "image": image_result})

@app.route("/pdf", methods=["POST"])
def crea_pdf():
    data = request.json
    testo = data.get("testo", "")
    image_path = data.get("img", "")
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    pdf_path = f"output/poem_{timestamp}.pdf"
    generate_pdf(testo, image_path, pdf_path)
    return send_file(pdf_path, as_attachment=True)

@app.route("/")
def index():
    return "API Backend Sogni di Inchiostro"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
