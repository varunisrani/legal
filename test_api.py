#!/usr/bin/env python3
"""
Test client for Claude Legal Agent API
"""

import requests
import json
from typing import Dict, Any

class LegalAgentClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
    
    def health_check(self) -> Dict[str, Any]:
        """Test health endpoint"""
        response = requests.get(f"{self.base_url}/health")
        return response.json()
    
    def query_legal_analysis(self, query: str, context: str = None, max_turns: int = 2) -> Dict[str, Any]:
        """Send legal query and get analysis"""
        payload = {
            "query": query,
            "context": context,
            "max_turns": max_turns
        }
        
        response = requests.post(
            f"{self.base_url}/legal/query",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        return response.json()
    
    def contract_review(self, contract_clause: str, context: str = None) -> Dict[str, Any]:
        """Specialized contract review"""
        payload = {
            "query": contract_clause,
            "context": context,
            "max_turns": 3
        }
        
        response = requests.post(
            f"{self.base_url}/legal/contract-review",
            json=payload
        )
        
        return response.json()
    
    def risk_assessment(self, risk_query: str, context: str = None) -> Dict[str, Any]:
        """Legal risk assessment"""
        payload = {
            "query": risk_query,
            "context": context,
            "max_turns": 2
        }
        
        response = requests.post(
            f"{self.base_url}/legal/risk-assessment",
            json=payload
        )
        
        return response.json()

def run_tests():
    """Run comprehensive API tests"""
    client = LegalAgentClient()
    
    print("Testing Claude Legal Agent API")
    print("=" * 50)
    
    # Test 1: Health Check
    print("\n1. Health Check:")
    try:
        health = client.health_check()
        print(f"Health: {health['status']}")
        print(f"   Claude SDK: {health['claude_sdk']}")
        print(f"   OAuth Mode: {health['oauth_mode']}")
    except Exception as e:
        print(f"Health check failed: {e}")
    
    # Test 2: Basic Legal Query
    print("\n2. Basic Legal Query:")
    try:
        result = client.query_legal_analysis(
            query="What are the legal implications of unlimited liability clauses?",
            context="Software licensing agreement"
        )
        print(f"Query ID: {result.get('query_id', 'N/A')}")
        print(f"   Status: {result.get('status', 'N/A')}")
        print(f"   Processing Time: {result.get('processing_time', 0):.2f}s")
        if 'response' in result:
            print(f"   Response Preview: {result['response'][:200]}...")
    except Exception as e:
        print(f"Legal query failed: {e}")
    
    # Test 3: Contract Review
    print("\n3. Contract Review:")
    try:
        result = client.contract_review(
            contract_clause="The licensee agrees to unlimited liability for any damages arising from use of the software, including indirect, consequential, and punitive damages.",
            context="SaaS licensing agreement"
        )
        print(f"Query ID: {result.get('query_id', 'N/A')}")
        print(f"   Status: {result.get('status', 'N/A')}")
        if 'response' in result:
            print(f"   Response Preview: {result['response'][:200]}...")
    except Exception as e:
        print(f"Contract review failed: {e}")
    
    # Test 4: Risk Assessment
    print("\n4. Risk Assessment:")
    try:
        result = client.risk_assessment(
            risk_query="Evaluate the risks of operating a SaaS business without terms of service",
            context="Startup business planning"
        )
        print(f"Query ID: {result.get('query_id', 'N/A')}")
        print(f"   Status: {result.get('status', 'N/A')}")
        if 'response' in result:
            print(f"   Response Preview: {result['response'][:200]}...")
    except Exception as e:
        print(f"Risk assessment failed: {e}")

def test_production_url(url: str):
    """Test against production URL"""
    print(f"\nTesting Production URL: {url}")
    client = LegalAgentClient(base_url=url)
    
    try:
        health = client.health_check()
        print(f"Production Health: {health['status']}")
        
        # Quick test query
        result = client.query_legal_analysis(
            query="What is a force majeure clause?",
            max_turns=1
        )
        print(f"Production Query: {result.get('status', 'N/A')}")
        print(f"   Processing Time: {result.get('processing_time', 0):.2f}s")
        
    except Exception as e:
        print(f"Production test failed: {e}")

if __name__ == "__main__":
    # Run local tests
    run_tests()
    
    # Uncomment to test production URL
    # test_production_url("https://your-app-name.onrender.com")