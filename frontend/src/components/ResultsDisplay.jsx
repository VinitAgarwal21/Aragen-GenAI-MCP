import React from 'react';
import SeverityBadge from './SeverityBadge';

export default function ResultsDisplay({ results }) {
    if (!results || results.length === 0) return null;

    return (
        <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-2">Analysis Results</h2>
            {results.map((res, index) => (
                <div key={index} className="p-6 bg-white shadow-sm rounded-xl border-l-8"
                     style={{ borderLeftColor: res.severity === 'Critical' ? '#ef4444' : res.severity === 'Warning' ? '#f59e0b' : '#22c55e'}}>
                    
                    <div className="flex justify-between items-start mb-4">
                        <div>
                            <h3 className="text-xl font-bold text-gray-900">{res.test_name}</h3>
                            <div className="text-sm text-gray-500 mt-1">
                                <span className="font-semibold text-gray-700">Value:</span> {res.value} {res.unit} &nbsp;|&nbsp; 
                                <span className="font-semibold text-gray-700 ml-2">Reference:</span> {res.min_reference} - {res.max_reference} {res.unit}
                            </div>
                        </div>
                        <SeverityBadge severity={res.severity} />
                    </div>
                    
                    <div className="bg-gray-50 p-4 rounded-lg border border-gray-100 mb-3">
                        <p className="font-semibold text-sm text-gray-800 mb-1">Explainable AI Insight:</p>
                        <p className="text-sm text-gray-700 leading-relaxed">{res.explanation}</p>
                    </div>
                    
                    <div className="bg-blue-50/50 p-4 rounded-lg border border-blue-100">
                        <p className="font-semibold text-sm text-blue-900 mb-1">Recommended Action:</p>
                        <p className="text-sm text-blue-800">{res.next_steps}</p>
                    </div>
                </div>
            ))}
        </div>
    );
}