import pandas as pd
from urllib.parse import urlparse
from flask_cors import CORS  # Import CORS
import re
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from flask import Flask, request, jsonify
import pickle

# Sample data
ads_data = [
    {"ad_id": "AD001", "url": "http://example.com/offer1", "is_phishing": False},
    {"ad_id": "AD002", "url": "http://example.com/offer2", "is_phishing": False},
    {"ad_id": "AD003", "url": "http://example.com/offer3", "is_phishing": False},
    {"ad_id": "AD004", "url": "http://example.com/offer4", "is_phishing": False},
    {"ad_id": "AD005", "url": "http://example.com/offer5", "is_phishing": True},
    {"ad_id": "AD006", "url": "http://example.com/offer6", "is_phishing": False},
    {"ad_id": "AD007", "url": "http://example.com/offer7", "is_phishing": True},
    {"ad_id": "AD008", "url": "http://example.com/offer8", "is_phishing": False},
    {"ad_id": "AD009", "url": "http://example.com/offer9", "is_phishing": False},
    {"ad_id": "AD010", "url": "http://example.com/offer10", "is_phishing": True},
    {"ad_id": "AD011", "url": "http://example.com/offer11", "is_phishing": False},
    {"ad_id": "AD012", "url": "http://example.com/offer12", "is_phishing": True},
    {"ad_id": "AD013", "url": "http://example.com/offer13", "is_phishing": False},
    {"ad_id": "AD014", "url": "http://example.com/offer14", "is_phishing": False},
    {"ad_id": "AD015", "url": "http://example.com/offer15", "is_phishing": True},
    {"ad_id": "AD016", "url": "http://example.com/offer16", "is_phishing": False},
    {"ad_id": "AD017", "url": "http://example.com/offer17", "is_phishing": False},
    {"ad_id": "AD018", "url": "http://example.com/offer18", "is_phishing": True},
    {"ad_id": "AD019", "url": "http://example.com/offer19", "is_phishing": False},
    {"ad_id": "AD020", "url": "http://example.com/offer20", "is_phishing": False},
    {"ad_id": "AD021", "url": "http://example.com/offer21", "is_phishing": True},
    {"ad_id": "AD022", "url": "http://example.com/offer22", "is_phishing": False},
    {"ad_id": "AD023", "url": "http://example.com/offer23", "is_phishing": False},
    {"ad_id": "AD024", "url": "http://example.com/offer24", "is_phishing": True},
    {"ad_id": "AD025", "url": "http://example.com/offer25", "is_phishing": False},
    {"ad_id": "AD026", "url": "http://example.com/offer26", "is_phishing": False},
    {"ad_id": "AD027", "url": "http://example.com/offer27", "is_phishing": True},
    {"ad_id": "AD028", "url": "http://example.com/offer28", "is_phishing": False},
    {"ad_id": "AD029", "url": "http://example.com/offer29", "is_phishing": False},
    {"ad_id": "AD030", "url": "http://example.com/offer30", "is_phishing": True}
]

