import os

from dotenv import load_dotenv

from ibm_watsonx_ai.credentials import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

load_dotenv()


class IBMProvider:

    def __init__(self):

        credentials = Credentials(

            url=os.getenv("IBM_URL"),

            api_key=os.getenv("IBM_API_KEY")

        )

        self.model = ModelInference(

            model_id="ibm/granite-4-h-small",

            credentials=credentials,

            project_id=os.getenv("IBM_PROJECT_ID"),

            params={

                "max_new_tokens": 600,

                "temperature": 0.7,

                "top_p": 0.9

            }

        )

    # ======================================================
    # NORMAL CHAT
    # ======================================================

    def generate(

        self,

        conversation,

        system_prompt

    ) -> str:

        prompt = system_prompt + "\n\n"

        for message in conversation:

            role = message["role"].capitalize()

            prompt += f"{role}: {message['content']}\n"

        prompt += "\nCreator Compass:"

        response = self.model.generate_text(

            prompt=prompt

        )

        return response.strip()

    # ======================================================
    # CREATOR DASHBOARD ANALYSIS
    # ======================================================

    def analyze_content(

        self,

        content

    ) -> str:

        dashboard_prompt = """

You are Creator Compass Creator Dashboard.

Analyze the user's content.

Return ONLY valid JSON.

Do not explain anything.

Do not use Markdown.

Return exactly this format:

{

"overall":85,

"title":17,

"hook":16,

"seo":18,

"creativity":17,

"audience":17,

"strengths":[

"Strength 1",

"Strength 2",

"Strength 3"

],

"suggestions":[

"Suggestion 1",

"Suggestion 2",

"Suggestion 3"

]

}

Scores:

overall -> /100

title -> /20

hook -> /20

seo -> /20

creativity -> /20

audience -> /20

Only return valid JSON.

"""

        prompt = dashboard_prompt + "\n\nUser Content:\n" + content

        response = self.model.generate_text(

            prompt=prompt

        )

        return response.strip()