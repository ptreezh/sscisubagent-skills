#!/usr/bin/env python3
"""
Questionnaire Designer Tool
Designs survey questionnaire structure following Dillman's Tailored Design Method.
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
        return {"research_objective": content}


def design_questionnaire(data: Dict) -> Dict[str, Any]:
    """Design questionnaire structure."""
    objective = data.get("research_objective", data.get("objective", ""))
    variables = data.get("variables", [])

    # Default questionnaire sections
    sections = [
        {
            "name": "Introduction",
            "description": "Welcome message, purpose, consent",
            "questions": [],
            "order": 1,
        },
        {
            "name": "Demographics",
            "description": "Background information",
            "questions": [],
            "order": 2,
        },
        {
            "name": "Main Constructs",
            "description": "Core measurement questions",
            "questions": [],
            "order": 3,
        },
        {
            "name": "Behavioral Questions",
            "description": "Behavior and action questions",
            "questions": [],
            "order": 4,
        },
        {
            "name": "Attitudinal Questions",
            "description": "Opinions and attitudes",
            "questions": [],
            "order": 5,
        },
        {
            "name": "Closing",
            "description": "Thank you, debrief",
            "questions": [],
            "order": 6,
        },
    ]

    # Generate question templates based on variables
    questions = []
    if variables:
        for var in variables:
            q = {
                "id": f"Q{len(questions) + 1}",
                "variable": var.get("name", "unknown"),
                "type": var.get("type", "multiple_choice"),
                "text": f"{var.get('label', 'Please rate...')}",
                "options": var.get(
                    "options", generate_default_options(var.get("type", "likert"))
                ),
                "required": var.get("required", True),
                "section": infer_section(var.get("type", "likert")),
            }
            questions.append(q)
    else:
        # Generate sample questions based on objective
        sample_questions = [
            {
                "id": "Q1",
                "type": "likert",
                "text": f"How satisfied are you with {objective}?",
                "options": [
                    "Very Dissatisfied",
                    "Dissatisfied",
                    "Neutral",
                    "Satisfied",
                    "Very Satisfied",
                ],
                "required": True,
                "section": "Main Constructs",
            },
            {
                "id": "Q2",
                "type": "likert",
                "text": "How likely are you to recommend this?",
                "options": [
                    "Very Unlikely",
                    "Unlikely",
                    "Neutral",
                    "Likely",
                    "Very Likely",
                ],
                "required": True,
                "section": "Main Constructs",
            },
            {
                "id": "Q3",
                "type": "multiple_choice",
                "text": "What is your age group?",
                "options": ["18-24", "25-34", "35-44", "45-54", "55+"],
                "required": True,
                "section": "Demographics",
            },
            {
                "id": "Q4",
                "type": "open",
                "text": "Any additional comments?",
                "options": None,
                "required": False,
                "section": "Closing",
            },
        ]
        questions = sample_questions

    # Assign questions to sections
    for q in questions:
        section_name = q.pop("section", "Main Constructs")
        for s in sections:
            if s["name"] == section_name:
                s["questions"].append(q)
                break

    return {
        "questionnaire_title": f"Survey: {objective}",
        "total_sections": len(sections),
        "total_questions": len(questions),
        "estimated_duration": f"{len(questions) * 2} minutes",
        "sections": sections,
        "design_principles": [
            "Logical flow from easy to difficult",
            "Demographics at the end to not bias responses",
            "Open-ended questions at the end",
            "Likert scales consistently formatted",
        ],
    }


def generate_default_options(question_type: str) -> List[str]:
    """Generate default options based on question type."""
    if question_type == "likert5":
        return ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]
    elif question_type == "likert7":
        return [
            "Strongly Disagree",
            "Disagree",
            "Somewhat Disagree",
            "Neutral",
            "Somewhat Agree",
            "Agree",
            "Strongly Agree",
        ]
    elif question_type == "frequency":
        return ["Never", "Rarely", "Sometimes", "Often", "Always"]
    elif question_type == "quality":
        return ["Poor", "Fair", "Good", "Very Good", "Excellent"]
    else:
        return ["Yes", "No"]


def infer_section(question_type: str) -> str:
    """Infer which section a question belongs to."""
    if question_type in ["demographic", "multiple_choice"]:
        return "Demographics"
    elif question_type == "open":
        return "Closing"
    else:
        return "Main Constructs"


def main():
    parser = argparse.ArgumentParser(description="Design survey questionnaire")
    parser.add_argument("-i", "--input", required=True, help="Input data file")
    parser.add_argument("-o", "--output", required=True, help="Output file path")
    args = parser.parse_args()

    data = load_input_data(args.input)
    result = design_questionnaire(data)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Questionnaire design saved to {args.output}")
    print(f"Total questions: {result['total_questions']}")
    print(f"Estimated duration: {result['estimated_duration']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
