import argparse
import os
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import json

animal = "your_animal_name"
frame_numbers = [1, 2, 3, 4]  # Replace with the frame numbers you have

line_counts = []


def count_tif_files(
    folder_path,
):
    tif_count = sum(
        1 for file in os.listdir(folder_path) if file.lower().endswith(".tif")
    )
    return tif_count


def count_division(cell_trackinng_path, frame_numbers):
    line_counts = []
    for frame_number in range(frame_numbers):
        file_name = f"dividing_cells_RN_{frame_number}.txt"
        file_path = cell_trackinng_path / file_name

        if file_path.exists():
            with file_path.open() as file:
                lines = file.readlines()
                line_count = len(lines)
                line_counts.append(line_count)
        else:
            line_counts.append(0)  # File doesn't exist

    return line_counts


def main(input_folder_path):
    dict_division = {}
    animals = [
        file_name.split(".")[0]
        for file_name in os.listdir(input_folder_path / Path("full_movies"))
        if file_name.lower().endswith((".tif"))
    ]
    for animal in animals:
        end_frame = count_tif_files(input_folder_path / animal)
        cell_trackinng_path = (
            input_folder_path / animal / f"SAP_{animal}" / f"CT_{animal}" / "LGrid"
        )

        dict_division[animal] = count_division(cell_trackinng_path, end_frame)
        # print(dict_division)
    return dict_division


def moving_average(data, window_size):
    return np.convolve(data, np.ones(window_size) / window_size, mode="valid")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="CREATE ALL THE SAP INFOS AND MAP PARAMS!!!!!!",
        epilog="hihi",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "parent_folder", type=Path, help="Path to folder containing the animal 1"
    )
    parser.add_argument("-plot", action="store_true", default=False, required=False)

    args = parser.parse_args()
    input_folder_paths = args.parent_folder
    data = main(input_folder_paths)
    peak_time = {}
    # Initialize the figure

    for idx, (animal, values) in enumerate(data.items()):
        values_tmp = values[5:]
        max_value = max(values_tmp)
        max_index = values.index(max_value)

        moving_avg = moving_average(values, 5)  # Assuming a window size of 5
        max_value = max(moving_avg[5:])
        max_index = list(moving_avg[:]).index(max_value)

        peak_time[animal] = int(max_index * 0.75)

        if args.plot:
            fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20, 1 * 8))
            values_tmp = values[5:]

            # Original data plot
            axes[0].plot(values, label=f"{animal} Original")
            max_value = max(values_tmp)
            max_index = values.index(max_value)
            axes[0].scatter(max_index, max_value, color="red", label="Max Value")

            # Annotation
            axes[0].annotate(
                f"Max Value: {max_value}\nIndex peak {max_index}",
                xy=(max_index, max_value),
                xycoords="data",
                xytext=(10, 30),
                textcoords="offset points",
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"),
            )

            # Moving average plot
            moving_avg = moving_average(values, 5)  # Assuming a window size of 5
            axes[1].plot(
                range(4, len(values)), moving_avg, label=f"{animal} Moving Avg"
            )
            # Original data plot
            max_value = max(moving_avg[5:])
            max_index = list(moving_avg[:]).index(max_value)
            axes[1].scatter(max_index, max_value, color="red", label="Max Value")

            # Annotation
            axes[1].annotate(
                f"Max Value: {max_value}\nIndex peak {max_index}",
                xy=(max_index, max_value),
                xycoords="data",
                xytext=(10, 30),
                textcoords="offset points",
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"),
            )

            # Axes labels and titles
            axes[0].set_xlabel("Time")
            axes[0].set_ylabel("Values")
            axes[0].set_title(f"{animal} Original Data")
            axes[0].legend()

            axes[1].set_xlabel("Time")
            axes[1].set_ylabel("Values")
            axes[1].set_title(f"{animal} Moving Average Data")
            axes[1].legend()

            peak_time[animal] = int(max_index * 0.75)
            print(peak_time)
            plt.tight_layout()
            plt.savefig(f"graph/{animal}_division_plot.png")

    # plt.show()
    # Show the figure

    print(peak_time)
    with open(input_folder_paths + "/peak_time.json", "w") as f:
        json.dump(peak_time, f)
