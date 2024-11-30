import { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import axios from 'axios';
import './Chatbot.css';

function Chatbot() {
  const location = useLocation();
  const initialMessages = location.state?.savedTexts || [];
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  useEffect(() => {
    if (initialMessages.length > 0) {
      const initialChatMessages = initialMessages.map(text => ({ sender: 'user', text }));
      setMessages(initialChatMessages);
    }
  }, [initialMessages]);

  const handleSend = async () => {
    if (input.trim()) {
      const userMessage = { sender: 'user', text: input };
      setMessages([...messages, userMessage]);

      try {
        const response = await axios.post('http://localhost:8000/chat', { message: input });
        const botMessage = { sender: 'bot', text: response.data.reply };
        const sentiment = response.data.sentiment;

        setMessages([...messages, userMessage, botMessage]);

        console.log('Sentiment:', sentiment);
      } catch (error) {
        console.error('Error sending message:', error);
      }

      setInput('');
    }
  };

  return (
    <div className="chatbot">
      <div className="messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            {msg.text}
          </div>
        ))}
      </div>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Type a message..."
      />
      <button onClick={handleSend}>Send</button>
    </div>
  );
}

export default Chatbot;