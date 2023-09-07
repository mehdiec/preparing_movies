import os
from pathlib import Path
import argparse
from create_sap_info import get_frame_ref_tr


def generate_files(input_folder, output_folder):
    """_summary_

    Parameters
    ----------
    input_folder : _type_
        _description_
    output_folder : _type_
        _description_
    """
    # Check if the output folder exists, if not, create it
    if not os.path.exists(output_folder):
        print("apprends à lire")
        return

    # List all the files in the input folder
    input_files = list(os.listdir(input_folder))
    input_files.sort()
    content = ""
    input_folder_path = Path(
        "/Volumes/u934/equipe_bellaiche/m_ech-chouini/fb_analysis/substraction-RNAi/"
    )
    output_folder_path = input_folder_path / "SAP_info"

    rescaling_file_path = "/path/to/rescaling/file.txt"  # Update with the actual path

    # rescaling_data = read_rescaling_file(rescaling_file_path)

    animals = [
        file_name.split(".")[0]
        for file_name in os.listdir(input_folder_path / Path("full_movies"))
        if file_name.lower().endswith((".tif"))
    ]

    time_ref_dict = get_frame_ref_tr(input_folder_path, animals)

    for file_name in input_files:
        # if not file_name.lower().endswith((".tif")):
        #     continue
        file_name = file_name.split(".")[0]
        t_ref = time_ref_dict.get(file_name, 71)
        start_frame = 1
        # if t_ref > 10 and t_ref < 180:
        #     continue
        print(file_name)
        content += f"clear all; close all;\nSAP_info_{file_name}\n"
    output_file_path = os.path.join(output_folder, "run_batch.m")
    print(content)
    with open(output_file_path, "w") as file:
        file.write(content)


if __name__ == "__main__":
    # Replace 'input_folder_path' and 'output_folder_path' with the actual paths
    parser = argparse.ArgumentParser(
        description="CREATE ALL RUN BATCH!!!!!!",
        epilog="hihi",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "parent_folder", type=Path, help="Path to folder containing the animal 1"
    )

    args = parser.parse_args()
    input_folder_path = args.parent_folder / "full_movies"

    output_folder_path = args.parent_folder / "SAP_info"

    generate_files(input_folder_path, output_folder_path)
