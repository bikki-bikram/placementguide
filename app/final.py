from flask import Flask,session,render_template,request,url_for,redirect,g,flash
from flaskext.mysql import MySQL
import os
from PIL import Image
#import base64
import cStringIO
import PIL.Image
#import cv2
#import numpy as np
#import matplotlib.pyplot as plt
#import os
#from PIL import Image
#from base64 import b64encode
import datetime
import cStringIO
import re
from email.utils import *


mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'bikki123'
app.config['MYSQL_DATABASE_DB'] = 'dbfinal'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
#data='unknown'
uid='unknown'
name='unknown'
data1='unknown'
dest='unknown'
dest2='dfgh'
app.secret_key=os.urandom(24)

UPLOAD_FOLDER = '/myproject/app/static'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/")
def front():
    return render_template("frontpage.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    global data
    global dest
    #if request.method == 'POST':
    global uid
    uid=request.form["uid"]
    password=request.form["pwd"]
    connection=mysql.get_db()
    cursor = connection.cursor()
      
    query=("SELECT * from user_details where uid='" + uid + "' and pwd='" + password + "'")
    cursor.execute(query)
    data2 = cursor.fetchone()
    cursor.execute(query)

    data=cursor.fetchall()

    if data2 is None:
        error = 'Invalid Credentials. Please try again.'
        return render_template('frontpage.html', error=error)
    else:
        query3=("SELECT destination from user_details where uid='" + uid + "' and pwd='" + password + "'")
        cursor.execute(query3)
        data4 = cursor.fetchone()
         #   global dest
        for item in data4:
            dest= item
  #      print item

        session['logged_in'] = True
   #     flash('You were logged in.')
        session['my_list'] = data
        session['my_list1'] = data
        return redirect(url_for('homepage'))
def abcc():
    global dest2
    dest2=dest
    print dest2
            


@app.route('/logout')
#@login_required
def logout():
    session.pop('logged_in', None)
    #flash('You were logged out.')
    return redirect(url_for('front'))


@app.route("/homepage")
def homepage():
    abcc()
    if request.method == 'GET':
        if session['logged_in'] == True:
            connection=mysql.get_db()
            cursor = connection.cursor()
            query=("SELECT name,date_visited from company_data")
            query1=("SELECT count(*) from company_data")
            cursor.execute(query)
            data2 = cursor.fetchall()
            cursor.execute(query1)
            data3 = cursor.fetchone()
            connection=mysql.get_db()
            cursor = connection.cursor()
            cursor.execute("SELECT * from comments")
            global data1
            data1=cursor.fetchall()
           # return data
            for item in data3:
                a= item
            if dest2=='Faculty':
                return render_template("homepage_faculty.html",data=data,data1=data1,data2=data2,data3=a)
                
            if dest2=='Student':
                return render_template("homepage_student.html",data=data,data1=data1,data2=data2,data3=a)
            
        #if session['logged_in'] == None:
        else:
            return "sesion closd"
        #return render_template('frontpage.html')

    

@app.route("/company_data/<filename>")
def company(filename):
     if session['logged_in'] == True:
         fn=filename
         connection=mysql.get_db()
         cursor = connection.cursor()
         query=("SELECT * from company_data where name='"+filename+"'")
         cursor.execute(query)
         data2 = cursor.fetchall()
         return render_template("company_data.html",data=data,data2=data2,fn=fn)
     if session['logged_in'] == False:
        return "session closed"

@app.route("/company_data/<filename>/question")
def company_question(filename):
     if session['logged_in'] == True:
         #print filename
         fn=filename
         connection=mysql.get_db()
         cursor = connection.cursor()
        # query2=("SELECT imgpath from company_data where name='"+filename+"'")
         #cursor.execute(query2)
         #data4 = cursor.fetchall()
         query5=("SELECT * from ques_images where company_name='"+filename+"'")
         cursor.execute(query5)
         data5 = cursor.fetchall()

         #query6=("SELECT count(*) from ques_images where company_name='"+filename+"'")
         #cursor.execute(query6)
         #data6 = cursor.fetchone()
         #for item in data6:
         #   count= item
         if dest=='Faculty':
             return render_template("question.html",data=data,data5=data5,fn=fn)
         if dest=='Student':
             return render_template("question_student.html",data=data,data5=data5,fn=fn)
     if session['logged_in'] == False:
        return "session closed"

@app.route('/company_data/<filename>/uploadques', methods = ['GET', 'POST'])
def upload_file1(filename):
    #if request.method == 'POST':
    fn=filename
    #id_no=uid
    #print uid
    for file in request.files.getlist("file"):
        filename=file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print filename
        foo = Image.open('static/'+filename)  
        foo.size
        foo = foo.resize((600,600),Image.BICUBIC)
        foo.save('static/'+filename,optimize=True,quality=1000)
        connection=mysql.get_db()
        cursor = connection.cursor()
        sql = "insert into ques_images(company_name,ques_img_path,uploaded_by) values('"+fn+"','"+filename+"','"+uid+"');"
        cursor.execute(sql)
        connection.commit()
    return redirect(url_for('homepage'))





@app.route("/company_data/<filename>/group-discussion")
def company_group_discussion(filename):
     if session['logged_in'] == True:
         #print filename
         fn=filename
         connection=mysql.get_db()
         cursor = connection.cursor()
         query3=("SELECT topic_name from group_discussion where company_name='"+filename+"'")
         cursor.execute(query3)
         data3 = cursor.fetchall()
         
         if dest=='Faculty':
             return render_template("group_discussion.html",data=data,data3=data3,fn=fn)
         if dest=='Student':
             return render_template("group_discussion_student.html",data=data,data3=data3,fn=fn)
     if session['logged_in'] == False:
        return "session closed"


@app.route('/company_data/<filename>/group-discussion-upload', methods = ['GET', 'POST'])
def upload_topic_gd(filename):
    #if request.method == 'POST':
    fn=filename
    #id_no=uid
    #print uid
    topic=request.form["data"]
    connection=mysql.get_db()
    cursor = connection.cursor()
    sql = "insert into group_discussion(company_name,topic_name,uploaded_by) values('"+fn+"','"+topic+"','"+uid+"');"
    cursor.execute(sql)
    connection.commit()
    query3=("SELECT topic_name from group_discussion where company_name='"+filename+"'")
    cursor.execute(query3)
    data3 = cursor.fetchall()
    return render_template("group_discussion.html",data=data,data3=data3,fn=fn)
   #return redirect(url_for('homepage'))
   # return redirect(url_for('upload_topic_gd(filename)'))


@app.route("/company_data/<filename>/interview-round")
def company_interview_round(filename):
     if session['logged_in'] == True:
         #print filename
         fn=filename
         connection=mysql.get_db()
         cursor = connection.cursor()
         query3=("SELECT * from interview_round where company_name='"+filename+"'")
         cursor.execute(query3)
         data3 = cursor.fetchall()
         if dest=='Faculty':
             return render_template("interview.html",data=data,data3=data3,fn=fn)
         if dest=='Student':
            return render_template("interview_student.html",data=data,data3=data3,fn=fn)
         
     if session['logged_in'] == False:
        return "session closed"


@app.route('/company_data/<filename>/interview-round-upload', methods = ['GET', 'POST'])
def upload_topic_interview(filename):
    #if request.method == 'POST':
    fn=filename
    #id_no=uid
    #print uid
    interview_ques=request.form["data"]
    connection=mysql.get_db()
    cursor = connection.cursor()
    sql = "insert into interview_round(company_name,interview_ques,uploaded_by) values('"+fn+"','"+interview_ques+"','"+uid+"');"
    cursor.execute(sql)
    connection.commit()
    return redirect(url_for('homepage'))


@app.route("/delete_interview_comment",  methods=["POST"])
def delete_interview_comment():
     if session['logged_in'] == True:
         delete=request.form["del"]
         comp_name=request.form["comp"]
         
         connection=mysql.get_db()
         cursor = connection.cursor()
         query="delete from interview_round where idir='"+delete+"' and company_name='"+comp_name+"';"
         cursor.execute(query)
         connection.commit()
         return redirect(url_for('homepage'))
    
     if session['logged_in'] == None:
         return "session closed"


@app.route("/form_add_company")
def add_company():
     if session['logged_in'] == True:
         return render_template("form_add_company.html")
     if session['logged_in'] == None:
        return "session closed"

@app.route("/form_delete_company")
def delete_company():
     if session['logged_in'] == True:
        connection=mysql.get_db()
        cursor = connection.cursor()
        query=("SELECT name from company_data")
        cursor.execute(query)
        data2 = cursor.fetchall()
        
        return render_template("form_delete_company.html",data2=data2)
     if session['logged_in'] == None:
        return "session closed"

@app.route("/company_details",  methods=["POST"])
def company_details():
     if session['logged_in'] == True:
         name=request.form["name"]
         cgpa=request.form["cgpa"]
         ten_marks=request.form["10_marks"]
         tweleve_marks=request.form["12_marks"]
         package=request.form["package"]
         subjects=request.form["specific subjects"]
         backlog=request.form["backlogs"]
         grp=request.form["grp-dicussion"]
         datevisited=request.form["datevisited"]
         profile_demanded=request.form["profiledemanded"]
         #filename=NULL
         connection=mysql.get_db()
         cursor = connection.cursor()
         print name,cgpa,ten_marks,tweleve_marks
         query="insert into company_data(name,cgpa,10_res,12_res,package,basic_deatils,gds,backlogs,date_visited,profile_demanded) values('"+name+"','"+cgpa+"','"+ten_marks+"','"+tweleve_marks+"','"+package+"','"+subjects+"','"+grp+"','"+backlog+"','"+datevisited+"','"+profile_demanded+"');"
         cursor.execute(query)
         connection.commit()
         return redirect(url_for('homepage'))
    
     if session['logged_in'] == None:
        return "session closed"

@app.route("/delete_company_details",  methods=["POST"])
def delete_company_details():
     if session['logged_in'] == True:
         delete=request.form["del_com"]
         connection=mysql.get_db()
         cursor = connection.cursor()
         query="delete from company_data where name='"+delete+"';"
         cursor.execute(query)
         query2="delete from ques_images where company_name='"+delete+"';"
         cursor.execute(query2)
         query3="delete from group_discussion where company_name='"+delete+"';"
         cursor.execute(query3)
         query4="delete from interview_round where company_name='"+delete+"';"
         cursor.execute(query4)
         connection.commit()
         return redirect(url_for('homepage'))
    
     if session['logged_in'] == None:
        return "session closed"



@app.route("/add_data", methods = ["POST"])
def add_data():
    name=request.form["name"]
    uid=request.form["uid"]
    password=request.form["pwd"]
    rpassword=request.form["rpwd"]
    contact=request.form["phno"]
    email=request.form["email"]
    global destination
    destination=request.form["destination"]
    Ph=re.compile(r'^[7-9]\d{9}$')
    email1 = parseaddr(email)
    connection=mysql.get_db()
    cursor = connection.cursor()
        
    query=("SELECT uid from user_details where uid='" + uid + "'")
    cursor.execute(query)
    data4 = cursor.fetchone()
    
    if data4 is None:
        if password==rpassword and Ph.match(contact) and bool(re.search(r'^[a-zA-Z][\w\-\.]*@[A-Za-z]+\.[a-zA-Z]{1,3}$', email1[1])):
            connection=mysql.get_db()
            cursor = connection.cursor()
            query="insert into user_details(name,uid,pwd,rpwd,contact_no,email,destination) values('"+name+"','"+uid+"','"+password+"','"+rpassword+"','"+contact+"','"+email+"','"+destination+"');"
            cursor.execute(query)
            connection.commit()
            return redirect(url_for("front"))
        else:
            if password!=rpassword:
                error1="Password didnot match"
            else:
                error1="Provide correct contact no. and email"
        #session['my_list'] = error1

    #return redirect(url_for("add_data"))
            return render_template("frontpage.html",error1=error1)
    else:
        error1="User Already Exsit"
        return render_template("frontpage.html",error1=error1)


@app.route('/comments', methods = ["POST"])
def comments():
    data=request.form["data"]
    name="abc"
    #uid="123"
    now = datetime.datetime.now()
    time= now.strftime("%H:%M,%d-%m-%Y")
    connection=mysql.get_db()
    cursor = connection.cursor()
    query="insert into comments(name,uid,data,time) values('"+name+"','"+uid+"','"+data+"','"+time+"');"
    cursor.execute(query)
    connection.commit()
    #return time
    return redirect(url_for('homepage'))


@app.route("/delete_comment",  methods=["POST"])
def delete_comment():
     if session['logged_in'] == True:
         delete=request.form["del"]
         connection=mysql.get_db()
         cursor = connection.cursor()
         print delete
         query="delete from comments where srno='"+delete+"';"
         cursor.execute(query)
         connection.commit()
         return redirect(url_for('homepage'))
    
     if session['logged_in'] == None:
        return "session closed"


"""
@app.route('/company_data/uploader', methods = ['GET', 'POST'])
def upload_file():
    #if request.method == 'POST':
    for file in request.files.getlist("file"):
        filename=file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print filename
        foo = Image.open('static/'+filename)  
        foo.size
        foo = foo.resize((600,600),Image.BICUBIC)
        foo.save('static/'+filename,optimize=True,quality=1000)
        connection=mysql.get_db()
        cursor = connection.cursor()
        sql = "insert into imgpath(imgpath) values('"+filename+"');"
        cursor.execute(sql)
        connection.commit()
    return redirect(url_for('homepage'))
"""          


if __name__=='__main__':
    #app.debug=True
    app.run()
