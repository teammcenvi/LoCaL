import os
import subprocess
from flask import Flask, render_template, flash, request, redirect, url_for, make_response, session, abort, send_from_directory
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import time

import numpy as np
import sys
from scipy.special import erfcinv as erfcinv
import time
import re
import subprocess
import time
import shutil

import pandas as pd 
import numpy as np
import pytesseract
import cv2
from PIL import Image, ImageEnhance, ImageFilter
import json

import env_core

epoch_time = str(time.time())
epoch_time = epoch_time.split(".")
epoch_time = epoch_time[0]


app = Flask(__name__)

UPLOAD_FOLDER = 'C:\\Python\\ENVI_V1\\static'
# These are the extension that we are accepting to be uploaded
ALLOWED_EXTENSIONS = set(['pdf','PDF','txt','TXT','html','png','PNG','jpg','JPG'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5000 * 1024 * 1024


@app.route('/')
def home():
   if not session.get('logged_in'):
      return render_template('login.html')
   else:
      role = session['role']
      username = session['username']
      if role == 'superuser':
          return render_template('home.html',role=role,username=username)
    

@app.route('/login', methods=['POST'])
def do_admin_login():
   ### AUTHENTICATED in users.py list existence and LDAP ###
   found=0
   userx = request.form['username']
   username = "admin"
   password = "001admin"
   role = "superuser"
  

   ## Local Users ##
   if request.form['username'] == "admin" or request.form['username'] == "viewonly" or request.form['username'] == "search":
        if request.form['username'] == username and request.form['password'] == password:
          found=1
          session['role']=role
          session['username']=username

   if found == 1 :
      session['logged_in'] = True
      if role == 'superuser':
          return render_template('home.html',role=role,username=username)

   else:
      flash('Invalid Credential!')
   return home()

@app.route("/logout")
def logout():
   session['logged_in'] = False
   return home()

@app.route('/input', methods=['GET', 'POST'])
def input():
   if not session.get('logged_in'):
      return render_template('login.html')

   else:
      role = session['role']
      username = session['username']
    
      if role == 'superuser':
          return render_template('upload.html',role=role,username=username)
 
@app.route('/uploadx', methods=['POST'])
def uploadx():
  if not session.get('logged_in'):
      return render_template('login.html')
  else:
    role = session['role']
    username = session['username']
    # Get the name of th uploaded files
    uploaded_files = request.files.getlist("file")
    filenames = []
    for file in uploaded_files:
          #Make the filename safe, remove unsupported chars
          filename = secure_filename(file.filename)
          #Move the file from the temporal flder to the upload folder we setup
          file.save(os.path.join(UPLOAD_FOLDER, filename))

          result = env_core.main_core(filename)
    if role == 'superuser':
          return render_template('ai_result.html',role=role,username=username,filename=filename,result=result)
         
      

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(host='127.0.0.1', port=5500)
