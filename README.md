# Game-of-Life-APT
Project for the course Advanced Programming Techniques.

Its main purpose is to demonstrate the serial and parallel implementation of [Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life).

## Python

### GameOfLife.py
This file contains GameOfLife class that has parallel and serial implementation of mesh update.

`python GameOfLife [-h] [-r] [-c] [-p]`

- -h => show help

- -r => mesh rows

- -r => mesh columns

- -p => number of parallel threads

### testScalings.py
This file tests strong and weak scaling of parallel implementation.

#### Strong scaling results
```
Strong scaling:
update_parallel took 5.870572090148926s with 1 threads for dimensions: 1000x500
update_parallel took 4.398038864135742s with 2 threads for dimensions: 1000x500
update_parallel took 2.917069435119629s with 3 threads for dimensions: 1000x500
update_parallel took 3.15442156791687s with 4 threads for dimensions: 1000x500
update_parallel took 3.016798734664917s with 5 threads for dimensions: 1000x500
update_parallel took 3.5692951679229736s with 6 threads for dimensions: 1000x500
update_parallel took 3.8126304149627686s with 7 threads for dimensions: 1000x500
update_parallel took 4.520707607269287s with 8 threads for dimensions: 1000x500
update_parallel took 4.20755934715271s with 9 threads for dimensions: 1000x500
update_parallel took 4.586529016494751s with 10 threads for dimensions: 1000x500
```
#### Weak scaling results
```
Weak scaling:
update_parallel took 5.6197192668914795s with 1 threads for dimensions: 1000x500
update_parallel took 6.031599760055542s with 2 threads for dimensions: 1000x1000
update_parallel took 8.258521318435669s with 3 threads for dimensions: 1000x1500
update_parallel took 9.505154609680176s with 4 threads for dimensions: 1000x2000
update_parallel took 11.748055696487427s with 5 threads for dimensions: 1000x2500
update_parallel took 13.519237518310547s with 6 threads for dimensions: 1000x3000
update_parallel took 16.355525732040405s with 7 threads for dimensions: 1000x3500
update_parallel took 17.51637029647827s with 8 threads for dimensions: 1000x4000
update_parallel took 19.950751066207886s with 9 threads for dimensions: 1000x4500
update_parallel took 21.311051607131958s with 10 threads for dimensions: 1000x5000
```
## Go
This file contains GameOfLife struct with its methods for parallel and serial implementation of mesh update.

`go build GameOfLife.go`

After running this command, an executable file (`GameOfLife.exe` on Windows) will appear.

`GameOfLife.exe param1 param2 param3`

- param1 => mesh rows

- param2 => mesh columns

- param3 => number of parallel threads

If the executable file is run without any parameters, the test for strong and weak scaling will start.

#### Strong scaling results
```
Strong scaling:
UpdateParallel took 387.0451ms with 1 threads for dimensions 1000x1000
UpdateParallel took 208.4423ms with 2 threads for dimensions 1000x1000
UpdateParallel took 167.5518ms with 3 threads for dimensions 1000x1000
UpdateParallel took 142.6184ms with 4 threads for dimensions 1000x1000
UpdateParallel took 149.6002ms with 5 threads for dimensions 1000x1000
UpdateParallel took 147.6061ms with 6 threads for dimensions 1000x1000
UpdateParallel took 152.5913ms with 7 threads for dimensions 1000x1000
UpdateParallel took 153.5899ms with 8 threads for dimensions 1000x1000
UpdateParallel took 147.6048ms with 9 threads for dimensions 1000x1000
UpdateParallel took 155.5842ms with 10 threads for dimensions 1000x1000
```
#### Weak scaling results
```
Weak scaling:
UpdateParallel took 369.4456ms with 1 threads for dimensions 1000x1000
UpdateParallel took 384.9699ms with 2 threads for dimensions 1000x2000
UpdateParallel took 490.6517ms with 3 threads for dimensions 1000x3000
UpdateParallel took 582.4032ms with 4 threads for dimensions 1000x4000
UpdateParallel took 766.9526ms with 5 threads for dimensions 1000x5000
UpdateParallel took 981.3765ms with 6 threads for dimensions 1000x6000
UpdateParallel took 1.0971804s with 7 threads for dimensions 1000x7000
UpdateParallel took 1.205777s with 8 threads for dimensions 1000x8000
UpdateParallel took 1.4930082s with 9 threads for dimensions 1000x9000
UpdateParallel took 1.4481288s with 10 threads for dimensions 1000x10000
```
## Pharo
Pharo implementation is serial only and its main purpose is visualisation.

To run it, the `Pharo/NTP-GameOfLife.st` package file needs to be imported into running Pharo image (can be done just by dragging the file into Pharo Browser Window).

Then, a window that simulates Game of Life can be opened by running the folowing line:

`(GameOfLife rows: 50 columns: 50 ) openInWindow 	`
