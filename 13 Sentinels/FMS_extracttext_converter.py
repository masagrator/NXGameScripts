import os
import sys

# Print script name
print("\t| .fms File Extractor and Converter for the game 13 Sentinels: Aegis Rim |\n")

def read_string(file):
    """Reads a string from a binary file."""
    chars = []
    while True:
        c = file.read(1)
        if c == b'\x00':
            return str(b"".join(chars).decode("UTF-8"))
        chars.append(c)


def extract_text_from_fms(fms_file):
    messages = []

    # Open the binary file for reading
    with open(fms_file, "rb") as file:
        # Seek to position 0x14 in the file
        file.seek(0x14)
        # Read the number of strings in the file
        string_count = int.from_bytes(file.read(4), byteorder="little")
        # Seek to position 0x20 in the file
        file.seek(0x20)
        # Skip the number of strings * 8 bytes
        file.seek(string_count * 8, 1)

        # Read each string from the file
        for _ in range(string_count):
            messages.append(read_string(file))

    # Get the file name without the extension
    filename, _ = os.path.splitext(fms_file)
    # Open the .txt file for writing
    with open(filename + ".txt", "w", encoding="UTF-8") as new_file:
        # Write each message on a separate line
        for i, message in enumerate(messages):
            new_file.write(message.replace("\n", "\\n"))
            if i < len(messages) - 1:
                new_file.write("\n")


def create_fms_from_text(txt_file):
    with open(txt_file, 'r', encoding="UTF-8") as f:
        txt_content = f.read().replace('\n', '\x00').replace('\\n', '\n')

    fms_file = os.path.splitext(txt_file)[0] + '.fms'

    with open(fms_file, 'rb') as f:
        fms_content = f.read()

    new_fms_content = bytearray(fms_content[:0x20])

    offset = int.from_bytes(fms_content[0x14:0x16][::-1], 'big') * 8
    new_fms_content.extend(b'\x00' * offset)
    new_fms_content.extend(txt_content.encode())

    footer_start = fms_content.find(b'\x00', len(new_fms_content))
    if footer_start != -1:
        new_fms_content.extend(fms_content[footer_start:])

    new_fms_file = os.path.splitext(fms_file)[0] + '_new.fms'
    with open(new_fms_file, 'wb') as f:
        f.write(new_fms_content)


def main():
    if len(sys.argv) > 1:
        file = sys.argv[1]
        ext = os.path.splitext(file)[1]

        if ext == ".fms":
            extract_text_from_fms(file)
        elif ext == ".txt":
            create_fms_from_text(file)
        else:
            print("Unsupported file format.")
    else:
        print("No file provided.")

    # Input to close the script
    input("\tPress ENTER to exit")


if __name__ == "__main__":
    main()
