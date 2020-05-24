import math
import timer

plus_infinity = float("inf")


class TravelingSalesman:
    def __init__(self):
        self.points_num = 0
        self.points = {}

    def execute(self):
        self.read_input()

        t = timer.start_timer('traveling salesman')

        start_point_index = 0
        closest_points_distances = self.recalculate_distances(
            [(i, plus_infinity) for i, p in enumerate(self.points.items()) if i > 0], start_point_index, True)

        salesman_cycle_distance = 0
        last_point = self.points[start_point_index]
        for step in range(1, self.points_num):
            if step % 1000 == 0:
                print('step = ' + str(step))
            next_point_index, next_point_distance = closest_points_distances.pop(0)
            next_point = self.points[next_point_index]
            salesman_cycle_distance += math.sqrt(self.distance_squared(last_point, next_point))
            closest_points_distances = self.recalculate_distances(closest_points_distances, next_point_index, False)
            last_point = next_point

        start_point = self.points[start_point_index]
        last_hop_distance = math.sqrt(self.distance_squared(last_point, start_point))
        salesman_cycle_distance += last_hop_distance

        t['finish_timer']()
        print('result = ' + str(salesman_cycle_distance))
        print('')

    def recalculate_distances(self, distances: list, new_point_index: int, is_all) -> list:
        new_point = self.points[new_point_index]
        for index, value in enumerate(distances):
            # if not is_all and index >= 1000:
            #     break
            distance_to_index, distance = value
            new_distance = self.distance_squared(new_point, self.points[distance_to_index])
            distances[index] = (distance_to_index, new_distance)

        return sorted(distances, key=lambda x: (x[1], x[0]))

    def distance_squared(self, first: tuple, second: tuple) -> float:
        distance = math.pow(first[0] - second[0], 2) + math.pow(first[1] - second[1], 2)
        return distance

    def read_input(self):
        text_file = open("traveling-salesman-input.txt", "r")
        text_file = open("traveling-salesman-heuristic-input.txt", "r")
        lines = text_file.readlines()

#         lines = '''12.00
# 1.000 1.00
# 1.125 1.00
# 1.250 1.00
# 1.500 1.00
# 1.750 1.00
# 2.000 1.00
# 1.000 2.00
# 1.125 2.00
# 1.250 2.00
# 1.500 2.00
# 1.750 2.00
# 2.000 2.00'''.splitlines()

        self.points_num = int(lines[0].strip('.00'))

        for index, line in enumerate(lines[1:]):
            if line.startswith('#'):
                continue
            splitted = line.strip('\n').split(' ')
            x, y = float(splitted[1]), float(splitted[2])
            self.points[index] = (x, y)


TravelingSalesman().execute()
