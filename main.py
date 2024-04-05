from flask import Flask, render_template, redirect, url_for
import os

app = Flask(__name__, static_url_path='/static', static_folder='static')

@app.route('/')
def index():
    return 'Hello, world! This is a Flask server.'

@app.route('/devices/<id>')
def show_device(id):
    cmd = "scrcpy -s " + str(id)
    os.system(cmd)
    return redirect(url_for('devices_list'))

@app.route('/devices')
def devices_list():
    os.system("adb devices > .list")
    f = open(".list")
    devices_list = f.readlines()

    devices_list.pop(0)
    devices_list.pop(-1)

    elt = ""
    script = ""

    for device in devices_list:
        tmp = device.split("\t")
        elt += "<li  id=\""+tmp[0]+"\"><img src=\"static/default_device.png\" alt=\"Image 1\">" + device + "</li>"
        script += "var item1 = document.getElementById('"+tmp[0]+"');item1.addEventListener('click', function() {window.location.href = 'devices/"+tmp[0]+"';});"
    
    return render_template('list_devices.html',list=elt,script=script)

@app.errorhandler(404)
def page_not_found(error):
    # Render a custom 404 page
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)