from flask import *
import os
import shutil

#https://axidraw.com/doc/cli_api
#having issues with the axidraw python api, using the cli instead for now. anyone else having issues? I get no errors even with the debugger
#from pyaxidraw import axidraw
#version = os.popen('axicli --mode sysinfo')



#make var to generate entirely new ./backup/conf_default.py incase of error
#make a read config file that outputs a list with all the vars in post action plot
def optimize(name,out,width,height):
    #probably not needed with axicli's reordering
    svg = ''
    with open(name, 'r') as f:
        svg += f.read() 
    splitlist = svg.split('<')
    newlist = []
    for each in splitlist:
        newlist.append(''.join(('<',each)))
    body = sorted(newlist[4:-2])
    body = newlist[4:-2]
    dimentions = newlist[3]
    w = dimentions.split('width=')[1].split('" ')[0]
    h = dimentions.split('height=')[1].split('" ')[0]
    
    newlist[3] = newlist[3].replace(w,f'"{width}in')
    newlist[3] = newlist[3].replace(h,f'"{height}in')
    print(newlist[3])
    with open(out,'w') as f:
        f.write(newlist[1])
        f.write(newlist[2])
        f.write(newlist[3])
        for each in body:
            f.write(each)
        f.write(newlist[-1])
    #print(f'svg optimized: {w},{h}')
    return svg

def readconfig():
    
    newconfig = {}
    with open('config.py', 'r', encoding='utf-8') as f:
        configvars = f.readlines()
    for each in configvars:
        for word in ['speed_pendown','speed_penup','accel ','pen_pos_down', 'pen_pos_up','pen_rate_raise','pen_rate_lower','pen_delay_up','pen_delay_down','x_travel_V3A3','y_travel_V3A3']:
            if word in each:
                newconfig[word] = each.split('= ')[1].split(' ')[0]
    #print(newconfig)
    return newconfig

def writeconfig():
    with open('config.py', 'r', encoding='utf-8') as f:
        configvars = f.readlines()
    with open('config.py', 'w', encoding='utf-8') as file:
        for e in configvars:
            for word in ['speed_pendown','speed_penup','accel ','pen_pos_down', 'pen_pos_up','pen_rate_raise','pen_rate_lower','pen_delay_up','pen_delay_down','x_travel_V3A3','y_travel_V3A3']:
                if word in e:
                    temp = f'{word} = '
                    req = request.form.get(f'{word}')
                    if word == 'accel ':
                        temp = f'{word}= '
                    if word == 'x_travel_V3A3' or word == 'y_travel_V3A3':
                        req = f'{float(req):.2f}'
                    #print(e.split(f'{temp}')[1].split(' ')[0], '->', req)
                    e = e.replace(e.split(f'{temp}')[1].split(' ')[0],str(req))
            file.write(e)
            
app = Flask(__name__)

@app.route('/')
def index():
    #read config file and get all
    config = readconfig()
    version = os.popen('axicli -m version').read()
    directory = f'{os.getcwd()}\svg\default.svg'
    return render_template('index.html', version=version, config = config, directory = directory)

@app.route('/home')
def home():
    
    return redirect('/')

@app.route('/penup')
def penup():
    os.system("axicli -m manual -M lower_pen")
    return redirect('/')

@app.route('/pendown')
def pendown():
    os.system("axicli -m manual -M raise_pen")
    return redirect('/')

@app.route('/align')
def align():
    os.system("axicli --mode align")
    return redirect('/')

@app.route('/plot', methods=['GET', 'POST'])
def plot():
    
    file = request.form.get('path')
    print(file)
    
    paper = request.form.get('paper').split('x')
    print(paper[1], paper[0])
    shutil.copyfile(file,f"{file}.bk")
    optimize(file,f"{file}.bk",paper[0],paper[1])
    reorder = request.form.get('reorder')
    
    default = f'axicli {file} --mode plot'
    if reorder != 0:
        reorder = f' -G{reorder}'
        default += reorder
        print('mode set to reorder', default) 
    os.system(f"axicli {file}.bk --mode plot --config config.py")
    return redirect('/')

@app.route('/config', methods=['GET', 'POST'])
def config():
    writeconfig()
    #edit all the config vars in the html into the py file here
    return redirect('/')

app.run(debug=True)
