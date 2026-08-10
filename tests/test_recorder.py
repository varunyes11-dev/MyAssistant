from rin.recorder import Recorder


def main():
    recorder = Recorder()

    filename = recorder.record(duration=5)

    print("\nReturned filename:")
    print(filename)


if __name__ == "__main__":
    main()