from flask import Flask,render_template,flash,request, redirect, url_for
from . import app
from blog.models import Entry,db
from blog.forms import EntryForm
from faker import Faker

@app.route("/")
def index():
   #generate_entries(10)
   all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
   return render_template("homepage.html", all_posts=all_posts)

@app.route("/entry_form/<int:entry_id>", methods=["GET", "POST"])
def entry_form(entry_id):
   if entry_id==0:
        form = EntryForm()
        errors = None
        if request.method == 'POST':
            if form.validate_on_submit():
                entry = Entry()
                entry.title=form.title.data
                entry.body=form.body.data
                entry.is_published=form.is_published.data
                    
                db.session.add(entry)
                db.session.commit()
                flash('Record was successfully created')
                return redirect(url_for('index'))
            else:
                errors = form.errors
        return render_template("entry_form.html", form=form, errors=errors)
   entry = Entry.query.filter_by(id=entry_id).first_or_404()
   form = EntryForm(obj=entry)
   errors = None
   if request.method == 'POST':
       if form.validate_on_submit():
           form.populate_obj(entry)
           db.session.commit()
           flash('Record was successfully updated')
           return redirect(url_for('index'))
       else:
           errors = form.errors
   return render_template("entry_form.html", form=form, errors=errors)

def generate_entries(how_many=10):
   fake = Faker()

   for i in range(how_many):
      post = Entry(
            title=fake.sentence(),
            body='\n'.join(fake.paragraphs(15)),
            is_published=True
      )
      db.session.add(post)
   db.session.commit()

