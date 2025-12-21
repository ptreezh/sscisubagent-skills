import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';
import './components/OnboardingFlow.css';
import './components/StigmergyConsole.css';
import './components/SkillConfiguration.css';
import './components/FileBrowser.css';
import './components/FileViewer.css';
import './components/HelpDocumentation.css';
import './components/ProjectCreationWizard.css';
import './components/UserPreferences.css';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);