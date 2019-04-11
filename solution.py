# parse the real time tsv into a dict
def open_real_time():
    # only add needed columns
    needed_columns = ['FlightId', 'InGateUtcChange', 'InGateUtc']
    real_time_dict = {}
    columns = True
    with open('realtime.txt') as real_time_txt:
        # build the dicitonary
        for line in real_time_txt:
            # if we are at the first line of values, these are column titles
            if (columns):
                # make a list of column headings for the dictionary
                col_names = tuple(line.split())
                columns = False
            # next we get to values
            else:
                # split on tab to get empy values out for flight info
                flight_info = tuple(line.split('\t'))
                # set the flight id as the key of inner dict for quick look ups
                real_time_dict[flight_info[0]] = {}
                # for each column heading, add as a key to dict with value being the approp. flight_info data point
                for index, col in enumerate(col_names):
                    # only if the col is in our needed list
                    if col in needed_columns:
                        real_time_dict[flight_info[0]][col] = flight_info[index]
    return real_time_dict

# build dict from notifications csv
def open_notification_log():
    notifications_dict = {}
    columns = True
    with open('notifications.csv') as notifications:
        # build the dctionary
        for line in notifications:
            # catch the column headings
            if (columns):
                # split on commas
                col_names = line.split(',')
                # extract the \n chars
                col_names[-1] = col_names[-1].strip()
                columns = False
            # move on to data
            else: 
                # split on commas and remove \n chars
                notifications_data = line.split(',')
                notifications_data[-1] = notifications_data[-1].strip()
                # set the flight id as the key of inner dict for quick look ups
                notifications_dict[notifications_data[0]] = {}
                # for each heading, add as a key then assign the approp. value from notifications_data
                for index, col in enumerate(col_names):
                    notifications_dict[notifications_data[0]][col] = notifications_data[index]
    return notifications_dict

# function to issue notificaitons if they are needed
def issue_notifications_if_needed(notifications_log, real_time_data, current_time):
    # notification flag
    send_notification = False
    # iterate the real_time_data and check if there has been a change
    for key in real_time_data:
        # if a change is present, via 'Y' check notification status
        if real_time_data[key]['InGateUtcChange'] == 'Y':
            # determine if the flight is delyed or cancelled
            arrival_time = real_time_data[key]['InGateUtc'] if not real_time_data[key]['InGateUtc'] == "" else 'CANCELLED'
            # if this notificaiton has been sent before, check to see if we need to send again
            if key in notifications_log:
                # check time with helper function
                if check_time(current_time, notifications_log[key]['SentTimestampUtc']):
                    # update flag
                    send_notification = True
            # if no notificaiton has been sent before, send one and add to the logs
            else: 
                # update flag
                send_notification = True
                # add to log, should write this to the csv
                notifications_log[key] = {
                    'FlightId': key,
                    'InGateUtc': arrival_time,
                    'SentTimestampUtc': current_time 
                }
            if (send_notification):
                # send notification
                if arrival_time == 'CANCELLED':
                    print("Flight {num} is now {time}".format(num=key, time=arrival_time))
                else:
                    print("Flight {num} is now scheduled to arrive at {time}".format(num=key, time=arrival_time))
                # reset notification flag
                send_notification = False

# helper function for checking time
def check_time(current, last):
    #check hour
    if (int(current[11:13]) != int(last[8:10])):
        # if hours dont match check minutes
        if ((60 - ((60 - int(current[14:])) - (60 - int(last[11:])))) > 30):
            return True
    # if hours are equal
    elif (int(current[11:13]) == int(last[8:10])):
        # check minutes
        if ((int(current[14:]) - int(last[11:])) > 30):
            return True
    return False


# get the prior notification data
notifications_data = open_notification_log()
# get the real time updates
real_time_data = open_real_time()
# set the current time
curr_time = '2017-04-13 20:28'
# using the prior notificaitons, the real time updates, and the current time...
# check to see if any notificaitons need to be sent!
issue_notifications_if_needed(notifications_data, real_time_data, curr_time)

