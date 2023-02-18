# This is a sample Python script.
import re


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    print('ascascsaca')


def set_severity(msg):
    print("severity: " + msg)


def get_yesterday_incidents(msg):
    print("INSIDE the get_yesterday_incidents()")
    print(msg)


def convert_msg_to_action(msg):
    if "get yesterday incidents" in msg:
        print("get incident method")
        # fpApiClient.get_yesterday_incidents()
    elif "set severity" in msg:
        print("in severity")
        # set_severity(msg)
    elif "another bla" in msg:
        print("bla bla bla")


def aaa():
    my_string = 'The "quick brown" fox jumps over the "lazy dog".'
    result_dict = {}
    # Use regular expression to find words within quotes
    pattern = r'"([^"]+)"'
    matches = re.findall(pattern, my_string)

    for i, match in enumerate(matches):
        key = f"val_{i + 1}"
        result_dict[key] = match

    # Print the dictionary
    print(result_dict)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    aaa()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
