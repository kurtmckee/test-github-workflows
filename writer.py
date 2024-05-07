import pathlib

path = pathlib.Path(__file__).parent / "README.md"
with open(path, "a") as file:
    file.write("- additional\n")
