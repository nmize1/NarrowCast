import os
# Library Manager
# Libraries know their name, path, and have a list of Shows
# Shows know their name, path, and have a list of Seasons
# Seasons know their name, path, and have a list of Episodes
# Episodes know their name and path.
# Aside from episodes, they all have a function to populate their lists.

# Libraries should be formatted on the drive as such:
# LIBRARY_FOLDER
#   SHOW1_FOLDER:
#       SEASON1_FOLDER:
#           EPISODE1.mp4 (Other filetypes may work, but aren't supported yet)
#           ..... (As many episodes as you want)
#       ..... (As many seasons as you want)
#   ..... (As many shows as you want)

class Episode:
    def __init__(self, name, path):
        self.name = name
        self.path = path

class Season:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.episodes = []

    def getEpisodes(self):
        for root, dirs, files in os.walk(self.path):
            for name in files:
                e = Episode(name, os.path.join(root, name))
                self.episodes.append(e)
                #print(name + " added with path: " + os.path.join(root, name))
            break

class Show:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.seasons = []

    def getSeasons(self):
        for root, dirs, files in os.walk(self.path):
            for name in dirs:
                s = Season(name, os.path.join(root, name))
                self.seasons.append(s)
                #print(name + " added with path: " + os.path.join(root, name))
            break

        for season in self.seasons:
            season.getEpisodes()

class Library:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.shows = []

    def getShows(self):
        for root, dirs, files in os.walk(self.path):
            for name in dirs:
                s = Show(name, os.path.join(root, name))
                self.shows.append(s)
                #print(name + " added with path: " + os.path.join(root, name))
            break

        for show in self.shows:
            show.getSeasons()

def addNewLibrary(name, path):
    l = Library(name, path)
    l.getShows()
    return l
