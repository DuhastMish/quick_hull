from datetime import datetime
from pathlib import Path
from typing import List, Tuple
import numpy as np
DATA_PATH = Path('data.txt')


def read_data_file() -> List:
    points = DATA_PATH.read_text().strip().split('\n')
    points_list = [eval(triangle) for triangle in points]
    return points_list


def determine_position_from_line(line_point_left: Tuple,
                                 line_point_right: Tuple,
                                 point: Tuple):
    lx, ly = line_point_left
    rx, ry = line_point_right
    px, py = point
    return (px-lx)*(ry-ly) - (py-ly)*(rx-lx)


def build_quick_hull(points: List[Tuple]):
    def get_left_and_right_points(points_list: List) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        minimal_x = minimal_y = float('inf')
        maximal_x = maximal_y = 0
        for point in points_list:
            coord_x, coord_y = point
            if coord_x < minimal_x:
                minimal_x = coord_x
                minimal_y = coord_y
            if coord_x > maximal_y:
                maximal_x = coord_x
                maximal_y = coord_y

        return ((int(minimal_x), int(minimal_y)), (maximal_x, maximal_y))

    upper_set = []
    bottom_set = []
    sorted_points = points.sort(key=lambda x: (x[0], x[1]))
    left_point, right_point = get_left_and_right_points(points)
    x, y = left_point
    upper_left_point = (x, y+1)
    upper_side_of_line = determine_position_from_line(left_point, right_point, upper_left_point)

    for point in points:
        if point not in [left_point, right_point]:
            side_of_line = determine_position_from_line(left_point, right_point, point)
            if np.sign(side_of_line) == np.sign(upper_side_of_line):
                upper_set.append(point)
            else:
                bottom_set.append(point)

    return upper_set, bottom_set


def quick_hull():
    points = read_data_file()
    start_time = datetime.now()

    build_quick_hull(points)

    end_time = datetime.now()
    print(f"Estimated time: {end_time - start_time} msc.")


if __name__ == "__main__":
    quick_hull()
