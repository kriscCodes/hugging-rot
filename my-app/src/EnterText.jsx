import { useState } from 'react';
import './EnterText.css';

function EnterText() {
  const [text, setText] = useState(''); // For current input
  const [savedTexts, setSavedTexts] = useState([]); // For saved entries

  const handleSave = () => {
    if (text.trim()) {
      // Add the current text to the savedTexts array
      setSavedTexts((prev) => [...prev, text]);
      console.log(`Saved text${savedTexts.length + 1}:`, text); // Log with dynamic variable name
      setText(''); // Clear the textbox after saving
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
      <button onClick={handleSave}>Save</button>
      <div className="saved-texts">
        <h2>Saved Texts:</h2>
        <ul>
          {savedTexts.map((saved, index) => (
            <li key={index}>
              <strong>Saved text{index + 1}:</strong> {saved}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default EnterText;
