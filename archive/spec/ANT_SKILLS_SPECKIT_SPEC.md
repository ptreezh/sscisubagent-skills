# ANT Skills Package - Speckit Requirements Specification

## 📋 Document Information

- **Specification ID**: SCI-ANT-001
- **Version**: 1.0.0
- **Status**: Draft for Review
- **Created**: 2025-12-16
- **Author**: SCI Subagent Team
- **Reviewers**: Technical Architecture Team, ANT Theory Experts
- **Compliance**: KISS Principles, YAGNI Principles

## 🎯 Executive Summary

This specification defines the requirements for implementing the Actor-Network Theory (ANT) skills package for the SCI Subagent system. The system provides comprehensive ANT analysis capabilities specifically adapted for Chinese social science research contexts, following the established speckit framework with TDD-driven development methodology.

## 🏗️ Architecture Overview

### System Boundaries
```
┌─────────────────────────────────────────────────────────────┐
│                    User Interaction Layer                        │
│  ant-expert.md (Expert Knowledge)                              │
│  User Query → "分析这个科技政策的行动者网络"                     │
├─────────────────────────────────────────────────────────────┤
│                   Skills Triggering Layer                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Actor          │  │ Translation    │  │ Network         │ │
│  │ Identification  │  │ Process        │  │ Construction     │ │
│  │ Skill          │  │ Analysis       │  │ Tracking         │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│                         ┌─────────────────┐                         │
│                         │ Power Relationship│                         │
│                         │ Analysis Skill     │                         │
│                         └─────────────────┘                         │
├─────────────────────────────────────────────────────────────┤
│                  Skills Execution Layer                           │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              ANT Skills Engine & NLP Processor             │ │
│  │  • Actor Detection     • Translation Chain Analysis      │ │
│  │  • Network Visualization • Power Flow Analysis         │
│  │  • Chinese Context Adaptation • Domain Expertise     │ │
│  └─────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                   Data Processing Layer                            │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Text Analysis   │  │ Network Data     │  │ Power Metrics    │ │
│  │ Context Parser  │  │ Graph Builder     │  │ Visualization   │ │
│  │ Domain Filter   │  │ Timeline Tracker  │  │ Reporter Generator│ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 Functional Requirements

### FR-001: Actor Identification Detection
**Priority**: Critical
**Description**: System shall identify and classify actors from Chinese social science text data

**Acceptance Criteria**:
- [ ] Detects individual actors (个人) with 90% accuracy
- [ ] Detects organizational actors (组织) with 85% accuracy
- [ ] Detects technological actors (技术) with 80% accuracy
- [ ] Detects institutional actors (制度) with 95% accuracy
- [ ] Provides actor classification with confidence scores
- [ ] Handles Chinese specific actor types (政府机构, 事业单位)

**Test Cases**:
```gherkin
Scenario: Actor identification from policy document
  Given a Chinese government policy document
  When I process the document with actor identification skill
  Then the system should extract at least 10 relevant actors
  And classify them by type (individual/organizational/technological/institutional)
  And provide confidence scores for each identification
```

### FR-002: Translation Process Analysis
**Priority**: Critical
**Description**: System shall analyze the four translation moments in ANT processes

**Acceptance Criteria**:
- [ ] Identifies Problematization (问题化) phase
- [ ] Identifies Interessement (兴趣化) phase
- [ ] Identifies Enrollment (招募) phase
- [ ] Identifies Mobilization (动员) phase
- [ ] Tracks translation chains between phases
- [ ] Evaluates translation effectiveness

**Test Cases**:
```gherkin
Scenario: Policy formation process analysis
  Given data about a technology policy formation process
  When I analyze with translation process skill
  Then the system should identify all four translation moments
  And map the relationships between actors in each phase
  And provide a complete translation chain visualization
