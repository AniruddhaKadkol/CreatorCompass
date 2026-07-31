from ai.workspace_ai import WorkspaceAI
from services.dashboard_service import DashboardService
from config.prompts import (
    CONTENT_CREATOR_PROMPT,
    CREATIVE_STUDIO_PROMPT,
)
class AIService:
    def __init__(self):
        self.ai = WorkspaceAI()

    # CONTENT CREATOR

    def content_creator(self, conversation):
        prompt = CONTENT_CREATOR_PROMPT + "\n\n"
        for message in conversation:
            role = message["role"].capitalize()
            prompt += f"{role}: {message['content']}\n"
        prompt += "\nCreator Compass:"
        return self.ai.generate(prompt)

    # CREATIVE STUDIO

    def creative_studio(self, conversation):
        prompt = CREATIVE_STUDIO_PROMPT + "\n\n"
        for message in conversation:
            role = message["role"].capitalize()
            prompt += f"{role}: {message['content']}\n"
        prompt += "\nCreator Compass:"
        return self.ai.generate(prompt)

    # CREATOR DASHBOARD

    def analyze_content(self, content):
        return DashboardService.analyze(
            content,
            self.ai
        )