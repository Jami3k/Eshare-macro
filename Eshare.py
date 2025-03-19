import pyautogui
import pytesseract
import time
from pynput.mouse import Listener
import threading

# Variables for locations (you can adjust these as needed)
GENERAL_OK_BUTTON = (1080, 730)
GENERAL_FIELD = (900, 730)
TARGET_OK_BUTTON = (1017, 594)
TRY_AGAIN_BUTTON = (960, 615)
TEXT_FIELD = (1000, 725)

# Global stop event to control the macro
stop_event = threading.Event()

# Function to stop the macro when a right-click is detected
def on_click(x, y, button, pressed):
    if pressed and button.name == 'right':
        print("Right-click detected, stopping the macro...")
        stop_event.set()

# Function to start listening for mouse events in a separate thread
def start_mouse_listener():
    listener = Listener(on_click=on_click)
    listener.start()

# Function to run the macro
def run_macro():
    time.sleep(2)  # Wait for the screen to be ready

    for number in range(100000, 1000000):
        if stop_event.is_set():
            print("Macro stopped due to mouse right-click.")
            break
        
        pyautogui.moveTo(TRY_AGAIN_BUTTON)
        pyautogui.click()
        pyautogui.typewrite(str(number))
        pyautogui.moveTo(TARGET_OK_BUTTON)
        pyautogui.click()
        time.sleep(0.2)
        
        screenshot = pyautogui.screenshot(region=(820, 560, 280, 40))
        text = pytesseract.image_to_string(screenshot)

        # For debugging purposes (optional)
        # print(repr(text))

        # Uncomment for a success condition (if needed)
        # if "input" not in text:
        #    print(f"Success! The Code is {number}")
        #    break

# Start the mouse listener thread
mouse_listener_thread = threading.Thread(target=start_mouse_listener)
mouse_listener_thread.start()

# Start the macro thread
macro_thread = threading.Thread(target=run_macro)
macro_thread.start()

# Wait for the macro to finish
macro_thread.join()

# start the macro
run_macro()
# Stop the mouse listener when the macro finishes
mouse_listener_thread.join()

print("Script execution completed.")

