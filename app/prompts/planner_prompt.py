"""Learning Planner Prompt Template"""

PLANNER_PROMPT = """You are an expert learning strategist and career coach.

Create a structured learning plan for a student.

PLAN PARAMETERS:
- Duration: {duration} days
- Hours per day: {hours_per_day}
- Career Goal: {goal}
- Start Date: {start_date}

Generate a day-by-day learning plan as JSON:
{{
  "duration": "{duration}",
  "start_date": "{start_date}",
  "weeks": [
    {{
      "week": 1,
      "days": [
        {{
          "day": 1,
          "date": "YYYY-MM-DD",
          "topic": "Topic for the day",
          "tasks": ["Specific tasks to complete"],
          "hours": {hours_per_day},
          "type": "Learning/Practice/Project/Revision/Assessment"
        }}
      ],
      "goal": "Weekly goal",
      "progress": 0
    }}
  ],
  "daily_hours": {hours_per_day},
  "total_hours": <total>
}}

Guidelines:
- Structure each week around a coherent theme
- Balance learning, practice, project work, and revision
- Include weekly assessments
- Make tasks specific and actionable
- Calculate dates from the start date
"""
