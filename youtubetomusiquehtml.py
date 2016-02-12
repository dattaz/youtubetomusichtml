#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import youtube_dl
import shutil
import slugify

type = ""
videos = []

def get_list_item_info(url):
    """
    Create dictionnary with all info about video playlist or user video
    structure is {dict [list of dict {dict for each video} ] }
    Only return list of video and write title of playlist/user name
    """
    with youtube_dl.YoutubeDL() as ydl:
        attempts = 0
        while attempts < 5:
            try:
                result = ydl.extract_info(url, download=False)
                break
            except:
                e = sys.exc_info()[0]
                attempts += 1
                print "error : " + str(e)
                if attempts == 5:
                    sys.exit("Error during getting list of video")
                print "We will re-try to get this video"
                time_to_wait = 60 * attempts
                time.sleep(time_to_wait)

    return result

def prepare_folder(list):
    global type
    type = list['extractor_key']
    if "www.youtube.com/user/" in sys.argv[1]:
        type = "user"
    global title
    global title_html

    if type == "YoutubePlaylist":
        title = slugify.slugify(list['title'])
        title_html = list['title']
    else:
        title =  slugify.slugify(list.get('entries')[0].get('uploader'))
        title_html = list.get('entries')[0].get('uploader')
    #add player on each folder
    global scraper_dir
    scraper_dir = script_dirname + "build/" + title + "/"

    if not os.path.exists(scraper_dir):
        os.makedirs(scraper_dir)
    if not os.path.exists(scraper_dir+"player.html/"):
        shutil.copy("templates/player.html", scraper_dir+"player.html")
    if not os.path.exists(scraper_dir+".htaccess"):
        shutil.copy("templates/.htaccess", scraper_dir+".htaccess")
    # add player on general folder 
    if not os.path.exists(script_dirname + "build/"+"player.html/"):
        shutil.copy("templates/player.html", script_dirname + "build/"+"player.html")
    if not os.path.exists(script_dirname + "build/"+".htaccess"):
        shutil.copy("templates/.htaccess", script_dirname + "build/"+".htaccess")

def write_video_info(list):
    """
    Save video in best quality in build/{title of user/playlist}/{name}.mp3
    """
    print 'Rendering template...'
    for item in list.get('entries'):
        title_clean = slugify.slugify(item.get('title'))
        video_directory = scraper_dir+title_clean+".mp3"
        if not os.path.exists(video_directory):
            ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'outtmpl': scraper_dir+title_clean+'.mp3"'
                }
            url = "https://www.youtube.com/watch?v="+item.get('id')
            with youtube_dl.YoutubeDL(ydl_opts)  as ydl:
                attempts = 0
                while attempts < 5:
                    try:
                        ydl.download([url])
                        break
                    except:
                        e = sys.exc_info()[0]
                        attempts += 1
                        print "error : " + str(e)
                        if attempts == 5:
                            sys.exit("Error during getting video")
                        print "We will re-try to get this video in 10s"
                        time_to_wait = 60 * attempts
                        time.sleep(time_to_wait)
        else:
            print "Video directory " + video_directory + "already exists. Skipping."

def usage():
    print "\nYoutube to mp3 player  script\n"
    print 'Usage: python youtubetomusiquehtml.py [your channel url or playlist url] \n'

if len(sys.argv) != 2:
    usage()
    exit()

script_dirname=(os.path.dirname(sys.argv[0]) or ".") + "/"
list=get_list_item_info(sys.argv[1])
prepare_folder(list)
write_video_info(list)
