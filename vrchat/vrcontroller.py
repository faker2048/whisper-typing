#!/usr/bin/env python3
from functools import cache
import sys
import time
from typing import Dict

import openvr as vr
from loguru import logger


class VRController:
    def __init__(self):
        self.hands: Dict[str, vr.ETrackedControllerRole] = {
            "left": vr.TrackedControllerRole_LeftHand,
            "right": vr.TrackedControllerRole_RightHand,
        }

        self.buttons: Dict[str, vr.EVRButtonId] = {
            "a": vr.k_EButton_IndexController_A,
            "b": vr.k_EButton_IndexController_B,
            "joystick": vr.k_EButton_SteamVR_Touchpad,
        }
        self.system: vr.IVRSystem = self.init_system()

    @cache
    def _controller_idx(self, hand: str) -> int:
        return self.system.getTrackedDeviceIndexForControllerRole(self.hands[hand])

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

    def is_pressed(self, hand: str = "right", button: str = "b") -> bool:
        controller_idx = self._controller_idx(hand)
        got_state, state = self.system.getControllerState(controller_idx)
        if not got_state:
            return False

        button_mask = 1 << self.buttons[button]
        return (state.ulButtonPressed & button_mask) != 0


if __name__ == "__main__":
    vr_controller = VRController()
    while True:
        time.sleep(0.1)
        if vr_controller.is_pressed(hand="right", button="b"):
            logger.info("Button B is pressed")
        else:
            logger.info("Button B is not pressed")
