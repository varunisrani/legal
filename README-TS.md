# 🏛️ Claude Legal Agent - TypeScript Edition

Professional legal analysis API using **TypeScript Claude Code SDK** with **OAuth authentication**. 

## 💰 **No Additional Costs!**
- ✅ Uses your existing **$200 Claude subscription**
- ✅ OAuth authentication via Claude Code SDK  
- ✅ No API usage fees
- ✅ Full Claude Max reasoning power

## 🚀 **Quick Deploy to Render**

### **Step 1: Update Your Repository**
```bash
cd claude-legal-agent-deploy
git add .
git commit -m "TypeScript Claude Legal Agent with OAuth - no API costs!"
git push origin main
```

### **Step 2: Update Render Service**
1. Go to your Render dashboard: [render.com](https://render.com)
2. Select your **legal-grcn** service
3. Go to **Settings**
4. Update **Environment** to: `Node`
5. Update **Build Command** to: `npm install && npm run build`
6. Update **Start Command** to: `npm start`
7. Click **Deploy Latest Commit**

### **Step 3: Test Your API**
Your API will be at: `https://legal-grcn.onrender.com/`

## 📖 **API Endpoints**

### **Health Check**
```bash
GET /health
```
Response:
```json
{
  "status": "healthy",
  "service": "Claude Legal Agent (TypeScript)",
  "authentication": "OAuth (Claude Code SDK)",
  "subscription": "Uses your existing Claude subscription"
}
```

### **Legal Analysis**
```bash
POST /legal/query
{
  "query": "What are the risks of unlimited liability clauses?",
  "context": "Software licensing agreement", 
  "maxTurns": 2
}
```

### **Contract Review**
```bash
POST /legal/contract-review
{
  "query": "The party agrees to indemnify and hold harmless...",
  "context": "Service agreement"
}
```

### **Risk Assessment**
```bash
POST /legal/risk-assessment  
{
  "query": "Operating without terms of service",
  "context": "SaaS startup"
}
```

## 🔐 **OAuth Authentication**

The TypeScript Claude Code SDK automatically uses OAuth with your Claude subscription:
- ✅ **No API keys needed**
- ✅ **Uses Claude Max subscription**  
- ✅ **Secure OAuth 2.0 flow**
- ✅ **No additional billing**

## 🧪 **Testing**

### **Production Test**
```bash
# Test health
curl https://legal-grcn.onrender.com/health

# Test legal query  
curl -X POST "https://legal-grcn.onrender.com/legal/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is a force majeure clause?", "maxTurns": 1}'
```

### **Local Development**
```bash
# Install dependencies
npm install

# Run in development mode
npm run dev

# Test locally
node test-ts-api.js
```

## ⚡ **Performance Benefits**

### **TypeScript Advantages:**
- ✅ **Native Node.js performance**
- ✅ **Type safety and IntelliSense**
- ✅ **Smaller memory footprint**
- ✅ **Better error handling**

### **Claude Code SDK Benefits:**
- ✅ **Direct Claude Max access**
- ✅ **Built-in OAuth handling**
- ✅ **Streaming responses**
- ✅ **Session management**

## 💡 **Usage Examples**

### **JavaScript/Node.js Client**
```javascript
const axios = require('axios');

const client = axios.create({
  baseURL: 'https://legal-grcn.onrender.com'
});

// Analyze contract clause
async function reviewContract(clause, context) {
  const response = await client.post('/legal/contract-review', {
    query: clause,
    context: context
  });
  
  return response.data.response;
}

// Usage
const analysis = await reviewContract(
  'The contractor shall indemnify and hold harmless...',
  'Independent contractor agreement'
);
console.log(analysis);
```

### **Python Client**
```python
import requests

def analyze_legal_issue(query, context=None):
    response = requests.post(
        'https://legal-grcn.onrender.com/legal/query',
        json={
            'query': query,
            'context': context,
            'maxTurns': 2
        }
    )
    return response.json()

# Usage
result = analyze_legal_issue(
    "What are data retention requirements for GDPR?",
    "E-commerce website"
)
print(result['response'])
```

### **cURL Examples**
```bash
# Risk assessment
curl -X POST "https://legal-grcn.onrender.com/legal/risk-assessment" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the legal risks of AI content generation?",
    "context": "Software company using AI"
  }'
```

## 🔧 **Architecture**

```
Client Request → Express.js → Claude Code SDK → OAuth → Claude Max → Response
```

### **Key Components:**
- **Express.js**: Fast Node.js web framework
- **TypeScript**: Type safety and better DX
- **Claude Code SDK**: Official Anthropic SDK
- **OAuth 2.0**: Secure authentication
- **Claude Max**: Advanced AI reasoning

## ✅ **Why This Approach Wins**

### **Cost Efficient:**
- 💰 **$0 additional costs** - uses your existing subscription
- 🚀 **Claude Max performance** - no API rate limits
- 🔐 **Enterprise OAuth** - secure and scalable

### **Developer Friendly:**
- 🛠️ **TypeScript support** - better development experience  
- 📦 **Simple deployment** - works on any Node.js platform
- 🔄 **Easy maintenance** - official SDK with updates

### **Production Ready:**
- ⚡ **High performance** - Node.js async processing
- 🛡️ **Error handling** - comprehensive error responses
- 📊 **Monitoring** - health checks and metrics

## 🎯 **Perfect For:**
- ✅ Legal analysis applications
- ✅ Contract review automation  
- ✅ Compliance checking tools
- ✅ Risk assessment platforms
- ✅ Legal document processing

**Your Claude Legal Agent is now powered by TypeScript + OAuth, using your existing $200 subscription with zero additional costs!** 🎉🏛️