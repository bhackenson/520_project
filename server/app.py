from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import secrets
import jwt
import mongoengine
from datetime import datetime, timezone
import bcrypt
from dotenv import load_dotenv
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

# request input: {"userid": "user_id"}
@app.route('/api/get_user', methods=['POST'])
def get_user():
    try:
        data = request.get_json()
        userid = data['userid']

        with open('db.json', 'r') as file:
            db = json.load(file)

        if (userid not in db):
            return jsonify({"error": "could not find user"}), 400
        
        return jsonify({"status": "OK", "user": db[userid]}), 200

    except Exception as e:
        handle_exception(e)

# request input: {"username": "username", "password": "password"}
@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']

        with open('db.json', 'r') as file:
            db = json.load(file)

        for user in db.values():
            print(user['username'])
            if user['username'] == username:
                bytes = password.encode('utf-8')
                salt = bcrypt.gensalt() 
                hash = bcrypt.hashpw(bytes, salt)
                user_pw_bytes = user['password'].encode('utf-8')
                if bcrypt.checkpw(user_pw_bytes, hash):
                    print("INSIDE")
                    # token = jwt.encode({"userid": user['id'], "exp": datetime.now(tz=timezone.utc) + datetime.timedelta(hours=1)}, os.getenv('JWT_KEY'), algorithm='HS256')
                    return jsonify({"status": "OK", "id": user['id']}), 200
                else:
                    return jsonify({"error": "Incorrect password"}), 400
                
        return jsonify({"error": "username does not exist"}), 400
    
    except Exception as e:
        handle_exception(e)

@app.route('/api/logout', methods=['POST'])
def logout():
    try:
        # remove token here
        return jsonify({"status": "OK"}), 200
    except Exception as e:
        handle_exception(e)

