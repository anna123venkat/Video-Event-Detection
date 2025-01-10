import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import UploadPage from './components/UploadPage';
import SearchPage from './components/SearchPage'; // Import your SearchPage component

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<UploadPage />} /> {/* Route for the UploadPage */}
                <Route path="/searchPage" element={<SearchPage />} /> {/* Route for the SearchPage */}
            </Routes>
        </Router>
    );
}

export default App;
