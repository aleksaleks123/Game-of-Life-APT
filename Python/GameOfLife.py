import argparse
from multiprocessing import Pool, Array
import ctypes
import numpy as np
import matplotlib.pyplot as plt
import time

# Possible cell statuses
DEAD = np.int8(0)
ALIVE = np.int8(1)


class GameOfLife:
    def __init__(self, n=50):
        self.n = n
        self.mesh = Array(ctypes.c_int8, n * n)  # np.zeros((n, n), dtype=np.int8)
        self.new_mesh = None

    def show_mesh(self):
        plt.imshow(self.mesh, cmap='gray', vmin=DEAD, vmax=ALIVE)
        plt.show()

    def generate_random_mesh(self):
        for i in range(self.n):
            for j in range(self.n):
                self.mesh[i * self.n + j] = np.random.randint(2, dtype=np.int8)

    def update_serial(self):
        self.new_mesh = Array(ctypes.c_int8, self.n * self.n)
        for i in range(self.n):
            for j in range(self.n):
                self.update_cell(i, j)
        self.mesh = self.new_mesh

    def update_parallel(self):
        self.new_mesh = Array(ctypes.c_int8, self.n * self.n)
        with Pool() as pool:
            pool.starmap(self.update_cell, [(i, j) for i in range(self.n) for j in range(self.n)])
        self.mesh = self.new_mesh

    def update_cell(self, i, j):
        neighbour_count = self.get_neighbour_count(i, j)
        if self.mesh[i * self.n + j] == ALIVE:
            if neighbour_count == 2 or neighbour_count == 3:
                self.new_mesh[i * self.n + j] = ALIVE
        else:
            if neighbour_count == 3:
                self.new_mesh[i * self.n + j] = ALIVE

    def get_neighbour_count(self, i, j):
        retval = 0
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x != 0 or y != 0:
                    if self.mesh[(i + x) % self.n * self.n + (j + y) % self.n] == ALIVE:
                        retval += 1
        return retval


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--ndimension",
                        help="Mesh dimension", type=int, choices=range(1, 100000),
                        default=50)
    args = parser.parse_args()

    np.random.seed(1)

    gol = GameOfLife(args.ndimension)
    gol.generate_random_mesh()
    while True:
        start = time.time()
        gol.update_parallel()
        end = time.time()
        print(end - start)
        gol.show_mesh()
