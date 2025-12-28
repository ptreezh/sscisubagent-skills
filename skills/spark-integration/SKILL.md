---
name: spark-integration
description: 闆嗘垚绉戝ぇ璁鏄熺伀澶фā鍨嬭繘琛屾櫤鑳藉垎鏋愮殑鏍囧噯鍖栨妧鑳斤紝鎻愪緵鏂囨湰鍒嗘瀽銆佹櫤鑳藉璇濄€佸唴瀹圭敓鎴愮瓑AI鑳藉姏锛屾敮鎸佸绉嶆槦鐏ā鍨嬶紝涓哄叾浠栨妧鑳芥彁渚涚粺涓€鐨凙I鑳藉姏鎺ュ彛
version: 2.0.0
author: socienceAI.com
license: MIT
tags: [ai-integration, spark-large-model, text-analysis, intelligent-dialogue, content-generation]
compatibility: Node.js environment with API access
metadata:
  domain: ai-integration
  methodology: ai-service-integration
  complexity: intermediate
  integration_type: ai-service
  last_updated: "2025-12-26"
allowed-tools: [node, bash, read_file, write_file]
---

# 绉戝ぇ璁鏄熺伀澶фā鍨嬮泦鎴愭妧鑳?(Spark Integration)

## 姒傝堪

绉戝ぇ璁鏄熺伀澶фā鍨嬮泦鎴愭妧鑳芥彁渚涗笌绉戝ぇ璁鏄熺伀澶фā鍨嬬殑API闆嗘垚鑳藉姏锛屾敮鎸佽皟鐢ㄨ椋炴槦鐏郴鍒楁ā鍨嬭繘琛屾櫤鑳藉垎鏋愬拰瀵硅瘽銆傝鎶€鑳藉皝瑁呬簡API璋冪敤缁嗚妭锛屼负鍏朵粬鎶€鑳芥彁渚涚粺涓€鐨凙I鑳藉姏鎺ュ彛锛岄伒寰猘gentskills.io瑙勮寖鍜屾笎杩涘紡鎶湶鍘熷垯銆?
## 浣跨敤鏃舵満

浣跨敤姝ゆ妧鑳藉綋鐢ㄦ埛璇锋眰锛?- 闇€瑕佽皟鐢ㄧ澶ц椋炴槦鐏ぇ妯″瀷杩涜鏅鸿兘鍒嗘瀽
- 闇€瑕佹枃鏈垎鏋愬姛鑳斤紙鎯呮劅鍒嗘瀽銆佹憳瑕佹彁鍙栥€佷富棰樿瘑鍒瓑锛?- 闇€瑕佹櫤鑳藉璇濅氦浜掑姛鑳?- 闇€瑕佸唴瀹圭敓鎴愬姛鑳斤紙鏂囩珷銆佹憳瑕併€佸ぇ绾茬瓑锛?- 闇€瑕佸叾浠朅I妯″瀷鑳藉姏鏀寔
- 闇€瑕佷笌AI妯″瀷闆嗘垚鐨勫叾浠栧垎鏋愪换鍔?
## 蹇€熷紑濮?
褰撶敤鎴疯姹侫I妯″瀷闆嗘垚鏈嶅姟鏃讹細
1. **閰嶇疆**API鍑瘉锛圓PP ID銆丄PI Key銆丄PI Secret锛?2. **閫夋嫨**閫傚綋鐨勬ā鍨嬪拰鍔熻兘
3. **璋冪敤**鐩稿簲鐨凙I鍔熻兘
4. **澶勭悊**杩斿洖鐨凙I鍝嶅簲
5. **搴旂敤**AI鍒嗘瀽缁撴灉

## 鏍稿績鍔熻兘

