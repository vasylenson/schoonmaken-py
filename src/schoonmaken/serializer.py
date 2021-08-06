import pandas as pd

from schoonmaken.common import Person, Task


def save_data(people, save_path):
    pass


def retrieve_data(data_path) -> list[tuple]:
    '''
    Layout of data:
        [
            (person_name: str, [TaskData, ...]),
            ...
        ]
    '''
    td = []
    return td


def retrieve_person_data(person_name: str, data_path: str):
    td = []
    return


def csv(task_table: list[list]):
    dataframe = pd.DataFrame(task_table)
    return dataframe.to_csv(header=False, index=False)


def html(task_table: list[list]):
    dataframe = pd.DataFrame(task_table)
    return dataframe.to_html(header=False, index=False, border=1)


def build_table(schedule, tasks, header=True):
    def names(assignments: dict[Task, Person]):
        def person_or_none(task: Task) -> str:
            if task in assignments:
                return ', '.join(person.name for person in assignments[task])
            else:
                return ''

        return [person_or_none(task) for task in tasks]

    table = [['Week'] + [task.name for task in tasks]] if header else []
    table += [[week.strftime('%d-%m-%y')] + names(tasks)
              for week, tasks in schedule]
    return table
