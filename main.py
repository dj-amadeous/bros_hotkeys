import window_utils as wu
import main_threads as mt
import threading
import time
import sys

if __name__ == "__main__":
    wu.setup_emulator_window_main()

    event = threading.Event()
    hotkey_listener = mt.HotkeyListener(event)
    hotkey_thread = mt.CustomThread(target=hotkey_listener.key_listener)
    hotkey_thread.start()
    while not event.is_set():
        time.sleep(1)
        print("working")

    sys.exit(0)