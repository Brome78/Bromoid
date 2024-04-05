from flask import Flask, render_template
import os

app = Flask(__name__, static_url_path='/static', static_folder='static')

@app.route('/')
def index():
    return 'Hello, world! This is a Flask server.'

@app.route('/devices')
def devices_list():
    os.system("adb devices > .list")
    f = open(".list")
    devices_list = f.readlines()

    devices_list.pop(0)
    devices_list.pop(-1)

    elt = ""

    for device in devices_list:
        elt += "<li><img src=\"static/default_device.png\" alt=\"Image 1\">" + device + "</li>"
    
    return render_template('list_devices.html',list=elt)

@app.errorhandler(404)
def page_not_found(error):
    # Render a custom 404 page
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)