from moviepy.editor import ImageClip, VideoFileClip, concatenate_videoclips
import subprocess
import ffmpeg

def makeFiller(time, folder, index):
    image = "FSLogo.png"
    output = folder + "\\short" + str(index) + ".mp4"
    img = []
    print(int(time))
    for i in range(int(time)):
        img.append(image)

    with open('mylist.txt', 'w+') as file:
        for im in img:
            file.write(f'file {im}\n')

    ffmpeg.input('mylist.txt', r='20', f='concat', safe='0').output(output, vcodec='libx264').run(overwrite_output=True)
    print("Filler complete.")

    return output
