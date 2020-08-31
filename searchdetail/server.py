import subprocess
import sqlite3
import pandas as pd
from flask import Flask,request,render_template,redirect,send_file,send_from_directory
import os
import time
# import requests
app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(e):
    return redirect('http://127.0.0.1:5000/home')

@app.route('/')
def home():
    return redirect('http://127.0.0.1:5000/home')

@app.route('/home')
def my_form():
    return render_template('home.html')

@app.route('/home', methods=['POST'])
def my_form_post():
    country_striped = request.form['input1']
    city_striped = request.form['input2']
    keyword_striped = request.form['input3']

    country = country_striped.strip()
    city = city_striped.strip()
    keyword = keyword_striped.strip()

    if country != '' and city != '' and keyword != '':
        if (os.stat(os.path.abspath(os.curdir)+'\country.txt').st_size != 0):
            with open(os.path.abspath(os.curdir)+'\country.txt', 'a') as f:
                f.write('\n')
        if(os.stat(os.path.abspath(os.curdir)+'\city.txt').st_size != 0):
            with open(os.path.abspath(os.curdir)+'\city.txt', 'a') as f:
                f.write('\n')
        if (os.stat(os.path.abspath(os.curdir)+'\keyword.txt').st_size != 0):
            with open(os.path.abspath(os.curdir)+'\keyword.txt', 'a') as f:
                f.write('\n')
        new_country=''
        new_city=''
        new_keyword=''

        for b in country:
            if(b=='\n'):
                new_country+=''
            else:
                new_country+=b

        for b in city:
            if(b=='\n'):
                new_city+=''
            else:
                new_city+=b

        for b in keyword:
            if(b=='\n'):
                new_keyword += ''
            else:
                new_keyword += b

        if request.method == 'POST':
            if country!='' and city!='' and keyword!='':
               with open(os.path.abspath(os.curdir)+'\country.txt', 'a') as f:
                    f.write(str(new_country))
               with open(os.path.abspath(os.curdir)+'\city.txt', 'a') as f:
                   f.write(str(new_city))
               with open(os.path.abspath(os.curdir)+'\keyword.txt', 'a') as f:
                   f.write(str(new_keyword))
    # return render_template('home.html', find=find,near=near)
    return redirect('http://127.0.0.1:5000/home')

@app.route("/view")
def view_get():
    con = sqlite3.connect(os.path.abspath(os.curdir)+"\searchdetail.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from detail")
    rows = cur.fetchall()

    return render_template("index.html", rows=rows)

@app.route("/delete")
def delete_all():
    con = sqlite3.connect(os.path.abspath(os.curdir)+"\searchdetail.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from detail")

    cur.execute('DELETE FROM detail;', )
    # rows = cur.fetchall()
    con.commit()

    return redirect('http://127.0.0.1:5000/view')


@app.route("/convertcsv")
def csv():
    con = sqlite3.connect(os.path.abspath(os.curdir)+"\searchdetail.db")
    con.row_factory = sqlite3.Row

    df = pd.read_sql_query("SELECT * FROM detail", con)
    print(df)
    print(type(df))

    with open(os.path.abspath(os.curdir)+'\static\details.csv', "w") as my_empty_csv:
        # now you have an empty file already
        pass

    df.to_csv(os.path.abspath(os.curdir)+'\static\details.csv', index=False)

    return redirect('http://127.0.0.1:5000/view')

# @app.route("/down")
# def downloadcsv():
#     con = sqlite3.connect(os.path.abspath(os.curdir) + "\searchdetail.db")
#     con.row_factory = sqlite3.Row
#
#     df = pd.read_sql_query("SELECT * FROM detail", con)
#     print(df)
#     print(type(df))
#     df.to_csv(os.path.abspath(os.curdir) + '\details.csv', index=False)
#     time.sleep(20)
#     print("for downloading csv")
# #
#     return send_file(os.path.abspath(os.curdir)+'\static\details.csv',
#                      mimetype='text/csv',
#                      attachment_filename='details',
#                      as_attachment=True)
    # print('hi')
    # return send_file(os.path.abspath(os.curdir)+'\static\details.csv',mimetype='text/csv',
    #                      attachment_filename='details.csv',as_attachment=True)
    # filename = 'details.csv'
    # uploads = os.path.abspath(os.curdir)+'\static'
    # return send_from_directory(directory=uploads, filename=filename)


@app.route("/deletebysearch", methods=['POST'])
def deletebysearch():
    key_striped = request.form['del']

    key = key_striped.strip()
    print(key)
    print(type(key))
    if(key!=''):
        sqliteConnection = sqlite3.connect(os.path.abspath(os.curdir)+'\searchdetail.db')
        cursor = sqliteConnection.cursor()

        # sql_delete_query = "SELECT * FROM detail WHERE keyword LIKE '%Dentist%'"
        # query = str("DELETE FROM detail WHERE keyword LIKE"+ " %{".format(key))
        query = "DELETE FROM detail WHERE keyword LIKE '%{}%'".format(key)
        sql_delete_query = query
        cursor.execute(sql_delete_query)
        sqliteConnection.commit()

    return redirect('http://127.0.0.1:5000/view')


@app.route("/view", methods=['POST'])
def view():
    con = sqlite3.connect(os.path.abspath(os.curdir)+"\searchdetail.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()



    # if request.method == 'POST':
    country_striped = request.form['input1']
    city_striped = request.form['input2']
    keyword_striped = request.form['input3']

    country = country_striped.strip()
    city = city_striped.strip()
    keyword = keyword_striped.strip()

    if(country!='' and city!='' and keyword!=''):
        # cur.execute("select * from detail where country")
        cur.execute("SELECT * FROM detail WHERE country=? and city=? and keyword=?", (country,city,keyword,))
        rows = cur.fetchall()
        if(len(rows)==0):
            cur.execute("select * from detail")
            rows = cur.fetchall()
    else:
        cur.execute("select * from detail")
        rows = cur.fetchall()
    return render_template("index.html",rows = rows)

if __name__ == '__main__':
    app.run(debug=True)