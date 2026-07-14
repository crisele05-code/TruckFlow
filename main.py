from generator.utils import load_comuni

def main():
    comuni = load_comuni()

    print(comuni.sample(10))


if __name__ == "__main__":
    main()