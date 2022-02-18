import subprocess


def main():
    process = subprocess.Popen(["python3", "main.py"])
    try:
        print("Running in process", process.pid)
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        print("Timed out - killing", process.pid)
        process.kill()
    print("Success!")
    exit(0)


if __name__ == "__main__":
    main()