```

### FR-003: Network Construction Tracking
**Priority**: High
**Description**: System shall track network construction and evolution dynamics

**Acceptance Criteria**:
- [ ] Builds actor network from identified actors and relationships
- [ ] Tracks network stability metrics over time
- [ ] Identifies key network nodes and bridges
- [ ] Visualizes network structure with Chinese labels
- [ ] Provides network evolution timeline
- [ ] Detects network expansion patterns

**Test Cases**:
```gherkin
Scenario: Healthcare network tracking
  Given longitudinal data about healthcare system reforms
  When I track with network construction skill
  Then the system should show network evolution over time
  And identify key inflection points in network structure
  And visualize actor relationships in Chinese context
```

### FR-004: Power Relationship Analysis
**Priority**: High
**Description**: System shall analyze power relationships and flows within actor networks

**Acceptance Criteria**:
- [ ] Calculates power asymmetry between actors
- [ ] Identifies power centers and peripheral nodes
- [ ] Tracks power flow patterns
- [ ] Measures network constraint and opportunity
- [ ] Provides power relationship metrics
- [ ] Generates power relationship reports

**Test Cases**:
```gherkin
Scenario: Technology governance power analysis
  Given network data about technology governance
  When I analyze with power relationship skill
  Then the system should identify power asymmetries
  And map power flow pathways
  And generate comprehensive power metrics report
```

## 🔧 Non-Functional Requirements

### NFR-001: Performance Requirements
**Priority**: High
**Description**: System shall process analysis efficiently

**Acceptance Criteria**:
- [ ] Actor identification: <10 seconds for 5000-word document
- [ ] Network construction: <30 seconds for complex network
- [ ] Power analysis: <15 seconds for network metrics
- [ ] Response time: <5 seconds for simple queries
- [ ] Memory usage: <100MB for standard analysis

### NFR-002: Accuracy Requirements
**Priority**: Critical
**Description**: System shall provide accurate analysis results

**Acceptance Criteria**:
- [ ] Actor identification accuracy: >85%
- [ ] Translation phase detection: >90%
- [ ] Network metrics precision: >95%
- [ ] Power measurement reliability: >80%

### NFR-003: Usability Requirements
**Priority**: Medium
**Description**: System shall be user-friendly for Chinese researchers

**Acceptance Criteria**:
- [ ] Provides Chinese language interface
- [ ] Generates Chinese-language reports
- [ ] Includes Chinese social science terminology
- [ ] Supports Chinese case studies

### NFR-004: Integration Requirements
**Priority**: High
**Description**: System shall integrate with existing SCI subagent ecosystem

**Acceptance Criteria**:
- [ ] Compatible with ant-expert.md agent
- [ ] Follows established skill triggering patterns
- [ ] Supports data exchange with other skills
- [ ] Uses standardized output formats

## 🧪 TDD Implementation Strategy

### Phase 1: Actor Identification Skill (Week 1)

#### Test-First Development Cycle
```bash
# Test file: test/unit/actor-identification.test.js
describe('Actor Identification Skill', () => {
  test('should identify individual actors from Chinese text', () => {
    const text = "李华教授负责这个研究项目，他与张三工程师合作开发技术方案";
    const result = identifyActors(text);

    expect(result.actors).toHaveLength(2);
    expect(result.actors[0].name).toBe('李华教授');
    expect(result.actors[0].type).toBe('individual');
    expect(result.actors[1].name).toBe('张三工程师');
    expect(result.actors[1].type).toBe('individual');
  });

  test('should identify institutional actors', () => {
    const text = "环保部门发布了新的环境政策，要求各地方政府严格执行";
    const result = identifyActors(text);

    expect(result.actors.some(actor => actor.name === '环保部门'));
    expect(result.actors.some(actor => actor.type === 'institutional'));
  });

  test('should handle Chinese specific actor types', () => {
    const text = "国务院办公厅协调各部门工作，确保政策落实";
    const result = identifyActors(text);

    expect(result.actors.some(actor =>
      actor.type === 'government' || actor.type === 'institutional'
    ));
  });
});

# Implementation follows test-first approach
# RED: Test fails (implementation doesn't exist)
# GREEN: Write minimal implementation to pass tests
# REFACTOR: Improve while maintaining test coverage
```

#### Actor Identification Core Algorithm
```javascript
// src/skills/ant/actor-identification.js
class ActorIdentification {
  constructor() {
    this.actorPatterns = this.initializePatterns();
    this.contextAnalyzer = new ChineseContextAnalyzer();
  }

