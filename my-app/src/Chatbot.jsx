import { useState, useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import axios from 'axios';
import './Chatbot.css';

function Chatbot() {
  const location = useLocation();
  const initialMessages = location.state?.savedTexts || [];
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const hasAnalyzed = useRef(false);

  useEffect(() => {
    if (initialMessages.length > 0 && !hasAnalyzed.current) {
      hasAnalyzed.current = true;
      const analyzeMessages = async () => {
        const allMessages = [];

        for (const text of initialMessages) {
          const userMessage = { sender: 'user', text };
          allMessages.push(userMessage);

          try {
            const response = await axios.post('http://localhost:8000/chat', {
              message: text,
              history: allMessages,
            });
            const botMessage = { sender: 'bot', text: response.data.reply };
            allMessages.push(botMessage);
          } catch (error) {
            console.error('Error analyzing message:', error);
          }
        }

        setMessages(allMessages);
      };

      analyzeMessages();
    }
  }, [initialMessages]);

  const handleSend = async () => {
    if (input.trim()) {
      const userMessage = { sender: 'user', text: input };
      const updatedMessages = [...messages, userMessage];
      setMessages(updatedMessages);

      try {
        const response = await axios.post('http://localhost:8000/chat', { 
          message: input,
          history: messages
        });
        const botMessage = { sender: 'bot', text: response.data.reply };
        
        setMessages([...updatedMessages, botMessage]);
        console.log('Sentiment:', response.data.sentiment);
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