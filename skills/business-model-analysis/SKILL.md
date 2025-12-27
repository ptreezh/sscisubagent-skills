---
name: business-model-analysis
description: 鍒嗘瀽浼佷笟鍟嗕笟妯″紡鐨凙I鎶€鑳斤紝浠庣湡瀹炴暟鎹簮鎼滈泦浼佷笟淇℃伅锛岃繘琛屽叏闈㈢殑鍟嗕笟妯″紡鍒嗘瀽锛屽寘鎷晢涓氭ā寮忕敾甯冦€佺珵浜夊垎鏋愩€佷环鍊间富寮犲垎鏋愮瓑
version: 1.0.0
author: AgentPsy Team
license: MIT
tags: [business, model, analysis, canvas, competitive-analysis, value-proposition]
compatibility: Node.js environment
metadata:
  domain: business-analysis
  methodology: business-modeling
  complexity: intermediate
  integration_type: analysis_tool
  last_updated: "2025-12-26"
allowed-tools: [node, bash, read_file, write_file]
---

# 鍟嗕笟妯″紡鍒嗘瀽鎶€鑳?(Business Model Analysis Skill)

## 姒傝堪

鍟嗕笟妯″紡鍒嗘瀽鎶€鑳芥槸涓€涓笓闂ㄧ敤浜庡垎鏋愪紒涓氬晢涓氭ā寮忕殑AI鎶€鑳姐€傝鎶€鑳借兘澶熶粠鐪熷疄鏁版嵁婧愭悳闆嗕紒涓氫俊鎭紝杩涜鍏ㄩ潰鐨勫晢涓氭ā寮忓垎鏋愶紝鍖呮嫭鍟嗕笟妯″紡鐢诲竷銆佺珵浜夊垎鏋愩€佷环鍊间富寮犲垎鏋愮瓑銆?
## 浣跨敤鏃舵満

浣跨敤姝ゆ妧鑳藉綋鐢ㄦ埛璇锋眰锛?- 浼佷笟鍟嗕笟妯″紡鐨勫叏闈㈠垎鏋?- 鍟嗕笟妯″紡鐢诲竷涔濆ぇ鏍稿績瑕佺礌鐨勫垎鏋?- 浼佷笟绔炰簤鏍煎眬鍜屽畾浣嶇殑璇勪及
- 浼佷笟浠峰€间富寮犲拰鏀跺叆娴佺殑鍒嗘瀽
- 甯傚満瀹氫綅鍜孲WOT鍒嗘瀽
- 浼佷笟鍟嗕笟妯″紡璐ㄩ噺鐨勮瘎浼?- 鍟嗕笟妯″紡鏀硅繘寤鸿鐨勫埗瀹?
## 蹇€熷紑濮?
褰撶敤鎴疯姹傚晢涓氭ā寮忓垎鏋愭椂锛?1. **纭畾**鐩爣鍏徃鍜屽垎鏋愮被鍨?2. **鎼滈泦**浼佷笟鐩稿叧淇℃伅
3. **鎵ц**鍟嗕笟妯″紡鐢诲竷鍒嗘瀽
4. **璇勪及**绔炰簤鏍煎眬鍜屽競鍦哄畾浣?5. **鎻愪緵**鏀硅繘寤鸿鍜岀瓥鐣?
## 鏍稿績鍔熻兘

### 1. 鏁版嵁鎼滈泦鑼冨洿
- **浼佷笟鍩烘湰淇℃伅**锛氬叕鍙哥畝浠嬨€佹垚绔嬫椂闂淬€佹€婚儴浣嶇疆銆佸憳宸ユ暟閲忕瓑
- **璐㈠姟鏁版嵁**锛氳惀鏀躲€佸埄娑︾巼銆佸競鍦轰唤棰濄€佹敹鍏ユ瀯鎴愮瓑
- **鏂伴椈璧勮**锛氫紒涓氬姩鎬併€佸競鍦鸿〃鐜般€佹垬鐣ヨ皟鏁寸瓑
- **琛屼笟鎶ュ憡**锛氬競鍦哄湴浣嶃€佺珵浜変紭鍔裤€佹寫鎴樼瓑

