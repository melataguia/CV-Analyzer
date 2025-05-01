import logging
import os
import tempfile

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from parsing import parse_cv

# Initialisation
load_dotenv()
logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
CORS(app)

@app.route('/parse', methods=['POST'])
def parse():
    if 'cv' not in request.files:
        return jsonify({"status": "error", "message": "No file part in the request"}), 400

    file = request.files['cv']
    if file.filename == '':
        return jsonify({"status": "error", "message": "No selected file"}), 400

    job_offer_text = request.form.get("job_offer", "").strip()
    if not job_offer_text:
        return jsonify({"status": "error", "message": "Missing job offer text"}), 400

    logging.info(f"Offre d'emploi reçue : {job_offer_text[:200]}...")
    suffix = os.path.splitext(file.filename)[1]
    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp:
            file.save(temp.name)
            temp_path = temp.name
            logging.info(f"Temporary file saved at: {temp_path}")

        # Diagnostic: appel de parse_cv
        try:
            logging.info(f"Appel parse_cv sur: {temp_path}")
            text = parse_cv(temp_path)
            logging.info("parse_cv renvoyé sans exception")
        except Exception as te:
            logging.exception("Échec parse_cv")
            raise

        return jsonify({"status": "success", "text": text})

    except TypeError as te:
        if 'Load failed' in str(te):
            logging.error(f"TypeError Load failed: {te}")
            return jsonify({"status": "error", "message": "Load failed during processing"}), 500
        logging.error(f"Unhandled TypeError: {te}")
        return jsonify({"status": "error", "message": str(te)}), 500

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
            logging.info(f"Temporary file deleted: {temp_path}")

if __name__ == '__main__':
    app.run(debug=True)