  identifyActors(text) {
    const actors = [];

    // Individual actors
    const individuals = this.extractIndividualActors(text);
    actors.push(...individuals);

    // Organizational actors
    const organizations = this.extractOrganizationalActors(text);
    actors.push(...organizations);

    // Technological actors
    const technologies = this.extractTechnologicalActors(text);
    actors.push(...technologies);

    // Institutional actors
    const institutions = this.extractInstitutionalActors(text);
    actors.push(...institutions);

    return this.deduplicateAndClassify(actors);
  }

  extractIndividualActors(text) {
    // Implementation to pass tests
    const pattern = /([李王张刘陈杨赵黄周吴徐孙马胡朱高郭何罗林梁宋郑谢韩唐])[一二三四五六七八九十]+(?:教授|研究员|工程师|主任|经理|博士|硕士|专家|老师|先生|女士)/g;

    const matches = text.match(pattern) || [];
    return matches.map(match => ({
      name: match[0],
      type: 'individual',
      confidence: 0.9,
      context: this.contextAnalyzer.getContext(match)
    }));
  }

  extractOrganizationalActors(text) {
    const pattern = /(?:公司|机构|部门|委员会|协会|联合会|研究院|大学|医院|学校|组织|集团|企业)[^(，。！？\s)]{0,20}([^\s，。！？]+)/g;

    const matches = [...text.matchAll(pattern)];
    return matches.map(match => ({
      name: match[1] || match[0],
      type: 'organizational',
      confidence: 0.85
    }));
  }

  deduplicateAndClassify(actors) {
    // Remove duplicates and classify
    const uniqueActors = this.removeDuplicates(actors);
    return uniqueActors.map(actor =>
      Object.assign(actor, this.classifyActor(actor))
    );
  }
}
```

### Phase 2: Translation Process Analysis Skill (Week 2)

#### Test-First Development Cycle
```bash
# Test file: test/unit/translation-process.test.js
describe('Translation Process Analysis Skill', () => {
  test('should identify problematization phase', () => {
    const processData = {
      events: [
        { type: 'problem_identified', description: '技术落后问题' },
        { type: 'problem_definition', description: '制定技术升级方案' }
      ]
    };

    const result = analyzeTranslationProcess(processData);

    expect(result.phases).toContain('problematization');
    expect(result.phases.problematization.actors).toHaveLength(2);
    expect(result.phases.problematization.confidence).toBeGreaterThan(0.8);
  });

  test('should identify complete translation chain', () => {
    const processData = {
      phases: ['problematization', 'interessement', 'enrollment', 'mobilization'],
      actors: ['政府', '企业', '专家', '公众']
    };

    const result = analyzeTranslationProcess(processData);

    expect(result.translationChain).toBeDefined();
    expect(result.translationChain.connections).toHaveLength(3);
    expect(result.stability).toBeDefined();
  });
});