### 1. 鏂囨湰鍒嗘瀽鍔熻兘
- **鎯呮劅鍒嗘瀽**锛氬垎鏋愭枃鏈儏鎰熷€惧悜鍜屾儏缁壊褰?- **鎽樿鎻愬彇**锛氫粠闀挎枃鏈腑鎻愬彇鍏抽敭淇℃伅鎽樿
- **涓婚璇嗗埆**锛氳瘑鍒枃鏈殑涓昏涓婚鍜岃瘽棰?- **閫氱敤鍒嗘瀽**锛氬鏂囨湰杩涜鍏ㄩ潰鍒嗘瀽
- **澶氭ā鍨嬫敮鎸?*锛氭敮鎸佷笉鍚屾槦鐏ā鍨嬩互閫傚簲涓嶅悓鍒嗘瀽闇€姹?
### 2. 鏅鸿兘瀵硅瘽鍔熻兘
- **鑷劧瀵硅瘽**锛氬熀浜庢槦鐏ぇ妯″瀷鐨勮嚜鐒惰瑷€浜や簰
- **鍘嗗彶璁板繂**锛氭敮鎸佸璇濆巻鍙茬鐞?- **涓婁笅鏂囩悊瑙?*锛氫繚鎸佸璇濅笂涓嬫枃杩炶疮鎬?- **澶氳疆浜や簰**锛氭敮鎸佸鏉傜殑澶氳疆瀵硅瘽鍦烘櫙
- **鎰忓浘璇嗗埆**锛氱悊瑙ｇ敤鎴峰璇濇剰鍥?
### 3. 鍐呭鐢熸垚鍔熻兘
- **鏂囩珷鐢熸垚**锛氱敓鎴愮粨鏋勫寲鏂囩珷鍐呭
- **鎽樿鐢熸垚**锛氬垱寤哄唴瀹规憳瑕?- **澶х翰鐢熸垚**锛氭瀯寤哄唴瀹瑰ぇ绾茬粨鏋?- **鍒涙剰鍐呭**锛氱敓鎴愬垱鎰忔€ф枃鏈唴瀹?- **涓撲笟鍐呭**锛氱敓鎴愮壒瀹氶鍩熺殑涓撲笟鍐呭

### 4. 妯″瀷绠＄悊鍔熻兘
- **澶氭ā鍨嬫敮鎸?*锛氭敮鎸乻park-max銆乻park-pro銆乻park-standard銆乻park-mini銆乻park-vision绛夋ā鍨?- **妯″瀷閫夋嫨**锛氭牴鎹换鍔￠渶姹傞€夋嫨鏈€閫傚悎鐨勬ā鍨?- **鎬ц兘浼樺寲**锛氭牴鎹换鍔″鏉傚害閫夋嫨鏈€浼樻ā鍨?- **鎴愭湰鎺у埗**锛氬湪鏁堟灉鍜屾垚鏈棿鍙栧緱骞宠　
- **妯″瀷鍒囨崲**锛氱伒娲诲垏鎹笉鍚屾ā鍨?
### 5. API闆嗘垚绠＄悊
- **鍑瘉绠＄悊**锛氬畨鍏ㄥ瓨鍌ㄥ拰绠＄悊API鍑瘉
- **璇锋眰鏋勫缓**锛氭爣鍑嗗寲API璇锋眰鏍煎紡
- **鍝嶅簲澶勭悊**锛氳В鏋愬拰澶勭悊API鍝嶅簲
- **閿欒澶勭悊**锛氬鐞咥PI璋冪敤寮傚父鍜岄敊璇?- **闄愭祦鎺у埗**锛氱鐞咥PI璋冪敤棰戠巼

## 璇︾粏浣跨敤娴佺▼

### 绗竴姝ワ細閰嶇疆API鍑瘉
```javascript
// 閰嶇疆绉戝ぇ璁API鍑瘉
const config = {
  appId: process.env.SPARK_APP_ID,      // 绉戝ぇ璁搴旂敤ID
  apiKey: process.env.SPARK_API_KEY,    // 绉戝ぇ璁API Key
  apiSecret: process.env.SPARK_API_SECRET, // 绉戝ぇ璁API Secret
  model: "spark-max",                   // 榛樿浣跨敤妯″瀷
  baseUrl: "https://spark-api-open.xf-yun.com/v1/chat/completions" // API鍩虹URL
};

const sparkSkill = new SparkIntegrationSkill(config);
```

**鍏抽敭瑕佺偣**锛?- 纭繚宸茶幏鍙栨湁鏁堢殑API鍑瘉
- 閫氳繃鐜鍙橀噺瀹夊叏瀛樺偍鏁忔劅淇℃伅
- 閫夋嫨閫傚悎浠诲姟鐨勬ā鍨?- 楠岃瘉閰嶇疆鏄惁姝ｇ‘

### 绗簩姝ワ細鎵ц鏂囨湰鍒嗘瀽
```javascript
// 鎵ц鏂囨湰鍒嗘瀽
const textAnalysisResult = await sparkSkill.analyzeText("浠婂ぉ澶╂皵鐪熷ソ锛屽績鎯呬篃寰堟剦鎮?, {
  analysisType: "sentiment",  // 鍒嗘瀽绫诲瀷锛歴entiment, summary, topic, general
  model: "spark-pro"          // 鎸囧畾妯″瀷
});
```

