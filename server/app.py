from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import secrets
from generator import build_model, generate_chord_progression, randomize_seed, transpose_chord, show_chord_name

app = Flask(__name__)
CORS(app)

model1 = None
tone1 = None
history1 = None

model2 = None
tone2 = None
history2 = None

major_keys = ["G-", 'B', 'E', 'A', 'D', 'G', 'C', 'F', 'B-', 'E-', 'A-', 'D-']
minor_keys = ['e-', 'g#', 'c#', 'f#', 'b', 'e', 'a', 'd', 'g', 'c', 'f', 'b-']

"""
with app.app_context():
    model1, tone1, history1 = build_model('major')
    model2, tone2, history2 = build_model('minor')
"""

@app.errorhandler(404)
def not_found_error(e):
    return jsonify({'error': 'Invalid input'}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({'error': 'Unexpected error', 'description': str(e)}), 500

# request input: {"username": "username", "password": "password"}
@app.route('api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
    except Exception as e:
        handle_exception(e)

# request input: {"username": "username", "password": "password"}
@app.route('/api/create_user', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']
        with open('database.json', 'r') as file:
            db = json.load(file)
        id = secrets.token_hex(16)
        db[id] = {"id": id, "username": username, "password": password, "projects": []}
        with open('database.json', 'w') as file:
            json.dump(db, file, indent=4)
        return jsonify({"id": id}), 200
    except Exception as e:
        handle_exception(e)

# request input: {"userid": "user_id", "name": "project_name", "date": "project_date"}
@app.route('api/create_project', methods=['POST'])
def create_project():
    try:
        data = request.get_json()
    except Exception as e:
        handle_exception(e)

# request input: {"userid": "user_id", "projid": "proj_id", "name": "prog_name", "key_signature": "key_sig", "mode": "major", "time_signature": "time_sig", "tempo": 120}
@app.route('/api/create_progression', methods=['POST'])
def generate_progression():
    data = request.get_json()
    key = data.get('key')
    if (key not in major_keys and key not in minor_keys):
        return jsonify({"error": "invalid key"}), 400
    if (key in major_keys):
        new_prog, chord_strings = generate_chord_progression(model1, randomize_seed(tone1), 4)
        return jsonify({"chords": [show_chord_name(c) for c in [transpose_chord(k, tone1, key) for k in chord_strings]]}), 201
    else:
        new_prog, chord_strings = generate_chord_progression(model2, randomize_seed(tone2), 4)
        return jsonify({"chords": [show_chord_name(c) for c in [transpose_chord(k, tone2, key) for k in chord_strings]]}), 201
    
# request input:
# {
#   "userid": "user_id",
#   "projid": "proj_id",
#   "progid": prog_id,
#   "name": "new_prog_name",
#   "key_signature": "new_key_sig",
#   "mode": "new_major",
#   "time_signature": "new_time_sig",
#   "tempo": 100,
#   "chords": [
#       {
#           "chord": "C major triad",
#           "notes": ["C", "E", "G"]
#       },
#       {
#           "chord": "A minor triad",
#           "notes": ["A", "C", "E"]
#       }
#   ],
#   "melody": [
#   ["E3", "G3", "C4", "E4"],
#   ["C3", "E3", "A3", "C4"]
#   ]
# }
app.route('api/update_progression', methods=['PUT'])
def update_progression():
    try:
        data = request.get_json()
    except Exception as e:
        handle_exception(e)

# request input: {"userid": "user_id", "projid": "proj_id"}
app.route('api/delete_project', methods=['PUT'])
def delete_project():
    try:
        data = request.get_json()
    except Exception as e:
        handle_exception(e)

# request input: {"userid": "user_id", "projid": "proj_id", "progid": "prog_id"}
app.route('api/delete_progression', methods=['PUT'])
def delete_progression():
    try:
        data = request.get_json()
    except Exception as e:
        handle_exception(e)

if __name__ == '__main__':
    app.run(debug=True)