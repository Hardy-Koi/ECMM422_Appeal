from pathlib import Path
import os
from datetime import datetime
import IPython
import shutil

def save_history():
    # Define the directory for storing history
    dir_path = Path(os.getcwd()) / "proof_of_work"
    dir_path.mkdir(parents=True, exist_ok=True)  # Create if it doesn't exist

    # Generate a timestamped filename
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    file_path = dir_path / f"CA_history_{timestamp}.txt"

    # Access IPython history
    profile_hist = IPython.core.history.HistoryAccessor(profile="default")
    session_id = profile_hist.get_last_session_id()

    try:
        with open(file_path, "w", encoding="utf-8") as file:
            for line in profile_hist.get_tail(n=1000, raw=False, output=False, include_latest=False):
                if session_id == line[0]:
                    # Replace newlines in commands with a space to avoid formatting issues
                    sanitized_command = line[2].replace("\n", " ")
                    out = f"{timestamp} {line[0]} {line[1]} {sanitized_command}"
                    file.write(f"{out}\n")
    
    except Exception as e:
        print(f"Error saving history: {e}")


def check_and_prepare_for_submission():
    try:
        # Define the proof_of_work directory
        path = Path("proof_of_work")

        # Check if the directory exists
        if not path.exists():
            raise FileNotFoundError(f"ERROR: The directory <{path}> is missing!")

        # Check if there are files inside the directory
        file_count = sum(1 for _ in path.rglob("*") if _.is_file())  # Count files
        if file_count == 0:
            raise ValueError(f"ERROR: The directory <{path}> is empty!")

        # Proceed with zipping the notebook and history files
        output_filename = "ecmm422ca2"
        current_dir = Path.cwd()
        parent_dir = current_dir.parent

        # Move to parent directory and create zip archive
        shutil.make_archive(parent_dir / output_filename, 'zip', current_dir)

        print(f"The notebook and the history are ready for submission.\n"
              f"The following archive has been created in the parent directory: {output_filename}.zip")

    except FileNotFoundError as e:
        print(f"Submission Error: {e}")
    except ValueError as e:
        print(f"Submission Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
