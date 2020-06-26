import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO - DONE uncomment the following line to initialize the database
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

# def check_credentials(permission):
#     '''Function that returns if user has permission
#     Args:
#         permission (str): persmission eg: 'get:drinks-detail'
#     Returns:
#         (bool): if permission in user's JWT
#     '''
#     # if no permissionsin token

#     # if permission not in users permissions

#     return True



## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
def get_drinks():
    # drinks = []
    # db_drinks = Drink.query.all()
    # for drink in db_drinks:
    #     drinks.append(drink.short())
    
    # return jsonify({
    #     'success': True,
    #     'drinks': drinks
    # })
    drinks = ['drink1', 'drink2']

    return jsonify({
        'success': True,
        'drinks': drinks
    })

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks-detail', methods=['GET'])
@requires_auth(permission='get:drinks-detail')
def get_drinks_detail(permission='get:drinks-detail'):
    # drinks = []
    # db_drinks = Drink.query.all()
    # for drink in db_drinks:
    #     drinks.append(drink.short())
    
    # return jsonify({
    #     'success': True,
    #     'drinks': drinks
    # })
    drs = Drink.query.all()
    drinks = [d.short() for d in drs]

    return jsonify({
        'success': True,
        'drinks': drinks
    })


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks', methods=['POST'])
@requires_auth(permission='post:drinks')
def create_drink(permission='post:drinks'):
    data = request.get_json()
    print(f'post drink data: {data}')
    title = data['title']
    recipe = json.dumps([data['recipe']])
    #title = 'harder wiskey coke'
    #recipe = 'more whiskey'
    print('title: ', title)
    print('recipe: ', recipe)


    drink = Drink(title=title, recipe=recipe)
    #{'color': r['color'], 'parts': r['parts']}
    drink.insert()

    drinks = Drink.query.all()
    for drink in drinks: 
        print(f'drink: {drink.title} id: {drink.id}')

    #print('\n\n\n created drink: ', drink , '\n\n\n')

    # return jsonify({
    #     'success': True,
    #     'drinks': drink.long()
    # })

    return jsonify({
        'success': True,
        'drinks': [drink.short()]
    })




'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth(permission='patch:drinks')
def patch_drink(permission='patch:drinks', id=id):
    print ('hello')
    drink = Drink.query.filter(Drink.id==id).one_or_none()
    if drink == None:
        abort(404)
    else:
        data = request.get_json()
        print(f'data {data}')
        if 'title' in data:
            title = data['title']
            drink.title = title
        if 'recipe' in data:
            recipe = json.dumps([data['recipe']])
            drink.recipe = recipe

        drink.update()

        return jsonify({
             'success': True,
             'drinks': [drink.long()]
        })




'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth(permission='delete:drinks')
def delete_drink(permission='delete:drinks', id=id):
    print ('hello ima delete son')
    drink = Drink.query.filter(Drink.id == id).one_or_none()

    if drink == None:
        abort(404)
    else:
        drink.delete()

    return jsonify({
        'success': True,
        "delete": id
    })



## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
    'success': False,
    'error': 404,
    'message': "resource not found"
    }), 404


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
    'success': False,
    'error': 401,
    'message': "unauthorized"
}), 401


