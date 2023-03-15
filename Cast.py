import random
import subprocess
import json
import os
import shutil

from VideoManager import *

# NEXT: Change logo filler creation to play a clip of a big video rather than making a new video for each one. Should be faster.
#       Ensure shorts and fillers are the correct amount of time and not being added extra times.

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

    if(len(schedules) == 48):
        block = 1800
    else:
        block = 3600

    for key, val in schedules.items():
        fillerIndex = 0
        print(key.name)
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
            tries = 0
            #tries!=5 is arbitrary, could change to a setting.
            #More tries lowers the chance of a long gap at the end of the block.
            #Less tries would be faster
            while(tries != 5):
                short = shortsFolder + "\\" + random.choice(os.listdir(shortsFolder))
                slen = getDuration(short)
                short = doConversion(short, dconv)
                if(slen < remainingTime):
                    blockList.append({"title": "short", "src": short})
                    remainingTime = remainingTime - slen
                tries = tries + 1

            blockList.append({"title": "logo", "src": makeFiller(remainingTime, key.name, fillerIndex)})
            fillerIndex += 1
            final += blockList

        if(os.path.exists(key.name) == False):
            os.mkdir(key.name)

        # Write the playlist to a JSON file
        with open(key.name + '\playlist.json', 'w') as f:
            json.dump(final, f)

        shutil.copyfile('index.html', key.name + '\index.html')
        shutil.copyfile('favicon.ico', key.name + '\favicon.ico')
        print(final)

    port = 17000
    subprocess.Popen(["python", "-m", "http.server", str(port)], cwd='.')


#keep track of the index in a dic in the schedule
#get lengths of seasons, use them to calculate appropriate season and episode to get the next one
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

def getRandomEpisode(show):
    s = random.randrange(len(show.seasons))
    e = random.randrange(len(show.seasons[s].episodes))
    path = show.seasons[s].episodes[e].path
    print(path)
    return path

#https://stackoverflow.com/questions/3844430/how-to-get-the-duration-of-a-video-in-python
def getDuration(filename):
    result = subprocess.check_output(
            f'ffprobe -v quiet -show_streams -select_streams v:0 -of json "{filename}"',
            shell=True).decode()
    fields = json.loads(result)['streams'][0]

    duration = fields['duration']

    return float(duration)
