import React, { useState } from 'react';
import Papa from 'papaparse';

export default function LabInput({ onProcess }) {
    const [loading, setLoading] = useState(false);

    const handleFileUpload = (e) => {
        const file = e.target.files[0];
        if (!file) return;
        setLoading(true);

        Papa.parse(file, {
            header: true,
            dynamicTyping: true,
            skipEmptyLines: true,
            complete: function (results) {
                // Map to match dataset columns exactly
                const data = results.data.map(row => ({
                    Test_Name: row.Test_Name,
                    Result: parseFloat(row.Result),
                    Unit: row.Unit,
                    Min_Reference: parseFloat(row.Min_Reference),
                    Max_Reference: parseFloat(row.Max_Reference)
                })).filter(row => row.Test_Name && !isNaN(row.Result));
                
                // Process the first 5 results to save API time for the demo
                onProcess(data.slice(0, 5));
                setLoading(false);
            }
        });
    };

    return (
        <div className="p-6 bg-white shadow-sm border rounded-xl mb-6">
            <h2 className="text-xl font-bold mb-4 text-gray-800">Upload Dataset</h2>
            <input
                type="file"
                accept=".csv"
                onChange={handleFileUpload}
                className="block w-full text-sm text-gray-500 file:mr-4 file:py-2.5 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 cursor-pointer"
            />
        </div>
    );
}