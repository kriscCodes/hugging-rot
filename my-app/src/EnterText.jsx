import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './EnterText.css';

function EnterText() {
    const [text, setText] = useState('');
    const [savedTexts, setSavedTexts] = useState([]);
    const [analysisResults, setAnalysisResults] = useState([]);
    const navigate = useNavigate();

    const handleAnalyze = async () => {
        const textsToAnalyze = text.trim() ? [...savedTexts, text] : savedTexts;

        if (text.trim()) {
            setSavedTexts(textsToAnalyze);
            setText('');
        }

        try {
            const analysisPromises = textsToAnalyze.map((textToAnalyze) =>
                axios.post('http://localhost:8000/analyze', { text: textToAnalyze })
            );

            const responses = await Promise.all(analysisPromises);

            const results = responses.map((res, index) => ({
                text: textsToAnalyze[index],
                result: res.data,
            }));

            setAnalysisResults(results);
            console.log('Analysis results:', results);
        } catch (error) {
            console.error('Error analyzing texts:', error);
        }
    };

    const handleChat = () => {
        navigate('/chat', { state: { savedTexts } });
    };

    return (
        <div className="enter-text">
            <h1>Enter Your Text</h1>
            <p>Write something in the textbox below and save it.</p>
            <textarea
                placeholder="Type your text here..."
                value={text}
                onChange={(e) => setText(e.target.value)}
                rows="5"
                cols="50"
            />
            <br />
            <button onClick={handleAnalyze} disabled={!text.trim()}>
                Analyze
            </button>
            <button onClick={handleChat} disabled={savedTexts.length === 0}>
                Chat about Texts
            </button>

            {analysisResults.length > 0 && (
                <div className="analysis-results">
                    <h2>Analysis Results:</h2>
                    <ul>
                        {analysisResults.map((result, index) => (
                            <li key={index}>
                                <strong>Text:</strong> {result.text} <br />
                                <strong>Sentiment:</strong> {result.result.sentiment} <br />
                                <strong>Confidence:</strong> {result.result.confidence}%
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}

export default EnterText;