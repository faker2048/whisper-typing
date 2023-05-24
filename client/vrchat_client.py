from pythonosc import udp_client
from loguru import logger


class OSCAddress:
    CHATBOX_TYPING = "/chatbox/typing"
    CHATBOX_INPUT = "/chatbox/input"


class VRChatClient:
    def __init__(self, ip="127.0.0.1", port=9000):
        self.osc_client = udp_client.SimpleUDPClient(ip, port)

    def set_chatbox_typing(self, value: bool) -> None:
        logger.debug(f"Set typing: {value}.")
        self.osc_client.send_message(OSCAddress.CHATBOX_TYPING, value)

    def input_to_chatbox(
        self,
        text: str,
        send_immediately: bool = True,
        trigger_notification: bool = True,
    ) -> None:
        logger.debug(f"Input text: {text}.")
        self.osc_client.send_message(
            OSCAddress.CHATBOX_INPUT,
            (text, send_immediately, trigger_notification),
        )
