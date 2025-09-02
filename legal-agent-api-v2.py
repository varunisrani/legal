#!/usr/bin/env python3
"""
Claude Legal Agent - Production API with Direct Anthropic Integration
Uses Anthropic API directly for production deployment
"""

import os
import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import uvicorn

# Try direct Anthropic API import
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    print("Warning: anthropic package not available. Install with: pip install anthropic")

class LegalQueryRequest(BaseModel):
    query: str
    context: Optional[str] = None
    max_turns: Optional[int] = 2

class LegalQueryResponse(BaseModel):
    query_id: str
    status: str
    response: str
    processing_time: float
    timestamp: str

class LegalAgent:
    def __init__(self):
        self.query_count = 0
        
        # Initialize Anthropic client
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if api_key:
            self.client = anthropic.Anthropic(api_key=api_key)
            self.auth_method = "API_KEY"
        else:
            # For OAuth, we'll need to implement token exchange
            self.client = None
            self.auth_method = "OAUTH"
        
    async def process_legal_query(self, request: LegalQueryRequest) -> LegalQueryResponse:
        """Process legal analysis query"""
        start_time = datetime.now()
        query_id = str(uuid.uuid4())
        
        if not ANTHROPIC_AVAILABLE:
            raise HTTPException(
                status_code=500, 
                detail="Anthropic API not available. Please install anthropic package."
            )
        
        if not self.client and not os.getenv('ANTHROPIC_API_KEY'):
            raise HTTPException(
                status_code=500,
                detail="Authentication not configured. Set ANTHROPIC_API_KEY environment variable."
            )
        
        try:
            # Prepare legal analysis prompt
            system_prompt = """You are a specialized legal analysis AI assistant. Provide detailed, accurate legal analysis while noting that your responses are for informational purposes only and do not constitute legal advice. Always recommend consulting with a qualified attorney for specific legal matters.

Focus on:
- Contract clause analysis
- Legal risk assessment
- Regulatory compliance guidance  
- Legal terminology explanation
- Best practices recommendations

Be thorough, professional, and cite relevant legal principles when applicable."""
            
            full_prompt = f"Legal Analysis Request: {request.query}"
            if request.context:
                full_prompt += f"\n\nContext: {request.context}"
            
            full_prompt += f"\n\nPlease provide a comprehensive legal analysis addressing the specific query above."
            
            # Make API call to Claude
            if self.client:
                message = self.client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=4000,
                    system=system_prompt,
                    messages=[
                        {
                            "role": "user",
                            "content": full_prompt
                        }
                    ]
                )
                
                response_content = message.content[0].text
            else:
                # Fallback response when no authentication is available
                response_content = """Legal analysis service is currently being configured. 

For immediate legal assistance, please consult with a qualified attorney.

This API will provide comprehensive legal analysis including:
- Contract clause review and risk assessment
- Legal terminology explanations
- Regulatory compliance guidance
- Best practices recommendations

Please ensure proper authentication is configured to access Claude's advanced legal reasoning capabilities."""
            
            # Calculate processing time
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            
            self.query_count += 1
            
            return LegalQueryResponse(
                query_id=query_id,
                status="completed",
                response=response_content,
                processing_time=processing_time,
                timestamp=end_time.isoformat()
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Legal analysis failed: {str(e)}"
            )

# Initialize legal agent
legal_agent = LegalAgent()

# FastAPI app setup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🏛️ Legal Agent API Starting...")
    print(f"📊 Anthropic API Available: {ANTHROPIC_AVAILABLE}")
    print(f"🔐 Authentication Method: {getattr(legal_agent, 'auth_method', 'NONE')}")
    print(f"🔑 API Key Configured: {'Yes' if os.getenv('ANTHROPIC_API_KEY') else 'No'}")
    yield
    # Shutdown
    print("🏛️ Legal Agent API Shutting down...")

app = FastAPI(
    title="Claude Legal Agent API",
    description="Professional legal analysis powered by Claude",
    version="2.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    api_key_available = bool(os.getenv('ANTHROPIC_API_KEY'))
    
    return {
        "status": "healthy",
        "anthropic_api": "available" if ANTHROPIC_AVAILABLE else "unavailable",
        "authentication": "configured" if api_key_available else "missing",
        "auth_method": getattr(legal_agent, 'auth_method', 'NONE'),
        "queries_processed": legal_agent.query_count,
        "timestamp": datetime.now().isoformat(),
        "note": "Set ANTHROPIC_API_KEY environment variable for full functionality"
    }

@app.post("/legal/query", response_model=LegalQueryResponse)
async def process_legal_query(request: LegalQueryRequest):
    """Process general legal analysis query"""
    return await legal_agent.process_legal_query(request)

@app.post("/legal/contract-review", response_model=LegalQueryResponse)
async def contract_review(request: LegalQueryRequest):
    """Specialized contract review endpoint"""
    # Add contract-specific context
    enhanced_request = LegalQueryRequest(
        query=f"CONTRACT REVIEW: {request.query}",
        context=f"Contract Analysis Context: {request.context or 'General contract review'}",
        max_turns=request.max_turns or 3
    )
    return await legal_agent.process_legal_query(enhanced_request)

@app.post("/legal/risk-assessment", response_model=LegalQueryResponse)
async def risk_assessment(request: LegalQueryRequest):
    """Legal risk assessment endpoint"""
    # Add risk assessment context
    enhanced_request = LegalQueryRequest(
        query=f"LEGAL RISK ASSESSMENT: {request.query}",
        context=f"Risk Analysis Context: {request.context or 'General risk assessment'}",
        max_turns=request.max_turns or 2
    )
    return await legal_agent.process_legal_query(enhanced_request)

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "Claude Legal Agent API v2.0",
        "status": "running",
        "authentication": "API_KEY" if os.getenv('ANTHROPIC_API_KEY') else "REQUIRED",
        "endpoints": {
            "health": "/health",
            "legal_query": "/legal/query",
            "contract_review": "/legal/contract-review", 
            "risk_assessment": "/legal/risk-assessment"
        },
        "setup_note": "Configure ANTHROPIC_API_KEY environment variable for full functionality"
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 Starting Legal Agent API v2.0 on port {port}")
    print(f"🔑 API Key: {'Configured' if os.getenv('ANTHROPIC_API_KEY') else 'Missing - Set ANTHROPIC_API_KEY'}")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=port,
        log_level="info"
    )