import os


input_folder_paths = (
    "/Volumes/u934/equipe_bellaiche/m_ech-chouini/fb_analysis/substraction-RNAi/Dghetero_pnr-no80ts_dgRNAi/full_movies",
)
animals = [
    file_name.split(".")[0]
    for file_name in os.listdir(input_folder_paths[0])
    if file_name[0].isalpha() and file_name.lower().endswith((".tif"))
]
tr_dict = {}


def get_frame_ref_tr(animals):
    for animal in animals:
        tr_file = f"/Volumes/u934/equipe_bellaiche/m_ech-chouini/fb_analysis/substraction-RNAi/Dghetero_pnr-no80ts_dgRNAi/{animal}/SAP_{animal}/timeReg_{animal}/{animal}_TR.txt"
        with open(tr_file, "r") as file:
            # Loop through the lines in the file
            for line in file:
                if "frame_ref20" in line:
                    frame_ref20 = int(line.split("=")[1])
                    tr_dict[animal] = frame_ref20

    return tr_dict
