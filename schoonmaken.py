from datetime import date, timedelta
from collections import defaultdict, namedtuple
from dataclasses import dataclass
from random import choice

@dataclass
class Task:
	name: str
	numpeople: int = 1
	ismonthly: bool = False
	weight: int = 1

	def __hash__(self):
		return hash(self.name)
	
	def __repr__(self):
		return self.name

	def due(self, week):
		return first_week_of_mounth(week)

TaskData = namedtuple('TaskData', ['name,', 'count', 'weeks_since_done'])

@dataclass(frozen=True)
class Person:
	name: str
	room: int

	def available(self, week):
		return True

	def cleaning_score(self, task) -> int:
		'''
		Cleaning score - the heart of the algorithms and 
		the most poorly documented and least readable function in it.
		'''
		any_last_week = min(self._weeks_since_done.values()) == 1
		any_2w_ago = min(self._weeks_since_done.values()) == 2
		t_counter = self._task_counters[task]
		any_counter = sum(self._task_counters.values())
		return Person.steven_score(any_last_week, any_2w_ago, t_counter, any_counter)

	def __hash__(self):
		return hash(self.room)

	def __str__(self):
		return self.name

	@staticmethod
	def steven_score(any_last_week, any_2w_ago, t_counter, any_counter) -> int:
		'''Based on works of S. Meuleman, Esq.'''
		return 8 * any_last_week + 2 * any_2w_ago + 2 * t_counter + 1 * any_counter

class TaskPersonTable():
	people: list[Person]
	tasks: list[Task]

	PeopleList = namedtuple('PeopleList', [person.name for person in people])
	TaskList = namedtuple('PeopleList', [task.name for task in tasks])

	_rows = TaskList(*[PeopleList(*[0 for person in people])])

	def __iter__(self):
		pass

tasks = [
	Task('Living room', numpeople=2),
	Task('Toilets'),
	Task('Bathroom'),
	Task('Showers'),
	Task('Hallways'),
	Task('Kitchen', numpeople=3, ismonthly=True),
	Task('Laundry room', ismonthly=True)
]

people = [ 
	Person('Eva', 101, )
]

def _fill_week(tasks: list[Task]=[], people: list[Person]=[]):
	'''
	1. choose candidates for each task
	2. if a candidate in multiple tasks:
		1. assign the candidate to the task with lower score
		2. choose a backup candidate for other tasks
	'''
	candidates = {task : task.candidates[:3] for task in tasks}
	while True:
		pass

def choose_people(task: Task, people: set[Person]) -> set[Person]:
	chosen = sorted(task.scores)[:task.numpeople]
	return set(person for score, person in chosen)


def fill_week(tasks: set[Task], people: set[Person]):
	assignments = {}
	for task in tasks:
		assignments[task] = choose_people(task, people)
		people -= assignments[task]

def _fill_week(tasks: list[Task]=[], people: list[Person]=[]):
	candidates = defaultdict([])
	for person in people:
		(chosen_task, score) = person.chosen_task
		candidates[chosen_task].append(chosen_task, score)
	
	assigned_people = {}
	for task in candidates:
		min_score = min(score for _, score in candidates[task])
		chosen_person = choice(person for person, score in candidates[task] if score == min_score)
		assigned_people[task] = chosen_person
		person.do(task)
	
	for person in people:
		person.pass_week()
	
	return assigned_people
	
def weeks(start: date, end: date) -> list[date]:
	'''
	start will be rounded down to the most recent Monday.
	weeks are represented by Mondays
	'''
	start -= timedelta(days=(start.weekday())) # most recent Monday
	while start < end:
		yield start
		start += timedelta(days=7) # next Monday

def first_week_of_mounth(week: date) -> bool:
	return week.day - week.weekday() <= 7

def fill_schedule(weeks):
	get_people = lambda week: (person.available(week) for person in people)
	get_tasks = lambda week: (task.due(week) for task in tasks)
	return ((week, fill_week(get_tasks(week), get_people(week))) for week in weeks)

def build_table(schedule, header=True):
	table = [['Week'] + [task.name for task in task]] if header else []
	task_row = lambda week_tasks: [week_tasks[task] or None for task in tasks]
	table += [[week.strftime('%d-%m-%y')] + task_row(tasks) for week, week_tasks in schedule]
	return table