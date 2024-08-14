# Flask API to integrate model
# app.py
from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)
model = pickle.load(open('models/fraud_detection_model.pkl', 'rb'))

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    features = [data['url_length'], data['domain_age'], data['has_https'], data['contains_special_chars']]
    prediction = model.predict([features])
    return jsonify({'fraudulent': bool(prediction[0])})

if __name__ == '__main__':
    app.run(debug=True)

# Save model
with open('models/fraud_detection_model.pkl', 'wb') as f:
    pickle.dump(model, f)