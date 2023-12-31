import argparse
import json
import os

import pandas as pd
from pathlib import Path

from constants import (
    create_map_param,
    create_sap_parameters,
    generate_animal_config,
)


def read_rescaling_file(input_file):
    df = pd.read_table(input_file, sep=" ")
    df.set_index("Name", inplace=True)
    # print(df)
    return df.to_dict()
    return


def get_frame_ref_tr(input_path, animals):
    tr_dict = {}
    for animal in animals:
        tr_file_rel = Path(f"{animal}/SAP_{animal}/timeReg_{animal}/{animal}_TR.txt")

        tr_file = input_path / tr_file_rel
        if not os.path.exists(tr_file):
            continue

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
        # print(rescaling_data)
        resize_data = rescaling_data.get(root_file_name, {})
        yml = resize_data.get("yML(pix)", "")
        xFactor = resize_data.get("xFactor", 1)
        yFactor = resize_data.get("yFactor", 1)
        ox = resize_data.get("Ox(pix)", 1100)
        oy = resize_data.get("Oy(pix)", 700)

        t_ref = time_ref_dict.get(root_file_name, 71)
        start_frame = 1
        # if t_ref < 10:
        #     start_frame = t_ref + 20
        #     t_ref = 70

        # if t_ref > 180:
        #     end_frame = t_ref - 10
        #     t_ref = 70

        content = generate_animal_config(
            root_file_name,
            start_frame,
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


def find_common_prefix(strings_list, min_occurrences=9):
    prefixes_counter = {}
    min_occurrences = min(min_occurrences, max(2, len(strings_list) // 2))

    for string in strings_list:
        for i in range(1, len(string) + 1):
            prefix = string[:i]
            if prefix in prefixes_counter:
                prefixes_counter[prefix] += 1
            else:
                prefixes_counter[prefix] = 1
    # print(prefixes_counter)

    common_prefix = None

    for prefix, count in prefixes_counter.items():
        if count >= min_occurrences and (
            common_prefix is None or len(prefix) > len(common_prefix)
        ):
            common_prefix = prefix

    return common_prefix


def main(
    input_folder_path,
    sr,
    piv,
    ra,
    vm,
    aot,
    aoa,
    dba,
    ffbp,
    ct,
    archetype,
    rescale,
    animal_number,
):
    output_folder_path = input_folder_path / "SAP_info"

    animals = [
        file_name.split(".")[0]
        for file_name in os.listdir(input_folder_path / Path("full_movies"))
        if file_name.lower().endswith((".tif"))
    ]
    try:
        with open(str(input_folder_paths) + "/peak_time.json", "r") as f:
            time_ref_dict = json.load(f)
    except FileNotFoundError:
        time_ref_dict = {}

    animal_roots = []
    filtered_animals = animals.copy()
    all_animal_groups = []

    while filtered_animals:
        current_root = find_common_prefix(filtered_animals)
        if current_root:
            animal_roots.append(current_root)
            current_group = [item for item in filtered_animals if current_root in item]
            all_animal_groups.append(current_group)
            filtered_animals = [
                item for item in filtered_animals if current_root not in item
            ]
        else:
            break
    if not animal_roots:
        animal_roots = [animal.split("_")[0] for animal in animals]
        all_animal_groups = [[animal] for animal in animals]
    print(animal_roots)

    rescaling_data = {}

    # Loop through the list of animal roots to try different paths
    for animal in animal_roots:
        rescaling_file_path = f"{input_folder_path}/{animal}_rescaled_21h40_nMacroUsed=4/rescalingOutput.txt"

        try:
            rescaling_data = read_rescaling_file(rescaling_file_path)
            if (
                rescaling_data
            ):  # Assuming an empty dictionary means failure to read the file
                break
        except FileNotFoundError:
            continue  # If the file doesn't exist, try the next animal root

    if not rescaling_data:
        print("Warning: No rescaling file could be read.")

    generate_sap_files(
        input_folder_path,
        output_folder_path,
        rescaling_data,
        time_ref_dict=time_ref_dict,
    )

    content = create_map_param(
        all_animal_groups,
        animal_roots,
        input_folder_path,
        archetype,
        rescale,
        animal_number,
        ra,
        aoa,
        dba,
    )

    output_file_path = output_folder_path / "MAP_parameters.m"
    with open(output_file_path, "w") as file:
        file.write(content)
    print(f"Generated file: {output_file_path}")
    content = create_map_param(
        all_animal_groups,
        animal_roots,
        input_folder_path,
        archetype,
        rescale,
        animal_number,
        ra,
        aoa,
        dba,
    )

    output_file_path = output_folder_path / f"MAP_parameters{animal_number}.m"
    with open(output_file_path, "w") as file:
        file.write(content)
    print(f"Generated file: {output_file_path}")

    content = create_sap_parameters(
        sr,
        piv,
        vm,
        ffbp,
        ct,
        aot,
    )

    output_file_path = output_folder_path / "SAP_parameters.m"
    with open(output_file_path, "w") as file:
        file.write(content)
    print(f"Generated file: {output_file_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="CREATE ALL THE SAP INFOS AND MAP PARAMS!!!!!!",
        epilog="hihi",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "parent_folder", type=Path, help="Path to folder containing the animal 1"
    )
    parser.add_argument("-sr", action="store_true", default=False, required=False)
    parser.add_argument("-ra", action="store_true", default=False, required=False)
    parser.add_argument("-vm", action="store_true", default=False, required=False)
    parser.add_argument("-aot", action="store_true", default=False, required=False)
    parser.add_argument("-ffbp", action="store_true", default=False, required=False)
    parser.add_argument("-ct", action="store_true", default=False, required=False)
    parser.add_argument("-aoa", action="store_true", default=False, required=False)
    parser.add_argument("-dba", action="store_true", default=False, required=False)
    parser.add_argument("-piv", action="store_true", default=False, required=False)
    parser.add_argument(
        "-archetype", action="store_true", default=False, required=False
    )
    parser.add_argument("-rescale", action="store_true", default=False, required=False)
    parser.add_argument(
        "--animal",
        type=int,
        help="Path to folder containing the animal 1",
        default=0,
        required=False,
    )
    args = parser.parse_args()
    input_folder_paths = args.parent_folder
    sr = 1 if args.sr else 0
    ra = 1 if args.ra else 0
    vm = 1 if args.vm else 0
    aot = 1 if args.aot else 0
    aoa = 1 if args.aoa else 0
    dba = 1 if args.dba else 0
    ffbp = 1 if args.ffbp else 0
    ct = 1 if args.ct else 0
    piv = 1 if args.piv else 0

    archetype = args.archetype
    rescale = args.rescale
    animal_number = args.animal
    main(
        input_folder_paths,
        sr,
        piv,
        ra,
        vm,
        aot,
        aoa,
        dba,
        ffbp,
        ct,
        archetype,
        rescale,
        animal_number,
    )
