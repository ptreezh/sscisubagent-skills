/**
 * 商业模式分析技能端到端测试
 */

const BusinessModelAnalysisSkill = require('./skill.js');

async function runEndToEndTest() {
  console.log("开始运行商业模式分析技能端到端测试...\n");
  
  try {
    const skill = new BusinessModelAnalysisSkill();
    
    // 测试综合分析
    const inputs = {
      targetCompany: "比亚迪",
      analysisType: "comprehensive",
      industryContext: "新能源汽车",
      analysisDepth: "standard",
      dataSources: ["all"]
    };
    
    console.log("输入参数:", JSON.stringify(inputs, null, 2));
    
    console.log("\n正在执行商业模式分析...");
    const result = await skill.execute(inputs);
    
    console.log("执行结果:", JSON.stringify({
      success: result.success,
      hasData: !!result.data,
      hasBusinessModelCanvas: !!result.data?.businessModelCanvas,
      hasCompetitiveAnalysis: !!result.data?.competitiveAnalysis,
      hasValueProposition: !!result.data?.valueProposition,
      hasRevenueStreams: !!result.data?.revenueStreams,
      hasMarketPositioning: !!result.data?.marketPositioning,
      hasSWOT: !!result.data?.strengthsWeaknesses,
      hasRecommendations: Array.isArray(result.data?.recommendations),
      recommendationCount: result.data?.recommendations?.length || 0,
      metadata: result.metadata
    }, null, 2));
    
    if (result.success) {
      console.log("\n✓ 技能执行成功");
      
      // 验证各个分析模块的输出
      const data = result.data;
      
      if (data.businessModelCanvas) {
        console.log("✓ 商业模式画布分析完成");
        console.log(`  - 关键合作伙伴: ${data.businessModelCanvas.keyPartners?.length || 0}个`);
        console.log(`  - 价值主张: ${data.businessModelCanvas.valuePropositions?.length || 0}项`);
        console.log(`  - 客户细分: ${data.businessModelCanvas.customerSegments?.length || 0}类`);
      }
      
      if (data.competitiveAnalysis) {
        console.log("✓ 竞争分析完成");
        console.log(`  - 直接竞争对手: ${data.competitiveAnalysis.directCompetitors?.length || 0}个`);
        console.log(`  - 市场份额: ${(data.competitiveAnalysis.competitivePosition?.marketShare * 100).toFixed(2)}%`);
      }
      
      if (data.valueProposition) {
        console.log("✓ 价值主张分析完成");
        console.log(`  - 主要价值: ${data.valueProposition.primaryValue?.length || 0}项`);
        console.log(`  - 差异化因素: ${data.valueProposition.differentiationFactors?.length || 0}项`);
      }
      
      if (data.revenueStreams) {
        console.log("✓ 收入流分析完成");
        console.log(`  - 主要收入: ¥${(data.revenueStreams.primaryRevenue / 100000000).toFixed(1)}亿`);
        console.log(`  - 收入增长率: ${(data.revenueStreams.revenueGrowthRate * 100).toFixed(1)}%`);
      }
      
      if (data.recommendations && Array.isArray(data.recommendations)) {
        console.log("✓ 改进建议生成完成");
        console.log(`  - 建议数量: ${data.recommendations.length}条`);
        console.log("  - 前三条建议:");
        data.recommendations.slice(0, 3).forEach((rec, i) => {
          console.log(`    ${i+1}. ${rec}`);
        });
      }
      
      if (data.dataQualityReport) {
        console.log("✓ 数据质量报告生成完成");
        console.log(`  - 数据完整性: ${(data.dataQualityReport.completeness.score * 100).toFixed(1)}%`);
        console.log(`  - 数据可靠性: ${(data.dataQualityReport.reliability * 100).toFixed(1)}%`);
      }
    } else {
      console.log("✗ 技能执行失败");
      console.log("错误:", result.error);
      return false;
    }
    
    console.log("\n✓ 端到端测试完成");
    return true;
    
  } catch (error) {
    console.error("端到端测试失败:", error);
    return false;
  }
}

// 运行测试
if (require.main === module) {
  runEndToEndTest().then(success => {
    if (!success) {
      process.exit(1);
    }
  }).catch(error => {
    console.error("测试执行出错:", error);
    process.exit(1);
  });
}
