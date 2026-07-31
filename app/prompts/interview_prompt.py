"""Interview Preparation Prompt Template"""

INTERVIEW_PROMPT = """You are an expert technical interviewer with experience at top tech companies.

Generate interview preparation questions for a {role} position.

REQUIREMENTS:
- Question Types: {types}
- Difficulty: {difficulty}
- Number of questions: {count}

Provide the questions as JSON:
{{
  "role": "{role}",
  "questions": [
    {{
      "question": "The interview question",
      "type": "Technical/HR/Behavioral/Coding",
      "difficulty": "Beginner/Intermediate/Advanced",
      "hint": "A helpful hint for the candidate",
      "answer": "A model answer explaining the expected response",
      "topics": ["Related topic tags"]
    }}
  ],
  "tips": ["5-6 interview preparation tips"]
}}

Guidelines:
- For Coding questions, include approach and complexity analysis in the answer
- For Behavioral questions, reference the STAR method
- For HR questions, provide professional and concise model answers
- For Technical questions, give thorough explanations
"""
