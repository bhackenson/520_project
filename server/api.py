from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import secrets
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from functools import wraps
import datetime
from datetime import timezone
from dotenv import load_dotenv
from mongoengine import connect
from mongoengine.errors import (
    NotUniqueError,
    ValidationError,
    DoesNotExist,
    MultipleObjectsReturned,
    FieldDoesNotExist,
    OperationError,
    LookUpError,
    SaveConditionError,
    InvalidQueryError
)
from model import User, Project, Progression
import os
from generator import build_model, generate_chord_progression, randomize_seed, transpose_chord, show_chord_name, show_melody_notes

app = Flask(__name__)
CORS(app)

load_dotenv()

model1 = None
tone1 = None
history1 = None

model2 = None
tone2 = None
history2 = None

major_keys = ["G-", 'B', 'E', 'A', 'D', 'G', 'C', 'F', 'B-', 'E-', 'A-', 'D-']
minor_keys = ['e-', 'g#', 'c#', 'f#', 'b', 'e', 'a', 'd', 'g', 'c', 'f', 'b-']

with app.app_context():
    model1, tone1, history1 = build_model('major')
    model2, tone2, history2 = build_model('minor')

@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({'error': 'Unexpected error', 'description': str(e)}), 500

# user authentication
def authenticate_user(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            token = request.headers.get("Authorization", None)
            if not token:
                return jsonify({"error": "unauthorized"}), 400
            decoded = jwt.decode(token.split(' ')[1], os.getenv('JWT_KEY'), algorithms=['HS256'])
            request.user = decoded
            return f(*args, **kwargs)
        except ExpiredSignatureError:
            return jsonify({"error": "expired token"}), 400
        except InvalidTokenError:
            return jsonify({"error": "invalid token"}), 400
    return wrapper

# get user info
@app.route('/api/get_user', methods=['GET'])
@authenticate_user
def get_user():
    userid = request.user['userid']
    user = User.objects(userid=userid).first()
    if user == None:
        return jsonify({"error": "could not find user"}), 404
    
    return jsonify({"status": "OK", "user": user.to_json()}), 200

# user login
# request input: {"username": "username", "password": "password"}
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = User.objects(username=username).first()
    if user == None:
        return jsonify({"error": "invalid username"}), 404
    if user.check_pw(password):
        token = jwt.encode({"userid": user.userid, "exp": datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(hours=1)}, os.getenv('JWT_KEY'), algorithm='HS256')
        return jsonify({"status": "OK", "token": token}), 200
    else:
        return jsonify({"error": "Incorrect password"}), 404

# logging out user
@app.route('/api/logout', methods=['POST'])
@authenticate_user
def logout():
    request.user = None
    token = jwt.encode({"exp": datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(seconds=1)}, os.getenv('JWT_KEY'), algorithm='HS256')
    return jsonify({"status": "OK", "token": token}), 200

# request input: {"username": "username", "password": "password"}
# creating/signing up/registering a new user
@app.route('/api/create_user', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']

        id = secrets.token_hex(16)
        user = User(userid=id, username=username, password=password)
        user.save()

        return jsonify({"status": "OK", "user": user.to_json()}), 200
    
    except NotUniqueError:
        return jsonify({"error": "not unique"}), 404
    except ValidationError:
        return jsonify({"error": "validation error"}), 404
    except DoesNotExist:
        return jsonify({"error": "does not exist"}), 404
    except MultipleObjectsReturned:
        return jsonify({"error": "multiple objects returned"}), 404
    except FieldDoesNotExist:
        return jsonify({"error": "field does not exist"}), 404
    except OperationError:
        return jsonify({"error": "operation error"}), 404
    except LookUpError:
        return jsonify({"error": "lookup error"}), 404
    except SaveConditionError:
        return jsonify({"error": "save condition error"}), 404
    except InvalidQueryError:
        return jsonify({"error": "invalid query error"}), 404

# request input: {"name": "project_name", "date": "project_date"}
# creating a new project
@app.route('/api/create_project', methods=['POST'])
@authenticate_user
def create_project():
    data = request.get_json()
    name = data['name']
    date = data['date']

    userid = request.user['userid']

    user = User.objects(userid=userid).first()
    if user == None:
        return jsonify({"error": "could not find user"}), 404
    
    projid = secrets.token_hex(16)

    projects = user.projects
    project = Project(projid=projid, name=name, date=date)

    projects.append(project)
    user.save()

    return jsonify({"status": "OK", "projid": projid, "project": project.to_json()}), 200

# request input: {"projid": "proj_id", "name": "prog_name", "key_signature": "B-", "mode": "major", "time_signature": "4/4", "tempo": 120}
# create a new progression
@app.route('/api/create_progression', methods=['POST'])
@authenticate_user
def generate_progression():
    data = request.get_json()
    projid = data['projid']
    name = data['name']
    key = data['key_signature']
    mode = data['mode']
    time_sig = data['time_signature']
    tempo = data['tempo']

    userid = request.user['userid']

    user = User.objects(userid=userid).first()
    if user == None:
        return jsonify({"error": "could not find user"}), 404
    if not any(proj.projid == projid for proj in user.projects):
        return jsonify({"error": "could not find project"}), 404
    if (key not in major_keys and key not in minor_keys):
        return jsonify({"error": "invalid key"}), 404
    
    user_project = next(project for project in user.projects if project.projid == projid)
    progid = secrets.token_hex(16)

    if (key in major_keys):
        new_prog, chord_strings = generate_chord_progression(model1, randomize_seed(tone1), 4)
        # return jsonify({"chords": [show_chord_name(c) for c in [transpose_chord(k, tone1, key) for k in chord_strings]]}), 201
    else:
        new_prog, chord_strings = generate_chord_progression(model2, randomize_seed(tone2), 4)
        # return jsonify({"chords": [show_chord_name(c) for c in [transpose_chord(k, tone2, key) for k in chord_strings]]}), 201
    progression = Progression(progid=progid, name=name, key_signature=key, mode=mode, time_signature=time_sig, tempo=tempo,
                                chords=[show_chord_name(c) for c in [transpose_chord(k, tone2, key) for k in chord_strings]],
                                melody=[show_melody_notes(c) for c in [transpose_chord(k, tone2, key) for k in chord_strings]])

    user_project.progressions.append(progression)
    user.save()

    return jsonify({"status": "OK", "progid": progid, "progression": progression.to_json()}), 200

"""
request input:
{
   "projid": "proj_id",
   "progid": "prog_id",
   "name": "new_prog_name",
   "key_signature": "B-",
   "mode": "minor",
   "time_signature": "3/4",
   "tempo": 100,
   "chords": [
       {
           "chord": "C major triad",
           "notes": ["C", "E", "G"]
       },
       {
           "chord": "A minor triad",
           "notes": ["A", "C", "E"]
       }
  ],
  "melody": [
  ["E3", "G3", "C4", "E4"],
  ["C3", "E3", "A3", "C4"]
  ]
}
"""
# updating a progression
@app.route('/api/update_progression', methods=['PUT'])
@authenticate_user
def update_progression():
    data = request.get_json()
    projid = data['projid']
    progid = data['progid']
    name = data['name']
    key = data['key_signature']
    mode = data['mode']
    time_sig = data['time_signature']
    tempo = data['tempo']
    chords = data['chords']
    melody = data['melody']

    userid = request.user['userid']
    
    user = User.objects(userid=userid).first()
    if user == None:
        return jsonify({"error": "could not find user"}), 404
    if not any(proj.projid == projid for proj in user.projects):
        return jsonify({"error": "could not find project"}), 404
    if not any(prog.progid == progid for prog in next(proj for proj in user.projects if proj.projid == projid).progressions):
        return jsonify({"error": "could not find progression"}), 404
    if (key not in major_keys and key not in minor_keys):
        return jsonify({"error": "invalid key"}), 404
    
    user_project = next(project for project in user.projects if project.projid == projid)
    new_progression = Progression(progid=progid, name=name, key_signature=key, mode=mode, time_signature=time_sig, tempo=tempo, chords=chords, melody=melody)

    for i in range(len(user_project.progressions)):
        if user_project.progressions[i].progid == progid:
            user_project.progressions[i] = new_progression
    
    user.save()

    return jsonify({"status": "OK", "new_progression": new_progression.to_json()}), 200

# request input: {"projid": "proj_id"}
# deleting a project
@app.route('/api/delete_project', methods=['PUT'])
@authenticate_user
def delete_project():
    data = request.get_json()
    projid = data['projid']

    userid = request.user['userid']

    user = User.objects(userid=userid).first()
    if user == None:
        return jsonify({"error": "could not find user"}), 404
    if not any(proj.projid == projid for proj in user.projects):
        return jsonify({"error": "could not find project"}), 404
    
    user.projects = [proj for proj in user.projects if proj.projid != projid]

    user.save()

    return jsonify({"status": "OK", "projid": projid}), 200

# request input: {"projid": "proj_id", "progid": "prog_id"}
# deleting a progression
@app.route('/api/delete_progression', methods=['PUT'])
@authenticate_user
def delete_progression():
    data = request.get_json()
    projid = data['projid']
    progid = data['progid']

    userid = request.user['userid']

    user = User.objects(userid=userid).first()
    if user == None:
        return jsonify({"error": "could not find user"}), 404
    if not any(proj.projid == projid for proj in user.projects):
        return jsonify({"error": "could not find project"}), 404
    if not any(prog.progid == progid for prog in next(proj for proj in user.projects if proj.projid == projid).progressions):
        return jsonify({"error": "could not find progression"}), 404
    
    progressions = next(proj for proj in user.projects if proj.projid == projid).progressions
    progressions = [p for p in progressions if p.progid != progid]
    next(proj for proj in user.projects if proj.projid == projid).progressions = progressions

    user.save()
    
    return jsonify({"status": "OK", "progid": progid}), 200

# request input: {"name": "prog_name", "key_signature": "B-", "mode": "major", "time_signature": "4/4", "tempo": 120}
# get progression info
@app.route('/api/get_progression', methods=['POST'])
@authenticate_user
def get_progression():
    data = request.get_json()
    name = data['name']
    key = data['key_signature']
    mode = data['mode']
    time_sig = data['time_signature']
    tempo = data['tempo']

    if (key not in major_keys and key not in minor_keys):
        return jsonify({"error": "invalid key"}), 400
    
    if (key in major_keys):
        new_prog, chord_strings = generate_chord_progression(model1, randomize_seed(tone1), 4)
    else:
        new_prog, chord_strings = generate_chord_progression(model2, randomize_seed(tone2), 4)
    progression = {
            "name": name,
            "key_signature": key,
            "mode": mode,
            "time_signature": time_sig,
            "tempo": tempo,
            "chords": [show_chord_name(c) for c in [transpose_chord(k, tone2, key) for k in chord_strings]],
            "melody": [show_melody_notes(c) for c in [transpose_chord(k, tone2, key) for k in chord_strings]]
        }
    
    return jsonify({"status": "OK", "progression": progression}), 200

"""
request input:
{
   "projid": "proj_id",
   "name": "new_prog_name",
   "key_signature": "B-",
   "mode": "minor",
   "time_signature": "3/4",
   "tempo": 100,
   "chords": [
       {
           "chord": "C major triad",
           "notes": ["C", "E", "G"]
       },
       {
           "chord": "A minor triad",
           "notes": ["A", "C", "E"]
       }
  ],
  "melody": [
  ["E3", "G3", "C4", "E4"],
  ["C3", "E3", "A3", "C4"]
  ]
}
"""
# send the progression
@app.route('/api/send_progression', methods=['POST'])
@authenticate_user
def send_progression():
    data = request.get_json()
    projid = data['projid']
    name = data['name']
    key = data['key_signature']
    mode = data['mode']
    time_sig = data['time_signature']
    tempo = data['tempo']
    chords = data['chords']
    melody = data['melody']

    userid = request.user['userid']
    
    user = User.objects(userid=userid).first()
    if user == None:
        return jsonify({"error": "could not find user"}), 404
    if not any(proj.projid == projid for proj in user.projects):
        return jsonify({"error": "could not find project"}), 404
    if (key not in major_keys and key not in minor_keys):
        return jsonify({"error": "invalid key"}), 404
    
    user_project = next(project for project in user.projects if project.projid == projid)
    progid = secrets.token_hex(16)

    progression = Progression(progid=progid, name=name, key_signature=key, mode=mode, time_signature=time_sig, tempo=tempo, chords=chords, melody=melody)

    user_project.progressions.append(progression)
    user.save()

    return jsonify({"status": "OK", "progid": progid, "progression": progression.to_json()}), 200

"""
request input:
{
   "progression1":
        {
            "chords": [
                {
                    "chord": "C major triad",
                    "notes": ["C", "E", "G"]
                },
                {
                    "chord": "A minor triad",
                    "notes": ["A", "C", "E"]
                }
            ],
            "melody": [
            ["E3", "G3", "C4", "E4"],
            ["C3", "E3", "A3", "C4"]
            ]
        },
    "progression2":
        {
            "chords": [
                {
                    "chord": "C major triad",
                    "notes": ["C", "E", "G"]
                },
                {
                    "chord": "A minor triad",
                    "notes": ["A", "C", "E"]
                }
            ],
            "melody": [
            ["E3", "G3", "C4", "E4"],
            ["C3", "E3", "A3", "C4"]
            ]
        },
    "naturalness": 5,
    "accuracy": 5,
    "inspiration": 5,
    "comment": "comment here"
}
"""
# feedback/evaluation info
@app.route('/api/feedback', methods=['POST'])
def feedback():
    with open('feedback.json', 'r') as file:
        db = json.load(file)
    
    data = request.get_json()
    prog1 = data['progression1']
    prog2 = data['progression2']
    nat = data['naturalness']
    acc = data['accuracy']
    insp = data['inspiration']
    comment = data['comment']
    
    db['feedback'].append({
        "progression1": prog1,
        "progression2": prog2,
        "naturalness": nat,
        "accuracy": acc,
        "inspiration": insp,
        "comment": comment
    })

    with open('feedback.json', 'w') as file:
        json.dump(db, file, indent=4)

    return jsonify({"status": "OK"}), 200

if __name__ == '__main__':
    connect(host=os.getenv('DB'))
    app.run(debug=True)