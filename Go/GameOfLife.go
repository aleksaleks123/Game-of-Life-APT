package main

import (
	"fmt"
	"math/rand"
	"os"
	"strconv"
	"sync"
	"time"
)

const DEAD = 0
const ALIVE = 1

type GameOfLife struct {
	mesh []int8
	n    int
}

func (gol *GameOfLife) GenerateRandomMesh() {
	gol.mesh = make([]int8, gol.n*gol.n)
	for i := range gol.mesh {
		gol.mesh[i] = int8(rand.Intn(2))
	}
}

func (gol *GameOfLife) PrintMesh() {
	for i := 0; i < gol.n; i++ {
		for j := 0; j < gol.n; j++ {
			fmt.Print(gol.mesh[i*gol.n+j], " ")
		}
		fmt.Println()
	}
	fmt.Println()
}

func (gol *GameOfLife) UpdateSerial() {
	defer elapsed("UpdateSerial")()
	newMash := make([]int8, gol.n*gol.n)
	for i := 0; i < gol.n; i++ {
		for j := 0; j < gol.n; j++ {
			gol.updateCell(nil, newMash, i, j)
		}
	}
	gol.mesh = newMash
}

func (gol *GameOfLife) UpdateParallel() {
	defer elapsed("UpdateParallel")()
	newMash := make([]int8, gol.n*gol.n)
	var waitgroup sync.WaitGroup
	for i := 0; i < gol.n; i++ {
		for j := 0; j < gol.n; j++ {
			waitgroup.Add(1)
			go gol.updateCell(&waitgroup, newMash, i, j)
		}
	}
	waitgroup.Wait()
	gol.mesh = newMash
}

func (gol *GameOfLife) updateCell(waitgroup *sync.WaitGroup, newMesh []int8, i, j int) {
	neighbourCount := gol.getNeighbourCount(i, j)
	if gol.mesh[i*gol.n+j] == ALIVE {
		if neighbourCount == 2 || neighbourCount == 3 {
			newMesh[i*gol.n+j] = ALIVE
		}
	} else {
		if neighbourCount == 3 {
			newMesh[i*gol.n+j] = ALIVE
		}
	}
	if waitgroup != nil{
		waitgroup.Done()
	}
}

func (gol *GameOfLife) getNeighbourCount(i, j int) int {
	retval := 0
	for x := -1; x < 2; x++ {
		for y := -1; y < 2; y++ {
			if x != 0 || y != 0 {
				if gol.mesh[mod((i+x), gol.n)*gol.n+mod(j+y, gol.n)] == ALIVE {
					retval++
				}
			}
		}
	}
	return retval
}

func mod(a, b int) int { // returns only positive modulus
	return (a%b + b) % b
}

func elapsed(what string) func() {
	start := time.Now()
	return func() {
		fmt.Printf("%s took %v\n", what, time.Since(start))
	}
}

func main() {
	n, err := strconv.Atoi(os.Args[1])
	if err != nil {
		// handle error
		fmt.Println(err)
		os.Exit(2)
	}

	rand.Seed(1)

	gol := GameOfLife{n: n}
	gol.GenerateRandomMesh()
	for {
		gol.UpdateParallel()
	}
}
