# plotplot

![plotplot](https://github.com/jrparadis/plotplot/blob/master/screenshot.png?raw=true)

A python/flask website for controlling an Axidraw pen plotter (and probably others). Can plot SVG files, align/depower motors, edit config, easily adjust for paper size, and display a webcam aimed at your plotter. 

Install instructions (python, axidraw cli, flask, vpype):

    install Python 3
    run these commands:
    pip install flask
    pip install https://cdn.evilmadscientist.com/dl/ad/public/AxiDraw_API.zip (https://axidraw.com/doc/cli_api/#about-axidraw)
    install vpype - https://github.com/abey79/vpype
    clone repo, cd to the directory and do "set FLASK_APP=plotplot.py" for windows, "export FLASK_APP=plotplot.py" for linux/mac, then "flask run"
    navigate to 127.0.0.1:5000. 

I wanted to get away from inkscape and the lagginess of loading files, and have something like octoprint where I could just load a webpage from anywhere to control it and view a webcam. I should be able to run this on an old raspberry pi as well - I'm not sure if that's possible with inkscape.

    There's a few comments in templates/index.html that explain some default settings you might like to change, but it's not required.

    Overall I'm satisfied with it for standard pen plotting. There's a few things that need fixing to make it a bit easier to use or give it more functionality:

    radio buttons for axidraw model or text listing model:model dimentions to be used with paper height/width. currently adjusted via model width/height textbox

    site loads indefinitely while plotting - quick fix is to just redirect to a new page while plotting.  show progress and svg if possible

    support for multiple plots in one click with a pause

    make values save without a db or having to set defaults via html (use cookies?)

    paint mode with axidraw API interactive mode
