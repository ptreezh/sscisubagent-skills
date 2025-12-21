/**
 * 集成测试 - ANT技能协作测试
 * 测试ant-participant-skill和ant-network-skill的协同工作
 */

const AntParticipantSkill = require('../participant-skill/index');
const AntNetworkSkill = require('../network-skill/index');

describe('ANT技能集成测试', () => {
  let participantSkill;
  let networkSkill;

  beforeEach(() => {
    // Arrange - 初始化技能
    participantSkill = new AntParticipantSkill({ enableLogging: false });
    networkSkill = new AntNetworkSkill({
      enableLogging: false,
      enableVisualization: false // 加速测试
    });
  });

  describe('完整分析流程', () => {
    test('应该完成从文本到网络可视化的完整流程', async () => {
      // Arrange
      const sampleText = `
        某市政府发布了智慧城市建设规划，要求在2025年前完成数字化转型。
        环保部门负责环境监测系统建设，交通部门负责智能交通系统优化。
        华为公司作为主要技术供应商，提供5G网络和云计算平台支持。
        阿里巴巴负责数据中台建设和AI算法支持。
        清华大学的李教授担任项目总顾问，张局长担任项目总指挥。
        相关企业被要求配合政府部门的工作，共同推进智慧城市建设。
        各部门需要协调配合，确保项目顺利实施。
      `;

      // Act - 第1步：参与者识别
      const participantResult = await participantSkill.execute(sampleText);

      // Assert - 第1步结果验证
      expect(participantResult).toBeDefined();
      expect(participantResult.overview.totalParticipants).toBeGreaterThan(5);
      expect(participantResult.overview.keyParticipants).toContain('环保部门');
      expect(participantResult.overview.keyParticipants).toContain('华为公司');

      // Act - 第2步：网络分析
      const networkResult = await networkSkill.execute(participantResult);

      // Assert - 第2步结果验证
      expect(networkResult).toBeDefined();
      expect(networkResult.overview.title).toBe('网络关系分析');
      expect(networkResult.overview.networkType).toBeDefined();
      expect(networkResult.summary.networkMetrics).toBeDefined();

      // 验证数据一致性
      expect(participantResult.overview.totalParticipants).toBe(
        networkResult.summary.networkMetrics.participantMetrics.highImportance +
        networkResult.summary.networkMetrics.participantMetrics.mediumImportance +
        networkResult.summary.networkMetrics.participantMetrics.lowImportance
      );
    });

    test('应该正确处理复杂的政策文档', async () => {
      // Arrange
      const complexPolicyText = `
        国家发展改革委、科技部、工信部联合发布了《数字经济发展规划》，
        要求各地方政府结合实际情况制定实施方案。
        工业和信息化部负责指导产业数字化转型，
        国家发改委负责统筹协调重大项目建设。
        阿里巴巴、腾讯、百度等互联网企业被鼓励参与数字基础设施建设。
        中国移动、中国联通、中国电信负责5G网络覆盖。
        各省级政府需要成立专项工作组，
        由省级领导担任组长，相关部门负责人为成员。
        企业需要与政府部门密切配合，
        共同推进数字经济发展目标的实现。
        技术创新和产业应用相结合，
        确保规划目标的顺利完成。
      `;

      // Act
      const participantResult = await participantSkill.execute(complexPolicyText);
      const networkResult = await networkSkill.execute(participantResult);

      // Assert
      // 验证参与者识别
      expect(participantResult.overview.totalParticipants).toBeGreaterThan(10);
      expect(participantResult.overview.keyParticipants).toContain('工业和信息化部');
      expect(participantResult.overview.keyParticipants).toContain('阿里巴巴');

      // 验证网络结构
      expect(networkResult.overview.networkType).toMatch(/网络/);
      expect(networkResult.summary.keyPlayersAnalysis.length).toBeGreaterThan(0);

      // 验证关键指标
      const metrics = networkResult.summary.networkMetrics;
      expect(metrics.participantMetrics.highImportance).toBeGreaterThan(0);
      expect(metrics.networkMetrics.nodeCount).toBeGreaterThan(10);
    });
  });

  describe('错误处理和边界情况', () => {
    test('应该处理空文本输入', async () => {
      // Arrange
      const emptyText = '';

      // Act
      const participantResult = await participantSkill.execute(emptyText);

      // Assert
      expect(participantResult.overview.totalParticipants).toBe(0);
      expect(participantResult.overview.keyParticipants).toEqual([]);

      // 网络分析应该优雅处理空数据
      await expect(networkSkill.execute(participantResult)).rejects.toThrow();
    });

    test('应该处理只有单个参与者的情况', async () => {
      // Arrange
      const singleParticipantText = '环保部门发布了新政策。';

      // Act
      const participantResult = await participantSkill.execute(singleParticipantText);

      // Assert
      expect(participantResult.overview.totalParticipants).toBe(1);
      expect(participantResult.details.participants[0].name).toBe('环保部门');

      // 网络分析应该处理单节点网络
      const networkResult = await networkSkill.execute(participantResult);
      expect(networkResult.overview.networkType).toBe('单节点网络');
    });

    test('应该处理无效输入', async () => {
      // Act & Assert
      await expect(participantSkill.execute(null)).rejects.toThrow('输入文本不能为空');
      await expect(participantSkill.execute(undefined)).rejects.toThrow('输入文本不能为空');
      await expect(participantSkill.execute(123)).rejects.toThrow('输入必须是字符串类型');
    });
  });

  describe('性能测试', () => {
    test('应该在合理时间内完成分析', async () => {
      // Arrange - 创建中等长度文本
      const mediumText = `
        ${'环保部门发布新政策，要求企业配合实施。'.repeat(20)}
        ${'华为公司提供技术支持，阿里巴巴提供平台支持。'.repeat(10)}
        ${'各地方政府负责具体执行，相关部门协调配合。'.repeat(15)}
        ${'专家教授提供咨询建议，技术人员负责方案设计。'.repeat(10)}
      `;

      // Act
      const startTime = Date.now();
      const participantResult = await participantSkill.execute(mediumText);
      const participantTime = Date.now() - startTime;

      const networkStartTime = Date.now();
      const networkResult = await networkSkill.execute(participantResult);
      const networkTime = Date.now() - networkStartTime;

      const totalTime = participantTime + networkTime;

      // Assert
      expect(totalTime).toBeLessThan(5000); // 总时间少于5秒
      expect(participantTime).toBeLessThan(3000); // 参与者识别少于3秒
      expect(networkTime).toBeLessThan(2000); // 网络分析少于2秒

      console.log(`性能测试结果: 参与者识别${participantTime}ms, 网络分析${networkTime}ms, 总计${totalTime}ms`);
    });

    test('应该处理大量参与者', async () => {
      // Arrange - 创建包含多个参与者的文本
      const largeText = this._generateLargeParticipantText(30);

      // Act
      const participantResult = await participantSkill.execute(largeText);

      // Assert
      expect(participantResult.overview.totalParticipants).toBeGreaterThan(20);

      // 网络分析应该处理大量节点
      const networkResult = await networkSkill.execute(participantResult);
      expect(networkResult.summary.networkMetrics.networkMetrics.nodeCount).toBeGreaterThan(20);
    });
  });

  describe('数据一致性验证', () => {
    test('参与者数据在网络分析中应保持一致', async () => {
      // Arrange
      const text = `
        环保部门监管企业排放，企业依赖技术支持，
        专家教授提供咨询建议，政府部门协调配合。
      `;

      // Act
      const participantResult = await participantSkill.execute(text);
      const networkResult = await networkSkill.execute(participantResult);

      // Assert - 验证参与者名称一致性
      const participantNames = participantResult.details.participants.map(p => p.name);
      const networkPlayerNames = networkResult.summary.keyPlayersAnalysis.map(p => p.name);

      participantNames.forEach(name => {
        expect(networkPlayerNames).toContain(name);
      });
    });

    test('关系数据应正确传递', async () => {
      // Arrange
      const text = '环保部门监管华为公司，华为公司与阿里巴巴合作。';

      // Act
      const participantResult = await participantSkill.execute(text);
      const networkResult = await networkSkill.execute(participantResult);

      // Assert
      expect(participantResult.details.relations.length).toBeGreaterThan(0);
      expect(networkResult.summary.networkMetrics.relationMetrics).toBeDefined();

      // 验证关系类型统计
      const relationMetrics = networkResult.summary.networkMetrics.relationMetrics;
      expect(Object.values(relationMetrics).some(count => count > 0)).toBe(true);
    });
  });

  describe('输出格式验证', () => {
    test('输出应符合规范格式', async () => {
      // Arrange
      const text = '环保部门发布政策，要求企业配合实施。';

      // Act
      const participantResult = await participantSkill.execute(text);
      const networkResult = await networkSkill.execute(participantResult);

      // Assert - 验证参与者技能输出格式
      expect(participantResult).toHaveProperty('overview');
      expect(participantResult).toHaveProperty('summary');
      expect(participantResult).toHaveProperty('details');
      expect(participantResult).toHaveProperty('metadata');

      expect(participantResult.overview).toHaveProperty('title');
      expect(participantResult.overview).toHaveProperty('totalParticipants');

      // Assert - 验证网络技能输出格式
      expect(networkResult).toHaveProperty('overview');
      expect(networkResult).toHaveProperty('summary');
      expect(networkResult).toHaveProperty('details');
      expect(networkResult).toHaveProperty('metadata');

      expect(networkResult.overview).toHaveProperty('networkType');
      expect(networkResult.overview).toHaveProperty('centralPlayer');
    });
  });

  /**
   * 生成包含大量参与者的测试文本
   * @private
   */
  _generateLargeParticipantText(count) {
    const organizations = ['环保部门', '科技部门', '教育部门', '卫生部门', '交通部门'];
    const companies = ['华为公司', '阿里巴巴', '腾讯公司', '百度公司', '字节跳动'];
    const universities = ['清华大学', '北京大学', '复旦大学', '上海交大', '浙江大学'];
    const individuals = ['张局长', '李教授', '王总', '陈主任', '刘专家'];

    let text = '';
    for (let i = 0; i < count; i++) {
      const org = organizations[i % organizations.length];
      const company = companies[i % companies.length];
      const university = universities[i % universities.length];
      const individual = individuals[i % individuals.length];

      text += `${org}与${company}合作，${university}的${individual}提供支持。`;
    }

    return text;
  }
});