### 2. 鍒嗘瀽绫诲瀷
- **鍟嗕笟妯″紡鐢诲竷**锛氬垎鏋愪節澶ф牳蹇冭绱?- **绔炰簤鍒嗘瀽**锛氳瘎浼扮珵浜夋牸灞€鍜屽畾浣?- **浠峰€间富寮?*锛氳瘑鍒鎴蜂环鍊煎拰宸紓鍖栧洜绱?- **鏀跺叆娴佸垎鏋?*锛氬垎鏋愭敹鍏ユ瀯鎴愬拰璐ㄩ噺
- **缁煎悎鍒嗘瀽**锛氬叏闈㈠晢涓氭ā寮忚瘎浼?
### 3. 鏁版嵁鏉ユ簮
- 鍏徃瀹樼綉鍜屽勾鎶?- 璐㈠姟鏁版嵁搴?- 鏂伴椈璧勮骞冲彴
- 琛屼笟鐮旂┒鎶ュ憡

## 璇︾粏浣跨敤娴佺▼

### 绗竴姝ワ細纭畾鍒嗘瀽鐩爣
```javascript
// 瀹氫箟鍒嗘瀽鐩爣鍜屽弬鏁?const analysisParams = {
  targetCompany: "姣斾簹杩?,              // 鐩爣鍏徃
  analysisType: ["canvas", "competitive", "value_proposition"], // 鍒嗘瀽绫诲瀷
  industryContext: "鏂拌兘婧愭苯杞?,         // 琛屼笟鑳屾櫙
  geographicScope: "鍏ㄧ悆",              // 鍦扮悊鑼冨洿
  analysisDepth: "comprehensive",       // 鍒嗘瀽娣卞害
  dataSources: ["company_website", "financial_db", "news", "reports"] // 鏁版嵁婧?};
```

**鍏抽敭瑕佺偣**锛?- 鏄庣‘鐩爣鍏徃鍜屽垎鏋愮被鍨?- 纭畾琛屼笟鑳屾櫙鍜屽湴鐞嗚寖鍥?- 閫夋嫨閫傚綋鐨勫垎鏋愭繁搴?
### 绗簩姝ワ細鏁版嵁鎼滈泦
```javascript
// 鎵ц鏁版嵁鎼滈泦
const companyData = await businessModelAnalysisSkill.collectData(analysisParams);
```

**鎼滈泦鍐呭**锛?- 浼佷笟鍩烘湰淇℃伅
- 璐㈠姟鏁版嵁
- 鏂伴椈璧勮
- 琛屼笟鎶ュ憡

### 绗笁姝ワ細鍟嗕笟妯″紡鐢诲竷鍒嗘瀽
```javascript
// 鎵ц鍟嗕笟妯″紡鐢诲竷鍒嗘瀽
const canvasAnalysis = await businessModelAnalysisSkill.analyzeCanvas(companyData);
```

**涔濆ぇ鏍稿績瑕佺礌**锛?- **鍏抽敭浼欎即**锛氬叕鍙镐緵搴斿晢鍜屽悎浣滀紮浼?- **鍏抽敭娲诲姩**锛氬叕鍙告渶閲嶈鐨勬椿鍔?- **鍏抽敭璧勬簮**锛氬叕鍙告渶閲嶈鐨勮祫浜?- **浠峰€间富寮?*锛氫负鐗瑰畾瀹㈡埛缁嗗垎鍒涢€犱环鍊肩殑浜у搧鍜屾湇鍔?- **瀹㈡埛鍏崇郴**锛氬叕鍙镐笌鐗瑰畾瀹㈡埛缁嗗垎缇や綋寤虹珛鐨勫叧绯?- **娓犻亾閫氳矾**锛氬叕鍙稿浣曟矡閫氥€佹帴瑙﹀鎴风粏鍒嗙兢浣撳苟浼犻€掍环鍊间富寮?- **瀹㈡埛缁嗗垎**锛氬叕鍙搁拡瀵圭殑涓€涓垨澶氫釜瀹㈡埛缇や綋
- **鎴愭湰缁撴瀯**锛氳繍钀ュ晢涓氭ā寮忔墍浜х敓鐨勬墍鏈夋垚鏈?- **鏀跺叆鏉ユ簮**锛氬叕鍙镐粠姣忎釜瀹㈡埛缁嗗垎缇や綋鑾峰彇鐨勭幇閲戞敹鍏?
### 绗洓姝ワ細绔炰簤鍒嗘瀽
```javascript
// 鎵ц绔炰簤鍒嗘瀽
const competitiveAnalysis = await businessModelAnalysisSkill.analyzeCompetition(companyData, analysisParams.industryContext);
```