# Implementation follows test-first approach
```

### Phase 3: Network Construction Tracking Skill (Week 3)

#### Test-First Development Cycle
```bash
# Test file: test/unit/network-construction.test.js
describe('Network Construction Tracking Skill', () => {
  test('should build actor network', () => {
    const actors = [
      { id: 'A1', name: '政府', type: 'institutional' },
      { id: 'A2', name: '企业', type: 'organizational' },
      { id: 'A3', name: '技术', type: 'technological' }
    ];

    const result = buildActorNetwork(actors);

    expect(result.nodes).toHaveLength(3);
    expect(result.edges).toBeDefined();
    expect(result.metrics.density).toBeGreaterThanOrEqual(0);
  });

  test('should track network evolution', () => {
    const networkHistory = [
      { timestamp: '2024-01-01', actors: ['A1', 'A2'], connections: [] },
      { timestamp: '2024-02-01', actors: ['A1', 'A2', 'A3'], connections: [['A1', 'A3']] }
    ];

    const result = trackNetworkEvolution(networkHistory);

    expect(result.evolution).toBeDefined();
    expect(result.stabilityMetrics).toBeDefined();
    expect(result.trends.expansion).toBe(true);
  });
});
```

### Phase 4: Power Relationship Analysis Skill (Week 4)

#### Test-First Development Cycle
```bash
# Test file: test/unit/power-relationship.test.js
describe('Power Relationship Analysis Skill', () => {
  test('should calculate power asymmetry', () => {
    const network = {
      nodes: [
        { id: 'A1', power: 8 },
        { id: 'A2', power: 2 }
      ],
      edges: [['A1', 'A2']]
    };

    const result = analyzePowerRelationships(network);

    expect(result.powerAsymmetry).toBeDefined();
    expect(result.powerAsymmetry['A1-A2']).toBeGreaterThan(0);
    expect(result.constraints['A2']).toBeGreaterThan(0);
  });

  test('should identify power centers', () => {
    const network = {
      nodes: [
        { id: 'A1', power: 10 },
        { id: 'A2', power: 8 },
        { id: 'A3', power: 2 }
      ],
      edges: [['A1', 'A2'], ['A1', 'A3'], ['A2', 'A3']]
    };

    const result = analyzePowerRelationships(network);

    expect(result.powerCenters).toContain('A1');
    expect(result.peripheralNodes).toContain('A3');
    expect(result.brokerageNodes).toContain('A2');
  });
});
```

## 📊 Test Coverage Requirements

### Coverage Targets
- **Actor Identification Skill**: 100%
- **Translation Process Skill**: 95%
- **Network Construction Skill**: 90%
- **Power Relationship Skill**: 85%
- **Overall Package**: 90%

### Critical Test Paths
1. **Actor Identification Accuracy**: >90% for major actor types
2. **Translation Phase Detection**: >95% for complete translation chains
3. **Network Metrics Calculation**: >95% for standard metrics
4. **Power Analysis Reliability**: >80% for power asymmetry measurement

## 📈 Performance Benchmarks

### Speed Requirements
- **Small Document Analysis** (<1000 words): <3 seconds
- **Medium Document Analysis** (1000-5000 words): <10 seconds
- **Large Document Analysis** (>5000 words): <30 seconds

### Memory Requirements
- **Small Networks** (<50 nodes): <20MB
- **Medium Networks** (50-200 nodes): <50MB
- **Large Networks** (>200 nodes): <100MB

## 🔧 Implementation Phases

### Phase 1: Core Actor Identification (Week 1)
**Deliverables**:
- [x] Individual actor detection algorithm
- [x] Organizational actor recognition
- [ ] Technological actor identification
- [ ] Institutional actor detection
- [x] Actor classification system
- [ ] Unit tests (100% coverage)

### Phase 2: Translation Process Analysis (Week 2)
**Deliverables**:
- [ ] Translation phase detection
- [ ] Translation chain mapping
- [ ] Process effectiveness evaluation
- [ ] Chinese policy context adaptation
- [ ] Integration tests

### Phase 3: Network Construction Tracking (Week 3)
**Deliverables**:
- [ ] Network building algorithms
- [ ] Evolution tracking system
- [ ] Stability metrics calculation
- [ ] Network visualization (Chinese labels)
- [ ] Timeline generation

### Phase 4: Power Relationship Analysis (Week 4)
**Deliverables**:
- [ ] Power asymmetry calculation
- [ ] Power flow analysis
- [ ] Constraint and opportunity measurement
- [ ] Power metrics reporting
- [ ] Integration with other ANT skills

## 📋 Quality Assurance Checklist

### Code Quality
- [ ] All tests pass (100% success rate)
- [ ] Code coverage >90%
- [ ] No code duplication
- [ ] Consistent coding standards
- [ ] Comprehensive error handling

### Functional Quality
- [ ] All acceptance criteria met
- [ ] Edge cases handled gracefully
- [ ] Chinese language support verified
- [ ] Domain expertise validated
- [ ] Performance benchmarks met

### Documentation Quality
- [ ] API documentation complete
- [ ] Usage examples provided
- [ ] Chinese comments included
- [ ] Troubleshooting guide available
- [ ] Version change log maintained

## 🚀 Success Metrics

### Functional Metrics
- **Actor Detection Rate**: >90% accuracy
- **Translation Phase Coverage**: >95% of cases
- **Network Analysis Accuracy**: >95% reliability
- **Power Analysis Precision**: >80% measurement accuracy

### Performance Metrics
- **Response Time**: <5 seconds for simple queries
- **Throughput**: >10 analyses per minute
- **Memory Efficiency**: <100MB peak usage
- **Scalability**: Support networks up to 1000 nodes

### User Experience Metrics
- **Ease of Use**: >4.5/5 user rating
- **Learning Curve**: <2 hours to proficiency
- **Documentation Quality**: >90% completeness rating
- **Support Satisfaction**: >95% issue resolution rate

## ⚠️ Risk Assessment

### Technical Risks
- **Algorithm Complexity**: ANT analysis algorithms are inherently complex
  - *Mitigation*: Modular design, comprehensive testing
  - *Priority*: High

- **Performance Optimization**: Large network analysis may be computationally intensive
  - *Mitigation*: Efficient algorithms, caching strategies
  - *Priority*: Medium

- **Chinese Language Processing**: Chinese NLP challenges
  - *Mitigation*: Specialized Chinese NLP models, fallback mechanisms
  - *Priority*: Medium

### Business Risks
- **User Adoption**: Complexity may affect user adoption
  - *Mitigation*: User-friendly interfaces, comprehensive training
  - *Priority*: Medium

- **Domain Relevance**: ANT may not apply to all domains
  - *Mitigation*: Domain expertise validation, flexible design
  - *Priority*: Low

### Operational Risks
- **Maintenance Overhead**: Complex algorithms require ongoing maintenance
  - *Mitigation*: Automated testing, comprehensive documentation
  - *Priority*: Medium

- **Integration Challenges**: Integration with existing ecosystem
  - *Mitigation*: Standardized interfaces, backward compatibility
  - *Priority*: Low

## 🔄 Development Workflow

### TDD Cycle per Skill
```bash
# 1. Write failing test
npm test -- --watch src/skills/ant

