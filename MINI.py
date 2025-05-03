import sys
import pyttsx3
import datetime
import speech_recognition as sr
import webbrowser as wb
import win32gui
import win32con
from chat import get_chatgpt_response
import os
import ctypes
import pygetwindow as gw
import time
#import asyncio
import pygetwindow as gw
import platform
import win32com.client
from pycaw.utils import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import pycaw.pycaw as pycaw
from app_open import open_app, close_app
import subprocess
from remember import remember_data, retrieve_remembered_data
import pyautogui
from floating_icon import FloatingIcon  # Import the floating icon class
from PyQt5.QtWidgets import QApplication
import threading

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(audio):
    """Speak the provided audio."""
    engine.say(audio)
    engine.runAndWait()

def time():
    """Provide the current time."""
    Time = datetime.datetime.now().strftime("%I:%M:%S %p")
    speak("The current time is")
    speak(Time)
    print("The current time is ", Time)

def date():
    """Provide the current date."""
    day = datetime.datetime.now().day
    month = datetime.datetime.now().month
    year = datetime.datetime.now().year
    speak("The current date is")
    speak(f"{day} {month} {year}")
    print(f"The current date is {day}/{month}/{year}")

def wishme():
    """Greet the user based on the time."""
    print("Welcome back sir!")
    speak("Welcome back sir!")

    hour = datetime.datetime.now().hour
    if 4 <= hour < 12:
        speak("Good Morning Sir!")
        print("Good Morning Sir!")
    elif 12 <= hour < 16:
        speak("Good Afternoon Sir!")
        print("Good Afternoon Sir!")
    elif 16 <= hour < 21:
        speak("Good Evening Sir!")
        print("Good Evening Sir!")

    speak("Mini at your service sir, please tell me how may I help you.")
    print("Mini at your service sir, please tell me how may I help you.")

def Screenshot():
    try:
        # Define the directory for saving screenshots
        screenshots_dir = os.path.expanduser("~\\Pictures")
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)  # Create the directory if it doesn't exist
        
        # Determine the next available screenshot name
        i = 1
        while True:
            img_path = os.path.join(screenshots_dir, f"screenshot_{i}.png")
            if not os.path.exists(img_path):
                break  # Use this filename if it doesn't already exist
            i += 1

        # Take and save the screenshot
        img = pyautogui.screenshot()
        img.save(img_path)

        # Provide feedback to the user
        speak(f"Screenshot saved as screenshot_{i} in your Pictures folder.")
        print(f"Screenshot saved at {img_path}")
    except Exception as e:

        print(f"An error occurred while taking a screenshot: {e}")
        speak("Sorry, I couldn't take the screenshot.")

def focus_chrome():
    """Focus the Chrome browser window."""
    windows = gw.getWindowsWithTitle("Chrome")  # Search for Chrome windows
    if windows:
        chrome_window = windows[0]
        chrome_window.activate()
        time.sleep(0.5)  # Give time to focus the window
        return True
    return False

def close_current_tab():
    """Close the currently active tab in the browser."""
    try:
        # Use PyAutoGUI to simulate "ctrl + w" to close the tab
        pyautogui.hotkey("ctrl", "w")
        print("Closed the current tab.")
    except Exception as e:
        speak(f"An error occurred while closing the tab: {e}")
        print(f"Error closing the tab: {e}")

def close_specific_tab(tab_title):
    """Close a specific tab in the browser by matching the title."""
    try:
        # Focus on the browser (e.g., Chrome) using pygetwindow
        windows = gw.getWindowsWithTitle(tab_title)
        if windows:
            browser_window = windows[0]
            browser_window.activate()  # Focus the browser window
            time.sleep(0.5)  # Give time to focus
            pyautogui.hotkey("ctrl", "w")  # Close the tab
            print(f"Closed the tab with title: {tab_title}")
        else:
            print(f"Tab with title {tab_title} not found.")
    except Exception as e:
        speak(f"An error occurred while closing the tab with title {tab_title}: {e}")
        print(f"Error closing the tab with title {tab_title}: {e}")

