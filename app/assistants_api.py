import openai
import os
import time

openai.api_key = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")
if not openai_api_key or not assistant_id:
    raise Exception("ENV variables OPENAI_API_KEY or ASSISTANT_ID not found!")

async def ask_assistant(user_input):
    # Create a new thread for each user
    thread = openai.beta.threads.create()

    openai.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_input
    )

    run = openai.beta.threads.runs.create(
        thread_id=thread.id, assistant_id=ASSISTANT_ID
    )

    while True:
        run_status = openai.beta.threads.runs.retrieve(run.id)
        if run_status.status == "completed":
            break
        time.sleep(1)

    messages = openai.beta.threads.messages.list(thread_id=thread.id)
    reply = messages.data[0].content[0].text.value
    return reply
