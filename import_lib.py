import importlib
import subprocess
# Define a function to install uninstalled modules
def install_library(library_name):
    try:
        importlib.import_module(library_name)
        print(f"{library_name} is already installed")
    except ImportError:
        print(f"{library_name} is not installed. Installing ...")
        subprocess.run((['pip', 'install', library_name]))
        print(f"{library_name} has been installed")

lib_to_install = ['pandas', 'matplotlib', 'tkinter', 'Pillow']

for library in lib_to_install:
    install_library(library)