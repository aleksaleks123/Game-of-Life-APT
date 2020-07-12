import argparse
from multiprocessing import Pool, Array, Process
from random import random

from multiprocessing.sharedctypes import RawArray
import numpy as np
import matplotlib.pyplot as plt
import time

# Possible cell statuses
DEAD = 0
ALIVE = 1


def log_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        retval = func(*args, **kwargs)
        end = time.time()
        parallel = len(args) > 1
        gol = args[0]
        print(f'{"update_parallel" if parallel else "update_serial"} took {end - start}s'
              f'{f" with {args[1]} threads" if parallel else ""} for dimensions: {gol.rows}x{gol.columns}')
        return retval

    return wrapper


class GameOfLife:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.mesh = RawArray(np.ctypeslib.ctypes.c_int8, rows * columns)  # np.zeros(n *n, dtype=np.int8) #
        self.new_mesh = None

    def show_mesh(self):
        image = np.array(self.mesh)
        image = image.reshape((self.rows, self.columns))
        plt.imshow(1 - image, cmap='gray', vmin=0, vmax=1)
        plt.show()

    def generate_random_mesh(self):
        for i in range(self.rows):
            for j in range(self.columns):
                self.mesh[
                    i * self.columns + j] = 1 if random() > 0.5 else 0  # np.random.randint(2, dtype=np.ctypeslib.ctypes.c_int8)

    @log_time
    def update_serial(self):
        self.new_mesh = RawArray(np.ctypeslib.ctypes.c_int8,
                                 self.rows * self.columns)  # np.zeros(self.n *self.n, dtype=np.int8)
        for i in range(self.rows):
            for j in range(self.columns):
                self.update_cell(i, j)
        self.mesh = self.new_mesh

    @log_time
    def update_parallel(self, tasks_num):
        self.new_mesh = RawArray(np.ctypeslib.ctypes.c_int8, self.rows * self.columns)
        processes = []
        for i in range(tasks_num):
            fromi = range(0, self.rows, int(self.rows / tasks_num))[i]
            toi = fromi + int(self.rows / tasks_num)
            if i == tasks_num - 1:
                toi = self.rows
            p = Process(target=self.update_submatrix, args=(fromi, 0, toi, self.columns))
            p.start()
            processes.append(p)
        for p in processes:
            p.join()
        self.mesh = self.new_mesh

    def update_submatrix(self, fromi, fromj, toi, toj):
        for i in range(fromi, toi):
            for j in range(fromj, toj):
                self.update_cell(i, j)

    def update_cell(self, i, j):
        neighbour_count = self.get_neighbour_count(i, j)
        if self.mesh[i * self.columns + j] == ALIVE:
            if neighbour_count == 2 or neighbour_count == 3:
                self.new_mesh[i * self.columns + j] = ALIVE
        else:
            if neighbour_count == 3:
                self.new_mesh[i * self.columns + j] = ALIVE

    def get_neighbour_count(self, i, j):
        retval = 0
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x != 0 or y != 0:
                    if self.mesh[(i + x) % self.rows * self.columns + (j + y) % self.columns] == ALIVE:
                        retval += 1
        return retval


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--rows",
                        help="Mesh dimension", type=int, choices=range(1, 100000),
                        default=50)
    parser.add_argument("-c", "--columns",
                        help="Mesh dimension", type=int, choices=range(1, 100000),
                        default=50)
    parser.add_argument("-p", "--parallel",
                        help="Number of parallel threads", type=int, choices=range(1, 1000))
    args = parser.parse_args()

    np.random.seed(1)

    gol = GameOfLife(args.rows, args.columns)
    gol.generate_random_mesh()
    # gol.show_mesh()

    while True:
        if args.parallel:
            gol.update_parallel(args.parallel)
        else:
            gol.update_serial()
        # gol.show_mesh()
