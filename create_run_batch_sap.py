import os


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

    for file_name in input_files:
        print(file_name)
        if not file_name.lower().endswith((".tif")):
            continue
        file_name = file_name.split(".")[0]
        content += f"clear all; close all;\nSAP_info_{file_name}\n"
    output_file_path = os.path.join(output_folder, "run_batch.m")
    with open(output_file_path, "w") as file:
        file.write(content)


if __name__ == "__main__":
    # Replace 'input_folder_path' and 'output_folder_path' with the actual paths
    input_folder_paths = [
        "/Volumes/u934/equipe_bellaiche/m_ech-chouini/fb_analysis/substraction-RNAi/Dghetero_pnr-no80ts_dgRNAi/full_movies",
        "/Volumes/u934/equipe_bellaiche/m_ech-chouini/fb_analysis/substraction-RNAi/Dghetero_pnr-no80ts_wRNAi/SAP_info",
    ]
    # input_folder_path = "/Volumes/u934/equipe_bellaiche/m_ech-chouini/fb_analysis"
    output_folder_paths = [
        "/Volumes/u934/equipe_bellaiche/m_ech-chouini/fb_analysis/substraction-RNAi/Dghetero_pnr-no80ts_dgRNAi/SAP_info",
        "/Volumes/u934/equipe_bellaiche/m_ech-chouini/fb_analysis/substraction-RNAi/Dghetero_pnr-no80ts_wRNAi/SAP_info",
    ]
    for input_folder_path, output_folder_path in zip(
        input_folder_paths, output_folder_paths
    ):
        generate_files(input_folder_path, output_folder_path)
