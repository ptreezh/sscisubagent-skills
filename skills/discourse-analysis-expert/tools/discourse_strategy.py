#!/usr/bin/env python3
"""
Discourse Strategy Analyzer
Identifies and analyzes discourse strategies in text
"""

import re
from typing import Dict, List, Tuple, Optional
from collections import Counter, defaultdict

class DiscourseStrategyAnalyzer:
    """Analyze discourse strategies following Wodak's DHA framework"""
    
    def __init__(self):
        self.strategies = {
            'referential': '指称策略',
            'predicational': '谓语策略',
            'argumentative': '论证策略',
            'perspectivization': '视角策略',
            'intensification': '强化策略',
            'mitigation': '弱化策略'
        }
        
        # Linguistic markers
        self.markers = {
            'us_them': {
                'us': ['我们', '我国', '国人', '人民', '同胞'],
                'them': ['他们', '那些人', '外来者', '外国人']
            },
            'positive_self': ['优秀的', '伟大的', '勤劳的', '勇敢的'],
            'negative_other': ['懒惰的', '危险的', '不负责任的', '不可靠的'],
            'intensifiers': ['非常', '极其', '特别', '绝对', '必须', '一定'],
            'mitigators': ['可能', '也许', '某种程度上', '可以说'],
            'modal_verbs': {
                'high': ['必须', '一定', '应该', '需要'],
                'medium': ['可以', '可能', '会'],
                'low': ['或许', '大概']
            }
        }
    
    def analyze_text(self, text: str) -> Dict:
        """
        Analyze discourse strategies in text
        
        Parameters
        ----------
        text : str
            Text to analyze
        
        Returns
        -------
        dict
            Analysis results for each strategy type
        """
        results = {
            'text_length': len(text),
            'strategies': {}
        }
        
        # Referential Strategy
        results['strategies']['referential'] = self._analyze_referential(text)
        
        # Predicational Strategy
        results['strategies']['predicational'] = self._analyze_predicational(text)
        
        # Argumentative Strategy
        results['strategies']['argumentative'] = self._analyze_argumentative(text)
        
        # Perspectivization Strategy
        results['strategies']['perspectivization'] = self._analyze_perspectivization(text)
        
        # Intensification/Mitigation
        results['strategies']['intensification'] = self._analyze_intensification(text)
        results['strategies']['mitigation'] = self._analyze_mitigation(text)
        
        # Overall assessment
        results['summary'] = self._generate_summary(results['strategies'])
        
        return results
    
    def _analyze_referential(self, text: str) -> Dict:
        """Analyze referential/nomination strategy"""
        result = {
            'us_references': [],
            'them_references': [],
            'social_actors': [],
            'binary_opposition': False
        }
        
        # Find us/them references
        for marker in self.markers['us_them']['us']:
            matches = list(re.finditer(marker, text))
            for m in matches:
                result['us_references'].append({
                    'term': marker,
                    'position': m.start(),
                    'context': text[max(0, m.start()-20):m.end()+20]
                })
        
        for marker in self.markers['us_them']['them']:
            matches = list(re.finditer(marker, text))
            for m in matches:
                result['them_references'].append({
                    'term': marker,
                    'position': m.start(),
                    'context': text[max(0, m.start()-20):m.end()+20]
                })
        
        # Check for binary opposition
        if result['us_references'] and result['them_references']:
            result['binary_opposition'] = True
            result['opposition_pattern'] = "建构'我们vs他们'的二元对立"
        
        # Count references
        result['us_count'] = len(result['us_references'])
        result['them_count'] = len(result['them_references'])
        
        return result
    
    def _analyze_predicational(self, text: str) -> Dict:
        """Analyze predicational strategy"""
        result = {
            'positive_predicates': [],
            'negative_predicates': [],
            'evaluation_pattern': None
        }
        
        # Find positive self-predicates
        for marker in self.markers['positive_self']:
            if marker in text:
                result['positive_predicates'].append(marker)
        
        # Find negative other-predicates
        for marker in self.markers['negative_other']:
            if marker in text:
                result['negative_predicates'].append(marker)
        
        # Determine evaluation pattern
        if result['positive_predicates'] and result['negative_predicates']:
            result['evaluation_pattern'] = "正面自我表征 + 负面他者表征"
        elif result['positive_predicates']:
            result['evaluation_pattern'] = "正面自我表征"
        elif result['negative_predicates']:
            result['evaluation_pattern'] = "负面他者表征"
        
        return result
    
    def _analyze_argumentative(self, text: str) -> Dict:
        """Analyze argumentative strategies"""
        result = {
            'topoi': [],
            'evidence_types': []
        }
        
        # Common topoi (argumentation schemes)
        topoi_patterns = {
            'topos_of_advantage': r'(有利|好处|优势|益处)',
            'topos_of_disadvantage': r'(不利|坏处|风险|危害)',
            'topos_of_danger': r'(危险|威胁|危机|风险)',
            'topos_of_humanitarianism': r'(人道|同情|帮助|关爱)',
            'topos_of_justice': r'(公平|正义|权利|平等)',
            'topos_of_authority': r'(专家|研究|数据|证明)',
            'topos_of_history': r'(历史|传统|一直以来)',
            'topos_of_numbers': r'(\d+%|大多数|多数)'
        }
        
        for topos, pattern in topoi_patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                result['topoi'].append({
                    'type': topos,
                    'markers': matches,
                    'count': len(matches)
                })
        
        # Evidence types
        evidence_patterns = {
            'statistical': r'(\d+\.?\d*%|\d+人|\d+个)',
            'expert': r'(专家|学者|研究表明|数据显示)',
            'anecdotal': r'(例如|比如|有一个)',
            'authority': r'(根据|依据|按照)'
        }
        
        for ev_type, pattern in evidence_patterns.items():
            if re.search(pattern, text):
                result['evidence_types'].append(ev_type)
        
        return result
    
    def _analyze_perspectivization(self, text: str) -> Dict:
        """Analyze perspectivization strategies"""
        result = {
            'explicit_stance': [],
            'implicit_stance': [],
            'modality': {}
        }
        
        # Explicit stance markers
        explicit_patterns = [
            r'我认为(.{1,20})',
            r'我们相信(.{1,20})',
            r'我支持(.{1,20})',
            r'我反对(.{1,20})',
            r'重要的是(.{1,20})'
        ]
        
        for pattern in explicit_patterns:
            matches = re.findall(pattern, text)
            for m in matches:
                result['explicit_stance'].append(m[:30])
        
        # Modality analysis
        for level, markers in self.markers['modal_verbs'].items():
            count = sum(text.count(m) for m in markers)
            result['modality'][level] = count
        
        # Dominant modality
        if result['modality']:
            dominant = max(result['modality'].items(), key=lambda x: x[1])
            result['dominant_modality'] = dominant[0]
        
        return result
    
    def _analyze_intensification(self, text: str) -> Dict:
        """Analyze intensification strategies"""
        result = {
            'intensifiers': [],
            'repetition': [],
            'exaggeration': []
        }
        
        # Find intensifiers
        for marker in self.markers['intensifiers']:
            count = text.count(marker)
            if count > 0:
                result['intensifiers'].append({
                    'marker': marker,
                    'count': count
                })
        
        # Check for repetition
        words = text.split()
        word_counts = Counter(words)
        repeated = {w: c for w, c in word_counts.items() if c > 2 and len(w) > 1}
        result['repetition'] = [{'word': w, 'count': c} for w, c in 
                               sorted(repeated.items(), key=lambda x: -x[1])[:5]]
        
        # Exaggeration markers
        exaggeration_patterns = [r'最', r'极其', r'前所未有', r'史无前例']
        for pattern in exaggeration_patterns:
            if re.search(pattern, text):
                result['exaggeration'].append(pattern)
        
        return result
    
    def _analyze_mitigation(self, text: str) -> Dict:
        """Analyze mitigation strategies"""
        result = {
            'mitigators': [],
            'hedging': [],
            'euphemisms': []
        }
        
        # Find mitigators
        for marker in self.markers['mitigators']:
            count = text.count(marker)
            if count > 0:
                result['mitigators'].append({
                    'marker': marker,
                    'count': count
                })
        
        # Hedging expressions
        hedging_patterns = [
            r'某种程度上',
            r'可以说',
            r'似乎',
            r'看起来'
        ]
        
        for pattern in hedging_patterns:
            if pattern in text:
                result['hedging'].append(pattern)
        
        return result
    
    def _generate_summary(self, strategies: Dict) -> Dict:
        """Generate overall summary"""
        summary = {
            'dominant_strategies': [],
            'discourse_pattern': None,
            'ideological_orientation': []
        }
        
        # Identify dominant strategies
        strategy_scores = {}
        
        if strategies['referential'].get('binary_opposition'):
            strategy_scores['referential'] = 2
            summary['discourse_pattern'] = "二元对立话语模式"
        
        if strategies['predicational'].get('positive_predicates'):
            strategy_scores['predicational'] = len(strategies['predicational']['positive_predicates'])
        
        if strategies['intensification'].get('intensifiers'):
            strategy_scores['intensification'] = len(strategies['intensification']['intensifiers'])
        
        if strategies['argumentative'].get('topoi'):
            strategy_scores['argumentative'] = len(strategies['argumentative']['topoi'])
        
        # Sort by score
        sorted_strategies = sorted(strategy_scores.items(), key=lambda x: -x[1])
        summary['dominant_strategies'] = [s[0] for s in sorted_strategies[:3]]
        
        return summary
    
    def compare_texts(self, texts: Dict[str, str]) -> Dict:
        """Compare discourse strategies across multiple texts"""
        results = {}
        
        for label, text in texts.items():
            results[label] = self.analyze_text(text)
        
        # Cross-text comparison
        comparison = {
            'us_reference_comparison': {},
            'modality_comparison': {},
            'strategy_comparison': {}
        }
        
        for label, result in results.items():
            comparison['us_reference_comparison'][label] = \
                result['strategies']['referential'].get('us_count', 0)
            comparison['modality_comparison'][label] = \
                result['strategies']['perspectivization'].get('dominant_modality', 'none')
            comparison['strategy_comparison'][label] = \
                result['summary'].get('dominant_strategies', [])
        
        return {
            'individual_analyses': results,
            'comparison': comparison
        }


