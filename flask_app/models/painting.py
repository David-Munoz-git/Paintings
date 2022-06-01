from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models import user
from flask import flash



class Painting:
  db = 'paintings_schema'  # variable connected to schema

  def __init__(self, data):
      self.id = data['id']

      self.title = data['title']
      self.description = data['description']
      self.price = data['price']

      self.users_id = data['users_id']
      #might need this to use the left join with paintings
      self.users = {}

# ===========================================================
# Validation
# ===========================================================


  @staticmethod
  def validate_form(form_data):
    is_valid = True

    if len(form_data["title"]) < 2:
      flash("Title Name must be atleast 2 characters long")
      is_valid = False

    if len(form_data["description"]) < 10:
      flash("Description must be atleast 5 characters long")
      is_valid = False

    if len(form_data["price"]) < 0:
      flash("Price must be greater then 0")
      is_valid = False

    return is_valid


#============================
#ADD A Painting
#============================

  @classmethod
  def addpainting(cls, data):
    query = "INSERT INTO paintings (title, description, price, created_at, updated_at, users_id) VALUES(%(title)s, %(description)s, %(price)s, NOW(), NOW(), %(users_id)s)"
    results = connectToMySQL(cls.db).query_db(query, data)
    return results


#==============================
#GET ALL PAINTINGS AND USERS
#==============================

  @classmethod
  def get_all(cls):
    query = "SELECT * FROM paintings LEFT JOIN users ON paintings.users_id = users.id ;"
    results = connectToMySQL(cls.db).query_db(query)

    all_paintings = []

    for row in results:
      painting = cls(row)

      user_data = {
        "id" : row['users.id'],
        "first_name" : row['first_name'],
        "last_name" : row['last_name'],
        "email" : row['email'],
        "password" : row['password'],
        "created_at" : row['users.created_at'],
        "updated_at" : row['users.updated_at']
      }
      painting.user = user.User(user_data)
      all_paintings.append(painting)
    return all_paintings


#==============================
#GET ONE PAINTING 
#==============================
  @classmethod
  def get_one_painting(cls, Data):
    query = "SELECT * FROM paintings WHERE id = %(painting_id)s;"
    results = connectToMySQL(cls.db).query_db(query, Data)
    return cls(results[0])


#==============================
#EDIT PAINTINGS
#==============================

  @classmethod
  def update_painting(cls,data):
    query = "UPDATE paintings SET title=%(title)s, description=%(description)s, price=%(price)s, updated_at=NOW() WHERE id = %(painting_id)s;"
    results = connectToMySQL(cls.db).query_db(query, data)
    return results


#==============================
# PAINTINGS INFO
#==============================


  @classmethod
  def get_info(cls, data):
    query = "SELECT * FROM paintings LEFT JOIN users ON paintings.users_id = users.id WHERE paintings.id = %(painting_id)s"
    results = connectToMySQL(cls.db).query_db(query, data)

    painting = cls(results[0])

    user_data = {
      "id" : results[0]['users.id'],
      "first_name" : results[0]['first_name'],
      "last_name" : results[0]['last_name'],
      "email" : results[0]['email'],
      "password" : results[0]['password'],
      "created_at" : results[0]['users.created_at'],
      "updated_at" : results[0]['users.updated_at']
      }

    painting.user = user.User(user_data)

    return painting





#==============================
#DELETE PANTINGS
#==============================

  @classmethod
  def delete(cls,data):
    query  = "DELETE FROM paintings WHERE id = %(painting_id)s;"
    return connectToMySQL(cls.db).query_db(query,data)
