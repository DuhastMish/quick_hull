from pathlib import Path
from typing import Tuple, List

DATA_PATH = Path('data.txt')


def read_data_file() -> List:
    points = DATA_PATH.read_text().strip().split('\n')
    points_list = [eval(triangle) for triangle in points]
    return points_list


def get_left_and_right_points(points_list: List) -> Tuple[Tuple]:
    minimal_x = minimal_y = float('inf')
    maximal_x = maximal_y = 0
    for point in points_list:
        coord_x, coord_y = point
        if coord_x < minimal_x:
            minimal_x = coord_x
            minimal_y = coord_y
        elif coord_x > maximal_y:
            maximal_x = coord_x
            maximal_y = coord_y

    return ((minimal_x, minimal_y), (maximal_x, maximal_y))

def quick_hull():
    points = read_data_file()
    left_point, right_point = get_left_and_right_points(points)
    import pdb; pdb.set_trace()


if __name__ == "__main__":
    quick_hull()
