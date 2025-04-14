from math import ceil
from flask import Flask, render_template, request, redirect, url_for, session, flash
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', '12Zouhair25Sabyoud@INSTA25ZohaiR')

# Données simulées (remplace la base de données)
# Utilisateurs (simule la table Utilisateur)
utilisateurs = [
    {'id': 1, 'nom': 'Sabyoud', 'prenom': 'Zohair', 'email': 'zohair@gmail.com', 'mot_de_passe': 'password123', 'type_utilisateur': 'secretaire'},
    {'id': 2, 'nom': 'Boussif', 'prenom': 'Youssef', 'email': 'youssef.boussif@gmail.com', 'mot_de_passe': 'password123', 'type_utilisateur': 'enseignant'},
    {'id': 3, 'nom': 'AA', 'prenom': 'Fatima', 'email': 'fatima.aitbenhassi@gmail.com', 'mot_de_passe': 'password123', 'type_utilisateur': 'eleve'},
]

# Cours (simule la table Cours)
cours = [
    {'id': 1, 'titre': 'Mathématiques', 'description': 'Cours de mathématiques pour le semestre 1', 'heures': 30, 'type_cours': 'CM'},
    {'id': 2, 'titre': 'Physique', 'description': 'Cours de physique pour le semestre 1', 'heures': 20, 'type_cours': 'TD'},
    {'id': 3, 'titre': 'Informatique', 'description': 'Cours de programmation en Python', 'heures': 25, 'type_cours': 'CM'},
    {'id': 4, 'titre': 'Chimie', 'description': 'Introduction à la chimie organique', 'heures': 20, 'type_cours': 'TD'},
    {'id': 5, 'titre': 'Biologie', 'description': 'Cours de biologie générale', 'heures': 30, 'type_cours': 'CM'},
]

# Enseignants (simule la table Enseignant)
enseignants = [
    {'id': 1, 'nom': 'Boussif', 'prenom': 'Youssef', 'fonction': 'Professeur', 'telephone': '0123456789'},
]

# Cours semestriels (simule la table CoursSemestriel)
cours_semestriels = [
    {'id': 1, 'id_cours': 1, 'id_enseignant': 1, 'semestre': 1, 'annee': 2025},
    {'id': 2, 'id_cours': 2, 'id_enseignant': 1, 'semestre': 1, 'annee': 2025},
]

# Séances (simule la table Seance pour les enseignants)
seances = [
    {'id': 1, 'id_enseignant': 2, 'description': 'Séance de TD en Physique', 'date': '2025-04-15'},
]

# Notes (simule la table Note pour enseignants et étudiants)
notes = [
    {'id': 1, 'id_enseignant': 2, 'id_eleve': 3, 'valeur': 15},
]

# Inscriptions (simule la table Inscription pour les étudiants)
inscriptions = [
    {'id': 1, 'id_eleve': 3, 'id_cours': 1},
]

# Route pour la page de connexion
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = next((u for u in utilisateurs if u['email'] == email and u['mot_de_passe'] == password), None)
        if user:
            session['loggedin'] = True
            session['id'] = user['id']
            session['type_utilisateur'] = user['type_utilisateur']
            if user['type_utilisateur'] == 'secretaire':
                return redirect(url_for('admin'))
            elif user['type_utilisateur'] == 'enseignant':
                return redirect(url_for('teacher'))
            elif user['type_utilisateur'] == 'eleve':
                return redirect(url_for('student'))
        else:
            flash('Email ou mot de passe incorrect', 'danger')
    return render_template('login.html')

