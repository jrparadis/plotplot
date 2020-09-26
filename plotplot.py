from flask import *
import os
import subprocess

def optimize(name,out,width,height,border):
    subprocess.check_output(f"vpype read {name} scaleto {int(width)-int(border)}in {int(height)-int(border)}in linemerge --tolerance 1mm linesort write --page-format {width}x{height}in --center {out}".split(' '))
    print(f'svg optimized via vpype')

def readconfig():
    newconfig = {}
    with open('config.py', 'r', encoding='utf-8') as f:
        configvars = f.readlines()
    for each in configvars:
        for word in ['speed_pendown','speed_penup','accel ','pen_pos_down', 'pen_pos_up','pen_rate_raise','pen_rate_lower','pen_delay_up','pen_delay_down','x_travel_V3A3','y_travel_V3A3']:
            if word in each:
                newconfig[word] = each.split('= ')[1].split(' ')[0]
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
                    e = e.replace(e.split(f'{temp}')[1].split(' ')[0],str(req))
            file.write(e)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.getcwd()
@app.route('/')
def index():
    config = readconfig()
    return render_template('index.html', config = config)

@app.route('/test')
def test():
    ad = init()
    disc(ad)
    return redirect('/')

@app.route('/penup')
def penup():
    os.system("axicli -m manual -M raise_pen")
    return redirect('/')

@app.route('/pendown')
def pendown():
    os.system("axicli -m manual -M lower_pen")
    return redirect('/')

@app.route('/align')
def align():
    os.system("axicli --mode align")
    return redirect('/')

@app.route('/plot', methods=['GET', 'POST'])
def plot():
    if request.method == 'POST':
        file = request.files['file']
        print(file)
        
        if file.filename == '':
            flash('No selected file')
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        paper = request.form.get('paper').split('x')
        border = request.form.get(f'border')
        optimize(file.filename,f"{file.filename}bk.svg",paper[0],paper[1],border)
        default = f'axicli {file.filename}bk.svg --mode plot --config config.py'
        os.system(f"{default}")
    else:
        redirect('/')
    return redirect('/')

@app.route('/config', methods=['GET', 'POST'])
def config():
    writeconfig()
    return redirect('/')

app.run(debug=True)