**鍒嗘瀽鍐呭**锛?- 鏍规嵁鍒嗘瀽绫诲瀷鏋勫缓閫傚綋鐨勬彁绀鸿瘝
- 璋冪敤鏄熺伀澶фā鍨嬭繘琛屽垎鏋?- 澶勭悊鍜岃В鏋愭ā鍨嬪搷搴?- 杩斿洖缁撴瀯鍖栧垎鏋愮粨鏋?
### 绗笁姝ワ細鎵ц鏅鸿兘瀵硅瘽
```javascript
// 鎵ц鏅鸿兘瀵硅瘽
const chatResult = await sparkSkill.chat("浣犺兘甯垜鍒嗘瀽涓€涓嬭繖浠芥姤鍛婂悧锛?, {
  history: [                  // 瀵硅瘽鍘嗗彶锛堝彲閫夛級
    { role: "user", content: "浣犲ソ" },
    { role: "assistant", content: "浣犲ソ锛佹垜鍙互甯綘鍒嗘瀽鎶ュ憡銆佸洖绛旈棶棰樼瓑銆? }
  ],
  model: "spark-max"         // 鎸囧畾妯″瀷
});
```

**瀵硅瘽澶勭悊**锛?- 鏁村悎瀵硅瘽鍘嗗彶鍜屽綋鍓嶆秷鎭?- 鏋勫缓涓婁笅鏂囪繛璐殑鎻愮ず璇?- 璋冪敤鏄熺伀澶фā鍨嬭繘琛屽璇?- 杩斿洖鑷劧娴佺晠鐨勫搷搴?
### 绗洓姝ワ細鎵ц鍐呭鐢熸垚
```javascript
// 鎵ц鍐呭鐢熸垚
const contentGenerationResult = await sparkSkill.generateContent("浜哄伐鏅鸿兘鍙戝睍瓒嬪娍", {
  contentType: "article",    // 鍐呭绫诲瀷锛歛rticle, summary, outline, general
  model: "spark-max"         // 鎸囧畾妯″瀷
});
```

**鐢熸垚澶勭悊**锛?- 鏍规嵁鍐呭绫诲瀷璋冩暣鎻愮ず璇?- 璋冪敤鏄熺伀澶фā鍨嬭繘琛屽唴瀹圭敓鎴?- 澶勭悊鐢熸垚鐨勫唴瀹瑰苟杩斿洖
- 纭繚鍐呭璐ㄩ噺鍜岀浉鍏虫€?
### 绗簲姝ワ細鎵ц楂樼骇AI鍔熻兘
```javascript
// 鏌ヨ鍙敤妯″瀷
const availableModels = sparkSkill.getAvailableModels();

// 鎵ц鍋ュ悍妫€鏌?const healthStatus = await sparkSkill.healthCheck();

// 浣跨敤鑷畾涔夋ā鍨嬪弬鏁?const customResult = await sparkSkill.analyzeText("鑷畾涔夊垎鏋愬唴瀹?, {
  model: "spark-vision",     // 浣跨敤澶氭ā鎬佹ā鍨?  analysisType: "general"
});
```

## 鎶€鏈疄鐜?
### 鏋舵瀯璁捐
- **妯″潡鍖栬璁?*锛欰PI璋冪敤銆佸搷搴斿鐞嗐€侀敊璇鐞嗙瓑妯″潡鍖?- **娓愯繘寮忔姭闇?*锛氭牴鎹敤鎴烽渶姹傞€愭灞曞紑璇︾粏鍔熻兘
- **瀹夊叏璁捐**锛氬嚟璇佸畨鍏ㄥ瓨鍌ㄥ拰浼犺緭
- **閿欒鎭㈠**锛欰PI璋冪敤閿欒澶勭悊鍜屾仮澶嶆満鍒?
### 鏁版嵁缁撴瀯
```javascript
// 杈撳叆鏁版嵁缁撴瀯
{
  prompt: "鐢ㄦ埛杈撳叆鐨勬彁绀鸿瘝",
  model: "spark-max",        // 鎸囧畾妯″瀷
  options: {
    analysisType: "general", // 鍒嗘瀽绫诲瀷锛堜粎鏂囨湰鍒嗘瀽鏃讹級
    contentType: "general",  // 鍐呭绫诲瀷锛堜粎鍐呭鐢熸垚鏃讹級
    history: [],             // 瀵硅瘽鍘嗗彶锛堜粎瀵硅瘽鏃讹級
    temperature: 0.7,        // 鐢熸垚娓╁害锛堝彲閫夛級
    maxTokens: 2048          // 鏈€澶т护鐗屾暟锛堝彲閫夛級
  }
}

// 杈撳嚭缁撴灉缁撴瀯
{
  success: true,             // 鎵ц鏄惁鎴愬姛
  result: {                  // API鍝嶅簲鍐呭
    content: "AI鐢熸垚鐨勫唴瀹?,
    model: "spark-max",      // 浣跨敤鐨勬ā鍨?    tokensUsed: 150          // 浣跨敤鐨勪护鐗屾暟
  },
  metadata: {
    timestamp: "2025-12-26T10:30:00Z", // 鏃堕棿鎴?    model: "spark-max",      // 浣跨敤鐨勬ā鍨?    skill: "spark-integration" // 鎶€鑳絀D
  }
}
```

