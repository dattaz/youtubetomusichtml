This script made a music directory of mp3 video from youtube user or youtube playlist.

== Usage ==
python youtubetomusiquehtml.py [your channel url or playlist url]

== Building ==

It's advised, that you have `pip` installed. 
Chose one of the following methods to do that:

    sudo apt-get install python-setuptools python-dev

    sudo easy_install pip

It's advised, that you have `virtualenv` installed:

    sudo pip install virtualenv

    virtualenv --no-site-packages venv 

Activiate the virtual enviroment:

    source venv/bin/activate

Requirements are in requirements.txt you just need to make :

    pip install -r requirements.txt

You will also need ffmpeg or avconf (and eventually libav-tools)

After you can copy your build/ folder (or build/[what you have extract folder]/ )to a apache web server when you can have your music from youtube video everywhere in mp3