def open_new_tab():
    """Open a new browser tab."""
    try:
        pyautogui.hotkey("ctrl", "t")
        print("Opened a new tab.")
    except Exception as e:
        print(f"Error opening a new tab: {e}")

def open_url_in_new_tab(url):
    """
    Open a specific URL in a new tab.
    Args:
        url (str): The URL to open in a new tab.
    """
    try:
        if focus_chrome():
            pyautogui.hotkey("ctrl", "t")  # Open a new tab
            time.sleep(0.5)  # Wait for the tab to open
            pyautogui.typewrite(url)  # Type the URL
            pyautogui.press("enter")  # Press Enter to load the URL
            print(f"Opened a new tab with URL: {url}")
            speak(f"Opened a new tab with URL: {url}")
        else:
            speak("No Chrome window found.")
            print("No Chrome window found.")
    except Exception as e:
        speak(f"Error opening URL in new tab: {e}")
        print(f"Error opening URL in new tab: {e}")

def is_admin():
    """Check if the script is running as an administrator."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Command Functions
def bluetooth_on():
    subprocess.call("powershell.exe Enable-NetAdapter -Name 'Bluetooth Network Connection'", shell=True)
    print("Bluetooth turned on")

def bluetooth_off():
    subprocess.call("powershell.exe Disable-NetAdapter -Name 'Bluetooth Network Connection'", shell=True)
    print("Bluetooth turned off")

def close_control_panel():
    try:
        # Locate windows with 'Control Panel' in the title
        windows = [win for win in gw.getAllTitles() if "Control Panel" in win]
        
        if windows:
            for win_title in windows:
                win = gw.getWindowsWithTitle(win_title)[0]
                win.close()  # Close the Control Panel window
                print(f"Closed: {win_title}")
        else:
            print("Control Panel window not found.")
    except Exception as e:
        print(f"Error closing Control Panel: {e}")

def toggle_wifi(turn_on):
    """Turn Wi-Fi on or off."""
    interface = "Wi-Fi"
    if turn_on:
        os.system(f"netsh interface set interface name=\"{interface}\" admin=enabled")
        speak("Wi-Fi has been turned on.")
    else:
        os.system(f"netsh interface set interface name=\"{interface}\" admin=disabled")
        speak("Wi-Fi has been turned off.")

def open_url_in_new_tab(url):
    try:
        # Ensure the URL starts with "http://" or "https://"
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://www." + url  # Prepend "https://www." for common cases
        # Open the URL in a new browser tab
        wb.open_new_tab(url)
        print(f"Opened a new tab with URL: {url}")
    except Exception as e:
        print(f"Failed to open the website. Error: {str(e)}")


def minimize_window(app_name):
    """
    Minimizes the window of a specified application.
    
    :param app_name: The name of the application window to minimize (partial match allowed).
    """
    try:
        # Get all windows that match the provided app name
        windows = gw.getWindowsWithTitle(app_name)
        if windows:
            window = windows[0]  # Take the first matched window
            hwnd = window._hWnd
            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)  # Minimize the window
            print(f"Minimized window: {window.title}")
            speak(f"Minimized the {app_name} window.")
        else:
            # No matching windows found
            print(f"No window found with title containing: {app_name}")
            speak(f"Could not find any window with the title {app_name}.")
    except Exception as e:
        # Handle unexpected errors
        print(f"An error occurred: {str(e)}")
        speak("Sorry, an error occurred while trying to minimize the window.")

# Function to maximize a specific application
def maximize_window(app_name):
    windows = gw.getWindowsWithTitle(app_name)
    if windows:
        window = windows[0]  # Take the first matched window
        hwnd = window._hWnd
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
        print(f"Maximized window: {window.title}")
        speak(f"Maximized the {app_name} window.")
    else:
        print(f"No window found with title containing: {app_name}")
        speak(f"Could not find any window with the title {app_name}.")

def set_brightness(level):
    """Set the brightness level."""
    try:
        os.system(f"powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{level})")
        speak(f"Brightness set to {level}%.")
    except Exception as e:
        speak(f"Failed to set brightness: {e}")

def set_volume(level):
    """Set system volume."""
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            pycaw.IAudioEndpointVolume._iid_, CLSCTX_ALL, None
        )
        volume = interface.QueryInterface(IAudioEndpointVolume)
        volume.SetMasterVolumeLevelScalar(level / 100, None)
        speak(f"Volume set to {level} percent.")
    except Exception as e:
        speak(f"Failed to set volume: {e}")

def put_system_to_sleep():
    """Put the system into sleep mode."""
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    speak("The system is going to sleep.")

def shutdown_system():
    """Shutdown the system."""
    os.system("shutdown /s /t 1")
    speak("Shutting down the system.")
    
import os

def toggle_theme(mode):
    """Enable or disable dark/light mode by modifying the registry."""
    try:
        # Check the current theme state before toggling
        current_mode = os.popen('reg query "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize" /v AppsUseLightTheme').read()
        
        # Determine if it's currently light mode or dark mode
        is_light_mode = "0x1" in current_mode  # Light mode if the registry value is 1, dark mode if 0
        
        if mode == "dark":
            if is_light_mode:
                # If light mode is enabled, change to dark mode
                os.system('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize" /v AppsUseLightTheme /t REG_DWORD /d 0 /f')
                speak("Dark mode enabled.")
                print("Dark mode enabled.")
            else:
                speak("Dark mode is already enabled.")
                print("Dark mode is already enabled.")
        
        elif mode == "light":
            if not is_light_mode:
                # If dark mode is enabled, change to light mode
                os.system('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize" /v AppsUseLightTheme /t REG_DWORD /d 1 /f')
                speak("Light mode enabled.")
                print("Light mode enabled.")
            else:
                speak("Light mode is already enabled.")
                print("Light mode is already enabled.")
    except Exception as e:
        speak(f"Failed to change theme: {e}")
        print(f"Error: {e}")

def restart_system():
    """Restart the system."""
    os.system("shutdown /r /t 1")
    speak("Restarting the system.")

def log_off_system():
    """Log off the current user."""
    os.system("shutdown /l")
    speak("Logging off the system.")

def system_info():
    """Display system information."""
    uname = platform.uname()
    print(f"System: {uname.system}")
    print(f"Node Name: {uname.node}")
    print(f"Release: {uname.release}")
    print(f"Version: {uname.version}")
    print(f"Machine: {uname.machine}")
    print(f"Processor: {uname.processor}")
    speak(f"System: {uname.system}")
    speak(f"Node Name: {uname.node}")
    speak(f"Release: {uname.release}")
    speak(f"Version: {uname.version}")
    speak(f"Machine: {uname.machine}")
    speak(f"Processor: {uname.processor}")

def turn_on_screen():
    """Turn on the screen by simulating a user input."""
    try:
        # Simulate a key press to wake up the screen
        ctypes.windll.user32.mouse_event(0x0001, 0, 0, 0, 0)  # Simulate a mouse move event
        speak("The screen is turning on.")
    except Exception as e:
        speak(f"Failed to turn on the screen: {e}")

def lock_system():
    """Lock the system."""
    ctypes.windll.user32.LockWorkStation()
    speak("The system is locked.")

def turn_off_screen():
    """Turn off the screen."""
    ctypes.windll.user32.SendMessageW(0xFFFF, 0x112, 0xF170, 2)
    speak("The screen is turning off.")

def takecommand():
    """Listen and recognize voice input."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        try:
            print("Listening...")
            audio = r.listen(source)
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            speak("Sorry, my speech service is down.")
            return None
        except Exception as e:
            print(e)
            speak("Please say that again.")
            return None

