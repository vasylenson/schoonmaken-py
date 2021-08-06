from collections import defaultdict, namedtuple
from datetime import date, timedelta
from random import choice

from schoonmaken.common import Counters, Person, Task


def score(task, person):
    return counters.score(task, person)


def choose_people(task: Task, people: set[Person]) -> set[Person]:
    scores = [(score(task, person), person) for person in people]
    scores.sort(key=lambda pair: pair[0])
    chosen = scores[:task.numpeople]
    return set([person for score, person in chosen])


def fill_week(tasks: set[Task], people: set[Person]):
    assignments = {}  # Map: Task -> [Person]
    for task in tasks:
        c = choose_people(task, people)
        assignments[task] = c
        people = people - c
    counters.update(assignments.items())
    return assignments


def fill_schedule(weeks, people, tasks):
    # TODO: eliminate global state
    global counters
    counters = Counters(tasks=tasks, people=people)

    get_people = lambda week: {
        person
        for person in people if person.available(week)
    }
    get_tasks = lambda week: (task for task in tasks if task.due(week))
    return ((week, fill_week(get_tasks(week), get_people(week)))
            for week in weeks)