## 杈撳嚭鏍煎紡

缁熶竴鐨勪笁灞侸SON鏍煎紡锛?
```json
{
  "summary": {
    "api_call_success": true,
    "model_used": "spark-max",
    "response_tokens": 156,
    "processing_time": "1.2s",
    "analysis_type": "text-analysis"
  },
  "details": {
    "response": {
      "content": "瀵规偍鎻愪緵鐨勬枃鏈繘琛屼簡璇︾粏鍒嗘瀽...",
      "model": "spark-max",
      "tokensUsed": 156,
      "temperature": 0.7
    },
    "metadata": {
      "timestamp": "2025-12-26T10:30:00Z",
      "model": "spark-max",
      "skill": "spark-integration"
    },
    "apiDetails": {
      "requestId": "req-1234567890",
      "usage": {
        "promptTokens": 25,
        "completionTokens": 156,
        "totalTokens": 181
      }
    }
  },
  "metadata": {
    "timestamp": "2025-12-26T10:30:00Z",
    "version": "2.0.0",
    "skill": "spark-integration",
    "validationScore": 95
  }
}
```

## 璐ㄩ噺妫€鏌ユ竻鍗?
鍦ㄥ畬鎴怉I妯″瀷闆嗘垚鍚庯紝璇锋鏌ヤ互涓嬮」鐩細

- [ ] API鍑瘉閰嶇疆姝ｇ‘
- [ ] 妯″瀷閫夋嫨閫傚綋
- [ ] 璇锋眰鏋勫缓姝ｇ‘
- [ ] 鍝嶅簲澶勭悊瀹屾暣
- [ ] 閿欒澶勭悊瀹屽杽
- [ ] 鏂囨湰鍒嗘瀽鍑嗙‘
- [ ] 瀵硅瘽浜や簰鑷劧
- [ ] 鍐呭鐢熸垚璐ㄩ噺楂?- [ ] 閬靛惊瀹夊叏鏈€浣冲疄璺?- [ ] 闄愭祦鎺у埗閫傚綋
- [ ] 楠岃瘉鍒嗘暟杈惧埌瑕佹眰锛?0鍒嗕互涓婏級

## 甯歌闂

**蹇€熻瘖鏂?*锛?- API璋冪敤澶辫触 鈫?妫€鏌PI鍑瘉閰嶇疆
- 鍝嶅簲璐ㄩ噺浣?鈫?鏇存崲鏇撮€傚悎鐨勬ā鍨?- 鍝嶅簲鏃堕棿闀?鈫?鑰冭檻浣跨敤鏇磋交閲忕骇妯″瀷
- 楠岃瘉鍒嗘暟浣?鈫?妫€鏌PI璋冪敤閫昏緫鍜屽弬鏁?
## 娣卞叆瀛︿範

- **绉戝ぇ璁API鏂囨。**锛歚references/spark-api-docs.md` - 鏄熺伀澶фā鍨婣PI璇︾粏鏂囨。
- **妯″瀷閫夋嫨鎸囧崡**锛歚references/model-selection.md` - 涓嶅悓妯″瀷鐨勯€傜敤鍦烘櫙
- **鎻愮ず宸ョ▼**锛歚references/prompt-engineering.md` - 浼樺寲鎻愮ず璇嶇殑鎶€宸?- **AI闆嗘垚妯″紡**锛歚references/ai-integration-patterns.md` - AI鏈嶅姟闆嗘垚鏈€浣冲疄璺?- **瀹夊叏瀹炶返**锛歚references/ai-security.md` - AI鏈嶅姟瀹夊叏鏈€浣冲疄璺?
## 瀹屾垚鏍囧織

瀹屾垚楂樿川閲忕殑AI妯″瀷闆嗘垚搴斾骇鍑猴細
1. 鎴愬姛璋冪敤鏄熺伀澶фā鍨?2. 鑾峰彇楂樿川閲廇I鍝嶅簲
3. 姝ｇ‘澶勭悊API鍝嶅簲
4. 閫傚綋閿欒澶勭悊
5. 瀹夊叏鐨勫嚟璇佺鐞?
---

*姝ゆ妧鑳戒负AI妯″瀷闆嗘垚鎻愪緵涓撲笟鐨勬帴鍙ｆ敮鎸侊紝纭繚涓庣澶ц椋炴槦鐏ぇ妯″瀷鐨勫畨鍏ㄣ€侀珮鏁堥泦鎴愶紝涓哄叾浠栨妧鑳芥彁渚涘彲闈犵殑AI鑳藉姏鏀寔銆?
