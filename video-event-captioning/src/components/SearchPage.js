import React, { useState, useEffect } from 'react';
import { Input, Button } from 'antd';
import '../styles/searchPageStyles.css';

const { Search } = Input;

const SearchPage = () => {
    const [searchQuery, setSearchQuery] = useState('');
    const [searchResults, setSearchResults] = useState(null);
    const [videoFiles, setVideoFiles] = useState([]);

    useEffect(() => {
        if (searchResults) {
            setVideoFiles(searchResults);
        }
    }, [searchResults]);

    const handleSearch = () => {
    
        setVideoFiles([]);

        fetch('/search', {
            method: 'POST',
            body: JSON.stringify({ query: searchQuery }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(response => response.json())
            .then(data => {
                setSearchResults(data.results);
            })
            .catch(error => {
                console.error('Error searching:', error);
            });
    };

    return (
        <div>
            <h1>Search Page</h1>
            <Search
                placeholder="Enter your search query"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onSearch={handleSearch}
                enterButton={<Button type="primary">Search</Button>}
                className="search-page-input"
            />

            <div className="video-grid">
                {videoFiles.map((filename, index) => (
                    <div key={index} className="video-item">
                        <video controls>
                            <source src={`/uploads/${filename}`} type="video/mp4" />
                            Your browser does not support the video tag.
                        </video>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default SearchPage;
