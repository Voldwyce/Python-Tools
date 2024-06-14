import argparse
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

def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-t", "--time", type=int, help="Tiempo en segundos para recordatorio", default=1800)
    args = parser.parse_args()
    if args.time == None:
        args.time = 1800

    while True:
        remind()
        time.sleep(args.time)

if __name__ == "__main__":
    main()