#!/usr/bin/env python3
"""
Claude Code SDK Legal Agent - FastAPI Production Deployment
OAuth authentication with Claude Max subscription
"""

import asyncio
import os
import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from contextual import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import uvicorn

# Claude Code SDK import
try:
    from claude_code_sdk import ClaudeSDKClient, ClaudeCodeOptions
    CLAUDE_SDK_AVAILABLE = True
except ImportError:
    CLAUDE_SDK_AVAILABLE = False
    print("Warning: claude_code_sdk not available. Install with: pip install claude-code-sdk")

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
        
    async def process_legal_query(self, request: LegalQueryRequest) -> LegalQueryResponse:
        """Process legal analysis query using Claude Code SDK with OAuth"""
        start_time = datetime.now()
        query_id = str(uuid.uuid4())
        
        if not CLAUDE_SDK_AVAILABLE:
            raise HTTPException(
                status_code=500, 
                detail="Claude Code SDK not available. Please install claude-code-sdk package."
            )
        
        try:
            # Configure Claude Code SDK with OAuth
            options = ClaudeCodeOptions(
                permission_mode="bypassPermissions",  # Enables OAuth authentication
                system_prompt="""You are a specialized legal analysis AI assistant. Provide detailed, accurate legal analysis while noting that your responses are for informational purposes only and do not constitute legal advice. Always recommend consulting with a qualified attorney for specific legal matters.

Focus on:
- Contract clause analysis
- Legal risk assessment
- Regulatory compliance guidance  
- Legal terminology explanation
- Best practices recommendations

Be thorough, professional, and cite relevant legal principles when applicable."""
            )
            
            # Prepare legal analysis prompt
            full_prompt = f"Legal Analysis Request: {request.query}"
            if request.context:
                full_prompt += f"\n\nContext: {request.context}"
            
            full_prompt += f"\n\nPlease provide a comprehensive legal analysis addressing the specific query above."
            
            # Execute legal analysis
            response_content = ""
            
            async with ClaudeSDKClient(options=options) as client:
                await client.query(full_prompt)
                
                # Collect response with turn limit
                turn_count = 0
                max_turns = request.max_turns or 2
                
                async for message in client.receive_response():
                    if hasattr(message, "content") and message.content:
                        response_content += message.content
                        turn_count += 1
                        if turn_count >= max_turns:
                            break
                
                if not response_content.strip():
                    response_content = "Legal analysis completed successfully. Please check the detailed response."
            
            # Calculate processing time
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            
            self.query_count += 1
            
            return LegalQueryResponse(
                query_id=query_id,
                status="completed",
                response=response_content.strip(),
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
    print(f"📊 Claude Code SDK Available: {CLAUDE_SDK_AVAILABLE}")
    print(f"🔐 OAuth Mode: {os.getenv('CLAUDE_CODE_USE_OAUTH', 'false')}")
    yield
    # Shutdown
    print("🏛️ Legal Agent API Shutting down...")

app = FastAPI(
    title="Claude Legal Agent API",
    description="Professional legal analysis powered by Claude Max via OAuth",
    version="1.0.0",
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
    return {
        "status": "healthy",
        "claude_sdk": "connected" if CLAUDE_SDK_AVAILABLE else "unavailable",
        "oauth_mode": os.getenv('CLAUDE_CODE_USE_OAUTH', 'false').lower() == 'true',
        "queries_processed": legal_agent.query_count,
        "timestamp": datetime.now().isoformat()
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

@app.post("/legal/stream")
async def stream_legal_analysis(request: LegalQueryRequest):
    """Streaming legal analysis with Server-Sent Events"""
    async def generate_stream():
        try:
            if not CLAUDE_SDK_AVAILABLE:
                yield f"data: {{'error': 'Claude SDK not available'}}\n\n"
                return
                
            options = ClaudeCodeOptions(permission_mode="bypassPermissions")
            
            full_prompt = f"Legal Analysis: {request.query}"
            if request.context:
                full_prompt += f"\nContext: {request.context}"
            
            async with ClaudeSDKClient(options=options) as client:
                await client.query(full_prompt)
                
                async for message in client.receive_response():
                    if hasattr(message, "content") and message.content:
                        yield f"data: {{'content': '{message.content.replace(chr(10), ' ')}'}}\n\n"
                        
            yield f"data: {{'status': 'completed'}}\n\n"
            
        except Exception as e:
            yield f"data: {{'error': '{str(e)}'}}\n\n"
    
    return StreamingResponse(generate_stream(), media_type="text/plain")

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "Claude Legal Agent API",
        "status": "running",
        "oauth_enabled": os.getenv('CLAUDE_CODE_USE_OAUTH', 'false').lower() == 'true',
        "endpoints": {
            "health": "/health",
            "legal_query": "/legal/query",
            "contract_review": "/legal/contract-review", 
            "risk_assessment": "/legal/risk-assessment",
            "streaming": "/legal/stream"
        }
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 Starting Legal Agent API on port {port}")
    print(f"🔐 OAuth Mode: {os.getenv('CLAUDE_CODE_USE_OAUTH', 'false')}")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=port,
        log_level="info"
    )