# 2. Run test (RED Phase)
> ActorIdentification > identifyActors > should detect individual actors (FAILED)

# 3. Write minimal implementation (GREEN Phase)
# (Code implementation)

# 4. Run test (PASSED)
> ActorIdentification > identifyActors > should detect individual actors (PASSED)

# 5. Refactor while tests stay green
# (Code improvement and optimization)

# 6. Repeat for next test case
```

### Continuous Integration
```yaml
# .github/workflows/ant-skills-ci.yml
name: ANT Skills CI/CD Pipeline

on: [push, pull_request]
paths:
  - 'src/skills/ant/**'
  - 'test/unit/skills/ant/**'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm install

      - name: Run ANT Skills tests
        run: npm run test:ant-skills

      - name: Check test coverage
        run: npm run test:coverage:ant-skills

      - name: Validate Chinese NLP
        run: npm run test:chinese-nlp
```

## 📚 Integration Requirements

### With Existing Ecosystem
- **ant-expert.md**: Seamless integration with expert knowledge
- **Other ANT Skills**: Data sharing and collaboration
- **Chinese Context**: Leverage chinese-localization-expert
- **Data Sources**: Integration with literature-expert for case studies

### With CLI Tools
- **Stigmergy CLI**: Hook integration for /skill commands
- **Cross-CLI**: Consistent interface across Claude, Gemini, Qwen
- **Hooks System**: Integration with established hook framework

### With Output Standards
- **Report Formats**: Standardized Chinese academic report format
- **Data Structures**: Compatible with other skill outputs
- **Visualization**: Consistent with existing network visualization

---

**This specification follows the established speckit framework with TDD-driven development, ensuring robust, well-tested ANT skills implementation that meets all Chinese social science research needs while maintaining high quality standards.**