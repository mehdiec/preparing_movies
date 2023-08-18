import os
import shutil


def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)


def copy_files(source, destination):
    for item in os.listdir(source):
        source_item = os.path.join(source, item)
        if os.path.isfile(source_item):
            shutil.copy(source_item, destination)


def organize_animal_folders(root_of_all_evil, animal_name):
    animal_folder = f"SEG_{animal_name}"
    animal_folder = os.path.join(root_of_all_evil, animal_folder)
    roi_folder = f"roi_{animal_name}"
    results_folder = f"results_{animal_name}"

    create_folder(animal_folder)
    create_folder(os.path.join(animal_folder, roi_folder))
    create_folder(os.path.join(animal_folder, results_folder))

    # copy_files(roi_folder, os.path.join(animal_folder, "ROI_mask"))
    # copy_files(roi_folder, roi_folder)
    # copy_files(roi_folder, results_folder)


if __name__ == "__main__":
    time_ref = {
        "210507_vi_pupa1": 105,
        "210507_vi_pupa3": 93,
        "210823_vi_pupa1": 53,
        "220218_vi_pupa3": 107,
        "220902_vi_pupa1": 86,
        "210603_Tolloi_pupa1": 58,
        "210603_Tolloi_pupa3": 71,
        "210604_Tolloi_pupa6": 97,
        "210818_Tolloi_pupa2": 101,
        "210823_Tolloi_pupa2": 69,
    }
    for animal_name in time_ref.keys():
        root_of_all_evil = f"/Volumes/u934/equipe_bellaiche/m_ech-chouini/test_movies_to_process/{animal_name}"

        organize_animal_folders(root_of_all_evil, animal_name)
