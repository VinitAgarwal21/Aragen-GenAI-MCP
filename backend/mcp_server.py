from mcp.server.fastmcp import FastMCP
import os

# Initialize MCP Server instance
mcp = FastMCP("Clinical Lab MCP Server")

# Clinical Reference Range Knowledge Base
REFERENCE_DATABASE = {
    "ferritin": {"min_reference": 15.0, "max_reference": 150.0, "unit": "ug/L"},
    "glikozile hemoglobin (hba1c)": {"min_reference": 4.0, "max_reference": 6.0, "unit": "%"},
    "total ige": {"min_reference": 0.1, "max_reference": 100.0, "unit": "KU/L"},
    "insülin": {"min_reference": 2.6, "max_reference": 24.9, "unit": "mU/L"},
    "serbest t4": {"min_reference": 0.87, "max_reference": 1.70, "unit": "ng/dL"},
    "glucose": {"min_reference": 70.0, "max_reference": 99.0, "unit": "mg/dL"},
    "hemoglobin": {"min_reference": 12.0, "max_reference": 15.5, "unit": "g/dL"},
    "creatinine": {"min_reference": 0.6, "max_reference": 1.2, "unit": "mg/dL"},
    "wbc": {"min_reference": 4.5, "max_reference": 11.0, "unit": "10*3/uL"},
    "platelets": {"min_reference": 150.0, "max_reference": 450.0, "unit": "10*3/uL"}
}

@mcp.tool()
def reference_range_lookup(test_name: str) -> dict:
    """
    Optional tool: Look up standard reference range, min, max, and unit for a given lab test name.
    Handles unrecognized test names gracefully with safe defaults.
    """
    if not test_name or not isinstance(test_name, str):
        return {"error": "Invalid test name provided", "min_reference": 0.0, "max_reference": 100.0, "unit": "units"}
    
    key = test_name.strip().lower()
    if key in REFERENCE_DATABASE:
        return REFERENCE_DATABASE[key]
    
    return {
        "min_reference": 0.0,
        "max_reference": 100.0,
        "unit": "units",
        "warning": f"Test '{test_name}' not found in database. Using estimated default reference range."
    }

@mcp.tool()
def validate_and_classify_lab(test_name: str, result: float, min_ref: float = None, max_ref: float = None) -> dict:
    """
    Validates input data, checks for missing data or out-of-range values, and classifies severity.
    """
    try:
        if not test_name or str(test_name).strip() == "":
            return {"status": "Error", "message": "Invalid or missing lab test name."}
        
        if result is None or (isinstance(result, str) and result.strip() == ""):
            return {"status": "Error", "message": f"Missing result value for test '{test_name}'."}

        try:
            val = float(result)
        except ValueError:
            return {"status": "Warning", "severity": "Warning", "message": f"Non-numeric result '{result}' received for '{test_name}'."}

        if min_ref is None or max_ref is None:
            lookup = reference_range_lookup(test_name)
            min_ref = min_ref if min_ref is not None else lookup.get("min_reference", 0.0)
            max_ref = max_ref if max_ref is not None else lookup.get("max_reference", 100.0)

        if min_ref <= val <= max_ref:
            severity = "Normal"
        else:
            range_span = max_ref - min_ref
            margin = 0.15 * range_span if range_span != 0 else 0.1 * val
            if val < (min_ref - margin) or val > (max_ref + margin):
                severity = "Critical"
            else:
                severity = "Warning"

        return {
            "test_name": test_name,
            "value": val,
            "min_reference": min_ref,
            "max_reference": max_ref,
            "severity": severity,
            "status": "Success"
        }
    except Exception as e:
        return {"status": "Error", "message": str(e)}

if __name__ == "__main__":
    mcp.run()