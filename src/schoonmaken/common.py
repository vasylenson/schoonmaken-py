from dataclasses import dataclass
from datetime import date, timedelta


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

class Counters:

	def __init__(self, tasks, people):
		self.tasks = tasks
		self.people = people
		self.times_done = {(t, p) : 0 for t in tasks for p in people}
		self.weeks_since_done = {(t, p) : 1e9 for t in tasks for p in people}

	def score(self, task: Task, person: Person) -> float:
		td = self.times_done[task, person]
		wsd = self.weeks_since_done[task, person]
		return td + 10 / wsd
	
	def update(self, assignments: list[tuple[Task, Person]]):
		"""
		Inrements total task counters and resets weeks since done for assigned people, updates WSD for the rest
		"""
		for task_person in self.weeks_since_done:
			self.weeks_since_done[task_person] += 1

		for task, people in assignments:
			for person in people:
				self.times_done[task, person] += task.weight
				self.weeks_since_done[task, person] = 1

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
