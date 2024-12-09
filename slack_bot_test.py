import os
import re

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

bot_token = os.getenv("SLACK_BOT_TOKEN_PINGOO")
app_token = os.getenv("SLACK_APP_TOKEN_PINGOO")

app = App(token=bot_token)


@app.message(re.compile(r"^test$"))
def test_handler(body):
    channel = body["event"]["channel"]
    app.client.chat_postMessage(channel=channel, text="Hi~ (casual greeting)")
    print("test message sent.")


if __name__ == "__main__":
    handler = SocketModeHandler(app, app_token)
    handler.start()
