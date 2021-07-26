# Huize Schommelbank cleaning scheduler

## Usage

### Setting up
1. Get the code
	- ```git clone``` or ```curl``` the repo
	- download directly from GitHub
2. Modify the config file or run config UI

### Config specification
### Config generator
### Running the scheduler script
### Interactive scheduer

## The nitty-gritty of the problem

### Objectives

0) Exclusive scheduling
	a) a person can only be assigned onetask in a week
	b) a task can only have the requirednumber of people assigned to it
1) Eqaul spread of tasks
	a) everybody gets each task as manytimes as everybody else
	which suffices for...
	b) total number of tasks assigned equalfor everybody
	c) tasks' relative difficulty sould beaccounted for
2) Variability of assignments
	a) you don't get to do the same taskmultiple weeks in a row
	b) you complete every task once beforerepeating any of them
	c) rotation in group tasks
3) Regular breaks
	- you're less likely to clean 2 or 3weeks in a row
4) Flexilibily
	a) accounting for people beingunavailable 
	b) (accounting for people doing extra)
	c) (allowing explicit switches)

### Testing metrics
- everybody gets each task as many times aseverybody else
- rotation in group tasks
- are there doubles? doubles with a skip?
- how fast the numbers normalize aftersomeone skipped two weeks? does it result in doubles?

### Methodology

0. just don't select anybody twice and have the right number of people on each task
1. keeping track of times the task wasdone and evening it out
2. 
	- caching last 2 weeks' schedule andavoiding repetitions
	- that's a tricky one...
	- randomization
3) caching last 2 weeks' schedule andavoiding repetitions (across all tasks)
4a) keeping track and chicking availability
4b) manually incrementing task counters
4c) prerpocessing the generated schedule with requested switches,
	    and adjusting the task counts accordingly

### Issues

1) if somebody is unavailable for a long time, their scores are lower than that of the rest
	- optionally, artificially add points in the amount derived from the rest's stats
	- in case of short unavailability, just ignore the issue
2) algorithm only chooses 1 person per task

### Algorithm

1) for the given week determine tasks due and people available
2) for each (task, person) pair determine the cleaning score
	- the cleaning score should reflect:
		- how many times the person did the task 
			- possibly reduced by minimum across all people
			- large deviation should have bigger effect,
				e.g. never let it go higher than 5
		- wether the person did THIS task lately (last week = significant)
		- wether the person did ANY task lately
3) assing people to minimize the total cleaning score across them
	1) select people with lowest scores for each task, in doubt randomize
	or
	1) select a task with the lowes score for each person
	2) eliminate collisions by comparing the score and choosing randomly