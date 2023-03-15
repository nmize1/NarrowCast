import pickle
from threading import Thread

def save_object(obj, filename):
    with open(filename, 'wb') as outp:  # Overwrites any existing file.
        pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)

#Helper function for debug checks
def printLibrary(library):
    print(library.name)
    for show in library.shows:
        print(show.name)
        #for season in show.seasons:
            #print(season.name)
            #for episode in season.episodes:
                #print(episode.name)
