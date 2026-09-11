#!/usr/bin/env python3
"""
Coding Scheme Manager for Content Analysis
Manages coding categories, definitions, and coding books
"""

import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum

class CategoryType(Enum):
    NOMINAL = "nominal"
    ORDINAL = "ordinal"
    INTERVAL = "interval"
    RATIO = "ratio"

@dataclass
class CodingCategory:
    """Represents a single coding category"""
    code: str
    name: str
    definition: str
    examples: List[str] = field(default_factory=list)
    exclusion_rules: List[str] = field(default_factory=list)
    category_type: str = "nominal"
    parent_code: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return asdict(self)

@dataclass
class CodingScheme:
    """Represents a complete coding scheme"""
    name: str
    description: str
    categories: List[Dict]
    coding_unit: str = "sentence"
    version: str = "1.0"
    created_date: str = ""
    author: str = ""
    
    def to_dict(self) -> Dict:
        return asdict(self)

class CodingSchemeManager:
    """Manages coding schemes for content analysis"""
    
    def __init__(self):
        self.scheme: Optional[CodingScheme] = None
    
    def create_scheme(self, name: str, description: str, 
                     coding_unit: str = "sentence") -> CodingScheme:
        """Create a new coding scheme"""
        from datetime import datetime
        
        self.scheme = CodingScheme(
            name=name,
            description=description,
            categories=[],
            coding_unit=coding_unit,
            created_date=datetime.now().strftime("%Y-%m-%d")
        )
        return self.scheme
    
    def add_category(self, code: str, name: str, definition: str,
                    examples: List[str] = None, 
                    exclusion_rules: List[str] = None,
                    category_type: str = "nominal",
                    parent_code: str = None) -> CodingCategory:
        """Add a category to the coding scheme"""
        
        if self.scheme is None:
            raise ValueError("No scheme created. Call create_scheme() first.")
        
        category = CodingCategory(
            code=code,
            name=name,
            definition=definition,
            examples=examples or [],
            exclusion_rules=exclusion_rules or [],
            category_type=category_type,
            parent_code=parent_code
        )
        
        self.scheme.categories.append(category.to_dict())
        return category
    
    def get_category(self, code: str) -> Optional[Dict]:
        """Get a category by code"""
        if self.scheme is None:
            return None
        
        for cat in self.scheme.categories:
            if cat['code'] == code:
                return cat
        return None
    
    def update_category(self, code: str, **kwargs) -> bool:
        """Update a category"""
        if self.scheme is None:
            return False
        
        for i, cat in enumerate(self.scheme.categories):
            if cat['code'] == code:
                for key, value in kwargs.items():
                    if key in cat:
                        cat[key] = value
                return True
        return False
    
    def remove_category(self, code: str) -> bool:
        """Remove a category"""
        if self.scheme is None:
            return False
        
        for i, cat in enumerate(self.scheme.categories):
            if cat['code'] == code:
                self.scheme.categories.pop(i)
                return True
        return False
    
    def validate_scheme(self) -> Dict:
        """Validate the coding scheme for mutual exclusivity and exhaustiveness"""
        results = {
            'valid': True,
            'warnings': [],
            'errors': []
        }
        
        if self.scheme is None:
            results['errors'].append("No scheme created")
            results['valid'] = False
            return results
        
        # Check for duplicate codes
        codes = [cat['code'] for cat in self.scheme.categories]
        duplicates = [code for code in set(codes) if codes.count(code) > 1]
        if duplicates:
            results['errors'].append(f"Duplicate codes found: {duplicates}")
            results['valid'] = False
        
        # Check for missing definitions
        for cat in self.scheme.categories:
            if not cat['definition']:
                results['warnings'].append(f"Category '{cat['code']}' lacks definition")
        
        # Check for missing examples
        for cat in self.scheme.categories:
            if not cat['examples']:
                results['warnings'].append(f"Category '{cat['code']}' lacks examples")
        
        # Check hierarchy consistency
        parent_codes = set()
        for cat in self.scheme.categories:
            if cat['parent_code']:
                parent_codes.add(cat['parent_code'])
        
        existing_codes = set(codes)
        missing_parents = parent_codes - existing_codes
        if missing_parents:
            results['errors'].append(f"Missing parent categories: {missing_parents}")
            results['valid'] = False
        
        return results
    
    def generate_coding_book(self) -> str:
        """Generate a formatted coding book"""
        if self.scheme is None:
            return "No scheme created"
        
        output = []
        output.append(f"# {self.scheme.name}")
        output.append(f"\n## Description\n{self.scheme.description}")
        output.append(f"\n## Coding Unit: {self.scheme.coding_unit}")
        output.append(f"\n## Categories ({len(self.scheme.categories)} total)\n")
        
        # Group by parent
        root_categories = [c for c in self.scheme.categories if not c['parent_code']]
        child_categories = [c for c in self.scheme.categories if c['parent_code']]
        
        for cat in root_categories:
            output.append(self._format_category(cat, level=1))
            
            # Add children
            children = [c for c in child_categories if c['parent_code'] == cat['code']]
            for child in children:
                output.append(self._format_category(child, level=2))
        
        return "\n".join(output)
    
    def _format_category(self, cat: Dict, level: int = 1) -> str:
        """Format a single category for the coding book"""
        indent = "  " * (level - 1)
        lines = []
        
        lines.append(f"\n{indent}### {cat['code']}: {cat['name']}")
        lines.append(f"{indent}**Definition**: {cat['definition']}")
        
        if cat['examples']:
            lines.append(f"{indent}**Examples**:")
            for ex in cat['examples'][:3]:
                lines.append(f"{indent}- {ex}")
        
        if cat['exclusion_rules']:
            lines.append(f"{indent}**Exclusion Rules**:")
            for rule in cat['exclusion_rules']:
                lines.append(f"{indent}- {rule}")
        
        return "\n".join(lines)
    
    def export_json(self) -> str:
        """Export scheme to JSON"""
        if self.scheme is None:
            return "{}"
        return json.dumps(self.scheme.to_dict(), indent=2, ensure_ascii=False)
    
    def import_json(self, json_str: str) -> CodingScheme:
        """Import scheme from JSON"""
        data = json.loads(json_str)
        self.scheme = CodingScheme(**data)
        return self.scheme
    
    def create_scheme_from_template(self, template_type: str) -> CodingScheme:
        """Create scheme from predefined template"""
        
        templates = {
            'sentiment': {
                'name': 'Sentiment Analysis Coding Scheme',
                'description': 'Coding scheme for sentiment analysis',
                'categories': [
                    {'code': 'POS', 'name': 'Positive', 'definition': 'Content expressing positive sentiment', 'examples': ['Great!', 'Excellent work']},
                    {'code': 'NEG', 'name': 'Negative', 'definition': 'Content expressing negative sentiment', 'examples': ['Terrible', 'Very disappointed']},
                    {'code': 'NEU', 'name': 'Neutral', 'definition': 'Content without clear sentiment', 'examples': ['The meeting is at 3pm']}
                ]
            },
            'news_frame': {
                'name': 'News Frame Analysis Coding Scheme',
                'description': 'Coding scheme for news framing analysis',
                'categories': [
                    {'code': 'ECO', 'name': 'Economic Frame', 'definition': 'Economic consequences or considerations', 'examples': ['Stock market impact', 'Cost to taxpayers']},
                    {'code': 'ENV', 'name': 'Environmental Frame', 'definition': 'Environmental impact or concerns', 'examples': ['Climate change', 'Pollution']},
                    {'code': 'POL', 'name': 'Political Frame', 'definition': 'Political aspects or implications', 'examples': ['Policy debate', 'Political pressure']},
                    {'code': 'SCI', 'name': 'Scientific Frame', 'definition': 'Scientific evidence or research', 'examples': ['Studies show', 'Research indicates']},
                    {'code': 'MOR', 'name': 'Moral Frame', 'definition': 'Ethical or moral considerations', 'examples': ['Right thing to do', 'Ethical concerns']}
                ]
            },
            'issue_attention': {
                'name': 'Issue Attention Coding Scheme',
                'description': 'Coding scheme for issue attention analysis',
                'categories': [
                    {'code': 'DEF', 'name': 'Problem Definition', 'definition': 'Defines or describes the problem'},
                    {'code': 'CAU', 'name': 'Causal Analysis', 'definition': 'Discusses causes of the problem'},
                    {'code': 'SOL', 'name': 'Solution Proposal', 'definition': 'Proposes solutions'},
                    {'code': 'EVA', 'name': 'Evaluation', 'definition': 'Evaluates solutions or policies'},
                    {'code': 'PRO', 'name': 'Prognosis', 'definition': 'Predicts future developments'}
                ]
            }
        }
        
        if template_type not in templates:
            raise ValueError(f"Unknown template: {template_type}. Available: {list(templates.keys())}")
        
        template = templates[template_type]
        scheme = self.create_scheme(
            name=template['name'],
            description=template['description']
        )
        
        for cat in template['categories']:
            self.add_category(**cat)
        
        return scheme


def main():
    """Test the coding scheme manager"""
    manager = CodingSchemeManager()
    
    # Create from template
    print("=" * 50)
    print("Creating Sentiment Analysis Scheme")
    print("=" * 50)
    
    scheme = manager.create_scheme_from_template('sentiment')
    
    # Validate
    results = manager.validate_scheme()
    print(f"\nValidation: {'✓ Valid' if results['valid'] else '✗ Invalid'}")
    if results['warnings']:
        print(f"Warnings: {results['warnings']}")
    if results['errors']:
        print(f"Errors: {results['errors']}")
    
    # Generate coding book
    print("\n" + "=" * 50)
    print("Coding Book Preview")
    print("=" * 50)
    print(manager.generate_coding_book())


if __name__ == '__main__':
    main()
