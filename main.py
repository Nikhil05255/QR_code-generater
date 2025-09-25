from flask import Flask, render_template, request, send_file
import qrcode
from io import BytesIO
from base64 import b64encode

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def generateQR():
    data = request.form.get('link')

    # Generate QR
    memory = BytesIO()
    img = qrcode.make(data)
    img.save(memory)
    memory.seek(0)

    # Base64 for preview
    base64_img = "data:image/png;base64," + b64encode(memory.getvalue()).decode('ascii')

    return render_template("index.html", data=base64_img, link=data)


@app.route("/download")
def download_qr():
    link = request.args.get("link")
    if not link:
        return "No data found", 400

    memory = BytesIO()
    img = qrcode.make(link)
    img.save(memory)
    memory.seek(0)

    return send_file(memory, mimetype="image/png", as_attachment=True, download_name="qrcode.png")
    return render_template("index.html", data=base64_img, link=data)


if __name__ == "__main__":
    app.run(debug=True)