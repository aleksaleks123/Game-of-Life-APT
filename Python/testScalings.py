from GameOfLife import GameOfLife

def strong_scaling():
    gol = GameOfLife(1000, 500)
    gol.generate_random_mesh()
    mesh = gol.mesh
    for i in range (1,11):
        gol.update_parallel(i)
        gol.mesh = mesh

def weak_scaling():
    for i in range(1, 11):
        gol = GameOfLife(1000, i*500)
        gol.update_parallel(i)

if __name__ == '__main__':
    print("Strong scaling:")
    strong_scaling()
    print("Weak scaling:")
    weak_scaling()