#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources=r'/ws/*')

users = [
    {
        "RefNo": 1,
        "ID": "bofa",
        "FULLNAME": "Bofa Alsarah",
        "passportno": "112233",
        "Nationality": "Libya"
    }
]

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/ws/staff/profile', methods=['GET'])
def get_users():
    return jsonify(users)

@app.route('/ws/staff/profile/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = [user for user in users if user['RefNo'] == user_id]
    if len(user) == 0:
        abort(404)
    return jsonify(user[0])



@app.route('/ws/staff/profile', methods=['POST'])
def create_user():
    if not request.json or not 'passportno' in request.json:
        abort(400)
    user = {
        'RefNo': users[-1]['RefNo'] + 1,
        'ID': request.json.get('ID', ""),
        'FULLNAME' : request.json.get('FULLNAME', ""),
        'passportno': request.json.get('passportno', ""),
        'Nationality' : request.json.get('Nationality', "")
        }
    users.append(user)
    return jsonify(user), 201

@app.route('/ws/staff/profile/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = [user for user in users if user['RefNo'] == user_id]
    if len(user) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'RefNo' in request.json and type(request.json['RefNo']) is not str:
        abort(400)
    if 'ID' in request.json and type(request.json['ID']) is not str:
        abort(400)
    if 'FULLNAME' in request.json and type(request.json['FULLNAME']) is not str:
        abort(400)
    if 'passportno' in request.json and type(request.json['passportno']) is not str:
        abort(400)
    if 'Nationality' in request.json and type(request.json['Nationality']) is not str:
        abort(400)
    user[0]['ID'] = request.json.get('ID', user[0]['ID'])
    user[0]['RefNo'] = request.json.get('RefNo', user[0]['RefNo'])
    user[0]['FULLNAME'] = request.json.get('FULLNAME', user[0]['FULLNAME'])
    user[0]['passportno'] = request.json.get('passportno', user[0]['passportno'])
    user[0]['Nationality'] = request.json.get('Nationality', user[0]['Nationality'])

    return jsonify({'user': user[0]})


@app.route('/ws/staff/profile/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = [user for user in users if user['RefNo'] == user_id]
    if len(user) == 0:
        abort(404)
    users.remove(user[0])
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)