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
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks')
@requires_auth("get:drinks")
def get_drinks(payload):
    start_code = 500
    try:
        # Retrieve drinks
        drinks = Drink.query.all()
    except Exception as e:
        print(f"{e}")
        abort(start_code)
    else:
        return jsonify({
            "success": True,
            "drinks": [drink.short() for drink in drinks]
        })


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail')
@requires_auth("get:drinks-detail")
def get_drinks_detail(payload):
    start_code = 500
    try:
        # Retrieve drinks
        drinks = Drink.query.all()
    except Exception as e:
        print(f"{e}")
        abort(start_code)
    else:
        return jsonify({
            "success": True,
            "drinks": [drink.long() for drink in drinks]
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
@requires_auth("post:drinks")
def get_create_drink(payload):
    start_code = 500
    try:
        body = request.get_json()
        #  Create drink object
        drink = Drink(
            title= body["title"],
            recipe= json.dumps(body["recipe"])
            ) 
        drink.insert()

        # Retrieve drinks
        drinks = Drink.query.all()
    except Exception as e:
        print(f"{e}")
        abort(start_code)
    else:
        return jsonify({
            "success": True,
            "drinks": [drink.long() for drink in drinks]
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
@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth("patch:drinks")
def update_drink(payload, drink_id:int):
    start_code = 500
    try:
        body = request.get_json()
        #  update drink object
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
        drink.title = body['title']
        drink.update()

        # Retrieve drinks
        drinks = Drink.query.all()
    except Exception as e:
        print(f"{e}")
        abort(start_code)
    else:
        return jsonify({
            "success": True,
            "drinks": [drink.long() for drink in drinks]
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
@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth("delete:drinks")
def get_delete_drink(payload, drink_id:int):
    start_code = 500
    try:
        drink = Drink.query.get(drink_id)
        drink.delete()
    except Exception as e:
        print(f"{e}")
        abort(start_code)
    else:
        return jsonify({
            "success": True,
            "delete": drink_id
        })


# Error Handling
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
@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal Server Error"
        }), 500

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": ""
        }), 422

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''
@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
        }), 404


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(422)
def method_not_allow(error):
    raise AuthError({
                'code': 'Invalid_request',
                'description': 'Method not Allowed.'
            }, 422)

