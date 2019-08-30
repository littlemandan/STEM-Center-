"""STEM Center Project by Dan Lee
"""

import math
current_units = 0
UNITS = {
    0: ("Celsius", "C"),
    1: ("Fahrenheit", "F"),
    2: ("Kelvin", "K"),
    }

DAYS = {
    0 : "SUN",
    1 : "MON",
    2 : "TUE",
    3 : "WED",
    4 : "THU",
    5 : "FRI",
    6 : "SAT"
}

HOURS = {
    0 : "Mid-1AM  ",
    1 : "1AM-2AM  ",
    2 : "2AM-3AM  ",
    3 : "3AM-4AM  ",
    4 : "4AM-5AM  ",
    5 : "5AM-6AM  ",
    6 : "6AM-7AM  ",
    7 : "7AM-8AM  ",
    8 : "8AM-9AM  ",
    9 : "9AM-10AM ",
    10 : "10AM-11AM",
    11 : "11AM-NOON",
    12 : "NOON-1PM ",
    13 : "1PM-2PM  ",
    14 : "2PM-3PM  ",
    15 : "3PM-4PM  ",
    16 : "4PM-5PM  ",
    17 : "5PM-6PM  ",
    18 : "6PM-7PM  ",
    19 : "7PM-8PM  ",
    20 : "8PM-9PM  ",
    21 : "9PM-10PM ",
    22 : "10PM-11PM",
    23 : "11PM-MID ",
}

def print_header():
    """Print a header"""
    print("STEM Center Temperature Project")
    print("Dan Lee")


def recursive_sort(list_to_sort, key=0):
    """Sort a list of 3-tuples"""
    length = len(list_to_sort)
    new_list = list_to_sort.copy()
    for i in range(length - 1):
        if new_list[i][key] > new_list[i + 1][key]:
            (new_list[i + 1], new_list[i]) = \
                (new_list[i], new_list[i + 1])
    save = [new_list[-1]]
    if length == 1:
        return save
    ret_value = recursive_sort(new_list[:length - 1], key) + save
    return ret_value


def main():
    current_set = TempDataset()
    stem_center = ("4213", "STEM Center", 0)
    foundations_lab = ("4201", "Foundations Lab", 1)
    cs_lab = ("4204", "CS Lab", 2)
    workshop_room = ("4218", "Workshop Room", 3)
    tiled_room = ("4205", "Tiled Room", 4)
    outside = ("Out", "Outside", 10)
    sensor_list = [stem_center,
                   foundations_lab,
                   cs_lab,
                   workshop_room,
                   tiled_room,
                   outside]
    active_sensors = [sensor_list[i][2] for i in range(len(sensor_list))]
    print_header()
    sensor_list = recursive_sort(sensor_list, 0)
    menu_selection = 0
    while (True):
        print_menu()
        try:
            menu_selection = int(input("\nWhat is your choice? "))
        except ValueError:
            print("Hey Goofy, that's not a valid choice!")
            continue
        if (menu_selection == 1):
            new_file(current_set)
        elif (menu_selection == 2):
            choose_units()
        elif (menu_selection == 3):
            change_filter(sensor_list, active_sensors)
        elif (menu_selection == 4):
            print_summary_statistics(current_set, active_sensors)
        elif (menu_selection == 5):
            print_temp_by_day_time(current_set, active_sensors)
        elif (menu_selection == 6):
            print_histogram(current_set, current_set)
        elif (menu_selection == 7):
            print("Thanks for using the STEM Temperature Project!")
            break
        else:
            print("Hey Goofy, that's not an option!")


def convert_units(celsius_value, units):
    """Convert Celsius value to Fahrenheit and Kelvin"""
    if units == 0:
        return celsius_value
    if units == 1:
        return celsius_value * 1.8 + 32
    return celsius_value + 273.15


def print_menu():
    """Print menu for user"""
    print("Main Menu\n ---------\n"
          "1 - Process a new data file\n"
          "2 - Choose units\n"
          "3 - Edit room filter\n"
          "4 - Show summary statistics\n"
          "5 - Show temperature by date and time\n"
          "6 - Show histogram of temperatures\n"
          "7 - Quit\n")


def new_file(dataset):
    """Load data file"""
    file_name = input("What is the file name? ")
    if dataset.process_file(file_name) == False:
        print("We can't load that!")
        return None
    print(f"Loaded {dataset.get_loaded_temps()} samples")
    valid = False
    while (not valid):
        set_name = input("Please input a 3 to 20 char name for the dataset ")
        try:
            dataset.name = set_name
            valid = True
        except ValueError:
            print("wat r u doin?? try again")


def choose_units():
    """Change units of temperature"""
    global current_units
    print(f"Current units are {UNITS[current_units][0]}")
    key = UNITS.keys()
    while (True):
        for item in key:
            print(f"{item} - {UNITS[item][0]}")
        try:
            unit_selection = int(input("Which unit?\n"))
            if unit_selection in UNITS:
                current_units = unit_selection
                break
            else:
                print("enter a valid selection")
        except ValueError:
            print("thats not even an int")


