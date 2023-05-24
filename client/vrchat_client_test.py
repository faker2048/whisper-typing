from time import sleep
from vrchat_client import VRChatClient


def main():
    client = VRChatClient()
    client.set_chatbox_typing(True)
    sleep(1)
    client.set_chatbox_typing(False)
    client.input_to_chatbox("Hello, world!")


if __name__ == "__main__":
    main()
