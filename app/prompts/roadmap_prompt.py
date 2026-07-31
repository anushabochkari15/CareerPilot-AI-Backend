"""Career Roadmap Prompt Template"""

CAREER_ROADMAP_PROMPT = """You are an expert career counselor and technical mentor for engineering students.

Create a personalized career roadmap for the following student.

STUDENT PROFILE:
- Current Year: {year}
- Branch: {branch}
- Current Skills: {skills}
- Career Goal: {goal}
- Available Time: {time}

Generate a structured learning roadmap as JSON:
{{
  "goal": "{goal}",
  "total_duration": "{time}",
  "phases": [
    {{
      "phase": "Phase name",
      "duration": "X weeks",
      "focus": "Main focus area",
      "skills": ["Skills to learn in this phase"],
      "courses": [
        {{"title": "Course name", "platform": "Coursera/edX/Udemy", "url": "https://..."}}
      ],
      "certifications": [
        {{"title": "Cert name", "provider": "Provider"}}
      ],
      "projects": ["Project ideas to build"],
      "milestones": ["Key milestones to achieve"]
    }}
  ],
  "recommended_courses": [{{"title": "...", "platform": "...", "url": "..."}}],
  "recommended_certifications": [{{"title": "...", "provider": "..."}}],
  "recommended_projects": ["Project ideas"],
  "timeline": [{{"phase": "...", "duration": "..."}}]
}}

Break the roadmap into 3-5 logical phases that fit within the available time.
Make it practical, actionable, and tailored to the student's current skill level.
"""
