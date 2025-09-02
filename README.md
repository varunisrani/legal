# 🏛️ Claude Legal Agent API - Production Deployment

Professional legal analysis API powered by Claude Max with OAuth authentication.

## 🚀 **Quick Deploy to Render**

### **Step 1: Push to GitHub**
```bash
cd claude-legal-agent-deploy
git init
git add .
git commit -m "Claude Legal Agent with OAuth authentication"
git remote add origin https://github.com/YOUR_USERNAME/claude-legal-agent.git
git push -u origin main
```

### **Step 2: Deploy on Render**
1. Go to [render.com](https://render.com) and sign up/login
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Configure deployment:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python legal-agent-api.py`
   - **Environment Variables:**
     - `CLAUDE_CODE_USE_OAUTH=true`
     - `PORT=10000`

### **Step 3: Test Your Deployment**
Your API will be available at: `https://your-app-name.onrender.com`

## 📖 **API Endpoints**

### Health Check
```bash
GET /health
```

### Legal Analysis
```bash
POST /legal/query
{
  "query": "What are the risks of unlimited liability clauses?",
  "context": "Software licensing agreement",
  "max_turns": 2
}
```

### Contract Review  
```bash
POST /legal/contract-review
{
  "query": "The party agrees to indemnify and hold harmless...",
  "context": "Service agreement"
}
```

### Risk Assessment
```bash
POST /legal/risk-assessment
{
  "query": "Evaluate legal risks of this business model",
  "context": "Startup planning"
}
```

### Streaming Analysis
```bash
POST /legal/stream
# Returns Server-Sent Events
```

## 🔐 **OAuth Authentication**

This API uses Claude Code SDK with OAuth 2.0:
- ✅ No API keys required
- ✅ Uses your Claude Max subscription automatically  
- ✅ Secure server-to-server authentication
- ✅ Production-ready deployment

## 🧪 **Testing**

### Local Testing
```bash
# Install dependencies
pip install -r requirements.txt

# Run the API
python legal-agent-api.py

# Test in another terminal
python test_api.py
```

### Production Testing
```bash
# Test health endpoint
curl https://your-app.onrender.com/health

# Test legal query
curl -X POST "https://your-app.onrender.com/legal/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is a force majeure clause?", "max_turns": 1}'
```

## 🎯 **Usage Examples**

### Python Client
```python
import requests

response = requests.post(
    "https://your-app.onrender.com/legal/query",
    json={
        "query": "Is this non-compete clause enforceable?",
        "context": "California employment contract"
    }
)

result = response.json()
print(f"Legal Analysis: {result['response']}")
```

### JavaScript/Web
```javascript
const analyzeContract = async (query, context) => {
  const response = await fetch('https://your-app.onrender.com/legal/query', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, context })
  });
  
  const result = await response.json();
  return result.response;
};
```

### cURL
```bash
curl -X POST "https://your-app.onrender.com/legal/contract-review" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "The contractor shall indemnify and hold harmless...",
    "context": "Independent contractor agreement"
  }'
```

## ⚙️ **Configuration**

### Environment Variables
- `PORT`: Server port (default: 8000)
- `CLAUDE_CODE_USE_OAUTH`: Enable OAuth authentication (required: true)
- `ALLOWED_ORIGINS`: CORS origins for web integration

### Files Included
- `legal-agent-api.py` - Main FastAPI application
- `requirements.txt` - Python dependencies
- `render.yaml` - Render deployment configuration
- `test_api.py` - API testing client
- `.env.example` - Environment variables template

## 🔒 **Security Features**

- OAuth 2.0 with PKCE authentication
- No API keys stored in production
- CORS configuration for web security
- Input validation with Pydantic models
- Comprehensive error handling

## 📊 **Monitoring**

Built-in monitoring features:
- Health check endpoints
- Response time tracking
- Query ID for request tracing
- OAuth status reporting

## 🚀 **Ready for Production!**

Your Claude Legal Agent API is production-ready with:
- ✅ OAuth authentication
- ✅ Multiple specialized endpoints
- ✅ Streaming support
- ✅ Comprehensive error handling
- ✅ Production deployment configuration

Deploy to Render and start providing professional legal analysis with Claude Max! 🏛️⚖️