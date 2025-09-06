from flask import Flask, request, jsonify, send_from_directory
from PIL import Image
import io
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration

app = Flask(__name__, static_folder='.')

# --------------------------
# Load pretrained BLIP model
# --------------------------
device = "cuda" if torch.cuda.is_available() else "cpu"
print("Loading BLIP model on", device)
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)
model.eval()

# --------------------------
# Serve HTML frontend
# --------------------------
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')   # make sure index.html is in same folder

# --------------------------
# API endpoint for captioning
# --------------------------
@app.route('/caption', methods=['POST'])
def caption():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']
    try:
        image = Image.open(io.BytesIO(file.read())).convert('RGB')
    except Exception as e:
        return jsonify({"error": f"Invalid image: {e}"}), 400

    try:
        inputs = processor(images=image, return_tensors="pt").to(device)
        with torch.no_grad():
            output_ids = model.generate(**inputs, max_length=40, num_beams=4)
        caption = processor.decode(output_ids[0], skip_special_tokens=True)
        return jsonify({"caption": caption})
    except Exception as e:
        return jsonify({"error": f"Model error: {e}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
