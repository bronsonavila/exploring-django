#! /usr/bin/env python3

# Run "chmod +x diary.py" once from the same directory as this file to turn the
# file into an executable file that can be ran without being prefaced with
# "python3". The shebang line above must also be present for this to work (OSX).

import datetime
from peewee import *

db = MySQLDatabase('diary', user='root',
                   password='strategies123', host='localhost')


class BaseModel(Model):
    class Meta:
        database = db


class Entry(BaseModel):
    # A TextField does not need a max length to be specified (unlike CharField).
    content = TextField()
    # Do not invoke a function when setting a default; the script will invoke
    # the function automatically at the appropriate time (i.e., when the entry
    # is created, as opposed to when the script is run).
    timestamp = DateTimeField(default=datetime.datetime.now)


def initialize():
    """ Connect to the database and create any tables that do not exist."""
    db.connect()
    db.create_tables([Entry], safe=True)


def menu_loop():
    """ Show the menu. """
    choice = None

    # End the program if the user enters "q" into the input.
    while choice != 'q':
        print('Enter "q" to quit.')
        # List all menu keys and accompanying description.
        for key, value in menu.items():
            # __doc__ returns the docstring for a function.
            print('{}) {}'.format(key, value.__doc__))
        choice = input('Action:').lower().strip()
        # Run the menu function that matches the user's choice.
        if choice in menu:
            menu[choice]()


def add_entry():
    """ Add a diary entry. """
    return


def view_entries():
    """ View previous diary entries. """
    return


def delete_entry():
    """ Delete a diary entry. """
    return


menu = dict([
    ('a', add_entry),
    ('v', view_entries)
])

if __name__ == '__main__':
    initialize()
    menu_loop()

('n', 'new challenge'),
('s', 'new step'),
('d', 'delete a challenge'),
('e', 'edit a challenge'),