import numpy as np
import pandas as pd
from datetime import date

### Settings
all_persons = [
    101, 102, 103, 104, 105, 106, 107, 211, 212, 213, 214, 215, 216, 217
]
persons_no_task = [0, 0, 0, 0, 0]

nr_of_tasks = 10
nr_of_weeks_new = 54

nr_of_monthly_tasks = 4
hallways = 5  #task number of hallways

### Determine other settings
nr_of_people = len(all_persons)
nr_of_weekly_tasks = nr_of_tasks - nr_of_monthly_tasks
nr_no_task = len(persons_no_task)

persons_no_task_nonzero_ind = []
for n in range(0, len(persons_no_task)):
    if persons_no_task[n] != 0:
        if persons_no_task[n] not in all_persons:
            print('Error: persons_no_task person is not in all_persons')
        else:
            persons_no_task_nonzero_ind = persons_no_task_nonzero_ind + [
                all_persons.index(persons_no_task[n])
            ]

#%% Preallocate memory

total_task_counter = np.zeros((nr_of_people, ), dtype=float)
task_counters = np.zeros((nr_of_people, nr_of_tasks), dtype=float)
#Example of task_counters table:
#           Task 1    Task 2     Task 3
#Person 1      x        x          x
#Person 2      x        x          x

tasks = np.full((nr_of_weeks_new, nr_of_tasks), -1, dtype=int)
#Example of tasks table:
#           Task 1    Task 2    Task 3
#Week 1        x        x         x
#Week 2        x        x         x

current_week_counter = np.zeros((nr_of_people, ), dtype=float)
last_week_counter = np.zeros((nr_of_people, ), dtype=int)
last_2week_counter = np.zeros((nr_of_people, ), dtype=int)

old_noclean_weeks = np.zeros(
    (nr_of_people, 1),
    dtype=int)  #amount of weeks that each person did not clean

datevector = np.zeros((nr_of_weeks_new, 1), dtype=int)  #vector for new dates
datevector_str = []  #vector for new dates
first_of_month = np.zeros((nr_of_weeks_new, 1),
                          dtype=int)  #bool if this week of the month

#%% Read old list

file_read = pd.read_csv('task_in.csv', delimiter=';')  #table
oldlist_export = np.array(file_read)[:, 0:nr_of_tasks + nr_no_task + 1]
oldlist = oldlist_export[:, 1::].astype(int)  #part without dates

#convert to hours from December , 1899 (Excel default) to January 0, 0000
excel_date = date(1899, 12, 30).toordinal()  #Start date of Excel numbering
startdate = oldlist_export[-1, 0] + excel_date
print('date = ' + str(date.fromordinal(startdate)))
startdate = startdate + 7  # start first new week

### Set current_week_couter to last old week
last_persons = oldlist[-1, 0:nr_of_tasks]
for current_task in range(0, nr_of_tasks):
    # find person that did the current task
    roomnr_oldtask = last_persons[current_task]
    if roomnr_oldtask != 0 and roomnr_oldtask != -1:
        # Find index of person
        pers_ind = all_persons.index(roomnr_oldtask)
        if current_task == hallways:
            current_week_counter[pers_ind] = 0.5
        else:
            current_week_counter[pers_ind] = 1

### load roomnr_oldtask into task_counters per week
for current_week in range(0, len(oldlist[:, 0])):
    for current_task in range(0, nr_of_tasks):
        # find person that did the current task
        roomnr_oldtask = oldlist[current_week, current_task]
        if roomnr_oldtask != 0 and roomnr_oldtask != -1:
            # Find index of person
            pers_ind = all_persons.index(roomnr_oldtask)
            task_counters[pers_ind,
                          current_task] = task_counters[pers_ind,
                                                        current_task] + 1.0

### load room nr of persons that do not have to clean in old_noclean_weeks ...
for current_person_nr in range(0, nr_no_task):
    for current_week in range(0, len(oldlist[:, 0])):
        roomnr_oldtask = oldlist[current_week, nr_of_tasks + current_person_nr]
        if roomnr_oldtask != 0 and roomnr_oldtask != -1:
            pers_ind = all_persons.index(roomnr_oldtask)
            old_noclean_weeks[pers_ind] = old_noclean_weeks[pers_ind] + 1

### ... and give them compensation points
nr_of_weeks_old = len(oldlist[:, 0])
avg_chance_per_task = np.ones((nr_of_tasks, ), dtype=float)
nr_of_weekly_tasks_done_old = np.sum(task_counters[:, 0])
weekly_chance_old = nr_of_weekly_tasks_done_old / (
    nr_of_people * nr_of_weeks_old - np.sum(old_noclean_weeks))
#chance of getting a weekly task
avg_chance_per_task[0:nr_of_weekly_tasks] = weekly_chance_old
nr_of_monthly_tasks_done_old = np.sum(task_counters[:, nr_of_tasks - 1])
monthly_chance_old = nr_of_monthly_tasks_done_old / (
    nr_of_people * nr_of_weeks_old - np.sum(old_noclean_weeks))
