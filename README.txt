Phishing Detection System

This project is a web-based phishing detection system. Users can input a URL to check if it is potentially a phishing site. The system also displays historical data on phishing detections in a line chart, allowing users to monitor trends over time.
Table of Contents

    Project Overview
    Features
    Tech Stack
    Prerequisites
    Installation
    Running the Application
    Project Structure
    API Endpoints
    Usage
    Contributing
    License

Project Overview

The Phishing Detection System provides a user-friendly interface to check if a given URL is likely to be a phishing site. 
It integrates a machine learning model on the backend to analyze URLs and returns a prediction. Additionally, the application displays historical phishing data in a line chart for easy visualization.
Features

    URL Input: Users can input a URL to check for phishing.
    Real-Time Prediction: The system returns a prediction (phishing or safe) based on the analysis.
    Historical Data Visualization: A line chart displays historical phishing detection data.
    Error Handling: The application provides clear error messages for failed predictions or data fetching.

Tech Stack
Frontend

    React.js: JavaScript library for building user interfaces.
    Chart.js: Used for data visualization in the line chart.
    Axios: Promise-based HTTP client for making requests to the backend.

Backend

    Flask: Python web framework for building the backend API.
    scikit-learn: Machine learning library used for phishing detection.

Prerequisites

    Node.js: Ensure you have Node.js installed (version 12 or later).
    Python: Python 3.6+ should be installed.
    Flask: Install Flask and necessary Python libraries.
    Virtual Environment: It's recommended to use a virtual environment for Python dependencies.

Installation
Clone the Repository

git clone https://github.com/toyosee/phishing-ads-url-detector.git
cd phishing-detection-system

Backend Setup

    Navigate to the backend directory:

cd backend

Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

Install the required Python packages:

pip install -r requirements.txt

Start the Flask server:

    flask run OR python main.py

Frontend Setup

    Navigate to the frontend directory:

cd frontend

Install Node.js dependencies:

npm install

Start the React development server:

    npm start

Running the Application

    Start the Flask backend server first.
    Start the React frontend server.
    Open your browser and navigate to http://localhost:3000 to use the application.

Project Structure

phishing-detection-system/
│
├── backend/                   # Backend Flask application
│   ├── main.py                 # Main Flask application
│   ├── model.py               # ML model loading and prediction
│   ├── data/                  # Sample data and datasets
│   ├── static/                # Static files served by Flask (if any)
│   ├── templates/             # HTML templates (if using Jinja2)
│   └── requirements.txt       # Python dependencies
│
└── frontend/                  # Frontend React application
    ├── public/                # Public static files
    ├── src/                   # React components and logic
    │   ├── App.js             # Main React component
    │   ├── index.js           # Entry point for React
    │   └── ...
    └── package.json           # Node.js dependencies

API Endpoints
POST /predict

    Description: Accepts a URL and returns a phishing prediction.
    Request:
        Body: { "url": "http://localhost:5000/predict" }
    Response:
        Success: { "phishing": true }
        Error: { "error": "Failed to make prediction." }

GET /data

    Description: Retrieves historical phishing detection data.
    Response:
        Success: { "labels": [...], "values": [...] }
        Error: { "error": "Failed to fetch data." }

Usage

    Enter a URL in the input field and click "Check" to get a phishing prediction.
    View the prediction result, which indicates whether the URL is safe or phishing.
    Check the line chart for historical data on phishing detections.

Contributing

Contributions are welcome! Please follow these steps:

    Fork the repository.
    Create a new branch: git checkout -b feature-branch-name.
    Make your changes and commit them: git commit -m 'Add new feature'.
    Push to the branch: git push origin feature-branch-name.
    Submit a pull request.

License

This project is licensed under the MIT License. See the LICENSE file for details.
