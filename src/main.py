from datetime import date

from schoonmaken.serializer import build_table, csv, html
from schoonmaken.config import STYLE
from schoonmaken.common import Person, Task, weeks
import schoonmaken.scheduler as schoonmaken

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

weeks = weeks(date.today(), date(2022, 12, 30))
schedule = schoonmaken.fill_schedule(weeks, people, tasks)
# print(list(schedule))
# print(len(list(schedule)))

table = build_table(schedule, tasks)

with open('out/task.html', 'w') as output:
    output.write(html(table) + STYLE)

with open('out/task.csv', 'w') as output:
    output.write(csv(table))
