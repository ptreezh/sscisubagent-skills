// UnifiedAgentService.test.js
const UnifiedAgentService = require('../services/UnifiedAgentService');

describe('UnifiedAgentService', () => {
  describe('getAgents', () => {
    it('should return a list of agents', () => {
      const agents = UnifiedAgentService.getAgents();
      expect(Array.isArray(agents)).toBe(true);
      expect(agents.length).toBeGreaterThan(0);
    });

    it('should include all expected agents', () => {
      const agents = UnifiedAgentService.getAgents();
      const agentIds = agents.map(agent => agent.id);
      
      expect(agentIds).toContain('stigmergy');
      expect(agentIds).toContain('claude');
      expect(agentIds).toContain('qwen');
      expect(agentIds).toContain('iflow');
      expect(agentIds).toContain('gemini');
      expect(agentIds).toContain('codex');
    });
  });

  describe('getAgentById', () => {
    it('should return the correct agent when given a valid ID', () => {
      const agent = UnifiedAgentService.getAgentById('claude');
      expect(agent).not.toBeNull();
      expect(agent.id).toBe('claude');
      expect(agent.name).toBe('Claude 助手');
    });

    it('should return null for invalid agent ID', () => {
      const agent = UnifiedAgentService.getAgentById('invalid-agent');
      expect(agent).toBeNull();
    });
  });

  describe('getSkillCategories', () => {
    it('should return a list of skill categories', () => {
      const categories = UnifiedAgentService.getSkillCategories();
      expect(Array.isArray(categories)).toBe(true);
      expect(categories.length).toBeGreaterThan(0);
    });
  });

  describe('getAllSkills', () => {
    it('should return a list of all skills', () => {
      const skills = UnifiedAgentService.getAllSkills();
      expect(Array.isArray(skills)).toBe(true);
      expect(skills.length).toBeGreaterThan(0);
    });
  });

  describe('getSkillById', () => {
    it('should return the correct skill when given a valid ID', () => {
      const skill = UnifiedAgentService.getSkillById('literature-review');
      expect(skill).not.toBeNull();
      expect(skill.id).toBe('literature-review');
      expect(skill.name).toBe('文献综述专家');
    });

    it('should return null for invalid skill ID', () => {
      const skill = UnifiedAgentService.getSkillById('invalid-skill');
      expect(skill).toBeNull();
    });
  });

  describe('getSkillsByAgent', () => {
    it('should return skills associated with a specific agent', () => {
      const skills = UnifiedAgentService.getSkillsByAgent('claude');
      expect(Array.isArray(skills)).toBe(true);
      // Check that all returned skills are associated with Claude
      skills.forEach(skill => {
        expect(skill.agent).toBe('claude');
      });
    });
  });

  describe('getSkillsByCategory', () => {
    it('should return skills in a specific category', () => {
      const skills = UnifiedAgentService.getSkillsByCategory('research');
      expect(Array.isArray(skills)).toBe(true);
      expect(skills.length).toBeGreaterThan(0);
    });
  });

  describe('toggleSkillStatus', () => {
    it('should toggle the status of a skill', () => {
      // Get initial status
      const initialSkill = UnifiedAgentService.getSkillById('social-network');
      const initialState = initialSkill.status;
      
      // Toggle status
      const toggledSkill = UnifiedAgentService.toggleSkillStatus('social-network');
      expect(toggledSkill).not.toBeNull();
      expect(toggledSkill.status).not.toBe(initialState);
      
      // Toggle back to original state
      const finalSkill = UnifiedAgentService.toggleSkillStatus('social-network');
      expect(finalSkill.status).toBe(initialState);
    });

    it('should return null for invalid skill ID', () => {
      const result = UnifiedAgentService.toggleSkillStatus('invalid-skill');
      expect(result).toBeNull();
    });
  });
});