**绔炰簤鍒嗘瀽鍐呭**锛?- 鐩存帴绔炰簤瀵规墜璇嗗埆
- 闂存帴绔炰簤瀵规墜璇嗗埆
- 绔炰簤浼樺娍鍜屽姡鍔垮姣?- 甯傚満瀹氫綅璇勪及

### 绗簲姝ワ細浠峰€间富寮犲垎鏋?```javascript
// 鎵ц浠峰€间富寮犲垎鏋?const valuePropositionAnalysis = await businessModelAnalysisSkill.analyzeValueProposition(companyData);
```

**浠峰€间富寮犲垎鏋愬唴瀹?*锛?- 瀹㈡埛浠峰€艰瘑鍒?- 宸紓鍖栧洜绱犲垎鏋?- 瀹㈡埛闇€姹傛弧瓒冲害璇勪及

### 绗叚姝ワ細缁煎悎璇勪及鍜屽缓璁?```javascript
// 鐢熸垚缁煎悎璇勪及鍜屽缓璁?const recommendations = await businessModelAnalysisSkill.generateRecommendations({
  canvasAnalysis: canvasAnalysis,
  competitiveAnalysis: competitiveAnalysis,
  valuePropositionAnalysis: valuePropositionAnalysis
});
```

## 鎶€鏈疄鐜?
### 鏋舵瀯璁捐
- **妯″潡鍖栬璁?*锛氭暟鎹悳闆嗐€佺敾甯冨垎鏋愩€佺珵浜夊垎鏋愩€佷环鍊间富寮犲垎鏋愮瓑妯″潡鍖?- **娓愯繘寮忔姭闇?*锛氭牴鎹垎鏋愭繁搴﹀弬鏁板喅瀹氬垎鏋愯鐣ョ▼搴?- **鐪熷疄鏁版嵁婧?*锛氫粠鍏徃瀹樼綉銆佽储鍔℃暟鎹簱銆佹柊闂诲钩鍙扮瓑鑾峰彇淇℃伅
- **鏁版嵁楠岃瘉**锛氬婧愪氦鍙夐獙璇佸拰瀹屾暣鎬ф鏌?
### 鏁版嵁缁撴瀯
```javascript
// 鍏徃鏁版嵁缁撴瀯
{
  basicInfo: {
    name: "鍏徃鍚嶇О",
    founded: "鎴愮珛鏃堕棿",
    headquarters: "鎬婚儴浣嶇疆",
    employees: "鍛樺伐鏁伴噺",
    description: "鍏徃绠€浠?
  },
  financialData: {
    revenue: "钀ユ敹",
    profitMargin: "鍒╂鼎鐜?,
    marketShare: "甯傚満浠介",
    revenueStreams: "鏀跺叆鏋勬垚"
  },
  news: [
    {
      title: "鏂伴椈鏍囬",
      date: "鏃ユ湡",
      summary: "鎽樿"
    }
  ],
  industryData: {
    marketPosition: "甯傚満鍦颁綅",
    competitiveAdvantages: "绔炰簤浼樺娍",
    challenges: "鎸戞垬"
  }
}

