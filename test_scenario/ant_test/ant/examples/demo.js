/**
 * ANT技能使用示例
 * 演示ant-participant-skill和ant-network-skill的完整使用流程
 */

const AntParticipantSkill = require('../participant-skill/index');
const AntNetworkSkill = require('../network-skill/index');

async function runDemo() {
  console.log('🚀 ANT技能演示开始\n');

  // 初始化技能
  const participantSkill = new AntParticipantSkill({
    enableLogging: true,
    confidenceThreshold: 0.5
  });

  const networkSkill = new AntNetworkSkill({
    enableLogging: true,
    enableVisualization: true,
    layout: 'force_directed'
  });

  try {
    // 示例文本 - 真实的政策场景
    const sampleText = `
      北京市人民政府发布了《智慧城市建设三年行动计划（2023-2025）》，
      要求各相关部门协调配合，共同推进城市数字化转型。

      市环保局负责环境监测系统建设，市交通委负责智能交通系统优化，
      市经信局负责产业数字化转型指导。各部门要建立协同工作机制，
      确保项目顺利实施。

      华为技术有限公司作为主要技术供应商，提供5G网络基础设施和云计算平台。
      阿里巴巴集团负责数据中台建设和人工智能算法支持。
      腾讯公司负责物联网平台建设和智慧应用开发。

      清华大学的李教授担任项目总顾问，北京大学的王教授负责技术方案评估。
      张局长担任项目总指挥，协调各部门工作。

      相关企业需要配合政府部门的工作安排，
      按时完成技术部署和系统对接。
      各区县政府负责具体落实，
      确保智慧城市建设目标如期实现。
    `;

    console.log('📝 输入文本长度:', sampleText.length, '字符');

    // 第1步：参与者识别
    console.log('\n🔍 第1步：执行参与者识别...');
    const startTime = Date.now();
    const participantResult = await participantSkill.execute(sampleText);
    const participantTime = Date.now() - startTime;

    console.log(`✅ 参与者识别完成，耗时: ${participantTime}ms`);
    console.log(`📊 识别结果统计:`);
    console.log(`   - 总参与者数量: ${participantResult.overview.totalParticipants}`);
    console.log(`   - 关键参与者: ${participantResult.overview.keyParticipants.join(', ')}`);
    console.log(`   - 网络类型: ${participantResult.overview.networkType}`);
    console.log(`   - 关系数量: ${participantResult.details.relations.length}`);

    // 显示第1层信息 - 核心概念
    console.log('\n🎯 第1层信息 - 核心概念:');
    console.log(participantResult.overview.description);

    // 显示第2层信息 - 关键发现
    console.log('\n🔍 第2层信息 - 关键发现:');
    console.log('主要参与者:');
    participantResult.summary.participants.forEach((p, i) => {
      console.log(`  ${i + 1}. ${p.name} (${p.type}) - ${p.role} [${p.importance}]`);
    });

    console.log('\n主要关系:');
    participantResult.summary.relations.forEach((r, i) => {
      console.log(`  ${i + 1}. ${r.from} → ${r.to} (${r.type}) [${r.strength}]`);
    });

    // 第2步：网络分析
    console.log('\n🕸️  第2步：执行网络分析...');
    const networkStartTime = Date.now();
    const networkResult = await networkSkill.execute(participantResult);
    const networkTime = Date.now() - networkStartTime;

    console.log(`✅ 网络分析完成，耗时: ${networkTime}ms`);
    console.log(`📊 网络分析结果:`);
    console.log(`   - 网络类型: ${networkResult.overview.networkType}`);
    console.log(`   - 中心节点: ${networkResult.overview.centralPlayer}`);
    console.log(`   - 网络密度: ${networkResult.summary.networkMetrics.networkMetrics.density}`);
    console.log(`   - 社区数量: ${networkResult.summary.communities.length}`);

    // 显示网络分析结果
    console.log('\n🎯 网络分析核心概念:');
    console.log(networkResult.overview.description);

    console.log('\n🔍 关键玩家分析:');
    networkResult.summary.keyPlayersAnalysis.forEach((p, i) => {
      console.log(`  ${i + 1}. ${p.name} - 中心性分数: ${p.centralityScore}`);
    });

    if (networkResult.summary.communities.length > 0) {
      console.log('\n🏘️  网络社区:');
      networkResult.summary.communities.forEach((c, i) => {
        console.log(`  社区${i + 1}: ${c.id} (大小: ${c.size}, 密度: ${c.density})`);
      });
    }

    // 性能统计
    const totalTime = participantTime + networkTime;
    console.log('\n⏱️  性能统计:');
    console.log(`   - 参与者识别: ${participantTime}ms`);
    console.log(`   - 网络分析: ${networkTime}ms`);
    console.log(`   - 总耗时: ${totalTime}ms`);
    console.log(`   - 处理速度: ${(sampleText.length / totalTime * 1000).toFixed(0)} 字符/秒`);

    // 质量验证
    console.log('\n🔍 质量验证:');
    const participantQuality = await participantSkill.validateResult(participantResult);
    console.log(`   - 参与者识别质量: ${participantQuality.score}/100`);
    if (participantQuality.issues.length > 0) {
      console.log('   - 问题:', participantQuality.issues.join(', '));
    }

    const networkQuality = networkSkill.validateResult(networkResult);
    console.log(`   - 网络分析质量: ${networkQuality.score}/100`);
    if (networkQuality.issues.length > 0) {
      console.log('   - 问题:', networkQuality.issues.join(', '));
    }

    // 生成可视化文件（如果启用）
    if (networkResult.visualizationHTML) {
      const fs = require('fs');
      const path = require('path');

      const vizFile = path.join(__dirname, '../network-visualization.html');
      fs.writeFileSync(vizFile, networkResult.visualizationHTML);
      console.log(`\n📊 网络可视化已保存到: ${vizFile}`);
      console.log('   可以在浏览器中打开查看网络关系图');
    }

    console.log('\n🎉 演示完成！');

  } catch (error) {
    console.error('❌ 演示过程中出错:', error.message);
    console.error(error.stack);
  }
}

// 运行演示
if (require.main === module) {
  runDemo();
}

module.exports = runDemo;