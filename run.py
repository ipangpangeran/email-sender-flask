from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import resend
import os

load_dotenv()

app = Flask(__name__)

resend.api_key = os.getenv("RESEND_API_KEY")

MAIL_FROM = os.getenv("MAIL_FROM")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/send-email", methods=["POST"])
def send_email():
    try:
        data = request.get_json()

        to_email = data.get("to")
        subject = data.get("subject")
        message = data.get("message")

        if not to_email:
            return jsonify({
                "success": False,
                "message": "Email tujuan wajib diisi"
            }), 400

        params = {
            "from": f"Ipangpangeran <{MAIL_FROM}>",
            "to": [to_email],
            "subject": subject,
            "html": f"""
            <p>{message}</p>
            """
        }

        result = resend.Emails.send(params)

        return jsonify({
            "success": True,
            "message": "Email berhasil dikirim",
            "data": result
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )