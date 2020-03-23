import json
import os
from datetime import datetime
from time import sleep


DAYS_WEEK = {
    0: "monday",
    1: "tuesday",
    2: "wednesday",
    3: "thursday",
    4: "friday",
    5: "saturday",
    6: "sunday"
}


def time_to_int(t_hour, t_minute):
    return int(t_hour)*60 + int(t_minute)


def get_weekday(t_datetime=None):
    return DAYS_WEEK[datetime.weekday(datetime.now() if t_datetime == None else t_datetime)]


def get_hour_from_str(t_time_str):
    hour = str()
    for c in t_time_str:
        if c != ':':
            hour += c
        else:
            break
    return int(hour)


def get_minute_from_str(t_time_str):
    div_pos = t_time_str.find(':')
    return int(str(t_time_str[div_pos + 1] + t_time_str[div_pos + 2]))


def is_it_time(t_start, t_finish, t_datetime=datetime.now()):
    now_int = time_to_int(t_datetime.hour, t_datetime.minute)
    start_int = time_to_int(get_hour_from_str(
        t_start), get_minute_from_str(t_start))
    finish_int = time_to_int(get_hour_from_str(
        t_finish), get_minute_from_str(t_finish))

    return now_int >= start_int and now_int <= finish_int


def main():
    DELAY_SECONDS = 1.2
    data = dict()
    with open("courses.json") as f:
        data = json.load(f)

    now = datetime.now()

    weekday = get_weekday(now)

    for course_name, course in data["courses"].items():
        for dow, time_range in course["sessions"].items():
            if dow == weekday:
                is_time = is_it_time(
                    time_range["start"], time_range["finish"], t_datetime=now)
                if is_time:
                    print("Joining your class {}.".format(course_name))
                    print("Start:\t{}\nFinish:\t{}".format(
                        time_range["start"], time_range["finish"]))
                    if DELAY_SECONDS > 0:
                        sleep(DELAY_SECONDS)
                    cmd = "start {}".format(course["url"])
                    os.system(cmd)
                    return
    print("You do not have class right now.")
    input("Press Enter to exit.")


if __name__ == "__main__":
    main()
