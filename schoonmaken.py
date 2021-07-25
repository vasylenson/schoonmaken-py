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
		return first_week_of_mounth(week) or not self.ismonthly

# TaskData = namedtuple('TaskData', ['name,', 'count', 'weeks_since_done'])

@dataclass(frozen=True)
class Person:
	name: str
	room: int

	def available(self, week):
		return True

	def __hash__(self):
		return hash(self.room)

	def __str__(self):
		return self.name

	@staticmethod
	def steven_score(any_last_week, any_2w_ago, t_counter, any_counter) -> int:
		'''Based on works of S. Meuleman, Esq.'''
		return 8 * any_last_week + 2 * any_2w_ago + 2 * t_counter + 1 * any_counter

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
	Person('Eva', 101),
	Person('Ab', 102),
	Person('Roos', 103),
	Person('Kees', 104),
	Person('Marko', 105),
	Person('Manu', 106),
	Person('Jasper', 107),
	Person('Stephanie', 211),
	Person('Daan', 212),
	Person('Marjo', 213),
	Person('Bas', 214),
	Person('Tom', 215),
	Person('Michelle', 216),
	Person('Diego', 217)
]

class Counters:
	times_done = {(t, p) : 0 for t in tasks for p in people}
	weeks_since_done = {(t, p) : 1e9 for t in tasks for p in people}

	@classmethod
	def score(cls, task: Task, person: Person) -> float:
		td = cls.times_done[task, person]
		wsd = cls.weeks_since_done[task, person]
		return td + 10 / wsd
	
	@classmethod
	def update(cls, assignments: list[tuple[Task, Person]]):
		"""
		Inrements total task counters and resets weeks since done for assigned people, updates WSD for the rest
		"""
		for task_person in cls.weeks_since_done:
			cls.weeks_since_done[task_person] += 1

		for task, people in assignments:
			for person in people:
				cls.times_done[task, person] += task.weight
				cls.weeks_since_done[task, person] = 1

def score(task, person):
	return Counters.score(task, person)

def choose_people(task: Task, people: set[Person]) -> set[Person]:
	scores = [(score(task, person), person) for person in people]
	scores.sort(key=lambda pair: pair[0])
	chosen = scores[:task.numpeople]
	return set([person for score, person in chosen])

def fill_week(tasks: set[Task], people: set[Person]):
	assignments = {} # Map: Task -> [Person]
	for task in tasks:
		c = choose_people(task, people)
		assignments[task] = c
		people = people - c
	Counters.update(assignments.items())
	return assignments

# def _fill_week(tasks: list[Task]=[], people: list[Person]=[]):
# 	candidates = defaultdict([])
# 	for person in people:
# 		(chosen_task, score) = person.chosen_task
# 		candidates[chosen_task].append(chosen_task, score)
	
# 	assigned_people = {}
# 	for task in candidates:
# 		min_score = min(score for _, score in candidates[task])
# 		chosen_person = choice(person for person, score in candidates[task] if score == min_score)
# 		assigned_people[task] = chosen_person
# 		person.do(task)
	
# 	for person in people:
# 		person.pass_week()
	
# 	return assigned_people
	
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
	get_people = lambda week: {person for person in people if person.available(week)}
	get_tasks = lambda week: (task for task in tasks if task.due(week))
	return ((week, fill_week(get_tasks(week), get_people(week))) for week in weeks)

def names(assignments: dict[Task, Person]):
	def person_or_none(task: Task):
		if task in assignments:
			return [person.name for person in assignments[task]]
		else:
			return None
	return [person_or_none(task) for task in tasks]

def build_table(schedule, header=True):
	# print(len(list(schedule)), "########################")
	table = [['Week'] + [task.name for task in tasks]] if header else []
	table += [[week.strftime('%d-%m-%y')] + names(tasks) for week, tasks in schedule]
	return table