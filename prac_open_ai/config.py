# prac_asyncio

import os
from dotenv import load_dotenv

# .env をロード
load_dotenv()

class Settings:
    # 環境変数から取得
    API_KEY: str = os.getenv("OPENAI_API_KEY")

settings = Settings()
