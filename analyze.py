import os
import json
from collections import OrderedDict
from member import Member
from datetime import date, datetime
from dateutil.rrule import rrule, MONTHLY

c_file = None
messages_sent = 0
chat_name = None
date_created = None
members = OrderedDict()
chat_log = OrderedDict()
data = {}
current_member_count = 0


# makes a file given the file name
def make_file(file_name, analyze=False):
    filename = "static/files/" + file_name
    global c_file
    c_file = open(filename, 'r')
    if analyze:
        analyze()


# goes through file line by line and employs various other helper analysis functions
def analyze():
    reset()
    global messages_sent
    global chat_name
    global date_created
    global chat_log

    # goes through file
    saved_pos = c_file.tell()
    first_line = c_file.readline()
    date_created = parse_date(first_line)
    c_file.seek(saved_pos)

    # setup the log dictionary before hand in order to have access to dates before hand
    chat_log = setup_log()

    for line in c_file:
        chat_etc = find_chat_name(line)
        if is_message(line) and not chat_etc:
            messages_sent += 1
            find_new_members(line)
            log(line)
        else:
            member_active_status(line)


# determines if the line is a message or not
def is_message(line):
    return line[0:1] == "[" and line.count(":") >= 3


# obtains the chat name if found in a line
def find_chat_name(line):
    global chat_name
    if ": ‎Messages to this group are now secured with end-to-end encryption." in line:
        chat_name = line[line.find("M] ")+3:line.find(": ")]
        return True
    return False


# setups dictionaries with all dates beforehand
# the initial date will be the first date recorded in the chat transcript
# the last date would be the current present day
# this will setup all days that fall between the 1st and 15th of each month between the above 2 dates
# by doing this, the ambuguity of how many messages and their dates can be avoided by having preset dates each
# message date can be bracketed into
def setup_log():
    global chat_log
    global date_created

    log = OrderedDict()
    c_date = date.today()
    initial_date = bracket_date(date_created)

    # this creates a list of all the dates in between
    dates = list(rrule(MONTHLY, bymonthday=(1, 15),
                       dtstart=initial_date, until=c_date))
    log[date_created] = 0
    for d in dates:
        log[d.date()] = 0
    log[c_date] = 0

    return log


# brackets date into which key it should be logged into
# the bracketed date would either be 1st of the next month or 15th of the current month
def bracket_date(b_date):
    return_date = None
    if b_date.day < 15:
        return_date = date(b_date.year, b_date.month, 15)
    else:
        new_year = b_date.year
        new_month = b_date.month + 1
        # note: in datetime.date, months go from 1 to 12
        if new_month > 12:
            new_year += 1
            new_month -= 12
        return_date = date(new_year, new_month, 1)

    if date.today() < return_date:
        return date.today()
    return return_date


# logs a message into the dictionary, the global dictionary will be updated
def log(line):
    global chat_log
    global members

    # obtain the name and the date of the message
    name = parse_name(line)
    l_date = parse_date(line)
    log_keys = list(chat_log.keys())
    logging_date = None

    # add entries for the first date point
    if l_date < log_keys[1]:
        chat_log[log_keys[0]] += 1
        members[name].chat_log[log_keys[0]] += 1
    else:
        # get the entered date and bracket to see where it would fall in the log
        logging_date = bracket_date(l_date)
        chat_log[logging_date] += 1
        members[name].chat_log[logging_date] += 1


# --MEMBER METHODS--
# The following methods relate to members within a chat

# parses the line to see if there is a new member
# if member already accounted for, update the message_sent
def find_new_members(line):
    global members
    global current_member_count

    name = parse_name(line)
    date = parse_date(line)
    new_member = Member(name, date)

    if name in members.keys():
        members[name].messages_sent += 1
    else:
        # member not found, add new one
        members[name] = new_member
        members[name].chat_log = setup_log()
        current_member_count += 1


