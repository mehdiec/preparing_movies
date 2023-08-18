import os
import pandas as pd

from constants import SAP_PARAMETERS, create_map_param, generate_animal_config


def read_rescaling_file(input_file):
    """
    Read and parse a rescaling input file to create a dictionary of resize data.

    Parameters
    ----------
    input_file : str
        Path to the input rescaling file.

    Returns
    -------
    dict
        A dictionary containing resize data with image names as keys.
    """
    df = pd.read_table(input_file, sep=" ")
    df.set_index("Name", inplace=True)
    return df.to_dict(orient="index")


def get_frame_ref_tr(animals):
    tr_dict = {}

    for animal in animals:
        tr_file = f"/Volumes/u934/equipe_bellaiche/m_ech-chouini/fb_analysis/substraction-RNAi/Dghetero_pnr-no80ts_dgRNAi/{animal}/SAP_{animal}/timeReg_{animal}/{animal}_TR.txt"
        with open(tr_file, "r") as file:
            # Loop through the lines in the file
            for line in file:
                if "frame_ref20" in line:
                    frame_ref20 = int(line.split("=")[1])
                    tr_dict[animal] = frame_ref20

    return tr_dict


def count_tif_files(folder_path):
    """
    Count the number of .tif files in a folder.

    Parameters
    ----------
    folder_path : str
        Path to the folder containing the files.

    Returns
    -------
    int
        Number of .tif files in the folder.
    """
    tif_count = sum(
        1 for file in os.listdir(folder_path) if file.lower().endswith(".tif")
    )
    return tif_count


def generate_files(
    input_folder, output_folder, rescaling_file_path=None, time_ref_dict={}
):
    """
    Generate SAP configuration files for a set of input files.

    Parameters
    ----------
    input_folder : str
        Path to the input folder containing files.
    output_folder : str
        Path to the output folder for generated files.
    rescaling_file_path : str, optional
        Path to the rescaling input file, by default None.
    time_ref_dict : dict, optional
        Dictionary mapping file names to time reference values, by default {}.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    input_files = [
        file_name for file_name in os.listdir(input_folder) if file_name[0].isalpha()
    ]
    rescaling_data = (
        read_rescaling_file(rescaling_file_path) if rescaling_file_path else {}
    )

    for file_name in input_files:
        if "SAP" in file_name or file_name.lower().endswith((".png", ".tif")):
            continue

        end_frame = count_tif_files(os.path.join(input_folder, file_name))
        output_file_path = os.path.join(
            output_folder, f"SAP_info_{file_name.replace('-', '_')}.m"
        )
        resize_data = rescaling_data.get(file_name, {})
        yml = resize_data.get("yML(pix)")
        xFactor = resize_data.get("xFactor")
        yFactor = resize_data.get("yFactor")
        ox = resize_data.get("Ox(pix)")
        oy = resize_data.get("Oy(pix)")
        t_ref = time_ref_dict.get(file_name)

        content = generate_animal_config(
            file_name,
            1,
            end_frame,
            4,
            yml,
            xFactor,
            yFactor,
            ox,
            oy,
            t_ref,
            input_folder=input_folder,
        )

        with open(output_file_path, "w") as file:
            file.write(content)

        print(f"Generated file: {output_file_path}")


def find_common_string(strings):
    common = []
    for chars in zip(*strings):
        if all(char == chars[0] for char in chars):
            common.append(chars[0])
        else:
            break
    return "".join(common)


if __name__ == "__main__":
    input_path_map = (
        "/Volumes/u934/equipe_bellaiche/m_ech-chouini/fb_analysis/substraction-RNAi/"
    )
    input_folder_paths = [
        "/Volumes/u934/equipe_bellaiche/m_ech-chouini/fb_analysis/substraction-RNAi/Dghetero_pnr-no80ts_dgRNAi/",
        "/Volumes/u934/equipe_bellaiche/m_ech-chouini/fb_analysis/substraction-RNAi/Dghetero_pnr-no80ts_wRNAi",
    ]
    # input_folder_path = "/Volumes/u934/equipe_bellaiche/m_ech-chouini/fb_analysis"
    output_folder_paths = [
        "/Volumes/u934/equipe_bellaiche/m_ech-chouini/fb_analysis/substraction-RNAi/Dghetero_pnr-no80ts_dgRNAi/SAP_info",
        "/Volumes/u934/equipe_bellaiche/m_ech-chouini/fb_analysis/substraction-RNAi/Dghetero_pnr-no80ts_wRNAi/SAP_info",
    ]
    use_all = False  # False
    # rescaling_file_path = "/Volumes/u934/equipe_bellaiche/m_ech-chouini/test_movies_to_process/rescaled_animal/v_tollo_rescaled_21h40_nMacroUsed=4/rescalingOutput.txt"

    # time_ref_dict = {
    #     "210507_vi_pupa1": 104,
    #     "210507_vi_pupa3": 93,
    #     ...
    # }
    animal_1 = [
        "'" + file_name.split(".")[0] + "'"
        for file_name in os.listdir(input_folder_paths[0])
        if file_name[0].isalpha() and file_name.lower().endswith((".tif"))
    ]
    animal_2 = [
        "'" + file_name.split(".")[0] + "'"
        for file_name in os.listdir(input_folder_paths[1])
        if file_name[0].isalpha() and file_name.lower().endswith((".tif"))
    ]

    animal_root_1 = find_common_string(animal_1).split("-")[0][1:]
    animal_root_2 = find_common_string(animal_2).split("-")[0][1:]

    for input_folder_path, output_folder_path in zip(
        input_folder_paths, output_folder_paths
    ):
        animals = [
            file_name.split(".")[0]
            for file_name in os.listdir(
                "/Volumes/u934/equipe_bellaiche/m_ech-chouini/fb_analysis/substraction-RNAi/Dghetero_pnr-no80ts_dgRNAi/full_movies/"
            )
            if file_name.lower().endswith((".tif"))
        ]

        time_ref_dict = get_frame_ref_tr(animals)

        if not os.path.exists(output_folder_path):
            os.makedirs(output_folder_path)
        if use_all:
            output_file_path = os.path.join(output_folder_path, "MAP_parameters.m")
            with open(output_file_path, "w") as file:
                map_param = create_map_param(
                    animal_1, animal_2, animal_root_1, animal_root_2, input_path_map
                )
                file.write(map_param)
            output_file_path = os.path.join(output_folder_path, "SAP_parameters.m")
            with open(output_file_path, "w") as file:
                file.write(SAP_PARAMETERS)

            print(f"Generated file: {output_file_path}")

        generate_files(
            input_folder_path,
            output_folder_path,
            # rescaling_file_path,
            time_ref_dict=time_ref_dict,
        )
        break
