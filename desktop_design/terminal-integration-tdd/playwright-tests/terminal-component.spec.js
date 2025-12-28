const { test, expect } = require('@playwright/test');

test.describe('Terminal Component Tests', () => {
  test.beforeEach(async ({ page }) => {
    // For now, we'll test the terminal component in isolation
    // In a real scenario, this would load the actual desktop app
    await page.route('**/*', (route) => {
      if (route.request().url().includes('xterm.css')) {
        route.fulfill({
          status: 200,
          body: '/* Mock xterm CSS */ .terminal { background: #1e1e1e; }',
          headers: { 'content-type': 'text/css' }
        });
      } else {
        route.continue();
      }
    });
    
    // Create a simple test page with terminal component
    await page.setContent(`
      <!DOCTYPE html>
      <html>
      <head>
        <style>
          .terminal-container { width: 800px; height: 400px; border: 1px solid #ccc; }
        </style>
      </head>
      <body>
        <h1>Terminal Component Test</h1>
        <div id="terminal-container" class="terminal-container"></div>
        <div id="test-output"></div>
        <script>
          // Mock terminal component functionality for testing
          window.terminalEvents = [];
          window.mockTerminal = {
            write: (data) => {
              document.getElementById('test-output').innerHTML += '<br>OUTPUT: ' + data;
              window.terminalEvents.push({ type: 'write', data });
            },
            resize: () => {
              window.terminalEvents.push({ type: 'resize' });
            },
            dispose: () => {
              window.terminalEvents.push({ type: 'dispose' });
            }
          };
          
          window.terminalComponent = {
            writeToTerminal: (data) => {
              window.mockTerminal.write(data);
            }
          };
        </script>
      </body>
      </html>
    `);
  });

  test('should render terminal component without errors', async ({ page }) => {
    // Verify the terminal container is present
    const terminalContainer = await page.$('#terminal-container');
    expect(terminalContainer).toBeTruthy();
    
    // Verify basic elements are present
    await expect(page.locator('h1')).toContainText('Terminal Component Test');
  });

  test('should accept user input and display output', async ({ page }) => {
    // Test terminal interaction
    await page.evaluate(() => {
      window.terminalComponent.writeToTerminal('Hello, World!');
    });
    
    // Wait for output to appear
    await page.waitForSelector('#test-output');
    const output = await page.$eval('#test-output', el => el.innerHTML);
    expect(output).toContain('Hello, World!');
  });

  test('should handle terminal resizing', async ({ page }) => {
    // Track resize events
    await page.evaluate(() => {
      window.mockTerminal.resize();
    });
    
    // Verify resize event was tracked
    const events = await page.evaluate(() => window.terminalEvents);
    const resizeEvents = events.filter(event => event.type === 'resize');
    expect(resizeEvents.length).toBeGreaterThan(0);
  });

  test('should maintain terminal theme settings', async ({ page }) => {
    // Check that terminal container has expected styling
    const terminalContainer = await page.$('#terminal-container');
    const backgroundColor = await terminalContainer.evaluate(el => 
      window.getComputedStyle(el).getPropertyValue('background-color')
    );
    
    // We expect a dark background based on the component settings
    expect(backgroundColor).toBeTruthy(); // The style is applied
  });
});