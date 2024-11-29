from mongoengine import Document, EmbeddedDocument, StringField, IntField, EmbeddedDocumentField, ListField
import bcrypt

class Chord(EmbeddedDocument):
    chord = StringField(required=True)
    notes = ListField(StringField(), required=True)

class Progression(EmbeddedDocument):
    progid = StringField(required=True)
    name = StringField(required=True)
    key_signature = StringField(required=True, choices=['G-', 'B', 'E', 'A', 'D', 'G', 'C', 'F', 'B-', 'E-', 'A-', 'D-',
                                                        'e-', 'g#', 'c#', 'f#', 'b', 'e', 'a', 'd', 'g', 'c', 'f', 'b-'])
    mode = StringField(required=True, choices=['major', 'minor'])
    time_signature = StringField(required=True, choices=['4/4', '3/4', '6/8'])
    tempo = IntField(required=True, min_value=24, max_value=200)
    chords = ListField(EmbeddedDocumentField(Chord))
    melody = ListField(ListField(StringField()))

class Project(EmbeddedDocument):
    projid = StringField(required=True)
    name = StringField(required=True)
    date = StringField(required=True)
    progressions = ListField(EmbeddedDocumentField(Progression), default=[])

class User(Document):
    userid = StringField(required=True)
    username = StringField(required=True, max_length=50)
    password = StringField(required=True)
    projects = ListField(EmbeddedDocumentField(Project), default=[])
    meta = {'collection': 'users'}

    def save(self, *args, **kwargs):
        self.password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        super(User, self).save(*args, **kwargs)
    
    def check_pw(self, password_str):
        return bcrypt.checkpw(password_str.encode('utf-8'), self.password.encode('utf-8'))