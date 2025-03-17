import openai
import os
import logging
import time

logger = logging.getLogger(__name__)

# Getting keys from the environment
openai_api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("ASSISTANT_ID")

if not openai_api_key or not assistant_id:
    logger.error("ENV variables OPENAI_API_KEY or ASSISTANT_ID not found!")
    raise ValueError("There are no environment variables for the OpenAI API.")

# Assigning a key to openai
openai.api_key = openai_api_key

async def ask_assistant(user_input):
    try:
        logger.info(f"Call an assistant with text: {user_input}")

        thread = openai.beta.threads.create()

        openai.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_input
        )

        run = openai.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )

        while True:
            run_status = openai.beta.threads.runs.retrieve(run.id)
            if run_status.status == "completed":
                break
            time.sleep(1)

        messages = openai.beta.threads.messages.list(thread_id=thread.id)
        reply = messages.data[0].content[0].text.value
        return reply

    except Exception as e:
        logger.error(f"Помилка у ask_assistant: {e}")
        return "Sorry, there was an error. Please try again later!"
