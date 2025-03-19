import openai
import os
import logging
import asyncio
from openai import RateLimitError, OpenAIError
from openai._exceptions import Timeout

logger = logging.getLogger(__name__)

# Getting keys from the environment
openai_api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("ASSISTANT_ID")

if not openai_api_key or not assistant_id:
    logger.error("ENV variables OPENAI_API_KEY or ASSISTANT_ID not found!")
    raise ValueError("There are no environment variables for the OpenAI API.")

# Create OpenAI client
client = openai.OpenAI(api_key=openai_api_key)


async def ask_assistant(user_input):
    try:
        logger.info(f"Виклик асистента з текстом: {user_input}")

        thread = client.beta.threads.create()
        logger.info(f"Створено thread з ID: {thread.id}")

        client.beta.threads.messages.create(
            thread_id=thread.id, role="user", content=user_input
        )

        run = client.beta.threads.runs.create(
            thread_id=thread.id, assistant_id=assistant_id
        )

        logger.info(f"Створено run з ID: {run.id}")

        # Очікуємо максимум 30 секунд (10 ітерацій по 3 сек)
        max_attempts = 10
        attempt = 0

        while attempt < max_attempts:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread.id, run_id=run.id
            )

            logger.info(f"Run статус: {run_status.status}")

            if run_status.status == "completed":
                break

            attempt += 1
            await asyncio.sleep(3)

        else:
            logger.error("Асистент обробляв запит занадто довго.")
            return (
                "Вибач, відповідь зайняла занадто багато часу. Спробуй ще раз пізніше."
            )

        messages = client.beta.threads.messages.list(thread_id=thread.id)
        reply = messages.data[0].content[0].text.value

        logger.info(f"Відповідь асистента: {reply}")

        return reply

    except RateLimitError:
        return "Вибач, забагато запитів до асистента. Спробуй трохи пізніше!"
    except Timeout:
        return "Асистент не відповів вчасно, спробуй знову!"
    except OpenAIError as e:
        logger.error(f"OpenAI API error: {e}")
        return "Щось пішло не так з OpenAI. Спробуй знову пізніше."
    except Exception as e:
        logger.error(f"Unexpected error in ask_assistant: {e}")
        return "Вибач, сталася помилка. Спробуй ще раз пізніше!"