def handle_commands(query, floating_icon):

    """Process recognized commands."""

    if "open settings" in query:
        os.system("start ms-settings:network")
        speak("Opening settings.")
        print("Opening settings.")
    
    elif "close system settings" in query or "close settings" in query:
        os.system("taskkill /f /im SystemSettings.exe")
        speak("Closing settings.")
        print("Closing settings.")

    elif "open command prompt" in query or "open cmd" in query:
        os.system("start cmd")
        speak("Opening command prompt.")
        print("Opening command prompt.")

    elif "close command prompt" in query or "close cmd" in query:
        os.system("taskkill /f /im cmd.exe")
        speak("Closing command prompt.")
        print("Closing command prompt.")

    elif "open control panel" in query:
        os.system("start control")
        speak("Opening control panel.")
        print("Opening control panel.")

    elif "close control panel" in query:
        close_control_panel()

    elif "open task manager" in query:
        os.system("start taskmgr")
        speak("Opening task manager.")
        print("Opening task manager.")

    elif "close task manager" in query:
        os.system("taskkill /f /im taskmgr.exe")
        speak("Closing task manager.")
        print("Closing task manager.")

    elif "turn on bluetooth" in query:
        bluetooth_on()

    elif "turn off bluetooth" in query:
        bluetooth_off()

    elif "turn on wifi" in query:
        toggle_wifi(True)

    elif "turn off wifi" in query:
        toggle_wifi(False)

    elif "set brightness to" in query:
        level = int(query.split("to")[1].strip("% "))
        set_brightness(level)

    elif "set volume to" in query:
        level = int(query.split("to")[1].strip("% "))
        set_volume(level)

    elif "sleep mode" in query:
        put_system_to_sleep()

    elif "shutdown" in query:
        shutdown_system()

    elif "restart" in query:
        restart_system()

    elif "log off" in query:
        log_off_system()

    elif "enable dark mode" in query or "disable white mode" in query or " disable light mode" in query or "turn on dark mode" in query:
        toggle_theme("dark")
        
    elif "disable dark mode" in query or "enable white mode" in query or "enable light mode" in query or "turn on white mode"in query or "turn on light mode" in query:
        toggle_theme("light")

    elif "system info" in query:
        system_info()

    elif "lock system" in query:
        lock_system()

    elif "turn off screen" in query:
        turn_off_screen()
    
    elif "turn on screen" in query:
        turn_on_screen()

    elif "close current tab" in query:
        close_current_tab()
        print("Closed the current tab.")

    elif "close" in query and "tab" in query:
        tab_title = query.replace("close", "").replace("tab", "").strip()
        if tab_title:
            close_specific_tab(tab_title)
            print(f"Attempting to close the tab with title containing '{tab_title}'.")
        else:
            print("Please specify the tab title to close.")

    elif "open new tab" in query:
        open_new_tab()
        print("Opened a new tab.")

    elif "what is " in query or "tell me" in query or "when" in query or "where" in query or "why" in query or "i want to know about" in query:
        # If the query matches common question patterns, pass it to ChatGPT
        if any(keyword in query for keyword in ["what is", "tell me", "when", "where", "why", "i want to know about"]):
            response = get_chatgpt_response(query)
        else:
            response = get_chatgpt_response(query)

    elif "open whatsapp" in query or "open Whatsapp" in query or "open WhatsApp" in query or "open WhatSapp application" in query:
       subprocess.run(["start", "whatsapp:"], shell=True)

    elif "close whatsapp" in query or "close Whatsapp" in query or "close WhatsApp" in query or "close WhatSapp application" in query:
       subprocess.run(["taskkill", "/f", "/im", "WhatsApp.exe"], shell=True)

    elif "open telegram" in query.lower():
        os.system("start telegram:")

    elif "close telegram" in query.lower():
        os.system("taskkill /f /im Telegram.exe")

    elif "open website" in query:
        # Extract the URL to open (e.g., "open YouTube in new tab")
        url = query.replace("open website", "").replace("tab", "").strip()
        if url:
            open_url_in_new_tab(url)
            print(f"Opened a new tab with URL: {url}")
        else:
            print("Please specify the URL to open.")

    elif 'send email' in query or "open gmail"in query or "email"in query:
        speak("opening gmail")
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # Update if installed elsewhere
        gmail_url = "https://mail.google.com/mail/u/0/#inbox"
        subprocess.Popen([chrome_path, gmail_url])

    elif "time" in query:
        time()

    elif "date" in query:
        date()

    elif "who are you" in query:
        speak("I'm mini, your desktop voice assistant.")
        print("I'm mini, your desktop voice assistant.")

    elif "how are you" in query:
        speak("I'm fine, sir. What about you?")
        print("I'm fine, sir. What about you?")

    elif "fine" in query or "good" in query:
        speak("Glad to hear that, sir!")
        print("Glad to hear that, sir!")

    elif "open youtube" in query:
        wb.open("https://www.youtube.com")

    elif "open google" in query:
        wb.open("https://www.google.com")

    elif "open stack overflow" in query:
        wb.open("https://stackoverflow.com")

    elif "minimize" in query or "minimise" in query:
        # Extract application name from query
        app_name = query.replace("minimize", "").replace("minimise", "").strip()
        minimize_window(app_name)

    elif "maximize" in query or "maximise" in query:
        # Extract application name from query
        app_name = query.replace("maximize", "").replace("minimise", "").strip()
        maximize_window(app_name)

    elif "search" in query:
    # Extract the search term after "search"
        search = query.replace("search", "").strip()
        if search:
           chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
           # Use an f-string to include the search term in the URL
           get_url = f"https://www.google.com/search?q={search}"
           subprocess.Popen([chrome_path, get_url])
        else:
           print("Please specify what you want to search for.")


    elif "open app" in query:
        app_name = query.replace("open app", "").strip()
        if app_name:
           result = open_app(app_name)
           speak(result)
           print(result)
        else:
           print("Please tell me the name of the app you want to open.")

    elif "close app" in query:
        app_name = query.replace("close app", "").strip()
        if app_name:
           result = close_app(app_name)
           speak(result)
           print(result)
        else:
           print("Please tell me the name of the app you want to close.")

    elif "play music" in query:
        speak("What music would you like to play?")
        attempts = 3  # Number of attempts to wait for user input
        for _ in range(attempts):
           song_name = takecommand()
           if song_name:
              speak(f"Searching {song_name} on Spotify.")
              wb.open(f"https://open.spotify.com/search/{song_name.replace(' ', '%20')}")
              return
           else:
            speak("I didn't hear anything. Please tell me the name of the song.")

    elif "screenshot" in query:
        Screenshot()

    elif "remember that" in query:
            speak("What should I remember?")
            data = takecommand()
            response = remember_data(data)
            speak(response)
            print(response)

    elif "do you remember" in query:
            speak("What keyword should I search for?")
            keyword = takecommand()
            matching_sentences = retrieve_remembered_data(keyword)

            if matching_sentences:
                for sentence in matching_sentences:
                    speak(f"I remember: {sentence}")
                    print(f"Remembered: {sentence}")
            else:
                speak(f"I don't remember anything about {keyword}.")
                print(f"No matching data for keyword: {keyword}")

    elif "stop listening" in query:
        speak("Stopping listening. Say 'Hello mini' or 'hey mini' to wake me again.")
        floating_icon.switch_to_normal()
        return "stop"

    elif "exit" in query or "bye" in query:
        speak("Goodbye! Have a great day!")
        floating_icon.close()
        sys.exit()

def listen_for_wake_word(floating_icon):
    """Continuously listen for the wake word and process commands."""
    while True:
        query = takecommand()
        if query and ("hey mini" in query or "hello mini" in query):
            floating_icon.switch_to_gif()  # Change icon to listening state
            speak("How can I assist you?")
            while True:
                command = takecommand()
                if command:
                    result = handle_commands(command, floating_icon)
                    if result == "stop":
                        break

def start_assistant():
    """Start the assistant with a floating icon."""
    app = QApplication(sys.argv)
    floating_icon = FloatingIcon()
    wishme()

    # Run the wake word detection in a separate thread
    listener_thread = threading.Thread(target=listen_for_wake_word, args=(floating_icon,), daemon=True)
    listener_thread.start()

    sys.exit(app.exec_())

if __name__ == "__main__":
    start_assistant()
