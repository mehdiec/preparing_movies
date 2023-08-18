import argparse
import os
from pathlib import Path
import warnings
import numpy as np
from skimage import io, exposure
from tqdm import tqdm
import shutil


def format_4_decimals(num):
    if 0 <= num <= 9999:
        return "{:04}".format(num)
    else:
        raise ValueError(
            "Number out of range. Please provide a number between 0 and 9999."
        )


def create_folder(path):
    if os.path.exists(path):
        return
    os.makedirs(path)


def rescale_to_uint8(
    image,
    reference_image="/Volumes/u934/equipe_bellaiche/m_ech-chouini/test_movies_to_process/210507_vi_pupa1/210507_vi_pupa1_0236.tif",
):
    reference_image = io.imread(reference_image)
    if reference_image is not None:
        matched_image = exposure.match_histograms(image, reference_image)
    else:
        min_val = matched_image.min()
        max_val = matched_image.max()
        matched_image = ((matched_image - min_val) / (max_val - min_val) * 255).astype(
            np.uint8
        )
    rescaled_image = matched_image.astype(np.uint8)

    return rescaled_image


def split_movie_in_frames(movie_folder, image):
    movie_name = os.path.basename(movie_folder[:-4])
    output_folder = movie_folder[:-4]

    create_folder(output_folder)

    for index, frame in tqdm(enumerate(image)):
        frame_path = os.path.join(
            output_folder, movie_name + f"_{format_4_decimals(index+1)}.tif"
        )
        if os.path.exists(frame_path):
            continue
        if frame.dtype != "uint8":
            frame = rescale_to_uint8(frame)

        io.imsave(frame_path, frame)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="SPLIT THE FULL MOVIES BECAUSE IM NOT DOING IT USING FIJI FOR HUNDREDS OF MOVIES!!!!!!",
        epilog="hihi",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "parent_folder", type=Path, help="Path to folder containing the project"
    )

    # Parse the arguments
    args = parser.parse_args()
    parent_folder = args.parent_folder
    create_folder(parent_folder / "full_movies")

    for tiff_file in os.listdir(parent_folder):
        if "-" in tiff_file:
            new_filename = tiff_file.replace("-", "_")
            old_filepath = os.path.join(parent_folder, tiff_file)
            new_filepath = os.path.join(parent_folder, new_filename)
            tiff_file = new_filename
            os.rename(old_filepath, new_filepath)
        item_path = os.path.join(parent_folder, tiff_file)
        print(tiff_file)
        if tiff_file.endswith(".tif"):
            if tiff_file:
                image = io.imread(item_path)
                shutil.move(item_path, parent_folder / "full_movies")
                split_movie_in_frames(item_path, image)

    print("Separation and storage completed.")
