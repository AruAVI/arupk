# whoami.py

if __name__ == "__main__":
    print(globals().get("__cwd__", "").split("/")[-1])
