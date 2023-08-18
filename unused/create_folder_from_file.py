import os


def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)


if __name__ == "__main__":
    root_of_all_evil = f"/Volumes/u934/equipe_bellaiche/m_ech-chouini/fb_analysis/"
    for item in os.listdir(root_of_all_evil):
        folder_of_dispair = os.path.join(root_of_all_evil, item.split(".")[0])

        create_folder(folder_of_dispair)
