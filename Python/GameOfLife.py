import argparse
from multiprocessing import Pool, Array, Process
from multiprocessing.sharedctypes import RawArray
import numpy as np
import matplotlib.pyplot as plt
import time

# Possible cell statuses
DEAD = 0
ALIVE = 1


class GameOfLife:
    def __init__(self, n=50):
        self.n = n
        self.mesh = RawArray(np.ctypeslib.ctypes.c_int8, n * n)  # np.zeros(n *n, dtype=np.int8) #
        self.new_mesh = None

    def show_mesh(self):
        image = np.array(self.mesh)
        image = image.reshape((self.n, self.n))
        plt.imshow(image, cmap='gray', vmin=0, vmax=1)
        plt.show()

    def generate_random_mesh(self):
        for i in range(self.n):
            for j in range(self.n):
                self.mesh[i * self.n + j] = np.random.randint(2, dtype=np.ctypeslib.ctypes.c_int8)

    def update_serial(self):
        self.new_mesh = RawArray(np.ctypeslib.ctypes.c_int8, self.n * self.n)  # np.zeros(self.n *self.n, dtype=np.int8)
        for i in range(self.n):
            for j in range(self.n):
                self.update_cell(i, j)
        self.mesh = self.new_mesh

    def update_parallel(self, tasks_num):
        self.new_mesh = RawArray(np.ctypeslib.ctypes.c_int8, self.n * self.n)
        processes = []
        for i in range(tasks_num):
            fromi = range(0, self.n, int(self.n / tasks_num))[i]
            toi = fromi + int(self.n / tasks_num)
            if i == tasks_num - 1:
                toi = self.n
            p = Process(target=self.update_submatrix, args=(fromi, 0, toi, self.n))
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
    parser.add_argument("-p", "--parallel",
                        help="Number of parallel threads", type=int, choices=range(1, 1000))
    args = parser.parse_args()

    np.random.seed(1)

    gol = GameOfLife(args.ndimension)
    gol.generate_random_mesh()

    while True:
        start = time.time()
        if args.parallel:
            gol.update_parallel(args.parallel)
        else:
            gol.update_serial()
        end = time.time()
        print(f'{"update_parallel" if args.parallel else "update_serial"} took {end - start}s'
              f'{f" with {args.parallel} threads" if args.parallel else ""}')
        gol.show_mesh()
