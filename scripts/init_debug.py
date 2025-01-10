import os

LOCAL_PATH = os.path.dirname(__file__)
DEBUG_PATH = os.path.join(LOCAL_PATH, "..", "debug.toml")
TEMPLATE_PATH = os.path.join(LOCAL_PATH, "debug_template.txt")

def main():
    with open(DEBUG_PATH, "w") as debug, open(TEMPLATE_PATH, "r") as template:
        debug.write(template.read())
    print(f"Debug file created at {DEBUG_PATH}.")

if __name__ == "__main__":
    main()
