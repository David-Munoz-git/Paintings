from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.painting import Painting

#==============================
#add a new painting route
#==============================

@app.route('/addpainting/')
def add_painting():
  if "user_id" not in session:
    flash("You need to log in or register before you enjoy this site")
    return redirect("/")

  return render_template("addpaintings.html")


@app.route("/addpaintingform", methods=["POST"])
def add_painting_form():

  data = {
    "title" : request.form["title"],
    "description" : request.form["description"],
    "price" : request.form["price"],
    "users_id" : session["user_id"],
  }

  if not Painting.validate_form(request.form):
    return redirect("/addpainting")

  Painting.addpainting(data)

  return redirect("/dashboard")



#=========================
#edit my paintings routes
#=========================

@app.route("/painting/<int:painting_id>/edit")
def edit_painting(painting_id):
  if "user_id" not in session:
    flash("You need to log in or register before you enjoy this site")
    return redirect("/")

  user_data = {
    "user_id" : session['user_id']
  }
  data = {
    "painting_id" : painting_id
  }
  
  user = User.get_user(user_data)
  painting = Painting.get_one_painting(data)
  return render_template("editpainting.html", painting = painting, user = user)

@app.route("/edit/<int:painting_id>/update", methods=["POST"])
def update_painting(painting_id):
  data = {
    "title" : request.form["title"],
    "description" : request.form["description"],
    "price" : request.form["price"],
    "painting_id" : painting_id,

    "users_id" : session["user_id"],
  }

  if not Painting.validate_form(request.form):
    return redirect(f"/painting/{painting_id}/edit")
  Painting.update_painting(data)
  return redirect("/dashboard")


#=========================
#  paintings info route
#=========================

@app.route("/painting/<int:painting_id>")
def painting_info(painting_id):

  data = {
    "painting_id" : painting_id
  }

  painting = Painting.get_info(data)
  return render_template("mypainting.html", painting = painting)



#=========================
#DELETE a band route
#=========================

@app.route('/painting/delete/<int:painting_id>')
def delete(painting_id):
  query_data = {
  'painting_id' : painting_id
}
  Painting.delete(query_data)
  return redirect ('/dashboard')