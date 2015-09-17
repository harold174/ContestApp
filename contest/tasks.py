from celery import task
import os
import subprocess


@task()
def add(x, y):
    return x + y


@task()
def convertVideos():
    subprocess.call(" ffmpeg -i /home/harold/Documents/CLOUD_PROYECT/contestApp/media/profile/2015/09/16/videotest.mp4 /home/harold/Documents/CLOUD_PROYECT/contestApp/media/profile/2015/09/16/output.avi", shell=True)

