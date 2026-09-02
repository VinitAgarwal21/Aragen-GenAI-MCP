import React, { useState } from 'react';
import axios from 'axios';
import LabInput from './components/LabInput';
import ResultsDisplay from './components/ResultsDisplay';

function App() {
    const [results, setResults] = useState([]);
    const [isAnalyzing, setIsAnalyzing] = useState(false);

    const handleProcess = async (data) => {
        setIsAnalyzing(true);
        try {
            const response = await axios.post('http://localhost:8000/analyze_labs', { labs: data });
            setResults(response.data.results);
        } catch (error) {
            console.error("Error analyzing labs:", error);
            alert("Failed to analyze labs. Ensure the FastAPI backend is running.");
        }
        setIsAnalyzing(false);
    };

    return (
        <div className="min-h-screen bg-gray-50 p-8">
            <div className="max-w-4xl mx-auto">
                <header className="mb-8 text-center">
                    <h1 className="text-4xl font-extrabold text-gray-900 mb-2">Clinical Lab Results Analyzer</h1>
                    <p className="text-gray-600">AI-driven classification and explainable clinical insights.</p>
                </header>
                
                <LabInput onProcess={handleProcess} />
                
                {isAnalyzing && (
                    <div className="text-center py-12">
                        <div className="animate-spin rounded-full h-12 w-12 border-b-4 border-blue-600 mx-auto"></div>
                        <p className="mt-4 text-gray-700 font-semibold animate-pulse">Agent is analyzing lab results...</p>
                    </div>
                )}
                
                <ResultsDisplay results={results} />
            </div>
        </div>
    );
}

export default App;