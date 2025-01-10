import React, { useState } from 'react';
import { Button, message as antdMessage, Input } from 'antd';
import { CopyOutlined } from '@ant-design/icons';
import { CopyToClipboard } from 'react-copy-to-clipboard';
import { useNavigate } from 'react-router-dom';
import '../styles/uploadPageStyles.css';

const UploadPage = () => {
    const [file, setFile] = useState(null);
    const [uploading, setUploading] = useState(false);
    const [messageText, setMessageText] = useState("");
    const [query, setQuery] = useState("");
    const [videoKey, setVideoKey] = useState(0);
    const [generatedText, setGeneratedText] = useState("");
    const navigate = useNavigate();

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        setFile(selectedFile);
        setMessageText("");
        setGeneratedText("");
        setVideoKey(prevKey => prevKey + 1);
    };

    const handleQueryChange = (e) => {
        setQuery(e.target.value);
    };

    const handleUpload = () => {
        if (!file) return;
        setUploading(true);
        const formData = new FormData();
        formData.append('file', file);
        if (query.trim() !== "") {
            formData.append('query', query);
        }
        fetch("/upload-video", {
            method: 'POST',
            body: formData
        }).then(
            res => res.json()
        ).then(
            data => {
                setMessageText(data.message);
                setGeneratedText(data.text);
                setUploading(false);
            }
        ).catch(error => {
            console.error('Error:', error);
            setUploading(false);
        });
    };

    const handleCopyText = () => {
        navigator.clipboard.writeText(generatedText);
        antdMessage.success('Text copied to clipboard');
    };

    const goToSearchPage = () => {
        navigate('/searchPage');
    };

    return (
        <div className="upload-container">
            <div className="header">
                <h1>Video Event Captioner</h1>
                <Button type="primary" className="search-page-button" onClick={goToSearchPage}>Search</Button>
                <p>Upload a video file and get automatic captioning</p>
            </div>
            <div className="upload-section">
                <input type="file" accept="video/*" onChange={handleFileChange} />
                {file && (
                    <div className="video-section">
                    <h2>Uploaded Video</h2>
                    <div className="video-container">
                        <video key={videoKey} controls>
                            <source src={URL.createObjectURL(file)} type="video/mp4" />
                            Your browser does not support the video tag.
                        </video>
                    </div>
                </div>
                
                )}
                <Input placeholder="Enter query (optional)" onChange={handleQueryChange} />
                <Button type="primary" onClick={handleUpload} disabled={!file} loading={uploading}>
                    {uploading ? 'Generating' : 'Generate'}
                </Button>
            </div>
            {messageText && <p className={`message ${messageText.startsWith("Error") ? 'error' : 'success'}`}>{messageText}</p>}
            {generatedText && (
                <div className="result-section">
                    <h2>Generated Text</h2>
                    <Input.TextArea className="generated-text" value={generatedText} readOnly />
                    <CopyToClipboard text={generatedText} onCopy={handleCopyText}>
                        <Button icon={<CopyOutlined />}>Copy Text</Button>
                    </CopyToClipboard>
                </div>
            )}
        </div>
    );
}

export default UploadPage;
