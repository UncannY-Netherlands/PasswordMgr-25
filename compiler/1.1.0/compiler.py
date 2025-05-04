import os
import subprocess
import sys

def compile_with_nuitka(source_file, icon_file):
    source_file = source_file.strip('"').strip("'").strip()
    source_file = os.path.expanduser(source_file)
    source_file = os.path.abspath(source_file)

    icon_file = icon_file.strip('"').strip("'").strip()
    icon_file = os.path.expanduser(icon_file)
    icon_file = os.path.abspath(icon_file)

    if not os.path.isfile(source_file):
        print(f"Error: File '{source_file}' does not exist.")
        return

    if not os.path.isfile(icon_file):
        print(f"Error: Icon file '{icon_file}' does not exist.")
        return

    try:
        command = [
            sys.executable,
            "-m", "nuitka",
            "--standalone",
            "--follow-imports",
            "--enable-plugin=pylint-warnings",
            f"--windows-icon-from-ico={icon_file}",
            source_file
        ]

        print("Compiling with Nuitka...")
        subprocess.run(command, check=True)
        print("Compilation successful!")

    except subprocess.CalledProcessError as e:
        print(f"Compilation failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    source_file = input("Enter the path to the source file: ").strip()
    icon_file = input("Enter the path to the icon file (.ico): ").strip()
    compile_with_nuitka(source_file, icon_file)