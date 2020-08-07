import subprocess
import sqlite3
from flask import Flask,request,render_template,redirect
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
    country = request.form['input1']
    city = request.form['input2']
    keyword = request.form['input3']
    if request.method == 'POST':
        if country!='' and city!='' and keyword!='':
           with open('country.txt', 'a') as f:
                f.write(str(country)+"\n")
           with open('city.txt', 'a') as f:
               f.write(str(city)+"\n")
           with open('keyword.txt', 'a') as f:
               f.write(str(keyword)+"\n")
    # return render_template('home.html', find=find,near=near)
    return redirect('http://127.0.0.1:5000/home')


@app.route('/run')
def run():
    """
    Run spider in another process and store items in file. Simply issue command:

    > scrapy crawl dmoz -o "output.json"

    wait for  this command to finish, and read output.json to client.
    """

    # p = subprocess.Popen(...)
    # """
    # A None value indicates that the process hasn't terminated yet.
    # """
    # poll = p.poll()
    # if poll == None:
    spider_name = "search"
    subprocess.check_output(['scrapy', 'crawl', spider_name])

    return redirect('http://127.0.0.1:5000/view')
    # with open("output.json") as items_file:
    #     return items_file.read()

@app.route("/view")
def view():
    con = sqlite3.connect("searchdetail.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from detail")
    rows = cur.fetchall()
    return render_template("index.html",rows = rows)

if __name__ == '__main__':
    app.run(debug=True)