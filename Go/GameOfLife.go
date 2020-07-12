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
	mesh    []int8
	rows    int
	columns int
}

func (gol *GameOfLife) GenerateRandomMesh() {
	gol.mesh = make([]int8, gol.rows*gol.columns)
	for i := range gol.mesh {
		gol.mesh[i] = int8(rand.Intn(2))
	}
}

func (gol *GameOfLife) GenerateEmptyMesh() {
	gol.mesh = make([]int8, gol.rows*gol.columns)
}

func (gol *GameOfLife) PrintMesh() {
	for i := 0; i < gol.rows; i++ {
		for j := 0; j < gol.columns; j++ {
			fmt.Print(gol.mesh[i*gol.columns+j], " ")
		}
		fmt.Println()
	}
	fmt.Println()
}

func (gol *GameOfLife) UpdateSerial() {
	defer logTime("UpdateSerial", nil, gol.rows, gol.columns)()
	newMash := make([]int8, gol.rows*gol.columns)
	for i := 0; i < gol.rows; i++ {
		for j := 0; j < gol.columns; j++ {
			gol.updateCell(newMash, i, j)
		}
	}
	gol.mesh = newMash
}

func (gol *GameOfLife) UpdateParallel(tasksNum int) {
	defer logTime("UpdateParallel", &tasksNum, gol.rows, gol.columns)()
	newMash := make([]int8, gol.rows*gol.columns)
	var waitgroup sync.WaitGroup
	taskSize := gol.rows / tasksNum
	for i := 0; i < tasksNum; i++ {
		waitgroup.Add(1)
		toi := gol.rows
		if i < tasksNum-1 {
			toi = (i + 1) * taskSize
		}
		go gol.updateSubMatrix(&waitgroup, newMash, i*taskSize, 0, toi, gol.columns)
	}
	waitgroup.Wait()
	gol.mesh = newMash
}

func (gol *GameOfLife) updateSubMatrix(waitgroup *sync.WaitGroup, newMesh []int8, fromi, fromj, toi, toj int) {
	for i := fromi; i < toi; i++ {
		for j := fromj; j < toj; j++ {
			gol.updateCell(newMesh, i, j)
		}
	}
	waitgroup.Done()
}

func (gol *GameOfLife) updateCell(newMesh []int8, i, j int) {
	neighbourCount := gol.getNeighbourCount(i, j)
	if gol.mesh[i*gol.columns+j] == ALIVE {
		if neighbourCount == 2 || neighbourCount == 3 {
			newMesh[i*gol.columns+j] = ALIVE
		}
	} else {
		if neighbourCount == 3 {
			newMesh[i*gol.columns+j] = ALIVE
		}
	}
}

func (gol *GameOfLife) getNeighbourCount(i, j int) int {
	retval := 0
	for x := -1; x < 2; x++ {
		for y := -1; y < 2; y++ {
			if x != 0 || y != 0 {
				if gol.mesh[mod((i+x), gol.rows)*gol.columns+mod(j+y, gol.columns)] == ALIVE {
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

func logTime(what string, tasksNum *int, rows, columns int) func() {
	start := time.Now()
	return func() {
		str := ""
		if tasksNum != nil {
			str = fmt.Sprintf(" with %v threads", *tasksNum)
		}
		fmt.Printf("%s took %v%s for dimensions: %vx%v\n", what, time.Since(start), str, rows, columns)
	}
}

func main() {
	var rows, columns, tasksNum int
	var err1, err2, err3 error

	if len(os.Args) < 3 {
		TestScaling()
		return
	}

	rows, err1 = strconv.Atoi(os.Args[1])
	if err1 != nil {
		// handle error
		fmt.Println(err1)
		os.Exit(2)
	}

	columns, err2 = strconv.Atoi(os.Args[2])
	if err2 != nil {
		// handle error
		fmt.Println(err2)
		os.Exit(2)
	}

	if len(os.Args) > 3 {
		tasksNum, err3 = strconv.Atoi(os.Args[3])
		if err3 != nil {
			// handle error
			fmt.Println(err3)
			os.Exit(2)
		}
	}

	rand.Seed(1)

	gol := GameOfLife{rows: rows, columns: columns}
	gol.GenerateRandomMesh()
	gol.PrintMesh()
	for {
		if len(os.Args) == 3 {
			gol.UpdateSerial()
		} else {
			gol.UpdateParallel(tasksNum)
		}
		gol.PrintMesh()
	}
}

func StrongScaling() {
	gol := GameOfLife{rows: 1000, columns: 1000}
	gol.GenerateRandomMesh()
	mesh := gol.mesh
	for i := 1; i < 11; i++ {
		gol.UpdateParallel(i)
		gol.mesh = mesh
	}
}

func WeakScaling() {
	for i := 1; i < 11; i++ {
		gol := GameOfLife{rows: 1000, columns: i * 1000}
		gol.GenerateRandomMesh()
		gol.UpdateParallel(i)
	}
}

func TestScaling() {
	fmt.Println("Strong scaling:")
	StrongScaling()
	fmt.Println("Weak scaling:")
	WeakScaling()
}
