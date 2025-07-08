import React, { useState } from 'react';
import './App.css';

function App() {
  const [files, setFiles] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleFileChange = (e) => {
    setFiles(e.target.files);
    setUploadStatus(''); // Reset status when new files are selected
  };

  const handleUpload = async () => {
    if (!files || files.length === 0) {
      setUploadStatus('Please select files first');
      return;
    }
    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
      formData.append('files', files[i]);
    }
    setUploadStatus('Uploading and processing...');
    try {
      const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
      });
      const responseData = await response.json();
      if (!response.ok) {
        throw new Error(responseData.detail || 'An unknown server error occurred.');
      }
      setUploadStatus(`Success: ${responseData.message}`);
    } catch (error) {
      setUploadStatus(`Error: ${error.message}`);
    }
  };

  const handleSendMessage = async () => {
    if (!message.trim() || isLoading) return;

    const currentMessage = message;
    // Add user's message to history immediately
    setChatHistory(prev => [...prev, { sender: 'user', text: currentMessage }]);
    setMessage('');
    setIsLoading(true);

    try {
      const formData = new FormData();
      formData.append('message', currentMessage);

      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Failed to get a response.');
      }

      // Add the AI's response to history
      setChatHistory(prev => [...prev, { sender: 'ai', text: data.response }]);
    } catch (err) {
      setChatHistory(prev => [...prev, { sender: 'ai', text: `Error: ${err.message}` }]);
    } finally {
      setIsLoading(false);
    }
  };

  const getFileListDisplay = () => {
    if (!files || files.length === 0) return 'No files selected';
    if (files.length === 1) return files[0].name;
    return `${files.length} files selected`;
  };

  return (
    <div className="container">
      <div className="header">
        <div className="header-content">
          <h1 className="title">RAG ChatBot</h1>
        </div>
      </div>

      <div className="main-container">
        {files && files.length > 0 && (
          <div className="file-upload-banner">
            <div className="file-upload-content">
              <div className="file-info">
                <span style={{ color: '#2563eb', fontSize: '16px' }}>📄</span>
                <span className="file-name">{getFileListDisplay()}</span>
              </div>
              <button onClick={handleUpload} className="upload-button">
                Upload & Process
              </button>
            </div>
            {uploadStatus && (
              <div className={`status-message ${
                uploadStatus.includes('Success') ? 'status-success' : 
                uploadStatus.includes('Error') ? 'status-error' : 'status-default'
              }`}>
                {uploadStatus.includes('Success') ? <span>✅</span> : uploadStatus.includes('Error') ? <span>❌</span> : null}
                {uploadStatus}
              </div>
            )}
          </div>
        )}

        <div className="chat-container">
          {chatHistory.length === 0 && !isLoading ? (
            <div className="empty-state">
              <img src="/AI_icon.jpg" alt="AI Icon" className="empty-state-icon" />
              <p className="empty-state-title">Upload your documents and start asking questions</p>
              <p className="empty-state-subtitle">I'll help you find information from your uploaded files</p>
            </div>
          ) : (
            chatHistory.map((item, index) => (
              <div key={index} className={`message-container ${item.sender === 'user' ? 'user-message' : 'ai-message'}`}>
                <img src={item.sender === 'ai' ? "/AI_icon.jpg" : "/human_icon.webp"} alt={`${item.sender} icon`} className="chat-icon" />
                <div className="message-bubble">
                  <p className="message-text">{item.text}</p>
                </div>
              </div>
            ))
          )}

          {isLoading && (
            <div className="message-container ai-message">
              <img src="/AI_icon.jpg" alt="AI icon" className="chat-icon" />
              <div className="message-bubble">
                <div className="loading-dots">
                  <div className="loading-dot"></div>
                  <div className="loading-dot"></div>
                  <div className="loading-dot"></div>
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="input-container">
          <div className="input-row">
            <label className="file-button">
              <span>📎</span>
              <input type="file" onChange={handleFileChange} accept=".pdf" multiple className="hidden-input" />
            </label>
            <input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Type your question..."
              className="message-input"
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              disabled={isLoading}
            />
            <button onClick={handleSendMessage} disabled={isLoading || !message.trim()} className="send-button">
              <span>➤</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;