import os
from dotenv import load_dotenv

load_dotenv()

IBM_API_KEY = os.getenv("IBM_API_KEY").strip()
IBM_PROJECT_ID = os.getenv("IBM_PROJECT_ID").strip()
IBM_URL = os.getenv("IBM_URL").strip()

print("API Key Length:", len(IBM_API_KEY))
print("Project ID:", IBM_PROJECT_ID)
print("URL:", IBM_URL)