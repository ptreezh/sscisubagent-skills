import React, { useState, useEffect } from 'react';

const OnboardingFlow = ({ onComplete }) => {
  const [step, setStep] = useState(1);
  const [completedSteps, setCompletedSteps] = useState([]);

  const steps = [
    {
      id: 1,
      title: '欢迎使用 Stigmergy 桌面应用',
      content: '这是一个为技术小白用户设计的图形化界面，让您无需接触命令行就能使用强大的 Stigmergy 功能。',
      image: null // We could add illustrations here
    },
    {
      id: 2,
      title: '什么是技能？',
      content: '技能是预先编写好的功能模块，可以帮助您完成特定任务，比如文献综述、数据分析等。您可以在技能管理页面查看和管理所有技能。',
      image: null
    },
    {
      id: 3,
      title: '什么是项目？',
      content: '项目是您工作的文件夹，包含所有相关的文档和数据。您可以在项目管理页面创建和管理项目。',
      image: null
    },
    {
      id: 4,
      title: '开始使用',
      content: '现在您已经了解了基本概念，可以开始使用应用了。如果需要帮助，可以随时点击右下角的帮助按钮。',
      image: null
    }
  ];

  const currentStep = steps.find(s => s.id === step);

  const handleNext = () => {
    if (step < steps.length) {
      setCompletedSteps([...completedSteps, step]);
      setStep(step + 1);
    } else {
      onComplete();
    }
  };

  const handlePrev = () => {
    if (step > 1) {
      setStep(step - 1);
    }
  };

  const handleSkip = () => {
    onComplete();
  };

  return (
    <div className="onboarding-overlay">
      <div className="onboarding-modal card">
        <div className="onboarding-header">
          <h2>{currentStep.title}</h2>
          <button className="onboarding-close btn" onClick={handleSkip}>跳过</button>
        </div>
        
        <div className="onboarding-content">
          <p>{currentStep.content}</p>
          
          {currentStep.image && (
            <div className="onboarding-image">
              {/* Image would go here */}
            </div>
          )}
        </div>
        
        <div className="onboarding-footer">
          <div className="onboarding-progress">
            {steps.map((s) => (
              <div 
                key={s.id} 
                className={`progress-step ${step >= s.id ? 'active' : ''} ${completedSteps.includes(s.id) ? 'completed' : ''}`}
              ></div>
            ))}
          </div>
          
          <div className="onboarding-actions">
            {step > 1 && (
              <button className="btn btn-secondary mr-10" onClick={handlePrev}>
                上一步
              </button>
            )}
            <button className="btn btn-primary" onClick={handleNext}>
              {step === steps.length ? '开始使用' : '下一步'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default OnboardingFlow;