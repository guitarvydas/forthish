import sys
import chardet

def main():
    # Read raw bytes from stdin
    raw = sys.stdin.buffer.read()

    # Detect encoding
    result = chardet.detect(raw)
    enc = result["encoding"] or "utf-8"

    try:
        text = raw.decode(enc)
    except Exception as e:
        print(f"Error decoding with {enc}: {e}", file=sys.stderr)
        sys.exit(1)

    # Write UTF-8 to stdout
    sys.stdout.buffer.write(text.encode("utf-8"))

if __name__ == "__main__":
    main()
