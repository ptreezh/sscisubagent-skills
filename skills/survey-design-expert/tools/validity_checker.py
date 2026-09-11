#!/usr/bin/env python3
"""
Validity Checker Tool
Checks content validity and construct validity of survey instruments.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Any


def load_input_data(input_path: str) -> Dict[str, Any]:
    """Load input data from file."""
    path = Path(input_path)
    if not path.exists():
        return {}

    if path.suffix == ".json":
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        return {"questions": [{"text": content[:200]}]}


def check_validity(data: Dict) -> Dict[str, Any]:
    """Check validity of survey instrument."""
    questions = data.get("questions", [])
    constructs = data.get("constructs", [])
    raw_text = data.get("raw_text", "")

    if not questions and raw_text:
        questions = [{"text": raw_text[:300], "type": "inferred"}]

    # Content validity assessment
    content_validity = assess_content_validity(questions, constructs)

    # Construct validity assessment
    construct_validity = assess_construct_validity(questions, constructs)

    # Face validity assessment
    face_validity = assess_face_validity(questions)

    return {
        "validity_summary": {
            "content_validity": content_validity,
            "construct_validity": construct_validity,
            "face_validity": face_validity,
            "overall_valid": content_validity["is_valid"]
            and construct_validity["is_valid"],
        },
        "detailed_results": {
            "content_validity": content_validity,
            "construct_validity": construct_validity,
            "face_validity": face_validity,
        },
        "recommendations": generate_validity_recommendations(
            content_validity, construct_validity, face_validity
        ),
    }


def assess_content_validity(
    questions: List[Dict], constructs: List[Dict]
) -> Dict[str, Any]:
    """Assess content validity."""
    if not questions:
        return {"is_valid": False, "coverage": 0, "issues": ["No questions to assess"]}

    issues = []

    # Check question-construct alignment
    if not constructs and len(questions) > 0:
        issues.append("No explicit construct definitions - recommend adding")

    # Check coverage
    coverage = min(len(questions) / 5.0, 1.0)  # At least 5 questions per construct

    # Check for different question types
    question_types = set(q.get("type", "unknown") for q in questions)
    if len(question_types) < 2 and len(questions) > 3:
        issues.append("Consider adding variety in question types")

    return {
        "is_valid": len(issues) == 0,
        "coverage": coverage,
        "question_count": len(questions),
        "issues": issues,
        "rating": "adequate" if coverage >= 0.6 else "needs_improvement",
    }


def assess_construct_validity(
    questions: List[Dict], constructs: List[Dict]
) -> Dict[str, Any]:
    """Assess construct validity."""
    if not constructs:
        return {
            "is_valid": False,
            "note": "Requires expert review for full construct validity assessment",
        }

    # Check if each construct has multiple items
    construct_items = {}
    for q in questions:
        construct = q.get("construct", "unknown")
        if construct not in construct_items:
            construct_items[construct] = 0
        construct_items[construct] += 1

    multi_item_constructs = sum(1 for v in construct_items.values() if v >= 3)

    return {
        "is_valid": multi_item_constructs > 0,
        "construct_count": len(construct_items),
        "multi_item_constructs": multi_item_constructs,
        "note": "Full construct validity requires factor analysis",
    }


def assess_face_validity(questions: List[Dict]) -> Dict[str, Any]:
    """Assess face validity."""
    if not questions:
        return {"is_valid": False, "note": "No questions to assess"}

    # Check for clear question wording
    unclear_count = 0
    for q in questions:
        text = q.get("text", "")
        if len(text) < 5 or len(text) > 200:
            unclear_count += 1

    clarity_ratio = 1 - (unclear_count / len(questions))

    return {
        "is_valid": clarity_ratio >= 0.8,
        "clear_questions": len(questions) - unclear_count,
        "unclear_questions": unclear_count,
        "rating": "good" if clarity_ratio >= 0.8 else "needs_review",
    }


def generate_validity_recommendations(
    content: Dict, construct: Dict, face: Dict
) -> List[str]:
    """Generate validity recommendations."""
    recommendations = []

    if not content["is_valid"]:
        recommendations.append(
            "Improve content validity by defining constructs explicitly"
        )

    if content.get("coverage", 0) < 0.8:
        recommendations.append("Add more questions to improve construct coverage")

    if not construct["is_valid"]:
        recommendations.append("Each construct should have at least 3 items")

    if not face["is_valid"]:
        recommendations.append("Review question clarity - simplify wording")

    if content["is_valid"] and construct["is_valid"] and face["is_valid"]:
        recommendations.append(
            "Validity assessment looks adequate - proceed with pilot testing"
        )

    return recommendations


def main():
    parser = argparse.ArgumentParser(description="Check survey validity")
    parser.add_argument("-i", "--input", required=True, help="Input data file")
    parser.add_argument("-o", "--output", required=True, help="Output file path")
    args = parser.parse_args()

    data = load_input_data(args.input)
    result = check_validity(data)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Validity check saved to {args.output}")
    print(f"Overall valid: {result['validity_summary']['overall_valid']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
