import pickle
from datetime import date, timedelta
import matplotlib.pyplot as plt


def datetify(date_str):
    if "-" in date_str:
        split_date = date_str.split("-")
        if split_date[0] == "nan":
            result = "nan"
        else:
            result = date(int(split_date[0]), int(split_date[1]), int(split_date[2]))
    elif "/" in date_str:
        split_date = date_str.split("/")
        if split_date[0] == "nan":
            result = "nan"
        else:
            result = date(int(split_date[0]), int(split_date[1]), int(split_date[2]))
    else:
        print("Other delimiter in date")
        print(date_str)
        result = "nan"

    return result


def iso_year_start(iso_year):
    # The Gregorian calendar date of the first day of the given ISO year
    fourth_jan = date(iso_year, 1, 4)
    delta = timedelta(fourth_jan.isoweekday()-1)
    return fourth_jan - delta


def iso_to_gregorian(iso_year, iso_week, iso_day):
    # The Gregorian calendar date for the given ISO year, week and day
    year_start = iso_year_start(iso_year)
    return year_start + timedelta(days=iso_day-1, weeks=iso_week-1)


def save_pickle(path, data_structure):
    save_ds = open(path, "wb")
    pickle.dump(data_structure, save_ds)
    save_ds.close()


def load_pickle(path):
    load_ds = open(path, "rb")
    data_structure = pickle.load(load_ds)
    load_ds.close()
    return data_structure


def plot_time_series(time_series_list, time_series_names,
                     time_series_colors, key_name, save_path, window_size=5):
    figure, ax_plots = plt.subplots(len(time_series_list), 1)
    figure.set_size_inches(9, 7)

    figure.suptitle(key_name + " \nWindow size: " + str(window_size))

    dimensions_str = str(len(time_series_list)) + "1" + "1"
    dimensions_int = int(dimensions_str)

    for idx, t_s in enumerate(time_series_list):
        plt.subplot(dimensions_int)
        plt.plot(t_s, 'b-', color=time_series_colors[idx], lw=2)
        plt.title(time_series_names[idx])
        dimensions_int += 1

    plt.subplots_adjust(left=0.2, wspace=0.8, top=0.8)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    plt.savefig(save_path, bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    for i in range(1, 51):
        c_date = iso_to_gregorian(2016, i, 1)
        print(str(c_date.year) + " " + str(c_date.month) + " " + str(c_date.day))
