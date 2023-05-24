import argparse


def parse_command_line_arguments():
    parser = argparse.ArgumentParser(description="Speech Recorder")
    parser.add_argument(
        "-r", "--rate", type=int, default=16000, help="Sampling rate (default: 16000)"
    )
    parser.add_argument(
        "-k",
        "--keyboard-key",
        type=str,
        default="i",
        help="Keyboard key to start/stop recording (default: 'i')",
    )
    parser.add_argument(
        "-l",
        "--language",
        type=str,
        default=None,
        help="Language code (default: None)",
    )
    parser.add_argument(
        "-s",
        "--save",
        type=bool,
        default=False,
        help="Save recorded audio (default: False)",
    )
    parser.add_argument(
        "-t",
        "--translate",
        type=bool,
        default=False,
        help="Translate text (default: False)",
    )
    parser.add_argument(
        "-m",
        "--model-name",
        type=str,
        default="large-v2",
        help="Model name (default: 'large-v2')",
    )

    return parser.parse_args()
