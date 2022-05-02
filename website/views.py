from flask import Blueprint, render_template, request, flash, jsonify, redirect
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)


# HOME
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    asked_status = request.args.get('status')
    
    notes = db.session.query(Note).filter(Note.user_id==current_user.id)
    if asked_status:
        notes = notes.filter(Note.status == asked_status)
    
    return render_template("home.html", user=current_user, notes=notes.all())


# NOTES
@views.route('/create-note', methods=['POST'])
@login_required
def create_note():
    note = request.form.get('note')

    if len(note) < 1:
        flash('Poznámka je příliš krátká', category='error')
        return render_template("home.html", user=current_user)
    else:
        new_note = Note(data=note, user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()
        flash('Poznámka přidána!', category='success')
        return redirect("/")


@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash('Poznámka úspěšně odstraněna.', category='success')

    return jsonify({})


@views.route('/update-note-state', methods=['POST'])
@login_required
def update_note_state():
        note = json.loads(request.data)
        noteId = note['noteId']
        note = Note.query.get(noteId)
        if note:
            if note.user_id == current_user.id:
                if(note.status == 'Rozpracovaný') :
                    note.status = 'Dokončený'
                elif (note.status == 'Dokončený'):
                    note.status = 'Udělat'
                elif (note.status == 'Udělat'):
                        note.status = 'Rozpracovaný'
                db.session.commit()

        return jsonify({})


@views.route('/edit-note', methods=['GET'])
@login_required
def edit_note():
    noteId = request.args.get('id')
    note = Note.query.get(noteId)

    return render_template("edit.html", note=note, user=current_user)


@views.route('/update-note', methods=['POST'])
@login_required
def update_note():
        noteId = request.args.get('id')
        note = Note.query.get(noteId)
        note_text = request.form.get('note')
        
        
        if len(note_text) < 1:
            flash('Poznámka je příliš krátká', category='error')
            return render_template("edit.html", note=note, user=current_user)
        else:
            note.data = note_text
            db.session.commit()
            flash('Poznámka upravena', category='success')
            return redirect("/")



