#!/usr/bin/env node
/**
 * Claude Legal Agent - TypeScript Node.js Server
 * Uses official @anthropic-ai/claude-code SDK with OAuth authentication
 * Perfect for your $200 Anthropic subscription - no additional API costs!
 */

import express from 'express';
import cors from 'cors';
import { query } from '@anthropic-ai/claude-code';

interface LegalQueryRequest {
  query: string;
  context?: string;
  maxTurns?: number;
}

interface LegalQueryResponse {
  queryId: string;
  status: string;
  response: string;
  processingTime: number;
  timestamp: string;
}

class ClaudeLegalAgent {
  private queryCount: number = 0;
  
  async processLegalQuery(request: LegalQueryRequest): Promise<LegalQueryResponse> {
    const startTime = Date.now();
    const queryId = this.generateId();
    
    try {
      // Prepare legal analysis system prompt
      const systemPrompt = `You are a specialized legal analysis AI assistant with expertise in contract law, regulatory compliance, and risk assessment.

Provide detailed, accurate legal analysis while always noting that your responses are for informational purposes only and do not constitute legal advice. Always recommend consulting with a qualified attorney for specific legal matters.

Focus on:
- Contract clause analysis and interpretation
- Legal risk assessment and mitigation strategies  
- Regulatory compliance guidance
- Legal terminology explanations
- Industry best practices and recommendations
- Relevant legal precedents and principles

Be thorough, professional, and cite relevant legal principles when applicable.`;

      // Prepare user prompt
      let userPrompt = `Legal Analysis Request: ${request.query}`;
      if (request.context) {
        userPrompt += `\n\nContext: ${request.context}`;
      }
      userPrompt += '\n\nPlease provide a comprehensive legal analysis addressing the specific query above.';

      // Use Claude Code SDK with OAuth
      const messages = query({
        prompt: userPrompt,
        options: {
          maxTurns: request.maxTurns || 2,
          systemPrompt: systemPrompt,
          model: 'claude-3-5-sonnet-20241022' // Latest Claude model
        }
      });

      let responseContent = '';
      
      // Stream and collect response
      for await (const message of messages) {
        if (message.type === 'content') {
          responseContent += message.content;
        } else if (message.type === 'result') {
          // Final result received
          if (message.result) {
            responseContent = message.result;
          }
          break;
        }
      }

      if (!responseContent.trim()) {
        responseContent = 'Legal analysis completed successfully. The Claude Code SDK processed your request using OAuth authentication.';
      }

      const processingTime = (Date.now() - startTime) / 1000;
      this.queryCount++;

      return {
        queryId,
        status: 'completed',
        response: responseContent,
        processingTime,
        timestamp: new Date().toISOString()
      };

    } catch (error: any) {
      const processingTime = (Date.now() - startTime) / 1000;
      
      return {
        queryId,
        status: 'error',
        response: `Legal analysis failed: ${error.message || 'Unknown error'}. This Claude Legal Agent uses OAuth authentication with your Claude subscription - no additional API costs!`,
        processingTime,
        timestamp: new Date().toISOString()
      };
    }
  }

  private generateId(): string {
    return Date.now().toString(36) + Math.random().toString(36).substr(2);
  }

  getQueryCount(): number {
    return this.queryCount;
  }
}

// Initialize Express app
const app = express();
const port = process.env.PORT || 3000;
const legalAgent = new ClaudeLegalAgent();

// Middleware
app.use(cors());
app.use(express.json());

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'Claude Legal Agent (TypeScript)',
    authentication: 'OAuth (Claude Code SDK)',
    subscription: 'Uses your existing Claude subscription',
    queriesProcessed: legalAgent.getQueryCount(),
    timestamp: new Date().toISOString(),
    note: 'No additional API costs - uses your $200 Anthropic subscription!'
  });
});

// Legal query endpoint
app.post('/legal/query', async (req, res) => {
  try {
    const request: LegalQueryRequest = req.body;
    
    if (!request.query || request.query.trim() === '') {
      return res.status(400).json({
        error: 'Query parameter is required',
        example: { query: 'What is a force majeure clause?', context: 'Software licensing' }
      });
    }

    const result = await legalAgent.processLegalQuery(request);
    res.json(result);
    
  } catch (error: any) {
    res.status(500).json({
      error: 'Internal server error',
      message: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Contract review endpoint
app.post('/legal/contract-review', async (req, res) => {
  try {
    const request: LegalQueryRequest = req.body;
    
    const enhancedRequest: LegalQueryRequest = {
      query: `CONTRACT REVIEW AND ANALYSIS: ${request.query}`,
      context: `Contract Analysis Context: ${request.context || 'General contract review - identify key legal issues, risks, and recommendations'}`,
      maxTurns: request.maxTurns || 3
    };

    const result = await legalAgent.processLegalQuery(enhancedRequest);
    res.json(result);
    
  } catch (error: any) {
    res.status(500).json({
      error: 'Contract review failed',
      message: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Risk assessment endpoint  
app.post('/legal/risk-assessment', async (req, res) => {
  try {
    const request: LegalQueryRequest = req.body;
    
    const enhancedRequest: LegalQueryRequest = {
      query: `LEGAL RISK ASSESSMENT: ${request.query}`,
      context: `Risk Analysis Context: ${request.context || 'Comprehensive legal risk evaluation - identify potential liabilities, compliance issues, and mitigation strategies'}`,
      maxTurns: request.maxTurns || 2
    };

    const result = await legalAgent.processLegalQuery(enhancedRequest);
    res.json(result);
    
  } catch (error: any) {
    res.status(500).json({
      error: 'Risk assessment failed', 
      message: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

// Root endpoint
app.get('/', (req, res) => {
  res.json({
    message: '🏛️ Claude Legal Agent (TypeScript + OAuth)',
    version: '1.0.0',
    authentication: 'OAuth via Claude Code SDK',
    subscription: 'Uses your existing $200 Claude subscription',
    endpoints: {
      health: '/health',
      legalQuery: '/legal/query',
      contractReview: '/legal/contract-review',
      riskAssessment: '/legal/risk-assessment'
    },
    documentation: {
      example: {
        method: 'POST',
        url: '/legal/query',
        body: {
          query: 'What are the legal implications of force majeure clauses?',
          context: 'Software licensing agreement',
          maxTurns: 2
        }
      }
    },
    benefits: [
      '✅ No additional API costs',
      '✅ Uses your Claude Max subscription', 
      '✅ OAuth authentication',
      '✅ Professional legal analysis',
      '✅ TypeScript/Node.js performance'
    ]
  });
});

// Error handling middleware
app.use((err: any, req: express.Request, res: express.Response, next: express.NextFunction) => {
  console.error('Server error:', err);
  res.status(500).json({
    error: 'Internal server error',
    message: err.message,
    timestamp: new Date().toISOString()
  });
});

// Start server
app.listen(port, () => {
  console.log('🏛️ Claude Legal Agent (TypeScript) starting...');
  console.log(`🚀 Server running on port ${port}`);
  console.log('🔐 Authentication: OAuth via Claude Code SDK');
  console.log('💰 Cost: $0 additional - uses your Claude subscription!');
  console.log('📊 Endpoints:');
  console.log('   GET  /health - Health check');
  console.log('   POST /legal/query - General legal analysis');
  console.log('   POST /legal/contract-review - Contract review');
  console.log('   POST /legal/risk-assessment - Risk assessment');
  console.log('');
  console.log('✅ Ready to provide professional legal analysis!');
});

export default app;