# checks whether member was removed or has left or added
def member_active_status(line):
    global members
    global current_member_count

    gone = 0
    name = parse_name(line)
    if line[0:1] == "[":
        if "removed" in line:
            gone = 1
        elif "left" in line:
            gone = 2

    # update active status
    if name in members.keys():
        if gone == 1:
            members[name].times_removed += 1
            members[name].active = False
            current_member_count -= 1
        elif gone == 2:
            members[name].times_left += 1
            members[name].active = False
            current_member_count -= 1
        else:
            members[name].times_added += 1
            members[name].active = True
            current_member_count += 1


# --PARSING METHODS--
# parses the date out of a line
def parse_date(line):
    date = line[line.find("[")+1:line.find(",")].replace("/", " ")
    format = '%m %d %y'
    return datetime.strptime(date, format).date()

# parses the name out of a line


def parse_name(line):
    if is_message(line):
        return line[line.find("M] ")+3:line.find(": ")]
    elif line[0:1] == "[":
        if "removed" in line:
            return line[line.find("removed")+8:len(line)-1]
        elif "left" in line:
            return line[line.find("M] ")+4:line.find("left")-1]
        elif "added" in line:
            return line[line.find("added")+6:len(line)-1]
    return ""


# resets all variables
def reset():
    global members
    global messages_sent
    global current_member_count
    global chat_name
    global chat_log
    global date_created
    global data
    data.clear()
    members.clear()
    chat_log.clear()
    messages_sent = 0
    current_member_count = 0
    chat_name = None
    date_created = None


# --GETTER METHODS--

# getter method for the chat name
def get_chat_name():
    return chat_name


# getter method for number of messages sent
def get_message_sent():
    return messages_sent


# getter method for the names of members
def get_members():
    names = ""
    for member in members:
        names += (members[member].to_string() + "\n\n")
    return names


# gets by_monthly log
def get_chat_log():
    count = 0
    for d, m in chat_log.items():
        print(d, m)
        count += m
    print(count)


# gets member logs
def get_member_logs():
    for name in members:
        print(name)
        count = 0
        for d, m in members[name].chat_log.items():
            print(d, m)
            count += m
        print(count)
        print()
        print()


# compiles all found data into a dictionary
def compile_data():
    global members
    global chat_log
    global chat_name
    global messages_sent
    global current_member_count
    global date_created
    global data

    data = {
        "chatName": chat_name,
        "messagesSent": messages_sent,
        "dateCreated": date_created.strftime('%m/%d/%y'),
        "currentMemberCount": current_member_count,
        "members": [],
        "chatLog": [],
        # "chatLogDates": list(chat_log.keys()),
        # "chatLogData": list(chat_log.values())
    }

    # setup member information in dict
    for member in members:
        new_entry = {
            "name": members[member].name,
            "dateAdded": members[member].date_added.strftime('%m/%d/%y'),
            "messagesSent": members[member].messages_sent,
            "timesAdded": members[member].times_added,
            "timesLeft": members[member].times_left,
            "timesRemoved": members[member].times_removed,
            "activeStatus": members[member].active,
            "memberChatLog": [],
            # "chatLogDates": list(members[member].chat_log.keys()),
            # "chatLogData": list(members[member].chat_log.values())
        }

        # enter in chat logs for each member
        for d, m in members[member].chat_log.items():
            new_log_entry = {
                "date": d.strftime('%m/%d/%y'),
                "amount": m
            }
            new_entry["memberChatLog"].append(new_log_entry)

        data["members"].append(new_entry)

    # enter in chat log
    for d, m in chat_log.items():
        new_entry = {
            "date": d.strftime('%m/%d/%y'),
            "amount": m
        }
        data["chatLog"].append(new_entry)

    return data


# converts all obtained data into a json file
def to_json(create_file=False):
    global data

    json_data = json.dumps(data)

    if create_file:
        with open('data.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)

    return json_data


def main():
    name = input("Enter file name: ")
    make_file(name)
    analyze()
    print(get_chat_name())
    print(get_message_sent())
    print(get_members())
    print()
    print()
    # get_member_logs()
    print()
    print()
    get_chat_log()

    # to_json()


if __name__ == "__main__":
    main()
