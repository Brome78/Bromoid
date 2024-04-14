from flask import Flask, render_template, redirect, url_for
import os
import subprocess

app = Flask(__name__, static_url_path='/static', static_folder='static')

def adb_command(serial_number, command):
    command_with_serial = ["adb", "-s", serial_number] + command.split()
    process = subprocess.Popen(command_with_serial, stdout=subprocess.PIPE)
    output, _ = process.communicate()
    return output.decode().strip()

# Get device serial number
def get_serial_number(id):
    return adb_command(id,"get-serialno")

# Get device model
def get_model(id):
    return adb_command(id,"shell getprop ro.product.model")

# Get Android version
def get_android_version(id):
    return adb_command(id,"shell getprop ro.build.version.release")

# Get device screen resolution
def get_screen_resolution(id):
    return adb_command(id,"shell wm size")

# Get device manufacturer
def get_manufacturer(id):
    return adb_command(id,"shell getprop ro.product.manufacturer")

def get_command_scrcpy(id):
    name = "opt/options_" + id + ".opt"

    with open(name,'r') as f:

        res = f.read()
        f.close()
    return res


@app.route('/')
def index():
    return redirect(url_for('devices_list'))

@app.route('/devices/<id>')
def show_device(id):
    cmd = "scrcpy -s " + str(id) + " " + get_command_scrcpy(id)
    os.system(cmd)
    return redirect(url_for('devices_list'))

@app.route('/info/<id>')
def info_device(id):
    elt = "<li> Serial Number : " +get_serial_number(id) + "</li>"
    elt += "<li> Model : " +get_model(id) + "</li>"
    elt += "<li> Android Version : " +get_android_version(id) + "</li>"
    elt += "<li> Screen Resolution : " +get_screen_resolution(id) + "</li>"
    elt += "<li> <div><img src=\"https://logo.clearbit.com/"+ get_manufacturer(id) +".com\"> Manufacturer : " +get_manufacturer(id) + "</div></li>"
    elt += "<input type=\'text\' id=\'options\' name=\'options\' value=\'" + get_command_scrcpy(id) + "\'>"
    elt += "<button onclick=\"saveFunction(\'"+id+"\',\'options\')\">Save</button>"

    return render_template('option_device.html',id=id,list=elt)

@app.route('/save/<id>/<func>')
def save_option_device(id,func):
    name = "opt/options_" + id + ".opt"
    with open(name,'w') as f:
        f.write(func)
        f.close()
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
        elt += "<li><div><img id=\""+tmp[0]+"\" src=\"static/default_device.png\" alt=\"Image 1\" onclick=\"redirectToDevice(\'"+ tmp[0] +"\')\">" + device + "</div><img id=\""+tmp[0]+"_conf\" src=\"static/options.png\" alt=\"Image 1\"onclick=\"redirectToInfo(\'"+ tmp[0] +"\')\">" +"</li>"
    
    return render_template('list_devices.html',list=elt,script=script)

@app.errorhandler(404)
def page_not_found(error):
    # Render a custom 404 page
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=False)