#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
准备真实场景测试数据
创建用于全面测试的模拟数据
"""

import json
import random
from pathlib import Path

def create_open_coding_test_data():
    """创建开放编码测试数据"""
    # 模拟深度访谈文本
    interview_texts = [
        """
我在学习过程中遇到了很多困难。有时候作业很难完成，我不知道该向谁求助。有一次我鼓起勇气向老师请教，老师很耐心地给我讲解了问题。从那以后，我开始主动寻求帮助。

我发现同学们之间也很重要。我们经常一起讨论问题，互相帮助解决难题。有时候我看到其他同学遇到了困难，我也会主动提供帮助。我觉得这种互相支持的氛围很重要。

对于家庭的支持，我也很感激。每当我遇到挫折时，家人总是鼓励我不要放弃。他们给我提供了很多学习资源，也帮我减轻了一些生活压力。这种支持让我能够更专注于学习。
        """,
        """
我觉得教学质量对学习效果影响很大。有的老师讲课很生动，能让学生很容易理解。但也有些老师讲课比较枯燥，学生们注意力很难集中。

课堂互动很重要。老师提问的时候，学生会更积极地思考。但有些学生比较内向，不敢在课堂上发言。我觉得老师应该创造更安全的发言环境。

作业设计也很关键。好的作业能够帮助学生巩固知识，但太多的作业会让学生感到压力。我希望能有更多实践性的作业，而不是纯理论性的。

考试制度也需要改革。现在的考试更多是记忆性的，很难真正考察学生的能力。我希望能有更多开放性的考试，让学生能够展示自己的理解。
        """,
        """
在学校里，师生关系对学习体验影响很大。有的老师很亲和，学生愿意和他们交流。但也有些老师很严厉，学生见了就害怕。

我觉得师生之间应该建立平等的关系。老师不仅仅是知识的传授者，也应该是学生的朋友和引路人。这种关系能让学生更放松地学习。

同学之间的竞争有时会激励大家进步，但过度的竞争会带来负面影响。有时候同学之间会因为成绩而产生矛盾。我觉得应该强调合作而不是竞争。

