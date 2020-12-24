from datetime import datetime
from pathlib import Path
from typing import List, Tuple
from math import sqrt

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


def distance_between_points(first_point, second_point):
    fx, fy = first_point
    sx, sy = second_point
    return sqrt((sy-fy)**2 + (sx-fx)**2)


def sign(side_1: int, side_2: int) -> bool:
    if side_1 > 0 and side_2 > 0:
        return True
    elif side_1 < 0 and side_2 < 0:
        return True
    elif side_1 == side_2:
        return True
    else:
        return False


def distance_from_point_to_line():
    pass


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

    def find_hull_point(points: List[Tuple], left_point: Tuple, right_point: Tuple):
        hulls = []
        default_distance = float('-inf')
        line_length = distance_between_points(left_point, right_point)
        for point in points:
            # dist_point_to_line = distance_from_point_to_line()
            # default_distance = max(dist_point_to_line, default_distance)
            # if default_distance == dist_point_to_line:
            #     hull_point = point
            pass
        # hulls.append(hull_point)
        import pdb; pdb.set_trace()

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
            if sign(side_of_line, upper_side_of_line):
                upper_set.append(point)
            else:
                bottom_set.append(point)

    if upper_set:
        find_hull_point(upper_set, left_point, right_point)
    if bottom_set:
        find_hull_point(bottom_set, left_point, right_point)


def quick_hull():
    points = read_data_file()
    start_time = datetime.now()

    build_quick_hull(points)

    end_time = datetime.now()
    print(f"Estimated time: {end_time - start_time} msc.")


if __name__ == "__main__":
    quick_hull()
