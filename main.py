from pathlib import Path
import numpy as np

DATA_PATH = Path('data.txt')


def read_data_file():
    points = DATA_PATH.read_text().strip().split('\n')
    points_list = [eval(triangle) for triangle in points]
    return np.array(points_list)


def quick_hull():
    points = read_data_file()


if __name__ == "__main__":
    quick_hull()
