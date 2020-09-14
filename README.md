# plotplot

![plotplot](https://github.com/jrparadis/plotplot/blob/master/screenshot.png?raw=true)

A fairly basic python/flask website for controlling an Axidraw pen plotter (and probably others). Can plot SVG files, align/depower motors, edit config, easily adjust for paper size, display a webcam aimed at your plotter. 

Install instructions (python, axidraw cli, flask):

install Python 3
run these commands:

pip install flask
pip install https://cdn.evilmadscientist.com/dl/ad/public/AxiDraw_API.zip (https://axidraw.com/doc/cli_api/#about-axidraw)

clone repo, cd to the directory and do "set FLASK_APP=plotplot.py" for windows, "export FLASK_APP=plotplot.py" for linux/mac, then "flask run"
navigate to 127.0.0.1:5000. 
 
I wanted to get away from inkscape and the lagginess of loading files, and have something like octoprint where I could just load a webpage from anywhere to control it and view a webcam. I should be able to run this on an old raspberry pi as well - I'm not sure if that's possible with inkscape.

There's a few comments in templates/index.html that explain some default settings you might like to change, but it's not required.

Overall I'm satisfied with it for standard pen plotting. There's a few things that need fixing to make it a bit easier to use or give it more functionality:

migrate from axicli to python api directly for interactive mode if possible, then I could use it to paint as well. (I can't get it to work with flask even when everything is initialized in one function, and I get no error message so I don't know what's going on. has anyone been able to get it working with flask? normal python scripts work fine)

radio buttons for axidraw model or text listing model:model dimentions to be used with paper height/width

change os.popen for version to subprocess, os.popen() doesn't seem to give a response with axicli? (it shows in print but won't save as variable, probably related to the python API thing and it's just something basic with flask I'm missing)

site loads indefinitely while plotting - quick fix is to just redirect to a new page while plotting.  show progress and svg if possible

find a better solution for choosing files instead of just a text box for direct path or a bunch of javascript - expand this to take multiple svg files or be able to handle single svgs with layers. there's some javascript in the html to choose the file but it makes it always comes up with a fake path. 

make values save without a db or having to set defaults via html (use cookies?)
