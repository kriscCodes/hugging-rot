import { useState } from 'react';
import axios from 'axios';
import './EnterText.css';

function EnterText() {
	const [text, setText] = useState(''); // For current input
	const [savedTexts, setSavedTexts] = useState([]); // For saved entries
	const [analysisResults, setAnalysisResults] = useState([]); // For storing analysis results

	// const handleSave = () => {
	// 	if (text.trim()) {
	// 		// Add the current text to the savedTexts array
	// 		setSavedTexts((prev) => [...prev, text]);
	// 		console.log(`Saved text${savedTexts.length + 1}:`, text); // Log with dynamic variable name
	// 		setText(''); // Clear the textbox after saving
	// 	}
	// };

	const handleAnalyze = async () => {
		// Create new array with current texts plus new text (if any)
		const textsToAnalyze = text.trim() 
			? [...savedTexts, text] 
			: savedTexts;

		if (text.trim()) {
			setSavedTexts(textsToAnalyze);
			setText(''); // Clear the textbox
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
			{/* <button onClick={handleSave}>Save</button> */}
			<button onClick={handleAnalyze} disabled={!text.trim()}>
				Analyze
			</button>

			{/* <div className="saved-texts">
				<h2>Saved Texts:</h2>
				<ul>
					{savedTexts.map((saved, index) => (
						<li key={index}>
							<strong>Saved text{index + 1}:</strong> {saved}
						</li>
					))}
				</ul>
			</div> */}

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