# Interface Secrétaire (Admin)
@app.route('/admin')
def admin():
    if 'loggedin' in session and session['type_utilisateur'] == 'secretaire':
        # Pagination pour les cours
        page_cours = request.args.get('page_cours', 1, type=int)
        per_page = 5
        total_cours = len(cours)
        total_pages_cours = ceil(total_cours / per_page)
        offset_cours = (page_cours - 1) * per_page
        cours_paginated = cours[offset_cours:offset_cours + per_page]

        # Pagination pour les enseignants
        page_enseignants = request.args.get('page_enseignants', 1, type=int)
        total_enseignants = len(enseignants)
        total_pages_enseignants = ceil(total_enseignants / per_page)
        offset_enseignants = (page_enseignants - 1) * per_page
        enseignants_paginated = enseignants[offset_enseignants:offset_enseignants + per_page]

        # Pagination pour les cours semestriels
        page_cours_semestriels = request.args.get('page_cours_semestriels', 1, type=int)
        total_cours_semestriels = len(cours_semestriels)
        total_pages_cours_semestriels = ceil(total_cours_semestriels / per_page)
        offset_cours_semestriels = (page_cours_semestriels - 1) * per_page
        cours_semestriels_paginated = cours_semestriels[offset_cours_semestriels:offset_cours_semestriels + per_page]

        return render_template(
            'admin.html',
            cours=cours_paginated, page_cours=page_cours, total_pages_cours=total_pages_cours,
            enseignants=enseignants_paginated, page_enseignants=page_enseignants, total_pages_enseignants=total_pages_enseignants,
            cours_semestriels=cours_semestriels_paginated, page_cours_semestriels=page_cours_semestriels, total_pages_cours_semestriels=total_pages_cours_semestriels
        )
    return redirect(url_for('login'))

# Interface Enseignant
@app.route('/teacher')
def teacher():
    if 'loggedin' in session and session['type_utilisateur'] == 'enseignant':
        user_seances = [s for s in seances if s['id_enseignant'] == session['id']]
        user_notes = [n for n in notes if n['id_enseignant'] == session['id']]
        return render_template('teacher.html', seances=user_seances, notes=user_notes)
    return redirect(url_for('login'))

# Interface Étudiant
@app.route('/student')
def student():
    if 'loggedin' in session and session['type_utilisateur'] == 'eleve':
        user_inscriptions = [i for i in inscriptions if i['id_eleve'] == session['id']]
        user_notes = [n for n in notes if n['id_eleve'] == session['id']]
        return render_template('student.html', inscriptions=user_inscriptions, notes=user_notes)
    return redirect(url_for('login'))

# Ajouter un cours
@app.route('/add_cours', methods=['POST'])
def add_cours():
    if 'loggedin' in session and session['type_utilisateur'] == 'secretaire':
        titre = request.form['titre']
        description = request.form['description']
        heures = int(request.form['heures'])
        type_cours = request.form['type_cours']
        new_id = max(c['id'] for c in cours) + 1 if cours else 1
        cours.append({'id': new_id, 'titre': titre, 'description': description, 'heures': heures, 'type_cours': type_cours})
        flash('Cours ajouté avec succès', 'success')
    return redirect(url_for('admin'))

# Ajouter un enseignant
@app.route('/add_enseignant', methods=['POST'])
def add_enseignant():
    if 'loggedin' in session and session['type_utilisateur'] == 'secretaire':
        nom = request.form['nom']
        prenom = request.form['prenom']
        fonction = request.form['fonction']
        telephone = request.form['telephone']
        new_id = max(e['id'] for e in enseignants) + 1 if enseignants else 1
        enseignants.append({'id': new_id, 'nom': nom, 'prenom': prenom, 'fonction': fonction, 'telephone': telephone})
        flash('Enseignant ajouté avec succès', 'success')
    return redirect(url_for('admin'))

# Supprimer un cours
@app.route('/delete_cours/<int:id>', methods=['GET'])
def delete_cours(id):
    if 'loggedin' in session and session['type_utilisateur'] == 'secretaire':
        global cours
        cours = [c for c in cours if c['id'] != id]
        flash('Cours supprimé avec succès', 'success')
    return redirect(url_for('admin'))

# Ajouter un cours semestriel
@app.route('/add_cours_semestriel', methods=['POST'])
def add_cours_semestriel():
    if 'loggedin' in session and session['type_utilisateur'] == 'secretaire':
        id_cours = int(request.form['id_cours'])
        id_enseignant = int(request.form['id_enseignant'])
        semestre = int(request.form['semestre'])
        annee = int(request.form['annee'])
        new_id = max(cs['id'] for cs in cours_semestriels) + 1 if cours_semestriels else 1
        cours_semestriels.append({'id': new_id, 'id_cours': id_cours, 'id_enseignant': id_enseignant, 'semestre': semestre, 'annee': annee})
        flash('Cours semestriel ajouté avec succès', 'success')
    return redirect(url_for('admin'))

# Déconnexion
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('type_utilisateur', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)