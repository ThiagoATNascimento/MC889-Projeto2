import sys

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <x> <y>")
        raise SystemExit(1)

    print(xor(sys.argv[1], sys.argv[2]))

def xor(x, y):
    return chr(ord(x) ^ ord(y))

if __name__ == "__main__":
    main()
