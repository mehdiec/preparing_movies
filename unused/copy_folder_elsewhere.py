import shutil
import os
import sys


def copy_folder(source_folder, destination_folder):
    try:
        # Check if the source folder exists
        if not os.path.exists(source_folder):
            print("Source folder does not exist.")
            return

        # Create the destination folder if it doesn't exist
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        # Copy the contents of the source folder to the destination folder
        for item in os.listdir(source_folder):
            source_item = os.path.join(source_folder, item)
            destination_item = os.path.join(destination_folder, item)

            if os.path.isdir(source_item):
                shutil.copytree(source_item, destination_item)
            else:
                shutil.copy2(source_item, destination_item)

        print("Folder copied successfully.")

    except Exception as e:
        print("An error occurred:", str(e))


if __name__ == "__main__":
    # Provide the paths of the source and destination folders here
    time_ref = {
                '210507_vi_pupa1'        :  104,
                '210507_vi_pupa3'        :  93,
                '210823_vi_pupa1'        :  55,
                '220218_vi_pupa3'        : 106,
                '220902_vi_pupa1'        :  88,
                '210603_Tolloi_pupa1'    :  58,
                '210603_Tolloi_pupa3'    :  81,
                '210604_Tolloi_pupa6'    :  95,
                '210818_Tolloi_pupa2'    :  97,
                '210823_Tolloi_pupa2'    :  69,
    }
    for animal_name in time_ref.keys():
        source_folder_path = f"/Volumes/u934/equipe_bellaiche/a_leroy/Movies/movies_v_Tollo/{animal_name}/SAP_{animal_name}/PIV_{animal_name}"  # Replace with the actual source folder path
        destination_folder_path = f"/Volumes/u934/equipe_bellaiche/m_ech-chouini/test_movies_to_process/{animal_name}/SAP_{animal_name}/PIV_{animal_name}"  # Replace with the actual destination folder path

        copy_folder(source_folder_path, destination_folder_path)
