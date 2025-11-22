"""
Market trends microservice / helper.
Returns dynamic or static trends for your frontend.
"""

import random

# --------------------------------------------------------
# STATIC SAMPLE TRENDS (Your original function)
# --------------------------------------------------------
def get_sample_trends():
    return {
        "skills": [
            {"skill": "React", "demand": 95},
            {"skill": "Python", "demand": 92},
            {"skill": "Kubernetes", "demand": 88},
            {"skill": "GraphQL", "demand": 75},
            {"skill": "AWS", "demand": 90},
            {"skill": "Node.js", "demand": 87},
        ],
        "hiringTrends": [
            {"month": "Jan", "hiring": 120, "salaries": 165},
            {"month": "Feb", "hiring": 140, "salaries": 168},
            {"month": "Mar", "hiring": 165, "salaries": 172},
            {"month": "Apr", "hiring": 155, "salaries": 170},
            {"month": "May", "hiring": 180, "salaries": 175},
            {"month": "Jun", "hiring": 195, "salaries": 180},
        ],
        "salaries": [
            {"role": "Junior Dev", "salary": 85},
            {"role": "Mid-Level", "salary": 130},
            {"role": "Senior Dev", "salary": 170},
            {"role": "Tech Lead", "salary": 200},
            {"role": "Manager", "salary": 220},
        ],
        "insights": {
            "growingMarkets": 18,
            "aiMlOpportunities": 45,
            "remotePositions": 62,
            "avgSalaryGrowth": 8
        }
    }


# --------------------------------------------------------
# DYNAMIC VERSION (Your FastAPI expects this)
# --------------------------------------------------------
def get_dynamic_market_trends():
    """Generate random but realistic dynamic trends."""
    return {
        "skills": [
            {"skill": "React", "demand": random.randint(85, 98)},
            {"skill": "Python", "demand": random.randint(80, 96)},
            {"skill": "Kubernetes", "demand": random.randint(75, 92)},
            {"skill": "GraphQL", "demand": random.randint(60, 85)},
            {"skill": "AWS", "demand": random.randint(78, 95)},
            {"skill": "Node.js", "demand": random.randint(82, 94)},
        ],
        "hiringTrends": [
            {"month": "Jan", "hiring": random.randint(110, 180), "salaries": random.randint(150, 180)},
            {"month": "Feb", "hiring": random.randint(130, 200), "salaries": random.randint(152, 183)},
            {"month": "Mar", "hiring": random.randint(145, 210), "salaries": random.randint(155, 190)},
        ],
        "salaries": [
            {"role": "Junior Dev", "salary": random.randint(70, 95)},
            {"role": "Mid-Level", "salary": random.randint(110, 140)},
            {"role": "Senior Dev", "salary": random.randint(150, 185)},
            {"role": "Tech Lead", "salary": random.randint(180, 220)},
            {"role": "Manager", "salary": random.randint(200, 240)},
        ],
        "insights": {
            "growingMarkets": random.randint(10, 25),
            "aiMlOpportunities": random.randint(30, 60),
            "remotePositions": random.randint(40, 70),
            "avgSalaryGrowth": random.randint(5, 12),
        }
    }