phishing_data = [
    {"url_id": "PH001", "url": "http://phishingexample.com/fake1", "detected_on": "2024-08-01"},
    {"url_id": "PH002", "url": "http://phishingexample.com/fake2", "detected_on": "2024-08-02"},
    {"url_id": "PH003", "url": "http://phishingexample.com/fake3", "detected_on": "2024-08-03"},
    {"url_id": "PH004", "url": "http://phishingexample.com/fake4", "detected_on": "2024-08-04"},
    {"url_id": "PH005", "url": "http://phishingexample.com/fake5", "detected_on": "2024-08-05"},
    {"url_id": "PH006", "url": "http://phishingexample.com/fake6", "detected_on": "2024-08-06"},
    {"url_id": "PH007", "url": "http://phishingexample.com/fake7", "detected_on": "2024-08-07"},
    {"url_id": "PH008", "url": "http://phishingexample.com/fake8", "detected_on": "2024-08-08"},
    {"url_id": "PH009", "url": "http://phishingexample.com/fake9", "detected_on": "2024-08-09"},
    {"url_id": "PH010", "url": "http://phishingexample.com/fake10", "detected_on": "2024-08-10"},
    {"url_id": "PH011", "url": "http://phishingexample.com/fake11", "detected_on": "2024-08-11"},
    {"url_id": "PH012", "url": "http://phishingexample.com/fake12", "detected_on": "2024-08-12"},
    {"url_id": "PH013", "url": "http://phishingexample.com/fake13", "detected_on": "2024-08-13"},
    {"url_id": "PH014", "url": "http://phishingexample.com/fake14", "detected_on": "2024-08-14"},
    {"url_id": "PH015", "url": "http://phishingexample.com/fake15", "detected_on": "2024-08-15"},
    {"url_id": "PH016", "url": "http://phishingexample.com/fake16", "detected_on": "2024-08-16"},
    {"url_id": "PH017", "url": "http://phishingexample.com/fake17", "detected_on": "2024-08-17"},
    {"url_id": "PH018", "url": "http://phishingexample.com/fake18", "detected_on": "2024-08-18"},
    {"url_id": "PH019", "url": "http://phishingexample.com/fake19", "detected_on": "2024-08-19"},
    {"url_id": "PH020", "url": "http://phishingexample.com/fake20", "detected_on": "2024-08-20"},
    {"url_id": "PH021", "url": "http://phishingexample.com/fake21", "detected_on": "2024-08-21"},
    {"url_id": "PH022", "url": "http://phishingexample.com/fake22", "detected_on": "2024-08-22"},
    {"url_id": "PH023", "url": "http://phishingexample.com/fake23", "detected_on": "2024-08-23"},
    {"url_id": "PH024", "url": "http://phishingexample.com/fake24", "detected_on": "2024-08-24"},
    {"url_id": "PH025", "url": "http://phishingexample.com/fake25", "detected_on": "2024-08-25"},
    {"url_id": "PH026", "url": "http://phishingexample.com/fake26", "detected_on": "2024-08-26"},
    {"url_id": "PH027", "url": "http://phishingexample.com/fake27", "detected_on": "2024-08-27"},
    {"url_id": "PH028", "url": "http://phishingexample.com/fake28", "detected_on": "2024-08-28"},
    {"url_id": "PH029", "url": "http://phishingexample.com/fake29", "detected_on": "2024-08-29"},
    {"url_id": "PH030", "url": "http://phishingexample.com/fake30", "detected_on": "2024-08-30"}
]

# Convert dictionaries to DataFrames
def load_data():
    ads_df = pd.DataFrame(ads_data)
    phishing_df = pd.DataFrame(phishing_data)
    return ads_df, phishing_df

# Feature extraction function
def extract_features(df):
    def url_features(url):
        parsed_url = urlparse(url)
        return [
            int(parsed_url.scheme == 'http'),  # 1 if HTTP, 0 otherwise
            int(parsed_url.scheme == 'https'), # 1 if HTTPS, 0 otherwise
            int('www.' in parsed_url.netloc),  # 1 if www. is in the domain
            int('.com' in parsed_url.netloc),  # 1 if .com is in the domain
            len(parsed_url.path)  # Length of the path
        ]
    
    features = [url_features(url) for url in df['url']]
    return pd.DataFrame(features, columns=['is_http', 'is_https', 'has_www', 'has_com', 'path_length'])

# Load and prepare data
ads_df, phishing_df = load_data()
ads_features = extract_features(ads_df)
ads_labels = ads_df['is_phishing']

# Combine phishing data for simplicity (assuming phishing URLs are indeed phishing)
phishing_features = extract_features(phishing_df)
phishing_labels = pd.Series([True] * len(phishing_df))

# Combine data
X = pd.concat([ads_features, phishing_features], ignore_index=True)
y = pd.concat([ads_labels, phishing_labels], ignore_index=True)

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save the model
with open('model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)

# Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/predict', methods=['POST'])
def predict():
    url = request.json.get('url')
    features = extract_features(pd.DataFrame([{'url': url}]))  # Extract features for the input URL
    prediction = model.predict(features)
    return jsonify({'phishing': bool(prediction[0])})

@app.route('/data', methods=['GET'])
def get_data():
    # Example dummy data for chart
    data = {
        'labels': ['Aug 01', 'Aug 02', 'Aug 03', 'Aug 08', 'Sep 02'],
        'values': [5, 10, 15, 12, 2]
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)