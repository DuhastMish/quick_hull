from datetime import datetime
from math import atan2, sqrt
from pathlib import Path
from typing import List, Tuple, Dict

DATA_PATH = Path('data.txt')


def read_data_file() -> List[Tuple[int, int]]:
    """Reading points from a file.

    Returns:
        List[Tuple[int, int]]: List of points, e.g. [(x,y)]
    """
    points = DATA_PATH.read_text().strip().split('\n')
    points_list = [eval(triangle) for triangle in points]
    return points_list


def determine_position_from_line(line_point_left: Tuple,
                                 line_point_right: Tuple,
                                 point: Tuple) -> int:
    """Determine the position of a point,
    relative to the first two that form a straight line.

    Args:
        line_point_left (Tuple): Left point of the straight line
        line_point_right (Tuple): Right point of a straight line
        point (Tuple): Point to determine position

    Returns:
        int: Returns a number:
            if negative, then the point lies on the left,
            if positive, then on the right,
            if zero, then on a straight line
    """
    lx, ly = line_point_left
    rx, ry = line_point_right
    px, py = point
    return (px-lx)*(ry-ly) - (py-ly)*(rx-lx)


def distance_between_points(first_point: Tuple, second_point: Tuple) -> float:
    """Return the distance between points

    Args:
        first_point (Tuple): First point
        second_point (Tuple): Second point

    Returns:
        float: Distance
    """
    fx, fy = first_point
    sx, sy = second_point
    return sqrt((sy-fy)**2 + (sx-fx)**2)


def sign(side_1: int, side_2: int) -> bool:
    if (side_1 > 0 and side_2 > 0) or (side_1 < 0 and side_2 < 0) or (side_1 == side_2):
        return True
    else:
        return False


def distance_from_point_to_line(orientation: int,
                                distance: int) -> float:
    """Distance from point to line

    Args:
        orientation (int): Point position
        distance (int): Distance

    Returns:
        float: Distance
    """
    return abs(orientation) / distance


def build_quick_hull(points: List[Tuple]) -> Tuple:
    """Builds a quick hull.

    Args:
        points (List[Tuple]): Point List

    Returns:
        Tuple: Returns the (leftmost, rightmost, top point sets, bottom point sets).
    """
    def find_hull_point(points: List[Tuple], left_point: Tuple, right_point: Tuple) -> List:
        """Returns a list of points that belong to the top/bot shell

        Args:
            points (List[Tuple]): Point.
            left_point (Tuple): Left point of the line.
            right_point (Tuple): Right point of the line.

        Returns:
            List: Point List
        """
        if points:
            hulls = []
            hull_point = None
            default_distance = float('-inf')
            line_length = distance_between_points(left_point, right_point)
            for point in points:
                point_orientation = determine_position_from_line(left_point, right_point, point)
                dist_point_to_line = distance_from_point_to_line(point_orientation, line_length)
                if dist_point_to_line == 0:
                    continue
                default_distance = max(dist_point_to_line, default_distance)
                if default_distance == dist_point_to_line:
                    hull_point = point
            if hull_point:
                hulls.append(hull_point)
                upper_set = []
                bottom_set = []
                upper_point_orientation = determine_position_from_line(left_point, hull_point, right_point)
                bottom_point_orientation = determine_position_from_line(hull_point, right_point, left_point)

                for point in points:
                    if point not in hulls:
                        if (not sign(determine_position_from_line(left_point, hull_point, point),
                                     upper_point_orientation)
                                and determine_position_from_line(left_point, hull_point, point) != 0):
                            upper_set.append(point)

                        if (not sign(determine_position_from_line(hull_point, right_point, point),
                                     bottom_point_orientation)
                                and determine_position_from_line(hull_point, right_point, point) != 0):
                            bottom_set.append(point)

                up_set = find_hull_point(upper_set, left_point, hull_point)
                bot_set = find_hull_point(bottom_set, hull_point, right_point)

                return hulls + bot_set + up_set
            else:
                return []
        else:
            return []

    upper_set = []
    bottom_set = []
    points.sort(key=lambda x: (x[0], x[1]))
    left_point, right_point = points[0], points[-1]
    x, y = left_point
    upper_left_point = (x, y+1)
    upper_side_of_line = determine_position_from_line(left_point, right_point, upper_left_point)

    for point in points:
        if point not in [left_point, right_point]:
            side_of_line = determine_position_from_line(left_point, right_point, point)
            if sign(side_of_line, upper_side_of_line) and side_of_line != 0:
                upper_set.append(point)
            else:
                bottom_set.append(point)

    if upper_set:
        upper_set = find_hull_point(upper_set, left_point, right_point)
    if bottom_set:
        bottom_set = find_hull_point(bottom_set, left_point, right_point)
    return left_point, right_point, upper_set, bottom_set


def make_indexes(points: List[Tuple]) -> Dict[Tuple, int]:
    """Specifies indices for original points

    Args:
        points (List[Tuple]): Points list

    Returns:
        Dict[Tuple, int]: Dictionary, where the key is the coordinates of the points, and the value is its index.
    """
    indexes = {}
    index = 0
    for point in points:
        indexes[point] = index
        index += 1
    return indexes


def quick_hull():
    """Builds a quick hull."""
    points = read_data_file()
    indexes = make_indexes(points)
    start_time = datetime.now()

    left_point, right_point, upper_set, bottom_set = build_quick_hull(points)
    print(f"Estimated time: {datetime.now() - start_time} msc.")

    result = []
    result.append(left_point)
    result.extend(upper_set)
    result.extend(bottom_set)
    result.append(right_point)
    sum_x = sum_y = 0
    for point in result:
        x, y = point
        sum_x += x
        sum_y += y
    sort_x, sort_y = sum_x/len(result), sum_y/len(result)

    result.sort(key=lambda x: (atan2(x[1]-sort_y, x[0]-sort_x)))
    print("Result:")
    for res_index, res_point in enumerate(result):
        try:
            if res_point != result[res_index + 1]:
                print(f"{indexes[res_point]} - {indexes[result[res_index + 1]]}")
        except IndexError:
            print(f"{indexes[res_point]} - {indexes[result[0]]}")


if __name__ == "__main__":
    quick_hull()
