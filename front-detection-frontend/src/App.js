import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';
import 'chart.js/auto'; // For chart.js auto-registering

const App = () => {
    const [url, setUrl] = useState('');
    const [prediction, setPrediction] = useState(null);
    const [data, setData] = useState({
        labels: [],
        datasets: [
            {
                label: 'Phishing Detection Data',
                data: [],
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
            },
        ],
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleChange = (e) => {
        setUrl(e.target.value);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        try {
            const response = await axios.post('http://localhost:5000/predict', { url });
            setPrediction(response.data.phishing);
            await fetchData();
        } catch (error) {
            console.error('Error making prediction:', error);
            setError('Failed to make prediction.');
        } finally {
            setLoading(false);
        }
    };

    const fetchData = async () => {
        setLoading(true);
        setError(null);
        try {
            const response = await axios.get('http://localhost:5000/data'); // Ensure this endpoint exists
            const chartData = response.data;
            setData({
                labels: chartData.labels || [],
                datasets: [
                    {
                        label: 'Phishing Detection Data',
                        data: chartData.values || [],
                        borderColor: 'rgba(75, 192, 192, 1)',
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    },
                ],
            });
        } catch (error) {
            console.error('Error fetching data:', error);
            setError('Failed to fetch data.');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData(); // Fetch initial data when the component mounts
    }, []);

    return (
        <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
            <h1>Phishing Detection System</h1>
            <form onSubmit={handleSubmit} style={{ marginBottom: '20px' }}>
                <label>
                    Enter URL:
                    <input
                        type="text"
                        value={url}
                        onChange={handleChange}
                        style={{ marginLeft: '10px', padding: '5px', width: '300px' }}
                    />
                </label>
                <button
                    type="submit"
                    style={{
                        marginLeft: '10px',
                        padding: '5px 10px',
                        backgroundColor: '#007bff',
                        color: 'white',
                        border: 'none',
                        borderRadius: '4px',
                    }}
                    disabled={loading} // Disable button while loading
                >
                    {loading ? 'Checking...' : 'Check'}
                </button>
            </form>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            {prediction !== null && (
                <h2>
                    The URL is {prediction ? 'phishing' : 'safe'}
                </h2>
            )}
            <div style={{ marginTop: '20px', width: '80%', maxWidth: '800px' }}>
                <Line data={data} />
            </div>
        </div>
    );
};

export default App;
