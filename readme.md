# API GESTION DE BIBLIOTHEQUE

## Getting Started

### Installing Dependencies

#### Python 3.8.5
#### pip 20.0.2 from /usr/lib/python3/dist-packages/pip (python 3.8)

Suivez les instructions pour installer la dernière version de python sur votre platformeen allant sur[python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Environnement virtuel

Nous recommandons d'utiliser un environnement virtuel à chaque fois que vous utilisez python pour vos projets. Cela vous permet de garder une independance et une organisation pour chaque projet. Vous pouvez retrouver les instructions vous permettant de configurer votre environnement virtuel sur [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### Les dependances pip

Une fois que vous avez installé le setup de votre environnement , installez les dependances en executant directement les commandes qui suivent:

```bash
pip install -r requirements.txt
or
pip3 install -r requirements.txt
```

##### Les clés de dependance 

- [Flask](http://flask.pocoo.org/)  Flask est un micro framework open-source de développement web en Python. Il est classé comme microframework car il est très léger. Flask a pour objectif de garder un noyau simple mais extensible.


- [SQLAlchemy](https://www.sqlalchemy.org/) SQLAlchemy est un toolkit open source SQL et un mapping objet-relationnel (ORM) écrit en Python et publié sous licence MIT. 



## Lancement du serveur

Pour ouvrir  `bibliotheque` assurez vous dans un premier temps que votre environnement virtuel fonctionne.

Pour lancer le serceur sur Linux ou Mac, executez les commandes suivantes:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
Pour lancer le serveur sous Windows, executez les commandes suivantes:

```bash
set FLASK_APP=flaskr
set FLASK_ENV=development
flask run
```

Affecter à `FLASK_ENV` la variable `development`  permettra de detecter les changements afin de redemarrer automatiquement le serveur.

Affacter à  `FLASK_APP` le nom de votre ficher pour lui permettre de pouvoir l'exporter

## REFERENCE API

Pour commencer

Base URL: Pour le moment cet api ne peut executé qu'en locale. Le backend de l'app est par défaut, http://localhost:5000.

## Gestion des erreurs
Les erreurs retournent un fichier JSON dans le format suivant:
{
    "success":False
    "error": 400
    "message":"Bad request"
}

L'API retourne trois types d'erreurs si la requête lancée echoue
. 400: Bad request
. 500: Internal server error
. 404: Not found

## Les routes
. ## GET/livre

    GENERAL:
       Cette route retourne la liste des livres contenus dans la base de données
        
    Exemple: curl http://localhost:5000/livre

        {

    "livres": [
        {
            "auteur": "Rousseau",
            "categorie_id": 6,
            "date_publication": "Tue, 20 Oct 2020 00:00:00 GMT",
            "editeur": "Brice",
            "id": 4,
            "isbn": "kdb14",
            "titre": "Le Monde"
        },
        {
            "auteur": "JJ",
            "categorie_id": 2,
            "date_publication": "Thu, 15 Oct 2020 00:00:00 GMT",
            "editeur": "Marc",
            "id": 3,
            "isbn": "kd4ki4",
            "titre": "Revolte"
        }
    ],
    "success": true

}

 .## GET/categorie

    GENERAL:
       Cette route retourne la liste des categorie des livres contenus dans la base de données
        
    Exemple: curl http://localhost:5000/categorie


{
    "cotegories": [
        {
            "id": 3,
            "libelle_categorie": "aventure"
        },
        {
            "id": 4,
            "libelle_categorie": "romance"
        },
        {
            "id": 5,
            "libelle_categorie": ""
        },
        {
            "id": 6,
            "libelle_categorie": "guerre"
        },
        {
            "id": 2,
            "libelle_categorie": "Negritude"
        }
    ]
}

```

. ## DELETE/supprimer_livre (id)

    GENERAL:
        Supprimer le livre en indiquant sont id s'il existe à la fin de la route. Retourne les informations sur le livre supprimé, success value
       
        Results are paginated in groups of 10. include a request argument to choose page number, starting from 1.

        Exemple: 
        curl -X DELETE http://localhost:5000/supprimer_livre/10
```
    {
        {
        "deleted": 3,
         "livres": {
        "auteur": "JJ",
        "categorie_id": 2,
        "date_publication": "Thu, 15 Oct 2020 00:00:00 GMT",
        "editeur": "Marc",
        "id": 3,
        "isbn": "kd4ki4",
        "titre": "Revolte"
    },
    "success": true
        },

. ## DELETE/supprimer_categorie (id)

    GENERAL:
        Supprimer la categorie en indiquant sont id s'il existe à la fin de la route. Retourne les informations sur la categorie supprimé, success value
       
        Exemple:
        ``` curl -X DELETE http://localhost:5000/supprimer_categorie/3
```

    
        {
        "deleted": 3,
        {
    "categories": {
        "id": 3,
        "libelle_categorie": "aventure"
    },
    "success": true

        },
        }
```

. ##PATCH/modifier_livre(id)
  GENERAL:
 Cette route modifie les caractéristiques d'un livre et renvois le livres sur lequel la modification a ete faite
  Exemple
    ``` curl -X PATCH http://localhost:5000/modifier_livre/4 -H "Content-Type:application/json" -d "{"auteur": "Rousseau",
     {   
        "{"categorie_id": 6,
        "date_publication": "Tue, 20 Oct 2020 00:00:00 GMT",
        "editeur": "Borice",
        "id": 4,
        "isbn": "kdb14",
        "titre": "Le Monde"}"
  ```
  ```
   
    }
    ```


. ##PATCH/modifier_categorie(id)
  GENERAL:
 Cette route modifie les caractéristiques d'une categorie et renvois la cetegorie  sur lequel la modification a ete faite
  Exemple
    ``` curl -X PATCH http://localhost:5000/modifier_livre/4 -H "Content-Type:application/json" -d "{"libelle_categorie": "Guerre",}
     {   
       {
    "categories": {
        "id": 4,
        "libelle_categorie": "Guerre"
    },
    "success": true
}
  ```
  ```
   
    }
    ```

. ##GET/livre_categorie(num) (num est une variable de type entier qui permettra de recuperer la valeur de l'id de la ctegorie dont on veut afficher la liste des livres)
  GENERAL:
 Cette route permet d'afficher la liste des livre d'une cetegorie en passand l'id de la categorie en parametre
  Exemple
    ``` curl -X GET http://localhost:5000/livre_categorie/2

    {
    "livres": [
        {
            "auteur": "JJ",
            "categorie_id": 2,
            "date_publication": "Thu, 15 Oct 2020 00:00:00 GMT",
            "editeur": "Marc",
            "id": 3,
            "isbn": "kd4ki4",
            "titre": "Revolte"
        }
    ],
    "success": true
}
}
  ```
  ```
   
    }
    ```




. ##POST/ajout_categorie
  GENERAL:
 Cette route permet d'ajouter une nouvelle categorie
  Exemple
    ``` curl -X PATCH http://localhost:5000/ajout_categorie/{
        "libelle_categorie":"Guerre",}
     {   
       {
    "categories": {
        "id": 6,
        "libelle_categorie": "Guerre"
    },
    "success": true
}
  ```
  ```
   
    }
    ```

. ##POST/ajout_livre
  GENERAL:
 Cette route permet d'ajouter un nouveau livre
  Exemple
    ``` curl -X PATCH http://localhost:5000/ajout_livre/{
       "livres": [
        {
            "auteur": "Rousseau",
            "categorie_id": 6,
            "date_publication": "Tue, 20 Oct 2020 00:00:00 GMT",
            "editeur": "Brice",
            "id": 4,
            "isbn": "kdb14",
            "titre": "Le Monde"
        },}
     {   
   "livres": [
        {
            "auteur": "Rousseau",
            "categorie_id": 6,
            "date_publication": "Tue, 20 Oct 2020 00:00:00 GMT",
            "editeur": "Brice",
            "id": 4,
            "isbn": "kdb14",
            "titre": "Le Monde"
        },
        {
            "auteur": "JJ",
            "categorie_id": 2,
            "date_publication": "Thu, 15 Oct 2020 00:00:00 GMT",
            "editeur": "Marc",
            "id": 3,
            "isbn": "kd4ki4",
            "titre": "Revolte"
        }
    ],
    "success": true
}
  ```
  ```
   
    }
    ```




