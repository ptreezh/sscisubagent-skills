/**
 * 商业生态系统数据搜集技能端到端测试
 * 验证整个数据搜集流程
 */

const BusinessEcosystemDataCollectionSkill = require('./skill.js');

async function runEndToEndTest() {
  console.log("开始运行端到端测试...\n");
  
  try {
    // 创建技能实例
    const skill = new BusinessEcosystemDataCollectionSkill();
    
    // 测试输入参数
    const testInputs = {
      targetIndustry: "新能源汽车",
      searchScope: {
        geographic: "中国",
        timeRange: "recent",
        entityTypes: ["all"]
      },
      dataTypes: ["all"],
      collectionDepth: "standard",
      verificationRequired: true
    };
    
    console.log("输入参数:", JSON.stringify(testInputs, null, 2));
    
    // 执行技能
    console.log("\n正在执行商业生态系统数据搜集...");
    const result = await skill.execute(testInputs);
    
    console.log("执行结果:", JSON.stringify(result, null, 2));
    
    // 验证结果
    console.log("\n验证结果...");
    if (result.success) {
      console.log("✓ 技能执行成功");
      
      const data = result.data;
      if (data && data.collectedEntities) {
        console.log(`✓ 成功搜集到 ${data.collectedEntities.length} 个实体`);
        
        // 检查搜集到的实体是否为真实数据
        for (const entity of data.collectedEntities) {
          console.log(`  - 实体: ${entity.name}, 类型: ${entity.type}, 网站: ${entity.website}`);
        }
      } else {
        console.log("⚠ 警告: 没有搜集到实体数据");
      }
      
      if (data && data.relationships) {
        console.log(`✓ 识别出 ${data.relationships.length} 个关系`);
        
        // 检查搜集到的关系是否合理
        for (const rel of data.relationships.slice(0, 3)) { // 只显示前3个
          console.log(`  - 关系: ${rel.sourceName} -> ${rel.targetName} (${rel.type})`);
        }
      }
    } else {
      console.log("✗ 技能执行失败");
      console.log("错误:", result.error);
    }
    
    console.log("\n✓ 端到端测试完成");
    return result;
    
  } catch (error) {
    console.error("端到端测试失败:", error);
    throw error;
  }
}

// 运行测试
if (require.main === module) {
  runEndToEndTest().catch(error => {
    console.error("测试执行出错:", error);
    process.exit(1);
  });
}
