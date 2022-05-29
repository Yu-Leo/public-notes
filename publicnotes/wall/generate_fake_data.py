"""Script for generating fake notes. ONLY FOR DEVELOPMENT"""

import random

from publicnotes.wsgi import *
from wall.models import Note, Category, User

N = 20  # Number of notes
TITLE_TEMPLATE = 'Lorem ipsum '
CONTENT = '''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce quis cursus nisl, eu ornare neque. Donec tristique, nunc quis euismod consectetur, risus enim tristique dui, nec auctor quam massa eget nisi. In sollicitudin felis in libero sollicitudin sagittis et ut nunc. Vestibulum sodales commodo diam sed cursus. Proin in tellus maximus, sollicitudin lectus et, laoreet massa. Aenean id ante tincidunt lacus ultricies vehicula. Nullam non tincidunt nulla. Quisque ex eros, finibus quis odio non, lacinia porta erat. Mauris ullamcorper bibendum efficitur. Nam aliquet accumsan leo at varius. Sed venenatis purus in rhoncus laoreet. Cras fringilla sapien a felis tempor iaculis. Phasellus ex sem, iaculis non orci sed, consequat egestas justo. '''


def main():
    global N, TITLE_TEMPLATE, CONTENT
    categories = Category.objects.all()
    authors = User.objects.all()

    for i in range(N):
        note = Note()
        note.title = TITLE_TEMPLATE + str(i)
        note.category = random.choice(categories)
        note.author = random.choice(authors)
        note.rating = random.randint(-100, 100)
        note.content = CONTENT
        note.save()


if __name__ == '__main__':
    main()
