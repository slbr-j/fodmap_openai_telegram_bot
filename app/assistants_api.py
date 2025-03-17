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
        logger.info(f"Виклик асистента з текстом: {user_input}")

        # Створюємо новий thread
        thread = openai.beta.threads.create()

        logger.info(f"Створено thread з ID: {thread.id}")

        # Додаємо повідомлення користувача до thread
        openai.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_input
        )

        # Запускаємо асистента (створюємо run)
        run = openai.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )

        logger.info(f"Створено run з ID: {run.id}")

        # Check the status of the run
        while True:
            run_status = openai.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )

            logger.info(f"Run статус: {run_status.status}")

            if run_status.status == "completed":
                break
            time.sleep(1)

        # Receive a message from the assistant
        messages = openai.beta.threads.messages.list(thread_id=thread.id)
        reply = messages.data[0].content[0].text.value

        logger.info(f"Assistant's response: {reply}")

        return reply

    except Exception as e:
        logger.error(f"Error in ask_assistant: {e}")
        return "Вибач, сталася помилка. Спробуй ще раз пізніше!"
