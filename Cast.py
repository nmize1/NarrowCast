import random
import subprocess
import json
import os
import shutil

from VideoManager import *

# NEXT: Change logo filler creation to play a clip of a big video rather than making a new video for each one. Should be faster.
#       Ensure shorts and fillers are the correct amount of time and not being added extra times.

# Convert path to networked path so video player can access files on different drives
def doConversion(path, dconv):
    for key, val in dconv.items():
        if(path.find(key) != -1):
            fpath = path.replace(key, val)
    return fpath


def cast(schedules, shortsFolder):
    final = []
    inOrderDic = {}
    dconv = {}
    with open('conversionsettings.json', 'r') as f:
        dconv = json.load(f)

    # Determine block length
    if(len(schedules) == 48):
        block = 1800
    else:
        block = 3600

    # For channel, schedule:
    # Config the blocks
    # Make a new folder for the channel and copy its files into it
    for key, val in schedules.items():
        fillerIndex = 0
        print(key.name)

        # For block in channel, [show, shuffled or in order bool]:
        # Get the appropriate episode for the block, get the correct path
        # Fill the remaining time at the end of the block
        # Add the files for this block to a list
        for k, v in val.items():
            blockList = []
            print(k)
            if(v[1]):
                if(k in inOrderDic.keys()):
                    index = inOrderDic[k] + 1
                    inOrderDic[k] = index
                else:
                    index = 0
                    inOrderDic[k] = index

                path = getNextEpisode(v[0], index)
            else:
                path = getRandomEpisode(v[0])

            fpath = doConversion(path, dconv)
            blockList.append({"title": str(k), "src": fpath})
            remainingTime = block - getDuration(path)

            # Choose from the shorts folder randomly to fill the remaining space in the block
            # tries!=5 is arbitrary, could change to a setting.
            # More tries lowers the chance of a long gap at the end of the block.
            # Less tries would be faster
            tries = 0
            while(tries != 5):
                short = shortsFolder + "\\" + random.choice(os.listdir(shortsFolder))
                slen = getDuration(short)
                short = doConversion(short, dconv)
                if(slen < remainingTime):
                    blockList.append({"title": "short", "src": short})
                    remainingTime = remainingTime - slen
                tries = tries + 1

            # Once there are no more shorts that can fit in the block, create a filler video to fill the rest of the block
            blockList.append({"title": "logo", "src": makeFiller(remainingTime, key.name, fillerIndex)})
            fillerIndex += 1
            final += blockList

        # Make the folder for the channel
        if(os.path.exists(key.name) == False):
            os.mkdir(key.name)

        # Write the playlist to a JSON file
        with open(key.name + '\playlist.json', 'w') as f:
            json.dump(final, f)

        # Copy the files to the channel folder
        shutil.copyfile('index.html', key.name + '\index.html')
        shutil.copyfile('favicon.ico', key.name + '\favicon.ico')
        print(final)

    # Once all the channels are in their appropriate folders, launch the server such that localhost/channel_name launches the channel
    port = 17000
    subprocess.Popen(["python", "-m", "http.server", str(port)], cwd='.')


# Keep track of the index in a dic in the schedule
# Get lengths of seasons, use them to calculate appropriate season and episode to get the next one
def getNextEpisode(show, index):
    slens = []
    for season in show.seasons:
        slens.append(len(seasons.episodes))

    i = 0
    for l in slens:
        if(index < l):
            path = show.seasons[i].episodes[index]
            print(path)
            return path
        else:
            index = index - l
            i = i + 1

# Get a random episode for shuffled shows
def getRandomEpisode(show):
    s = random.randrange(len(show.seasons))
    e = random.randrange(len(show.seasons[s].episodes))
    path = show.seasons[s].episodes[e].path
    print(path)
    return path

# https://stackoverflow.com/questions/3844430/how-to-get-the-duration-of-a-video-in-python
# Get length of a video
def getDuration(filename):
    result = subprocess.check_output(
            f'ffprobe -v quiet -show_streams -select_streams v:0 -of json "{filename}"',
            shell=True).decode()
    fields = json.loads(result)['streams'][0]

    duration = fields['duration']

    return float(duration)
