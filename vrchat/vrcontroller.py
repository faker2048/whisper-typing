#!/usr/bin/env python3
import openvr as vr
import sys
import time
from loguru import logger

# Event types
EVENT_NONE = 0
EVENT_RISING_EDGE = 1
EVENT_FALLING_EDGE = 2


class InputEvent:
    def __init__(self, opcode: int):
        self.opcode = opcode


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
        self.last_packet = 0
        self.event_high = False

    def init_system(self):
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

    def poll_button_press(self, hand="right", button="b") -> int:
        while True:
            time.sleep(0.01)
            controller_idx = self.system.getTrackedDeviceIndexForControllerRole(
                self.hands[hand]
            )
            got_state, state = self.system.getControllerState(controller_idx)
            if not got_state or state.unPacketNum == self.last_packet:
                continue

            dead_zone_radius = 0.7
            button_mask = 1 << self.buttons[button]
            if (state.ulButtonPressed & button_mask) and (
                state.rAxis[0].x ** 2 + state.rAxis[0].y ** 2 < dead_zone_radius**2
            ):
                if not self.event_high:
                    yield InputEvent(EVENT_RISING_EDGE)
                    self.event_high = True
            elif self.event_high:
                self.event_high = False
                yield InputEvent(EVENT_FALLING_EDGE)


if __name__ == "__main__":
    vr_controller = VRController()
    for event in vr_controller.poll_button_press(hand="right", button="b"):
        if event.opcode == EVENT_RISING_EDGE:
            logger.info("Rising edge")
        elif event.opcode == EVENT_FALLING_EDGE:
            logger.info("Falling edge")
