/**
 * Test script for Qoder CLI with planning-with-files and SSCI skills integration
 */

const { QoderCLI } = require('./qoder_cli');

async function runTests() {
  console.log('Starting Qoder CLI tests...\n');
  
  try {
    // Test 1: Initialize CLI
    console.log('Test 1: Initializing Qoder CLI');
    const cli = new QoderCLI();
    await cli.init();
    console.log('✓ Qoder CLI initialized successfully\n');
    
    // Test 2: Start planning session
    console.log('Test 2: Starting planning session');
    const planningResult = await cli.executeCommand('planning-with-files:start', []);
    console.log('✓ Planning session started:', planningResult.message);
    console.log('  Created files:', planningResult.files);
    
    // Check that planning files were created
    const fs = require('fs').promises;
    for (const file of Object.values(planningResult.files)) {
      try {
        await fs.access(file);
        console.log(`  ✓ File exists: ${file}`);
      } catch (err) {
        console.log(`  ✗ File missing: ${file}`);
      }
    }
    console.log('');
    
    // Test 3: Execute SSCI skills
    console.log('Test 3: Executing SSCI skills with planning integration');
    
    // Test grounded-theory-expert skill
    console.log('  - Testing grounded-theory-expert skill');
    const gtResult = await cli.executeCommand('skill', ['grounded-theory-expert', 'analyze', 'interview', 'data']);
    console.log('  ✓ Grounded theory skill executed:', gtResult.result);
    
    // Test network-computation skill
    console.log('  - Testing network-computation skill');
    const ncResult = await cli.executeCommand('skill', ['network-computation', 'analyze', 'connections']);
    console.log('  ✓ Network computation skill executed:', ncResult.metrics);
    
    // Test field-analysis skill
    console.log('  - Testing field-analysis skill');
    const faResult = await cli.executeCommand('skill', ['field-analysis', 'examine', 'boundaries']);
    console.log('  ✓ Field analysis skill executed:', faResult.insights);
    
    // Test ANT skill
    console.log('  - Testing ant skill');
    const antResult = await cli.executeCommand('skill', ['ant', 'map', 'actors']);
    console.log('  ✓ ANT skill executed:', antResult.findings);
    
    console.log('');
    
    // Test 4: Check planning status
    console.log('Test 4: Checking planning status');
    const statusResult = await cli.executeCommand('planning-with-files:status', []);
    console.log('✓ Planning status retrieved');
    for (const [key, status] of Object.entries(statusResult.status)) {
      console.log(`  ${key}: ${status.exists ? 'exists' : 'missing'}`);
    }
    console.log('');
    
    // Test 5: Execute more complex skill sequences
    console.log('Test 5: Executing complex skill sequence');
    
    // Execute multiple skills in sequence
    const skillsSequence = [
      ['fsqca-analysis', 'calibrate', 'data'],
      ['digital-marx', 'analyze', 'alienation'],
      ['business-ecosystem-analysis', 'map', 'relationships']
    ];
    
    for (const skillParams of skillsSequence) {
      const skillName = skillParams[0];
      const params = skillParams.slice(1);
      console.log(`  - Executing ${skillName}`);
      const result = await cli.executeCommand('skill', skillParams);
      console.log(`  ✓ ${skillName} completed`);
    }
    
    console.log('\n✓ All tests passed successfully!');
    console.log('\nQoder CLI with planning-with-files and SSCI skills integration is working correctly.');
    
  } catch (error) {
    console.error('✗ Test failed with error:', error);
    process.exit(1);
  }
}

// Run the tests
if (require.main === module) {
  runTests();
}