def main():
    """Test discourse strategy analyzer"""
    analyzer = DiscourseStrategyAnalyzer()
    
    # Sample text
    sample_text = """
    我们必须团结起来，面对那些试图破坏我们伟大国家的危险势力。
    我们的人民是勤劳勇敢的，而那些外来者带来了不确定性和风险。
    研究表明，我们的政策是正确的。非常重要的一点是，我们要
    坚持自己的道路。也许有些人不同意，但我们必须前进。
    """
    
    print("=" * 60)
    print("DISCOURSE STRATEGY ANALYSIS")
    print("=" * 60)
    
    result = analyzer.analyze_text(sample_text)
    
    print("\n1. REFERENTIAL STRATEGY")
    print("-" * 40)
    print(f"Us references: {result['strategies']['referential']['us_count']}")
    print(f"Them references: {result['strategies']['referential']['them_count']}")
    print(f"Binary opposition: {result['strategies']['referential']['binary_opposition']}")
    
    print("\n2. PREDICATIONAL STRATEGY")
    print("-" * 40)
    print(f"Positive predicates: {result['strategies']['predicational']['positive_predicates']}")
    print(f"Negative predicates: {result['strategies']['predicational']['negative_predicates']}")
    
    print("\n3. SUMMARY")
    print("-" * 40)
    print(f"Dominant strategies: {result['summary']['dominant_strategies']}")
    print(f"Discourse pattern: {result['summary']['discourse_pattern']}")


if __name__ == '__main__':
    main()
