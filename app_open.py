import json
import os
import psutil

def load_apps():
    """Load the app data from the JSON file."""
    with open('apps.json', 'r') as f:
        data = json.load(f)
        if "apps" in data and isinstance(data["apps"], list):
            return data["apps"]
        return []

def open_app(app_name):
    """Open an app by its name or synonym."""
    apps = load_apps()
    for app in apps:
        if app_name in app["synonyms"]:
            try:
                os.startfile(app["path"])
                return f"Opening {app_name}."
            except FileNotFoundError:
                return f"Error: The path for {app_name} is invalid or the application is not installed."
    return f"Sorry, I couldn't find an application named {app_name}."

def close_app(app_name):
    """Close an app by its name or synonym."""
    apps = load_apps()
    for app in apps:
        if app_name in app["synonyms"]:
            executable = os.path.basename(app["path"])
            for process in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    # Match standard apps
                    if process.info['name'].lower() == executable.lower():
                        process.terminate()
                        return f"Closed {app_name}."

                    # Additional check for UWP apps
                    cmdline = process.info.get('cmdline', [])
                    if cmdline and "WindowsApps" in cmdline[0]:
                        if app_name in ' '.join(cmdline).lower():
                            process.terminate()
                            return f"Closed {app_name}."
                except (psutil.NoSuchProcess, IndexError, KeyError):
                    # Ignore processes that disappear during iteration or have unexpected structures
                    continue

            return f"{app_name} is not currently running."
    return f"Sorry, I couldn't find an application named {app_name}."
