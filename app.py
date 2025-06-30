import json
from flask import Flask, request, jsonify
from flask_cors import CORS

# Flask uygulamasını başlat
app = Flask(__name__)
# CORS ayarlarını yaparak tarayıcıdan gelen isteklere izin ver
CORS(app)

SCORES_FILE = 'scores.json'

def get_scores():
    """scores.json dosyasından skorları okur."""
    try:
        with open(SCORES_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Dosya yoksa veya boşsa, boş liste döndür
        return []

def save_scores(scores):
    """Skorları scores.json dosyasına yazar."""
    with open(SCORES_FILE, 'w') as f:
        json.dump(scores, f, indent=4)

# --- API Adresleri (Endpoints) ---

@app.route('/scores', methods=['GET'])
def handle_get_scores():
    """En yüksek 5 skoru döndüren adres."""
    scores = get_scores()
    return jsonify(scores)

@app.route('/add-score', methods=['POST'])
def handle_add_score():
    """Yeni bir skor ekleyen adres."""
    new_score_data = request.json
    
    if not new_score_data or 'name' not in new_score_data or 'score' not in new_score_data:
        return jsonify({"error": "Geçersiz veri"}), 400

    scores = get_scores()
    scores.append(new_score_data)
    
    # Skorları puana göre büyükten küçüğe sırala
    scores.sort(key=lambda x: x['score'], reverse=True)
    
    # Sadece en iyi 5 skoru tut
    top_scores = scores[:5]
    
    save_scores(top_scores)
    
    return jsonify({"success": True, "scores": top_scores}), 201

# --- Sunucuyu Çalıştırma ---
if __name__ == '__main__':
    # debug=True, kodu her değiştirdiğinde sunucunun yeniden başlamasını sağlar
    app.run(debug=True, port=5000)