from  flask import Flask, abort, jsonify, redirect,render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os


app=Flask(__name__)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
  return response


motdepasse=quote_plus(os.getenv('db_password'))
host = os.getenv('hostname')
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:{}@{}:5432/bibliotheque'.format(motdepasse, host)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)


class Categorie(db.Model):
  __tablename__='categories'
  id=db.Column(db.Integer,primary_key=True)
  libelle_categorie=db.Column(db.String(100),nullable=False)
  livre=db.relationship('Livre',backref='categories',lazy=True)

  def format(self):
    return {
      'id':self.id,
      'libelle_categorie':self.libelle_categorie
      
    }

  def supprimer_cat(self):
    db.session.delete(self)
    db.session.commit()

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def update(self):
    db.session.commit()



class Livre(db.Model):
  __tablename__='livres'
  id=db.Column(db.Integer,primary_key=True)
  isbn=db.Column(db.String(50),nullable=False)
  titre=db.Column(db.String(50),nullable=False)
  date_publication=db.Column(db.Date,nullable=False)
  auteur=db.Column(db.String(50),nullable=False)
  editeur=db.Column(db.String(50),nullable=False)
  categorie_id=db.Column(db.Integer,db.ForeignKey(Categorie.id),nullable=False)

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def format(self):
    return {
      'id':self.id,
      'isbn':self.isbn,
      'titre':self.titre,
      'date_publication':self.date_publication,
      'auteur':self.auteur,
      'editeur':self.editeur,
      'categorie_id':self.categorie_id
      
    }

  def supprimer_liv(self):
    db.session.delete(self)
    db.session.commit()

  def update(self):
    db.session.commit()

db.create_all()



#======================================================================================================
#                                           affichage des listes
#======================================================================================================
@app.route('/livre', methods=['GET'])
def Liste_livres():
  livres=Livre.query.all()

  return jsonify({    
        "success":True,
        "livres":[et.format() for et in Livre.query.all()]
      })


@app.route('/categorie',methods=['GET'])
def Liste_categories():
  categories=Categorie.query.all()
  return jsonify({    
        "cotegories":[et.format() for et in Categorie.query.all()]
      })

#======================================================================================================
#                                           suppression
#======================================================================================================


@app.route('/supprimer_livre/<int:id>', methods=['DELETE'])
def supprimer_liv(id):
  livres=Livre.query.get(id)

  if livres is None:
    abort(404) #404 est le status code pour dire que la ressource n'existe pas

  else:
    livres.supprimer_liv()
    return jsonify({
      'success':True,
      'categories':[et.format for et in Livre.query.all()]
    })


@app.route('/supprimer_categorie/<int:id>', methods=['DELETE'])
def supprimer_cat(id):
  categories=Categorie.query.get(id)

  if categories is None:
    abort(404) #404 est le status code pour dire que la ressource n'existe pas

  else:
    categories.supprimer_cat()
    return jsonify({
      'success':True,
      'categories':[et.format() for et in Categorie.query.all()]
    })

                               




#======================================================================================================
#                                           ajout
#======================================================================================================


@app.route('/ajout_categorie', methods=['POST'])
def Ajout_categories():
  body=request.get_json()
  libelle=body.get('libelle_categorie','') 
  categories=Categorie(libelle_categorie=libelle)
  categories.insert()
  
  return jsonify({
    'success':True,
    'Liste categories':categories.format()
  })


@app.route('/ajout_livre', methods=['POST'])
def Ajout_livres():
  body=request.get_json()
  code=body.get('isbn','') 
  title=body.get('titre','')
  date=body.get('date_publication','')
  auteur=body.get('auteur','')
  editeur=body.get('editeur','')
  categorie=body.get('categorie_id','')
  livres=Livre(isbn=code, titre=title, date_publication=date,auteur=auteur,editeur=editeur,categorie_id=categorie)
  livres.insert()
  return jsonify({
    'success':True,
    'Liste categories':livres.format()
})



#======================================================================================================
#                                           recherche
#======================================================================================================

@app.route('/rechercher_categorie/<int:id>', methods=['GET'])
def selection_categorie(id):
  categories=Categorie.query.get(id)

#Verifions si cet Livre existe dans la base

  if categories is None:
    abort(404) #404 est le status code pour dire que la ressource n'existe pas

  else:
    return jsonify({
      'success':True,
      'categories':categories.format()
    })




@app.route('/rechercher_livre/<int:id>', methods=['GET']) 
def selection_livre(id):
  livres=Livre.query.get(id)

#Verifions si cet Livre existe dans la base

  if livres is None:
    abort(404) #404 est le status code pour dire que la ressource n'existe pas

  else:
    return jsonify({
      'success':True,
      'livres':livres.format()
    })



#======================================================================================================
#                                           Liste d'une categorie
#======================================================================================================

#Lister la liste des livres d'une categorie
@app.route('/livre_categorie/<int:num>', methods=['GET'])
def selection_li(num):
  livres=Livre.query.filter_by(categorie_id=num)
 # livres=Livre.query.get(categorie_id)

#Verifions si cet Livre existe dans la base

  if livres is None:
    abort(404) #404 est le status code pour dire que la ressource n'existe pas

  else:
    return jsonify({
      'success':True,
      'livres':[et.format() for et in livres]
    })



#======================================================================================================
#                                   Modifier les informations d'un livre
#======================================================================================================

@app.route('/modifier_livre/<int:id>', methods=['PATCH']) 
def modifier_liv(id):
  livres=Livre.query.get(id)

#Verifions si cet Livre existe dans la base

  if livres is None:
    abort(404) #404 est le status code pour dire que la ressource n'existe pas

  else:
    body=request.get_json()
    livres=Livre.query.get(id)
    livres.isbn=body.get('isbn')
    livres.titre=body.get('titre')
    livres.date_publication=body.get('date_publication')
    livres.auteur=body.get('auteur')
    livres.editeur=body.get('editeur')
    livres.categorie_id=body.get('categorie_id')

    livres.update()
    return jsonify({
      'success':True,
      'livres':livres.format()
    })



#======================================================================================================
#                                     Modifier le libelle d'une categorie
#======================================================================================================

@app.route('/modifier_categorie/<int:id>', methods=['PATCH']) 
def modifier_cat(id):
  categories=Categorie.query.get(id)

#Verifions si cet Livre existe dans la base

  if categories is None:
    abort(404) #404 est le status code pour dire que la ressource n'existe pas

  else:
    body=request.get_json()
    categories=Categorie.query.get(id)
    categories.libelle_categorie=body.get('libelle_categorie')
    
    categories.update()
    return jsonify({
      'success':True,
      'livres':categories.format()
    })


@app.errorhandler(404)
def server_error(error):
  return jsonify({
    'success':False,
    'error':404,
    'message': "Search not found"

  }),404

@app.errorhandler(400)
def server_error(error):
  return jsonify({
    'success':False,
    'error':400,
    'message': "Bad request"

  }),400

@app.errorhandler(500)
def server(error):
  return jsonify({
    'success':False,
    'error':500,
    'message': "Internal Server Error"

  }),500








