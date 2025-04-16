# date.py
import datetime

if __name__ == "__main__":
    now = datetime.datetime.now()
    print(now.strftime("%a %b %d %H:%M:%S %Y"))
    print()  # Add an empty line for spacing

