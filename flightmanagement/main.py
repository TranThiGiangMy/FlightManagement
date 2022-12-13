from flask import render_template
from flightmanagement import app
from flask import render_template, request, redirect, session, jsonify
from flightmanagement import dao, app, admin
from flask_login import login_user, logout_user, current_user, login_required
import cloudinary.uploader
from flightmanagement import admin


@app.route('/employee')
def employee():

    return render_template('home/employee.html')





@app.route("/")
def index():

    return render_template('home/index.html')


if __name__ == '__main__':
    from flightmanagement.admin import *
    app.run(debug=True)