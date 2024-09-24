from typing import Tuple

from flask import Flask, jsonify, request, Response
import mockdb.mockdb_interface as db

app = Flask(__name__)


def create_response(
    data: dict = None, status: int = 200, message: str = ""
) -> Tuple[Response, int]:
    """Wraps response in a consistent format throughout the API.
    
    Format inspired by https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
    Modifications included:
    - make success a boolean since there's only 2 values
    - make message a single string since we will only use one message per response
    IMPORTANT: data must be a dictionary where:
    - the key is the name of the type of data
    - the value is the data itself

    :param data <str> optional data
    :param status <int> optional status code, defaults to 200
    :param message <str> optional message
    :returns tuple of Flask Response and int, which is what flask expects for a response
    """
    if type(data) is not dict and data is not None:
        raise TypeError("Data should be a dictionary 😞")

    response = {
        "code": status,
        "success": 200 <= status < 300,
        "message": message,
        "result": data,
    }
    return jsonify(response), status


"""
~~~~~~~~~~~~ API ~~~~~~~~~~~~
"""

@app.route("/")
def hello_world():
    return create_response({"content": "hello world!"})


@app.route("/mirror/<name>")
def mirror(name):
    data = {"name": name}
    return create_response(data)


# TODO: Implement the rest of the API here!

#### START

@app.route('/users', methods=['GET'])
def get_users():
    users = db.get('users')
    name = request.args.get('name')
    age = request.args.get('age')

    if name:
        users = [user for user in users if user['name'] == name]
    if age:
        users = [user for user in users if user['age'] == int(age)]

    return create_response({'users': users})

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = db.getById('users', user_id)
    if user:
        return create_response(user)
    else:
        return create_response(status=404, message='User not found')

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('age'):
        return create_response(status=400, message='Name and age are required')
    new_user = db.create('users', data)
    return create_response(new_user, status=201)

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    updated_user = db.updateById('users', user_id, data)
    if updated_user:
        return create_response(updated_user)
    else:
        return create_response(status=404, message='User not found')

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    deleted = db.deleteById('users', user_id)
    if deleted:
        return create_response(message='User deleted')
    else:
        return create_response(status=404, message='User not found')

#### END

"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == "__main__":
    app.run(debug=True)
