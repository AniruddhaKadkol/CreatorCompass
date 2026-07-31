import json
class DashboardService:
    @staticmethod
    def analyze(content, ai):
        prompt = f"""
You are Creator Compass's Creator Dashboard.
Analyze the following content exactly like an experienced content strategist.
Score each category out of 20.
Return ONLY valid JSON.
Required format:
{{
    "overall": 0,
    "rating": "",
    "title": 0,
    "hook": 0,
    "seo": 0,
    "creativity": 0,
    "audience": 0,
    "strengths": [
        "",
        "",
        ""
    ],
    "suggestions": [
        "",
        "",
        ""
    ]
}}
Content:
\"\"\"
{content}
\"\"\"
"""
        try:
            response = ai.generate_json(prompt)
            start = response.find("{")
            end = response.rfind("}") + 1
            if start == -1 or end == 0:
                raise ValueError("JSON not found.")
            response = response[start:end]
            dashboard = json.loads(response)
            return dashboard
        except Exception:
            return {
                "overall": 0,
                "rating": "Unable to Analyze",
                "title": 0,
                "hook": 0,
                "seo": 0,
                "creativity": 0,
                "audience": 0,
                "strengths": [
                    "Analysis unavailable."
                ],
                "suggestions": [
                    "Please try again."
                ]
            }