// 鍟嗕笟妯″紡鐢诲竷缁撴瀯
{
  keyPartners: "鍏抽敭浼欎即",
  keyActivities: "鍏抽敭娲诲姩",
  keyResources: "鍏抽敭璧勬簮",
  valuePropositions: "浠峰€间富寮?,
  customerRelationships: "瀹㈡埛鍏崇郴",
  channels: "娓犻亾閫氳矾",
  customerSegments: "瀹㈡埛缁嗗垎",
  costStructure: "鎴愭湰缁撴瀯",
  revenueStreams: "鏀跺叆鏉ユ簮"
}
```

## 杈撳嚭鏍煎紡

缁熶竴鐨勪笁灞侸SON鏍煎紡锛?
```json
{
  "summary": {
    "company_analyzed": "姣斾簹杩?,
    "analysis_types": ["canvas", "competitive", "value_proposition"],
    "competitors_identified": 5,
    "analysis_quality_score": 0.88
  },
  "details": {
    "company_data": {...},
    "canvas_analysis": {...},
    "competitive_analysis": {...},
    "value_proposition_analysis": {...},
    "swot_analysis": {...},
    "recommendations": [...]
  },
  "metadata": {
    "timestamp": "2025-12-26T10:30:00Z",
    "version": "1.0.0",
    "skill": "business-model-analysis"
  }
}
```

## 璐ㄩ噺妫€鏌ユ竻鍗?
鍦ㄥ畬鎴愬晢涓氭ā寮忓垎鏋愬悗锛岃妫€鏌ヤ互涓嬮」鐩細

- [ ] 鐩爣鍏徃鍜屽垎鏋愮被鍨嬪畾涔夋槑纭?- [ ] 鏁版嵁鎼滈泦鍏ㄩ潰涓斿彲闈?- [ ] 鍟嗕笟妯″紡鐢诲竷涔濆ぇ瑕佺礌瀹屾暣鍒嗘瀽
- [ ] 绔炰簤瀵规墜璇嗗埆鍑嗙‘
- [ ] 浠峰€间富寮犲垎鏋愭繁鍏?- [ ] SWOT鍒嗘瀽瀹㈣
- [ ] 鏀硅繘寤鸿鍏蜂綋鍙
- [ ] 鏁版嵁璐ㄩ噺鍒嗘暟杈惧埌瑕佹眰

## 甯歌闂

**蹇€熻瘖鏂?*锛?- 鐢诲竷鍒嗘瀽涓嶅畬鏁?鈫?妫€鏌ユ暟鎹悳闆嗘槸鍚﹀叏闈?- 绔炰簤瀵规墜璇嗗埆涓嶅噯纭?鈫?纭琛屼笟鑳屾櫙璁剧疆姝ｇ‘
- 浠峰€间富寮犲垎鏋愭祬鏄?鈫?澧炲姞鍒嗘瀽娣卞害鍙傛暟
- 鏁版嵁璐ㄩ噺鍒嗘暟浣?鈫?妫€鏌ユ暟鎹簮閫夋嫨

## 娣卞叆瀛︿範

- **鍟嗕笟妯″紡鐢诲竷**锛歚references/business-model-canvas.md` - 涔濆ぇ瑕佺礌璇︾粏鍒嗘瀽
- **绔炰簤鍒嗘瀽鏂规硶**锛歚references/competitive-analysis.md` - 绔炰簤瀵规墜璇嗗埆鍜屽垎鏋愭柟娉?- **浠峰€间富寮犺璁?*锛歚references/value-proposition.md` - 瀹㈡埛浠峰€艰瘑鍒拰宸紓鍖栧垎鏋?- **SWOT鍒嗘瀽**锛歚references/swot-analysis.md` - 浼樺娍銆佸姡鍔裤€佹満浼氥€佸▉鑳佸垎鏋?
## 瀹屾垚鏍囧織

瀹屾垚楂樿川閲忕殑鍟嗕笟妯″紡鍒嗘瀽搴斾骇鍑猴細
1. 瀹屾暣鐨勫晢涓氭ā寮忕敾甯冨垎鏋?2. 璇︾粏鐨勭珵浜夋牸灞€鍒嗘瀽
3. 娣卞叆鐨勪环鍊间富寮犲垎鏋?4. 瀹㈣鐨凷WOT鍒嗘瀽
5. 鍏蜂綋鍙鐨勬敼杩涘缓璁?6. 鏁版嵁璐ㄩ噺鎶ュ憡鍜岄獙璇佺粨鏋?
---

*姝ゆ妧鑳戒负浼佷笟鍟嗕笟妯″紡鍒嗘瀽鎻愪緵涓撲笟鐨勫垎鏋愭敮鎸侊紝浠庣湡瀹炴暟鎹簮鑾峰彇淇℃伅锛屾墽琛屽叏闈㈢殑鍟嗕笟妯″紡鍒嗘瀽锛岀‘淇濆垎鏋愮粨鏋滅殑鍑嗙‘鎬у拰瀹炵敤鎬с€?
