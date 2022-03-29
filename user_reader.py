#!/usr/bin/python
import csv

class UserReader():
    def __init__(self, input = "users"):
        self.inputFile = input

    def get_users(self):
        users = []
        with open(self.inputFile, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in reader:
                if row[0][0] != '#':
                    days_start = int(row[2].split(',')[0])
                    days_end = int(row[2].split(',')[1])
                    days = range(days_start,days_end)
                    hours_start = int(row[3].split(',')[0])
                    hours_end = int(row[3].split(',')[1])
                    hours = range(hours_start, hours_end)
                    user = {}
                    user['name'] = row[0]
                    user['key'] = row[1]
                    user['days'] = days
                    user['hours'] = hours
                    users.append(user)
                    #print("name:{}, key:{}, days:{}, hours:{}".format(row[0], row[1], days, hours))
        return users
        
if __name__ == '__main__':
    reader = UserReader("example_users")
    users = reader.get_users()
    print(users)
