#!/usr/bin/env python3
import openvr as vr
import sys
import time
from loguru import logger
from typing import Generator, List

# Event types
EVENT_NONE = 0
EVENT_RISING_EDGE = 1
EVENT_FALLING_EDGE = 2


class InputEvent:
    def __init__(self, opcode: int, button: str):
        self.opcode = opcode
        self.button = button


class VRController:
    def __init__(self):
        self.hands = {
            "left": vr.TrackedControllerRole_LeftHand,
            "right": vr.TrackedControllerRole_RightHand,
        }

        self.buttons = {
            "a": vr.k_EButton_IndexController_A,
            "b": vr.k_EButton_IndexController_B,
            "joystick": vr.k_EButton_IndexController_JoyStick,
        }
        self.system = self.init_system()
        self.last_packet = {button: 0 for button in self.buttons}
        self.event_high = {button: False for button in self.buttons}

    def init_system(self) -> vr.IVRSystem:
        loop_cnt = 0
        while True:
            try:
                return vr.init(vr.VRApplication_Background)
            except Exception as e:
                if loop_cnt % 10 == 0:
                    logger.warning(
                        f"Failed to start SteamVR input thread: {repr(e)}",
                        file=sys.stderr,
                    )
                loop_cnt += 1
                time.sleep(1)

    def poll_button_press(self, hand: str = "right", buttons: List[str] = ["b"]) -> Generator[InputEvent, None, None]:
        while True:
            time.sleep(0.01)
            controller_idx = self.system.getTrackedDeviceIndexForControllerRole(
                self.hands[hand]
            )
            got_state, state = self.system.getControllerState(controller_idx)
            if not got_state:
                continue

            for button in buttons:
                button_mask = 1 << self.buttons[button]
                if (state.ulButtonPressed & button_mask) and (state.unPacketNum != self.last_packet[button]):
                    if not self.event_high[button]:
                        yield InputEvent(EVENT_RISING_EDGE, button)
                        self.event_high[button] = True
                elif self.event_high[button]:
                    self.event_high[button] = False
                    yield InputEvent(EVENT_FALLING_EDGE, button)

                self.last_packet[button] = state.unPacketNum


if __name__ == "__main__":
    vr_controller = VRController()
    for event in vr_controller.poll_button_press(hand="right", buttons=["a", "b"]):
        if event.opcode == EVENT_RISING_EDGE:
            logger.info(f"Rising edge on {event.button}")
        elif event.opcode == EVENT_FALLING_EDGE:
            logger.info(f"Falling edge on {event.button}")
