import time
import tkinter as tk
from plyer import notification

def remind():
    # Display a pop-up notification
    notification.notify(
        title="Water Reminder",
        message="It's time to drink!",
        app_name="Water Reminder",
        timeout=10
    )

# Remind every 30 minutes
while True:
    remind()
    time.sleep(1800)