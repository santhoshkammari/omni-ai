import React, { useState, useRef, useEffect } from 'react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    setMessages(prev => [...prev, { text: input, sender: 'user' }]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8888/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: input}),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      let assistantResponse = '';

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.trim() === '') continue;

          try {
            const jsonResponse = JSON.parse(line);
            if (jsonResponse.content) {
              assistantResponse += jsonResponse.content;
              setMessages(prev => {
                const lastMessage = prev[prev.length - 1];
                if (lastMessage && lastMessage.sender === 'assistant') {
                  const updatedLastMessage = {
                    ...lastMessage,
                    text: assistantResponse
                  };
                  return [...prev.slice(0, -1), updatedLastMessage];
                } else {
                  return [...prev, { text: assistantResponse, sender: 'assistant' }];
                }
              });
            }
          } catch (error) {
            console.error('Error parsing JSON:', error);
          }
        }
      }
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev, { text: 'An error occurred.', sender: 'assistant' }]);
    }

    setIsLoading(false);
  };

  const renderMessageText = (text) => {
    const parts = text.split(/<artifact_area>|<\/artifact_area>/);
    return parts.map((part, index) => {
      if (index % 2 === 0) {
        return <span key={index}>{part}</span>;
      } else {
        return (
          <pre key={index} className="artifact-area">
            <code>{part.trim()}</code>
          </pre>
        );
      }
    });
  };

  return (
    <div className="app">
      <div className="chat-container">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.sender}`}>
            <div className="message-content">
              <span className="sender-icon">{message.sender === 'user' ? 'SK' : 'Claude'}</span>
              {renderMessageText(message.text)}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message assistant">
            <div className="message-content">
              <span className="sender-icon">Claude</span>
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <div className="input-container">
        <form onSubmit={handleSubmit} className="input-form">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Reply to Claude..."
            disabled={isLoading}
          />
          <button type="submit" disabled={isLoading}>
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M7 11L12 6L17 11M12 18V7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;