# request input: {"username": "username", "password": "password"}
@app.route('/api/create_user', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']

        with open('db.json', 'r') as file:
            db = json.load(file)

        id = secrets.token_hex(16)
        db[id] = {"id": id, "username": username, "password": password, "projects": []}

        with open('db.json', 'w') as file:
            json.dump(db, file, indent=4)

        return jsonify({"status": "OK", "user": db[id]}), 200
    
    except Exception as e:
        handle_exception(e)

# request input: {"userid": "user_id", "name": "project_name", "date": "project_date"}
@app.route('/api/create_project', methods=['POST'])
def create_project():
    try:
        data = request.get_json()
        userid = data['userid']
        name = data['name']
        date = data['date']
        with open('db.json', 'r') as file:
            db = json.load(file)

        projid = secrets.token_hex(16)
        if (userid not in db):
            return jsonify({"error": "could not find user"}), 400
        
        projects = db[userid]['projects']
        project = {
            "id": projid,
            "name": name,
            "date": date,
            "progressions": []
        }
        projects.append(project)
        db[userid]['projects'] = projects

        with open('db.json', 'w') as file:
            json.dump(db, file, indent=4)

        return jsonify({"status": "OK", "project": project}), 200

    except Exception as e:
        handle_exception(e)

# request input: {"userid": "user_id", "projid": "proj_id", "name": "prog_name", "key_signature": "B-", "mode": "major", "time_signature": "4/4", "tempo": 120}
@app.route('/api/create_progression', methods=['POST'])
def generate_progression():
    try:
        data = request.get_json()
        userid = data['userid']
        projid = data['projid']
        name = data['name']
        key = data['key_signature']
        mode = data['mode']
        time_sig = data['time_signature']
        tempo = data['tempo']

        with open('db.json', 'r') as file:
            db = json.load(file)

        if userid not in db:
            return jsonify({"error": "could not find user"}), 400
        if not any(proj['id'] == projid for proj in db[userid]['projects']):
            return jsonify({"error": "could not find project"}), 400
        if (key not in major_keys and key not in minor_keys):
            return jsonify({"error": "invalid key"}), 400
        
        progressions = next(proj for proj in db[userid]['projects'] if proj['id'] == projid)['progressions']
        progid = secrets.token_hex(16)

        if (key in major_keys):
            new_prog, chord_strings = generate_chord_progression(model1, randomize_seed(tone1), 4)
            # return jsonify({"chords": [show_chord_name(c) for c in [transpose_chord(k, tone1, key) for k in chord_strings]]}), 201
        else:
            new_prog, chord_strings = generate_chord_progression(model2, randomize_seed(tone2), 4)
            # return jsonify({"chords": [show_chord_name(c) for c in [transpose_chord(k, tone2, key) for k in chord_strings]]}), 201
        progression = {
                "id": progid,
                "name": name,
                "key_signature": key,
                "mode": mode,
                "time_signature": time_sig,
                "tempo": tempo,
                "chords": [show_chord_name(c) for c in [transpose_chord(k, tone2, key) for k in chord_strings]],
                "melody": [show_melody_notes(c) for c in [transpose_chord(k, tone2, key) for k in chord_strings]]
            }

        progressions.append(progression)

        with open('db.json', 'w') as file:
            json.dump(db, file, indent=4)

        return jsonify({"status": "OK", "progression": progression}), 200
    
    except Exception as e:
        handle_exception(e)

"""
request input:
{
   "userid": "user_id",
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
@app.route('/api/update_progression', methods=['PUT'])
def update_progression():
    try:
        data = request.get_json()
        userid = data['userid']
        projid = data['projid']
        progid = data['progid']
        name = data['name']
        key = data['key_signature']
        mode = data['mode']
        time_sig = data['time_signature']
        tempo = data['tempo']
        chords = data['chords']
        melody = data['melody']
    
        with open('db.json', 'r') as file:
            db = json.load(file)
        
        if userid not in db:
            return jsonify({"error": "could not find user"}), 400
        if not any(proj['id'] == projid for proj in db[userid]['projects']):
            return jsonify({"error": "could not find project"}), 400
        if not any(prog['id'] == progid for prog in next(proj for proj in db[userid]['projects'] if proj['id'] == projid)['progressions']):
            return jsonify({"error": "could not find progression"}), 400
        if (key not in major_keys and key not in minor_keys):
            return jsonify({"error": "invalid key"}), 400
        
        progressions = next(proj for proj in db[userid]['projects'] if proj['id'] == projid)['progressions']
        new_progression = {
                "id": progid,
                "name": name,
                "key_signature": key,
                "mode": mode,
                "time_signature": time_sig,
                "tempo": tempo,
                "chords": chords,
                "melody": melody
        }
        for i in range(len(progressions)):
            if progressions[i]['id'] == progid:
                progressions[i] = new_progression

        with open('db.json', 'w') as file:
            json.dump(db, file, indent=4)

        return jsonify({"status": "OK", "new_progression": new_progression})

    except Exception as e:
        handle_exception(e)

# request input: {"userid": "user_id", "projid": "proj_id"}
@app.route('/api/delete_project', methods=['PUT'])
def delete_project():
    try:
        data = request.get_json()
        userid = data['userid']
        projid = data['projid']

        with open('db.json', 'r') as file:
            db = json.load(file)

        if userid not in db:
            return jsonify({"error": "could not find user"}), 400
        if not any(proj['id'] == projid for proj in db[userid]['projects']):
            return jsonify({"error": "could not find project"}), 400
        
        projects = db[userid]['projects']
        projects = [proj for proj in projects if proj['id'] != projid]
        db[userid]['projects'] = projects

        with open('db.json', 'w') as file:
            json.dump(db, file, indent=4)

        return jsonify({"status": "OK", "projid": projid}), 400
    
    except Exception as e:
        handle_exception(e)

# request input: {"userid": "user_id", "projid": "proj_id", "progid": "prog_id"}
@app.route('/api/delete_progression', methods=['PUT'])
def delete_progression():
    try:
        data = request.get_json()
        userid = data['userid']
        projid = data['projid']
        progid = data['progid']

        with open('db.json', 'r') as file:
            db = json.load(file)

        if userid not in db:
            return jsonify({"error": "could not find user"}), 400
        if not any(proj['id'] == projid for proj in db[userid]['projects']):
            return jsonify({"error": "could not find project"}), 400
        if not any(prog['id'] == progid for prog in next(proj for proj in db[userid]['projects'] if proj['id'] == projid)['progressions']):
            return jsonify({"error": "could not find progression"}), 400

        progressions = next(proj for proj in db[userid]['projects'] if proj['id'] == projid)['progressions']
        print(progressions)
        progressions = [p for p in progressions if p['id'] != progid]
        next(proj for proj in db[userid]['projects'] if proj['id'] == projid)['progressions'] = progressions
    
        with open('db.json', 'w') as file:
            json.dump(db, file, indent=4)
        
        return jsonify({"status": "OK", "progid": progid}), 200

    except Exception as e:
        handle_exception(e)

if __name__ == '__main__':
    app.run(debug=True)