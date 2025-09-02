#!/usr/bin/env node
/**
 * Test client for TypeScript Claude Legal Agent
 */

const axios = require('axios');

const BASE_URL = process.env.API_URL || 'http://localhost:3000';

async function testAPI() {
  console.log('🧪 Testing Claude Legal Agent (TypeScript)');
  console.log('=' .repeat(50));
  
  try {
    // Test 1: Health Check
    console.log('\n1. Health Check:');
    const healthResponse = await axios.get(`${BASE_URL}/health`);
    console.log(`✅ Status: ${healthResponse.data.status}`);
    console.log(`   Service: ${healthResponse.data.service}`);
    console.log(`   Authentication: ${healthResponse.data.authentication}`);
    console.log(`   Queries Processed: ${healthResponse.data.queriesProcessed}`);
    
    // Test 2: Legal Query
    console.log('\n2. Legal Query Test:');
    const queryResponse = await axios.post(`${BASE_URL}/legal/query`, {
      query: 'What is a force majeure clause?',
      context: 'Software licensing agreement',
      maxTurns: 1
    });
    
    console.log(`✅ Query ID: ${queryResponse.data.queryId}`);
    console.log(`   Status: ${queryResponse.data.status}`);
    console.log(`   Processing Time: ${queryResponse.data.processingTime}s`);
    console.log(`   Response Preview: ${queryResponse.data.response.substring(0, 200)}...`);
    
    // Test 3: Contract Review
    console.log('\n3. Contract Review Test:');
    const contractResponse = await axios.post(`${BASE_URL}/legal/contract-review`, {
      query: 'The licensee agrees to unlimited liability for any damages.',
      context: 'SaaS agreement'
    });
    
    console.log(`✅ Query ID: ${contractResponse.data.queryId}`);
    console.log(`   Status: ${contractResponse.data.status}`);
    console.log(`   Processing Time: ${contractResponse.data.processingTime}s`);
    
    // Test 4: Risk Assessment
    console.log('\n4. Risk Assessment Test:');
    const riskResponse = await axios.post(`${BASE_URL}/legal/risk-assessment`, {
      query: 'Operating without terms of service',
      context: 'SaaS startup'
    });
    
    console.log(`✅ Query ID: ${riskResponse.data.queryId}`);
    console.log(`   Status: ${riskResponse.data.status}`);
    
    console.log('\n🎉 All tests completed successfully!');
    console.log('💰 Using your Claude subscription - no additional API costs!');
    
  } catch (error) {
    console.error('❌ Test failed:', error.response?.data || error.message);
  }
}

// Run tests
if (require.main === module) {
  testAPI();
}

module.exports = { testAPI };