#chance of getting a monthly task
avg_chance_per_task[nr_of_weekly_tasks:nr_of_tasks] = monthly_chance_old
old_noclean_tasks = old_noclean_weeks * avg_chance_per_task

task_counters = task_counters + old_noclean_tasks  #sum all points
total_task_counter_old = np.sum(task_counters, 1)
print('total_task_counter_before= ' + str(total_task_counter_old))

#%% Start calculation

### Fill datevector and find first mondays of the month
t = startdate
for current_week in range(0, nr_of_weeks_new):
    datevector[current_week, :] = t
    datevector_str = datevector_str + [
        date.fromordinal(t).strftime("%d-%m-%Y")
    ]
    first_monday_of_month = date.fromordinal(t).day
    if first_monday_of_month <= 7:
        first_of_month[current_week] = 1
    t = t + 7  #add a week

### Use task_counters to build the tasks table
for current_week in range(0, nr_of_weeks_new):
    last_2week_counter = last_week_counter
    last_week_counter = current_week_counter
    current_week_counter = np.zeros((nr_of_people, ), dtype=float)
    for current_task in range(0, nr_of_tasks):
        # check if it is hallways because this is the least work so easiest
        # to do as task two weeks in a row

        # determine if the task has to be done (weekly task or first monday of the month)
        if (current_task < nr_of_tasks - nr_of_monthly_tasks) or (
                first_of_month[current_week] == 1):

            total_task_counter = np.sum(task_counters, 1)

            #choose person based on their cleaning score
            current_task_counter = np.round(task_counters[:, current_task])
            total_task_counter2 = np.round(total_task_counter)
            cleaning_score = 18 * current_week_counter + 8 * last_week_counter + 2 * last_2week_counter + 2 * current_task_counter + total_task_counter2

            # give people not doing task infinite cleaning score
            for n in range(0, len(persons_no_task)):
                if persons_no_task[n] != 0:
                    cleaning_score[all_persons.index(
                        persons_no_task[n])] = np.inf

            # find possibilities
            lowest_counter = np.min(cleaning_score)
            lowest_ind = np.arange(0, nr_of_people)[
                cleaning_score == lowest_counter]  #lowest indices
            #round cleaning scores because of decimals
            random_of_lowest = np.random.randint(
                0, len(lowest_ind))  #choose random person
            lowest_person = lowest_ind[random_of_lowest]

            task_counters[lowest_person,
                          current_task] = task_counters[lowest_person,
                                                        current_task] + 1
            current_week_counter[
                lowest_person] = current_week_counter[lowest_person] + 1
            if current_task == hallways:
                task_counters[lowest_person,
                              current_task] = task_counters[lowest_person,
                                                            current_task] - 0.5
                current_week_counter[
                    lowest_person] = current_week_counter[lowest_person] - 0.5

            tasks[current_week, current_task] = lowest_person

### update total task counters for people not doing task
total_task_counter = np.sum(task_counters, 1)
total_task_counter_diff = np.sum(total_task_counter) - np.sum(
    total_task_counter_old)
tasks_per_pers = total_task_counter_diff / (nr_of_people -
                                            len(persons_no_task_nonzero_ind))
total_task_counter[persons_no_task_nonzero_ind] = total_task_counter[
    persons_no_task_nonzero_ind] + tasks_per_pers
print('total_task_counter =' + str(total_task_counter))

# print std deviation
std_deviation = np.std(total_task_counter)
print('std = ' + str(std_deviation))

# convert count of persons back to room numbers
for current_person in range(0, len(all_persons)):
    tasks[tasks == current_person] = all_persons[current_person]

#make table with dates, tasks and persons that do not have a task
newlist = np.zeros((nr_of_weeks_new, nr_of_tasks + nr_no_task + 1), dtype=int)
newlist[:, 0] = datevector[:, 0] - excel_date
newlist[:, 1:nr_of_tasks + 1] = tasks
newlist[:, nr_of_tasks + 1:nr_of_tasks + 1 + nr_no_task] = np.ones(
    (nr_of_weeks_new, 1), dtype=int) * persons_no_task

colnames = [
    'Date', 'Living', 'room', 'Toilets', 'Bathroom', 'Showers', 'Hallways',
    'Kit', 'ch', 'en', 'Laundry', 'Notask1', 'Notask2', 'Notask3', 'Notask4',
    'Notask5'
]
outtable = pd.DataFrame(
    newlist,  # values
    index=newlist[:, 0],  # 1st column as index
    columns=colnames)  # 1st row as the column names

vector_str = pd.DataFrame({'Day': datevector_str})
outtablee = outtable.join(vector_str)

outtable.jo

#outtable.to_csv('out.csv', sep =';',index=False)

outtable2 = file_read.append(outtable, ignore_index=True)
outtable2.to_csv('out2.csv', sep=';', index=False)

# %%
