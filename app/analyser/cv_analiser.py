import httpx
import os
from app.core.config import settings

TOKEN = settings.bot.token


async def download_file(file_id: str):
    url = f"https://api.telegram.org/bot{TOKEN}/getFile?file_id={file_id}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()

            file_path = response.json()["result"]["file_path"]
            file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"

            file_response = await client.get(file_url)
            file_response.raise_for_status()

            path_save = os.path.join(os.path.dirname(__file__), file_path)
            print(path_save)

            with open(path_save, "wb") as f:
                f.write(file_response.content)

    except Exception as e:
        print(str(e))

    return path_save


def get_result(requirements: str, path_cv: str):

    sentence_1 = requirements
    sentence_2 = path_cv
    similarity_score = f"Result {sentence_1} + {sentence_2}"
    return similarity_score
