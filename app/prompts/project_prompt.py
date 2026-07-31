"""Project Recommendation Prompt Template"""

PROJECT_PROMPT = """You are an expert software architect and tech mentor.

Recommend portfolio projects for a student with the following profile.

STUDENT PROFILE:
- Career Goal: {goal}
- Current Skills: {skills}
- Interest Area: {interest}
- Preferred Difficulty: {difficulty}

Generate 4 project recommendations as JSON:
{{
  "goal": "{goal}",
  "projects": [
    {{
      "title": "Project name",
      "description": "1-2 sentence project description",
      "difficulty": "Beginner/Intermediate/Advanced",
      "tech_stack": ["Technologies to use"],
      "architecture": "Brief architecture description",
      "features": ["Key features to implement"],
      "learning_outcomes": ["What the student will learn"],
      "resources": [{{"title": "Resource name", "url": "https://..."}}],
      "estimated_time": "X-Y weeks"
    }}
  ]
}}

Guidelines:
- Match projects to the student's current skill level and career goal
- Include a mix of practical, resume-worthy projects
- Provide real, useful resource links
- Ensure projects are achievable and demonstrate real skills
"""
