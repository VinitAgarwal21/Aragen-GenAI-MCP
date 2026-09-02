import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from mcp_server import validate_and_classify_lab

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

async def generate_explanation(test_name, value, unit, min_ref, max_ref, severity):
    """Calls the LLM to generate explainable AI clinical insights."""
    if severity == "Normal":
        return {
            "explanation": f"The {test_name} level of {value} {unit} is within the normal reference range ({min_ref} - {max_ref}).",
            "next_steps": "No immediate clinical intervention required. Continue routine monitoring."
        }

    prompt = f"""
    You are an expert clinical laboratory AI. Explain the following abnormal lab result based on Explainable AI principles.
    Explain WHY it was flagged and WHAT it means clinically.
    
    Test: {test_name}
    Value: {value} {unit}
    Reference Range: {min_ref} - {max_ref} {unit}
    Severity: {severity}

    Provide a concise clinical explanation and a specific recommended next step.
    Output MUST be valid JSON with exact keys: "explanation" and "next_steps".
    """

    model = genai.GenerativeModel('gemini-3.5-flash-lite', generation_config={"response_mime_type": "application/json"})
    
    try:
        response = model.generate_content(prompt)
        return json.loads(response.text)
    except Exception as e:
        return {
            "explanation": f"The result for {test_name} ({value} {unit}) falls outside the reference range ({min_ref}-{max_ref}), indicating a {severity.lower()} clinical finding.",
            "next_steps": "Consult with a healthcare provider for follow-up evaluation."
        }

async def process_lab_results(labs):
    """
    Agent Pipeline:
    1. Validate & Classify via MCP Server tools (handling missing data, invalid names, out-of-range values).
    2. Optional Tool Reference Range Lookup triggered automatically when ranges are missing.
    3. Generate Explainable AI Clinical Explanations.
    4. Route/Sort results by severity (Critical -> Warning -> Normal).
    """
    analyzed = []
    
    for lab in labs:
        test_name = getattr(lab, 'Test_Name', None) or lab.get('Test_Name')
        result_val = getattr(lab, 'Result', None) if hasattr(lab, 'Result') else lab.get('Result')
        unit = getattr(lab, 'Unit', 'units') or lab.get('Unit', 'units')
        min_ref = getattr(lab, 'Min_Reference', None) if hasattr(lab, 'Min_Reference') else lab.get('Min_Reference')
        max_ref = getattr(lab, 'Max_Reference', None) if hasattr(lab, 'Max_Reference') else lab.get('Max_Reference')

        # Communicate exclusively through MCP Server validation/classification tools
        classification_result = validate_and_classify_lab(
            test_name=test_name, 
            result=result_val, 
            min_ref=min_ref, 
            max_ref=max_ref
        )

        if classification_result.get("status") == "Error":
            analyzed.append({
                "test_name": test_name or "Unknown Test",
                "value": result_val,
                "unit": unit,
                "min_reference": min_ref,
                "max_reference": max_ref,
                "severity": "Warning",
                "explanation": f"Data validation error: {classification_result.get('message')}",
                "next_steps": "Verify lab entry data format and re-submit."
            })
            continue

        min_ref = classification_result.get("min_reference")
        max_ref = classification_result.get("max_reference")
        severity = classification_result.get("severity", "Warning")

        # Explain via LLM
        ai_insights = await generate_explanation(
            test_name, result_val, unit, min_ref, max_ref, severity
        )

        analyzed.append({
            "test_name": test_name,
            "value": result_val,
            "unit": unit,
            "min_reference": min_ref,
            "max_reference": max_ref,
            "severity": severity,
            "explanation": ai_insights.get("explanation"),
            "next_steps": ai_insights.get("next_steps")
        })

    # Route: Group results (Critical first, then Warnings, then Normals)
    severity_order = {"Critical": 1, "Warning": 2, "Normal": 3}
    analyzed.sort(key=lambda x: severity_order.get(x["severity"], 4))

    return analyzed