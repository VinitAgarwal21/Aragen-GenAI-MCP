from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Any
from agent import process_lab_results

app = FastAPI(title="Clinical Lab Results Analyzer - MCP Powered")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LabResult(BaseModel):
    Test_Name: Optional[Any] = None
    Result: Optional[Any] = None
    Unit: Optional[str] = "units"
    Min_Reference: Optional[float] = None
    Max_Reference: Optional[float] = None

class LabAnalysisRequest(BaseModel):
    labs: List[LabResult]

@app.post("/analyze_labs")
async def analyze_labs(request: LabAnalysisRequest):
    """
    Endpoint: POST /analyze_labs
    Accepts lab inputs, routes through MCP tools and AI Agent, and returns sorted analysis.
    """
    try:
        analyzed_results = await process_lab_results(request.labs)
        return {"status": "success", "results": analyzed_results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.get("/health")
def health_check():
    return {"status": "healthy", "mcp_server": "active"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)