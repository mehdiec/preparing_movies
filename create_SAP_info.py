import argparse
import os
import pandas as pd
from pathlib import Path

from constants import SAP_PARAMETERS, create_map_param, generate_animal_config


def read_rescaling_file(input_file):
    df = pd.read_table(input_file, sep=" ")
    df.set_index("Name", inplace=True)
    return df.to_dict(orient="index")


def get_frame_ref_tr(input_path, animals):
    tr_dict = {}
    for animal in animals:
        tr_file_rel = Path(f"{animal}/SAP_{animal}/timeReg_{animal}/{animal}_TR.txt")

        tr_file = input_path / tr_file_rel
        with open(tr_file, "r") as file:
            # Loop through the lines in the file
            for line in file:
                if "frame_ref20" in line:
                    frame_ref20 = int(line.split("=")[1])

                    tr_dict[animal] = frame_ref20

    return tr_dict


def count_tif_files(folder_path):
    tif_count = sum(
        1 for file in os.listdir(folder_path) if file.lower().endswith(".tif")
    )
    return tif_count


def generate_sap_config_file(output_file_path, content):
    with open(output_file_path, "w") as file:
        file.write(content)
    print(f"Generated file: {output_file_path}")


def generate_sap_files(
    input_folder, output_folder, rescaling_data={}, time_ref_dict={}
):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    movie_path = Path("full_movies")
    input_folder = input_folder / movie_path
    for file_name in os.listdir(input_folder):
        if file_name[0].isalpha() and not file_name.lower().endswith((".png", ".tif")):
            continue

        root_file_name = file_name.split(".")[0]

        end_frame = count_tif_files(os.path.join(input_folder.parent, root_file_name))
        output_file_path = os.path.join(
            output_folder, f"SAP_info_{root_file_name.replace('-', '_')}.m"
        )
        resize_data = rescaling_data.get(root_file_name, {})
        yml = resize_data.get("yML(pix)", "")
        xFactor = resize_data.get("xFactor", 1)
        yFactor = resize_data.get("yFactor", 1)
        ox = resize_data.get("Ox(pix)", 1100)
        oy = resize_data.get("Oy(pix)", 700)

        t_ref = time_ref_dict.get(root_file_name, 71)

        content = generate_animal_config(
            root_file_name,
            1,
            end_frame,
            4,
            yml,
            xFactor,
            yFactor,
            ox,
            oy,
            t_ref,
            input_folder=input_folder.parent,
        )

        generate_sap_config_file(output_file_path, content)


def main(input_folder_paths):
    output_folder_paths = [path / "SAP_info" for path in input_folder_paths]

    # rescaling_file_path = "/path/to/rescaling/file.txt"  # Update with the actual path

    # rescaling_data = read_rescaling_file(rescaling_file_path)

    for input_folder_path, output_folder_path in zip(
        input_folder_paths, output_folder_paths
    ):
        animals = [
            file_name.split(".")[0]
            for file_name in os.listdir(input_folder_path / Path("full_movies"))
            if file_name.lower().endswith((".tif"))
        ]

        time_ref_dict = get_frame_ref_tr(input_folder_path, animals)

        generate_sap_files(
            input_folder_path,
            output_folder_path,
            # rescaling_data,
            time_ref_dict=time_ref_dict,
        )
        break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="CREATE ALL THE SAP INFOS AND MAP PARAMS!!!!!!",
        epilog="hihi",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "parent_folder_1", type=Path, help="Path to folder containing the animal 1"
    )

    parser.add_argument(
        "parent_folder_2", type=Path, help="Path to folder containing the animal 2"
    )
    args = parser.parse_args()
    input_folder_paths = [args.parent_folder_1, args.parent_folder_2]
    main(input_folder_paths)