def change_filter(sensor_list, active_sensors):
    """Create dictionary of room numbers for reference"""
    sensors = {sensor[0]: sensor[2] for sensor in sensor_list}
    while True:
        print()
        print_filter(sensor_list, active_sensors)
        print()
        print(f"Type the sensor to toggle (e.g. {sensor_list[0][0]})"
              f" or x to end", end=' ')
        choice = input()
        if choice == "x":
            break
        if choice in sensors:
            if sensors[choice] in active_sensors:
                active_sensors.remove(sensors[choice])
            else:
                active_sensors.append(sensors[choice])
        else:
            print("Invalid Sensor")


def print_summary_statistics(dataset, active_sensors):
    """Print summary statistics"""
    try:
        mini = dataset.get_summary_statistics(active_sensors)[0]
        avg = dataset.get_summary_statistics(active_sensors)[1]
        maxi = dataset.get_summary_statistics(active_sensors)[2]
    except TypeError:
        print("please load some data and/or activate a sensor")
        return
    print("Summary for " + dataset.name)
    print(f"Minimum: "
          f"{convert_units(mini, current_units):5.2f} "
          f"{UNITS[current_units][0]}")
    print(f"Average: "
          f"{convert_units(avg, current_units):5.2f} "
          f"{UNITS[current_units][0]}")
    print(f"Maximum: "
          f"{convert_units(maxi, current_units):5.2f} "
          f"{UNITS[current_units][0]}")


def print_temp_by_day_time(dataset, active_sensors):
    """Print table of average temp by day/time"""
    print("Print Temp by Day/Time Function Called")
    if dataset.get_loaded_temps() == None:
        print("There's no data loaded!")
        return
    else:
        name = dataset.name
        print(f"Average Temperatures for {name}")
        print(f"Units are in {UNITS[current_units][0]}")

        for i in range(len(HOURS)):
            if i == 0:
                print("            ", end="")
                for k in range(len(DAYS)):
                    print(f"{DAYS[k]}", end="    ")
                print("")
            else:
                print(f"{HOURS[i]}   ", end="")
                for j in range(len(DAYS)):
                    avg = dataset.get_avg_temperature_day_time(active_sensors,
                                                               j, i)
                    converted_avg = convert_units(avg, current_units)
                    print(f"{converted_avg:.1f}", end="   ")
                print("")


def print_histogram(dataset, active_sensors):
    print("Print Histogram Function Called")


def print_filter(sensor_list, active_sensors):
    """Print sorted list of filters"""
    for i in range(len(sensor_list)):
        if sensor_list[i][2] in active_sensors:
            print(f"{sensor_list[i][0]}: {sensor_list[i][1]} [ACTIVE]")
        else:
            print(f"{sensor_list[i][0]}: {sensor_list[i][1]}")


class TempDataset:
    """Hold and perform operations on temperature data"""
    MAX_NAME = 20
    MIN_NAME = 3
    objects = 0

    def __init__(self):
        self._data_set = None
        self._name = "Unnamed"
        TempDataset.objects += 1

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if not (TempDataset.MIN_NAME <= len(new_name) <= TempDataset.MAX_NAME):
            raise ValueError
        self._name = new_name

    def process_file(self, filename):
        """ load temperature data from a file """
        try:
            datafile = open(filename, 'r')
        except IOError:
            return False
        self._data_set = []
        for line in datafile:
            day, time, sensor, readtype, temp = line.split(",")
            time = math.floor(float(time) * 24)
            if readtype == "TEMP":
                self._data_set.append((int(day), time,
                                      int(sensor), float(temp)))
        datafile.close()
        return True

    def get_summary_statistics(self, active_sensors):
        if self._data_set == None:
            return None
        else:
            check = [i[3] for i in self._data_set if i[2] in active_sensors]
            if len(check) == 0:
                return None
            minimum = min(check)
            maximum = max(check)
            samples = len(check)
            average = sum(check) / samples
            return (minimum, average, maximum)

    def get_avg_temperature_day_time(self, active_sensors, day, time):
        if self._data_set == None:
            return None
        else:
            check = [i[3] for i in self._data_set if
                     day in i
                     and time in i
                     and i[2] in active_sensors
                     ]
            if len(check) == 0:
                return None
            samples = len(check)
            average = sum(check)/samples
            return average

    def get_num_temps(self, active_sensors, lower_bound, upper_bound):
        if self._data_set == None:
            return None
        else:
            return 0

    def get_loaded_temps(self):
        if self._data_set == None:
            return None
        else:
            samples = len(self._data_set)
            return samples

    @classmethod
    def get_num_objects(cls):
        """returns total number of objects created"""
        return TempDataset.objects


if __name__ == "__main__":
    main()
