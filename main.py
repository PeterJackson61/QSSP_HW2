import subprocess

if __name__ == "__main__":
     # Libraries installer
    process_1_command = ["python", "import_lib.py"]
    subprocess.run(process_1_command, check=True)

    # Define the command for the graph builder and data conversion
    process_2_command = ["python", "graph_builder.py"]

    # Run the first for graph building and data conversion
    subprocess.run(process_2_command, check=True)

    # Define the command for the graph viewer code
    process_3_command = ["python", "graph_viewer.py"]

    # Run the graph viewer app
    subprocess.run(process_3_command, check=True)