#!/usr/bin/env python3
"""
Claude Legal Agent - Final Production Version
Uses Anthropic API directly since Claude CLI is not available on Render
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

# Try to import anthropic
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

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

class ClaudeLegalAgent:
    def __init__(self):
        self.query_count = 0
        
        # Try to get API key from environment
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if api_key and ANTHROPIC_AVAILABLE:
            self.client = anthropic.Anthropic(api_key=api_key)
            self.available = True
        else:
            self.client = None
            self.available = False
        
    async def process_legal_query(self, request: LegalQueryRequest) -> LegalQueryResponse:
        """Process legal analysis using Claude"""
        start_time = datetime.now()
        query_id = str(uuid.uuid4())
        
        if not self.available:
            # Return informative response about setup
            response_content = f"""🏛️ **Claude Legal Agent Setup Required**

Your legal analysis API is deployed and running, but requires authentication configuration.

**To enable full Claude Max legal analysis:**
1. Go to your Render dashboard
2. Add environment variable: `ANTHROPIC_API_KEY`
3. Set the value to your Anthropic API key

**Your Query:** {request.query}
{f'**Context:** {request.context}' if request.context else ''}

**What this API will provide once configured:**
- Professional legal analysis powered by Claude
- Contract clause review and risk assessment  
- Regulatory compliance guidance
- Legal terminology explanations
- Best practices recommendations

**Note:** All responses are for informational purposes only and do not constitute legal advice. Always consult with a qualified attorney for specific legal matters.

🔗 Get your API key: https://console.anthropic.com/"""
            
        else:
            try:
                # Prepare legal system prompt
                system_prompt = """You are a specialized legal analysis AI assistant with expertise in contract law, regulatory compliance, and risk assessment. 

Provide detailed, accurate legal analysis while always noting that your responses are for informational purposes only and do not constitute legal advice. Always recommend consulting with a qualified attorney for specific legal matters.

Focus on:
- Contract clause analysis and interpretation
- Legal risk assessment and mitigation strategies
- Regulatory compliance guidance
- Legal terminology explanations
- Industry best practices and recommendations
- Relevant legal precedents and principles

Be thorough, professional, and cite relevant legal principles when applicable. Structure your responses clearly with headings and bullet points where appropriate."""

                # Prepare the user message
                user_message = f"**Legal Analysis Request:** {request.query}"
                if request.context:
                    user_message += f"\n\n**Context:** {request.context}"
                
                user_message += "\n\nPlease provide a comprehensive legal analysis addressing the specific query above."

                # Make API call to Claude
                message = self.client.messages.create(
                    model="claude-3-5-sonnet-20241022",  # Latest Claude model
                    max_tokens=4000,
                    system=system_prompt,
                    messages=[
                        {
                            "role": "user", 
                            "content": user_message
                        }
                    ]
                )
                
                response_content = message.content[0].text
                
            except Exception as e:
                response_content = f"""⚠️ **Legal Analysis Service Error**

An error occurred while processing your legal query: {str(e)}

**Your Query:** {request.query}
{f'**Context:** {request.context}' if request.context else ''}

**Troubleshooting Steps:**
1. Verify ANTHROPIC_API_KEY is set in Render environment variables
2. Check API key is valid and has sufficient credits
3. Ensure network connectivity to Anthropic servers

**For immediate legal assistance, please consult with a qualified attorney.**

This is a temporary service issue - your legal analysis API is properly configured and will resume normal operation once resolved."""

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

# Initialize legal agent
legal_agent = ClaudeLegalAgent()

# FastAPI app setup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🏛️ Claude Legal Agent API Starting...")
    print(f"📊 Anthropic Available: {ANTHROPIC_AVAILABLE}")
    print(f"🔑 API Key Configured: {'Yes' if os.getenv('ANTHROPIC_API_KEY') else 'No'}")
    print(f"✅ Agent Available: {legal_agent.available}")
    yield
    # Shutdown
    print("🏛️ Legal Agent API Shutting down...")

app = FastAPI(
    title="Claude Legal Agent API",
    description="Professional legal analysis powered by Claude - Production Ready",
    version="3.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "anthropic_available": ANTHROPIC_AVAILABLE,
        "claude_configured": legal_agent.available,
        "api_key_set": bool(os.getenv('ANTHROPIC_API_KEY')),
        "queries_processed": legal_agent.query_count,
        "timestamp": datetime.now().isoformat(),
        "setup_required": "Set ANTHROPIC_API_KEY environment variable" if not legal_agent.available else "Ready for legal analysis"
    }

@app.post("/legal/query", response_model=LegalQueryResponse)
async def process_legal_query(request: LegalQueryRequest):
    """Process general legal analysis query"""
    return await legal_agent.process_legal_query(request)

@app.post("/legal/contract-review", response_model=LegalQueryResponse)  
async def contract_review(request: LegalQueryRequest):
    """Specialized contract review endpoint"""
    enhanced_request = LegalQueryRequest(
        query=f"CONTRACT REVIEW AND ANALYSIS: {request.query}",
        context=f"Contract Analysis Context: {request.context or 'General contract review - please identify key legal issues, risks, and recommendations'}",
        max_turns=request.max_turns or 3
    )
    return await legal_agent.process_legal_query(enhanced_request)

@app.post("/legal/risk-assessment", response_model=LegalQueryResponse)
async def risk_assessment(request: LegalQueryRequest):
    """Legal risk assessment endpoint"""
    enhanced_request = LegalQueryRequest(
        query=f"LEGAL RISK ASSESSMENT: {request.query}",
        context=f"Risk Analysis Context: {request.context or 'Comprehensive legal risk evaluation - identify potential liabilities, compliance issues, and mitigation strategies'}",
        max_turns=request.max_turns or 2
    )
    return await legal_agent.process_legal_query(enhanced_request)

@app.get("/")
async def root():
    """API root endpoint with setup instructions"""
    return {
        "message": "🏛️ Claude Legal Agent API v3.0",
        "status": "running",
        "claude_available": legal_agent.available,
        "endpoints": {
            "health": "/health",
            "legal_query": "/legal/query",
            "contract_review": "/legal/contract-review",
            "risk_assessment": "/legal/risk-assessment",
            "api_docs": "/docs"
        },
        "setup_instructions": {
            "step_1": "Add ANTHROPIC_API_KEY to Render environment variables",
            "step_2": "Get API key from https://console.anthropic.com/",
            "step_3": "Redeploy service after adding the key",
            "note": "API will work immediately after configuration"
        } if not legal_agent.available else {
            "status": "✅ Ready for professional legal analysis",
            "note": "All endpoints are fully functional"
        }
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 Starting Claude Legal Agent API v3.0 on port {port}")
    
    if legal_agent.available:
        print("✅ Claude configured - Ready for legal analysis")
    else:
        print("⚠️ Setup required - Add ANTHROPIC_API_KEY environment variable")
    
    uvicorn.run(
        app,
        host="0.0.0.0", 
        port=port,
        log_level="info"
    )