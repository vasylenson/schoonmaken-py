import schoonmaken
from datetime import date

weeks = schoonmaken.weeks(date.today(), date(2021, 12, 30))
schedule = schoonmaken.fill_schedule(weeks)
print(list(schedule))



