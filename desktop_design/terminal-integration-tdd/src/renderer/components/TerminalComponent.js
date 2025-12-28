import React, { useEffect, useRef } from 'react';
import { Terminal } from '@xterm/xterm';
import { FitAddon } from '@xterm/addon-fit';
import '@xterm/xterm/css/xterm.css';

const TerminalComponent = ({ terminalId, onData }) => {
  const terminalRef = useRef(null);
  const termRef = useRef(null);
  const fitAddonRef = useRef(null);

  useEffect(() => {
    // Create terminal instance
    const term = new Terminal({
      cursorBlink: true,
      theme: {
        background: '#1e1e1e',
        foreground: '#d4d4d4'
      }
    });
    
    // Load fit addon for resizing
    const fitAddon = new FitAddon();
    term.loadAddon(fitAddon);
    
    // Store references
    termRef.current = term;
    fitAddonRef.current = fitAddon;
    
    // Open terminal in container
    if (terminalRef.current) {
      term.open(terminalRef.current);
      fitAddon.fit();
    }
    
    // Listen for data from terminal
    term.onData((data) => {
      if (onData) {
        onData(terminalId, data);
      }
    });
    
    // Handle window resize
    const handleResize = () => {
      fitAddon.fit();
    };
    
    window.addEventListener('resize', handleResize);
    
    // Cleanup
    return () => {
      window.removeEventListener('resize', handleResize);
      term.dispose();
    };
  }, [terminalId, onData]);
  
  // Expose methods to parent component
  useEffect(() => {
    if (termRef.current && fitAddonRef.current) {
      // Method to write data to terminal
      TerminalComponent.writeToTerminal = (data) => {
        termRef.current.write(data);
      };
      
      // Method to resize terminal
      TerminalComponent.resizeTerminal = () => {
        fitAddonRef.current.fit();
      };
    }
  }, []);
  
  return (
    &lt;div className="terminal-container"&gt;
      &lt;div ref={terminalRef} className="terminal" /&gt;
    &lt;/div&gt;
  );
};

export default TerminalComponent;