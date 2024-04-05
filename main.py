from flask import Flask, render_template
import os

app = Flask(__name__, static_url_path='/static', static_folder='static')

t = "fd"
t = t.replace("fd","ag",-1)
print(t)

@app.route('/')
def index():
    return 'Hello, world! This is a Flask server.'

@app.route('/devices')
def devices_list():
    os.system("adb devices > .list")
    f = open(".list")
    devices_list = f.read()
    
    return render_template('list_devices.html',list=devices_list)

@app.errorhandler(404)
def page_not_found(error):
    # Render a custom 404 page
    return render_template('404.html'), 404

@app.route('/404')
def error_404():
    return render_template('404.html')

if __name__ == '__main__':
    app.run(debug=True)