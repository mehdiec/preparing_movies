import os


def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)


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
        root_of_all_evil = f"/Volumes/u934/equipe_bellaiche/m_ech-chouini/test_movies_to_process/{animal_name}/SAP_{animal_name}/PIV_{animal_name}"

        create_folder(
            root_of_all_evil,
        )
