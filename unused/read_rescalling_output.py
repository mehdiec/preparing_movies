import pandas as pd


def rescalling_dict(input_file):
    df = pd.read_table(input_file, sep=" ")
    df.set_index("Name", inplace=True)
    df.to_json()
    dict_dict = df.to_dict(orient="dict")
    print("Dict-like (dict):", dict_dict)


if __name__ == "__main__":
    input_file = "/Volumes/u934/equipe_bellaiche/m_ech-chouini/test_movies_to_process/rescaled_animal/v_tollo_rescaled_21h40_nMacroUsed=4/rescalingOutput.txt"
    rescalling_dict(input_file)
