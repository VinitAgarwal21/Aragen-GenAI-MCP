import React from 'react';

export default function SeverityBadge({ severity }) {
    let colorClass = "bg-gray-100 text-gray-800 border-gray-200";
    let displayLabel = severity;

    if (severity === "Critical") {
        colorClass = "bg-red-100 text-red-800 border-red-200";
        displayLabel = "🚨 Critical";
    } else if (severity === "Warning") {
        colorClass = "bg-yellow-100 text-yellow-800 border-yellow-200";
        displayLabel = "⚠️ Warning";
    } else if (severity === "Normal") {
        colorClass = "bg-green-100 text-green-800 border-green-200";
        displayLabel = "✅ Normal";
    }

    return (
        <span className={`px-4 py-1.5 rounded-full text-xs font-bold tracking-wide border inline-flex items-center gap-1.5 ${colorClass}`}>
            {displayLabel}
        </span>
    );
}