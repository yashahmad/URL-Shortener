from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from helper import id_generator

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urlshortener.db'
db = SQLAlchemy(app)

class Url(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	long_url = db.Column(db.String(),nullable=False)
	short_url = db.Column(db.String(),unique=True, nullable=False)
	views = db.Column(db.Integer())

@app.route('/', methods=['GET','POST'])
def index():
	if request.method == 'POST':
		url = request.form['url']
		# print('URL', url)
		# print(id_generator())
		try:
			short_url = id_generator()
			u=Url(long_url=url,short_url=short_url,views=1)
			db.session.add(u)
			db.session.commit()
			msg = "Successfully converted"
			converted_url = "https://urlshortener.herokuapp.com/"+short_url
		except:
			#Try again after sometime
			msg = "Server at it's best performance. Try again later"
		return render_template("index.html",msg=msg,url=converted_url)
	return render_template("index.html")

@app.route('/<string:short_url>',methods=['GET'])
def view(short_url):
	s = Url.query.filter_by(short_url=short_url).first()
	s.views += 1
	db.session.commit()
	return redirect(s.long_url,301)

@app.route('/admin', methods=['GET'])
def admin():
	s = Url.query.all()
	return render_template("admin.html",context=s)

if __name__ == "__main__":
	app.run()