校园环境也很重要。一个好的学习环境能让学生更专注于学习。我们需要更安静的学习空间，更多的学习资源，更好的设施。
        """
    ]

    # 创建测试数据目录
    test_dir = Path("test_data/real/open_coding")
    test_dir.mkdir(parents=True, exist_ok=True)

    # 保存访谈数据
    for i, text in enumerate(interview_texts, 1):
        with open(test_dir / f"interview_{i}.txt", "w", encoding="utf-8") as f:
            f.write(text.strip())

    print(f"开放编码测试数据已创建: {test_dir}")

def create_network_analysis_test_data():
    """创建网络分析测试数据"""
    # 模拟社交网络数据
    networks = {
        "small_network": {
            "nodes": ["张三", "李四", "王五", "赵六", "钱七", "孙八", "周九", "吴十"],
            "edges": [
                ["张三", "李四", 5], ["张三", "王五", 3], ["张三", "赵六", 2],
                ["李四", "王五", 4], ["李四", "钱七", 3], ["王五", "赵六", 6],
                ["王五", "钱七", 2], ["赵六", "孙八", 4], ["钱七", "孙八", 3],
                ["钱七", "周九", 5], ["孙八", "周九", 2], ["周九", "吴十", 3]
            ]
        },
        "medium_network": {
            "nodes": [f"节点{i}" for i in range(1, 21)],
            "edges": []
        },
        "classroom_network": {
            "nodes": [],
            "edges": []
        }
    }

    # 生成中等规模网络
    nodes_medium = networks["medium_network"]["nodes"]
    edges_medium = networks["medium_network"]["edges"]

    # 创建随机连接
    for i in range(30):
        node1 = random.choice(nodes_medium)
        node2 = random.choice([n for n in nodes_medium if n != node1])
        weight = random.randint(1, 10)
        edges_medium.append([node1, node2, weight])

    # 生成教室网络（学生网络）
    students = [f"学生{i:02d}" for i in range(1, 31)]
    teachers = ["张老师", "李老师", "王老师"]

    networks["classroom_network"]["nodes"] = students + teachers

    # 学生之间的连接
    for i, student in enumerate(students):
        # 每个学生连接3-8个同学
        num_connections = random.randint(3, 8)
        classmates = random.sample([s for s in students if s != student], num_connections)
        for classmate in classmates:
            strength = random.randint(1, 5)
            networks["classroom_network"]["edges"].append([student, classmate, strength])

    # 学生与老师的连接
    for teacher in teachers:
        # 每个老师连接5-15个学生
        num_students = random.randint(5, 15)
        connected_students = random.sample(students, num_students)
        for student in connected_students:
            networks["classroom_network"]["edges"].append([teacher, student, random.randint(3, 8)])

    # 创建测试数据目录
    test_dir = Path("test_data/real/network_analysis")
    test_dir.mkdir(parents=True, exist_ok=True)

    # 保存网络数据
    for network_name, network_data in networks.items():
        with open(test_dir / f"{network_name}.json", "w", encoding="utf-8") as f:
            json.dump(network_data, f, ensure_ascii=False, indent=2)

    print(f"网络分析测试数据已创建: {test_dir}")

def create_theory_saturation_test_data():
    """创建理论饱和度测试数据"""
    # 模拟编码数据
    existing_codes = [
        {"code": "寻求支持", "frequency": 15, "type": "行动概念", "examples": ["向老师请教", "寻求同学帮助"]},
        {"code": "获得帮助", "frequency": 12, "type": "行动概念", "examples": ["得到老师指导", "获得同学支持"]},
        {"code": "提供帮助", "frequency": 8, "type": "行动概念", "examples": ["帮助同学", "分享经验"]},
        {"code": "建立关系", "frequency": 10, "type": "关系概念", "examples": ["建立友好关系", "维护人脉"]},
        {"code": "学习困难", "frequency": 7, "type": "问题概念", "examples": ["作业太难", "理解困难"]},
        {"code": "家庭支持", "frequency": 6, "type": "支持概念", "examples": ["家人鼓励", "提供资源"]},
        {"code": "师生关系", "frequency": 9, "type": "关系概念", "examples": ["平等关系", "友好互动"]},
        {"code": "同学合作", "frequency": 11, "type": "行动概念", "examples": ["小组讨论", "互相帮助"]}
    ]

    # 模拟新访谈中的数据
    new_interviews = [
        {
            "interview_id": "new_001",
            "segments": [
                {
                    "text": "我发现现在学习压力很大，有时候晚上睡不着觉，担心考试考不好。",
                    "concepts": ["学习压力", "睡眠问题", "考试焦虑"]
                },
                {
                    "text": "我尝试了一些放松的方法，比如深呼吸和听音乐，确实感觉好多了。",
                    "concepts": ["放松方法", "深呼吸", "音乐疗法", "情绪调节"]
                }
            ]
        },
        {
            "interview_id": "new_002",
            "segments": [
                {
                    "text": "我参加了一个学习小组，大家一起复习考试，效率提高了不少。",
                    "concepts": ["学习小组", "集体学习", "效率提升"]
                },
                {
                    "text": "但有时候组员之间也会有分歧，需要学会沟通和妥协。",
                    "concepts": ["团队分歧", "沟通技巧", "妥协策略", "团队协作"]
                }
            ]
        }
    ]

    # 模拟范畴数据
    categories = [
        {
            "name": "学习支持系统",
            "definition": "学生在学习过程中获得的各种支持和帮助",
            "attributes": [
                {"name": "支持来源", "dimensions": ["老师", "同学", "家人", "朋友"]},
                {"name": "支持类型", "dimensions": ["学术支持", "情感支持", "资源支持"]},
                {"name": "主动性", "dimensions": ["主动寻求", "被动接受", "相互支持"]}
            ],
            "concepts": ["寻求支持", "获得帮助", "提供帮助"],
            "examples": ["向老师请教", "同学互助", "家庭支持"]
        },
        {
            "name": "人际关系管理",
            "definition": "学生处理和管理各种人际关系的策略和实践",
            "attributes": [
                {"name": "关系类型", "dimensions": ["师生关系", "同学关系", "家庭关系"]},
                {"name": "互动方式", "dimensions": ["面对面", "线上交流", "书面沟通"]},
                {"name": "关系质量", "dimensions": ["亲密程度", "信任度", "稳定性"]}
            ],
            "concepts": ["建立关系", "师生关系", "同学合作"],
            "examples": ["建立友好关系", "团队合作", "师生互动"]
        }
    ]

    # 创建测试数据目录
    test_dir = Path("test_data/real/theory_saturation")
    test_dir.mkdir(parents=True, exist_ok=True)

    # 保存数据
    with open(test_dir / "existing_codes.json", "w", encoding="utf-8") as f:
        json.dump(existing_codes, f, ensure_ascii=False, indent=2)

    with open(test_dir / "new_interviews.json", "w", encoding="utf-8") as f:
        json.dump(new_interviews, f, ensure_ascii=False, indent=2)

    with open(test_dir / "categories.json", "w", encoding="utf-8") as f:
        json.dump(categories, f, ensure_ascii=False, indent=2)

    print(f"理论饱和度测试数据已创建: {test_dir}")

def create_statistical_test_data():
    """创建统计分析测试数据"""
    # 模拟调查问卷数据
    survey_data = {
        "demographics": {
            "participants": 50,
            "age_mean": 21.5,
            "age_std": 2.3,
            "gender_distribution": {"male": 25, "female": 24, "other": 1}
        },
        "scales": {
            "learning_satisfaction": {
                "items": [
                    {"item_id": "ls1", "text": "我对课程内容满意", "response": [4, 3, 5, 4, 2, 5, 3, 4, 5, 4, 3, 2, 4, 5, 3, 4, 2, 3, 4, 5, 4, 3, 2, 4, 5, 3, 4, 2, 3, 4, 5, 3, 4, 2, 3, 4, 5, 3, 4, 2, 3, 4, 5, 3, 4, 2, 3, 4, 5, 3, 4]},
                    {"item_id": "ls2", "text": "教学方法适合我", "response": [3, 4, 4, 3, 5, 2, 4, 3, 4, 5, 3, 4, 2, 3, 4, 5, 3, 2, 4, 3, 4, 5, 3, 4, 2, 3, 4, 5, 3, 4, 2, 3, 4, 5, 3, 4, 2, 3, 4, 5, 3, 4, 2]},
                    {"item_id": "ls3", "text": "作业量合理", "response": [2, 3, 2, 4, 3, 4, 5, 2, 3, 4, 3, 4, 5, 2, 3, 4, 3, 2, 4, 3, 4, 5, 3, 4, 2, 3, 4, 5, 3, 4, 2, 3, 4, 5, 3, 4, 2, 3, 4, 5, 3, 4, 2]},
                    {"item_id": "ls4", "text": "考试公平", "response": [3, 4, 3, 4, 2, 3, 4, 5, 2, 3, 4, 3, 4, 5, 2, 3, 4, 3, 2, 4, 3, 4, 5, 3, 4, 2, 3, 4, 5, 3, 4, 2, 3, 4, 5, 3, 4, 2, 3, 4, 5, 3, 4, 2]},
                    {"item_id": "ls5", "text": "整体满意度", "response": [4, 3, 4, 4, 5, 3, 2, 4, 3, 4, 5, 3, 4, 2, 3, 4, 5, 3, 2, 4, 3, 4, 5, 3, 4, 2, 3, 4, 5, 3, 4, 2, 3, 4, 5, 3, 4, 2, 3, 4, 5, 3, 4, 2]}
                ],
                "reliability": {
                    "cronbach_alpha": 0.87,
                    "split_half": 0.83
                }
            },
            "peer_interaction": {
                "items": [
                    {"item_id": "pi1", "text": "同学关系良好", "response": [4, 5, 3, 4, 5, 3, 4, 5, 2, 3, 4, 5, 3, 4, 2, 3, 4, 5, 3, 4, 2, 3, 4, 5, 3, 4, 2, 3, 4, 5, 3, 4, 2, 3, 4, 5, 3, 4, 2, 3, 4, 5, 3, 4, 2]},
                    {"item_id": "pi2", "text": "经常合作学习", "response": [3, 4, 3, 2, 4, 5, 3, 4, 5, 2, 3, 4, 5, 3, 4, 2, 3, 4, 5, 3, 2, 4, 3, 4, 5, 3, 4, 2, 3, 4, 5, 3, 4, 2, 3, 4, 5, 3, 4, 2, 3, 4, 5, 3, 4, 2]},
                    {"item_id": "pi3", "text": "愿意帮助同学", "response": [5, 4, 3, 4, 2, 3, 4, 5, 3, 4, 5, 2, 3, 4, 5, 3, 4, 2, 3, 4, 5, 3, 2, 4, 3, 4, 5, 3, 4, 2, 3, 4, 5, 3, 4, 2, 3, 4, 5, 3, 4, 2]},
                    {"item_id": "pi4", "text": "感到孤独", "response": [2, 3, 4, 2, 3, 4, 5, 2, 3, 4, 5, 2, 3, 4, 5, 2, 3, 4, 5, 3, 2, 4, 3, 4, 5, 2, 3, 4, 5, 3, 4, 2, 3, 4, 5, 3, 4, 2, 3, 4, 5, 3, 4, 2]},
                    {"item_id": "pi5", "text": "感觉被接纳", "response": [4, 3, 4, 5, 3, 2, 4, 3, 4, 5, 2, 3, 4, 5, 3, 4, 2, 3, 4, 5, 3, 2, 4, 3, 4, 5, 3, 4, 2, 3, 4, 5, 3, 4, 2, 3, 4, 5, 3, 4, 2]}
                ],
                "reliability": {
                    "cronbach_alpha": 0.82,
                    "split_half": 0.79
                }
            }
        }
    }

    # 创建测试数据目录
    test_dir = Path("test_data/real/statistical_analysis")
    test_dir.mkdir(parents=True, exist_ok=True)

    # 保存调查数据
    with open(test_dir / "survey_data.json", "w", encoding="utf-8") as f:
        json.dump(survey_data, f, ensure_ascii=False, indent=2)

    print(f"统计分析测试数据已创建: {test_dir}")

def main():
    """主函数"""
    print("正在创建真实场景测试数据...")

    create_open_coding_test_data()
    create_network_analysis_test_data()
    create_theory_saturation_test_data()
    create_statistical_test_data()

    print("\n✅ 所有测试数据创建完成!")
    print("数据目录: test_data/real/")

if __name__ == "__main__":
    main()