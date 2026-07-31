import os

from dotenv import load_dotenv
from ibm_watsonx_ai.credentials import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

load_dotenv()


class WorkspaceAI:

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
                "max_new_tokens": 500,
                "temperature": 0.7,
                "top_p": 0.9
            }

        )

    def generate(self, prompt):

        return self.model.generate_text(
            prompt=prompt
        ).strip()

    def generate_json(self, prompt):

        return self.model.generate_text(
            prompt=prompt
        ).strip()