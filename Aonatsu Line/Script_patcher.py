import sys
import glob
import os
from pathlib import Path

files = glob.glob(f"{sys.argv[1]}/*.binu8")

os.makedirs("Patched", exist_ok=True)

for i in range(len(files)):
	compiled_script = open(files[i], "rb")
	buffer = compiled_script.read()
	compiled_script.close()

	original_script = open(f"Script/{Path(files[i]).stem}.binu8", "rb")
	script_type = int.from_bytes(original_script.read(4), "little")
	if (script_type != 0):
		original_script.close()
		print("This is not a valid scenario file. Ignoring...")
		continue
	commands_count = int.from_bytes(original_script.read(4), "little")
	original_script.seek(commands_count * 8, 1)
	strings_count = int.from_bytes(original_script.read(4), "little")
	for x in range(strings_count):
		string_size = int.from_bytes(original_script.read(4), "little")
		original_script.seek(string_size, 1)
	data = original_script.read()
	original_script.close()

	new_script = open(f"Patched/{Path(files[i]).stem}.binu8", "wb")
	new_script.write(buffer)
	new_script.write(data)
	new_script.close()
