from math import ceil

from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = 'votre_clé_secrète'

# Configuration de la base de données
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'universite_db'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])  # Autoriser GET et POST
def login():
    if request.method == 'POST':
        # Traitement du formulaire de connexion
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Utilisateur WHERE email = %s AND mot_de_passe = %s', (email, password))
        user = cursor.fetchone()
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
    return render_template('login.html')  # Afficher le formulaire de connexion pour les requêtes GET

# Page admin (secrétaire)
@app.route('/admin')
def admin():
    if 'loggedin' in session and session['type_utilisateur'] == 'secretaire':
        # Pagination pour les cours
        page_cours = request.args.get('page_cours', 1, type=int)
        per_page = 5  # Nombre d'éléments par page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT COUNT(*) AS total FROM Cours')
        total_cours = cursor.fetchone()['total']
        total_pages_cours = ceil(total_cours / per_page)
        offset_cours = (page_cours - 1) * per_page
        cursor.execute('SELECT * FROM Cours LIMIT %s OFFSET %s', (per_page, offset_cours))
        cours = cursor.fetchall()

        # Pagination pour les enseignants
        page_enseignants = request.args.get('page_enseignants', 1, type=int)
        #cursor.execute('SELECT COUNT(*) AS total FROM Utilisateur WHERE type_utilisateur = secretaire')
        cursor.execute('SELECT COUNT(*) AS total FROM Enseignant')
        total_enseignants = cursor.fetchone()['total']
        total_pages_enseignants = ceil(total_enseignants / per_page)
        offset_enseignants = (page_enseignants - 1) * per_page
        #cursor.execute('SELECT * FROM Utilisateur WHERE type_utilisateur = secretaire LIMIT %s OFFSET %s', (per_page, offset_enseignants))
        cursor.execute('SELECT * FROM Enseignant LIMIT %s OFFSET %s', (per_page, offset_enseignants))
        enseignants = cursor.fetchall()

        # Pagination pour les cours semestriels
        page_cours_semestriels = request.args.get('page_cours_semestriels', 1, type=int)
        cursor.execute('SELECT COUNT(*) AS total FROM CoursSemestriel')
        total_cours_semestriels = cursor.fetchone()['total']
        total_pages_cours_semestriels = ceil(total_cours_semestriels / per_page)
        offset_cours_semestriels = (page_cours_semestriels - 1) * per_page
        cursor.execute('SELECT * FROM CoursSemestriel LIMIT %s OFFSET %s', (per_page, offset_cours_semestriels))
        cours_semestriels = cursor.fetchall()

        cursor.close()

        return render_template(
            'admin.html',
            cours=cours, page_cours=page_cours, total_pages_cours=total_pages_cours,
            enseignants=enseignants, page_enseignants=page_enseignants, total_pages_enseignants=total_pages_enseignants,
            cours_semestriels=cours_semestriels, page_cours_semestriels=page_cours_semestriels, total_pages_cours_semestriels=total_pages_cours_semestriels
        )
    else:
        return redirect(url_for('login'))


# Page enseignant
@app.route('/teacher')
def teacher():
    if 'loggedin' in session and session['type_utilisateur'] == 'enseignant':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Seance WHERE id_enseignant = %s', (session['id'],))
        seances = cursor.fetchall()
        cursor.execute('SELECT * FROM Note WHERE id_enseignant = %s', (session['id'],))
        notes = cursor.fetchall()
        return render_template('teacher.html', seances=seances, notes=notes)
    else:
        return redirect(url_for('login'))

# Page étudiant
@app.route('/student')
def student():
    if 'loggedin' in session and session['type_utilisateur'] == 'eleve':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Inscription WHERE id_eleve = %s', (session['id'],))
        inscriptions = cursor.fetchall()
        cursor.execute('SELECT * FROM Note WHERE id_eleve = %s', (session['id'],))
        notes = cursor.fetchall()
        return render_template('student.html', inscriptions=inscriptions, notes=notes)
    else:
        return redirect(url_for('login'))

# Route pour ajouter un cours
@app.route('/add_cours', methods=['POST'])
def add_cours():
    if request.method == 'POST':
        titre = request.form['titre']
        description = request.form['description']
        heures = request.form['heures']
        type_cours = request.form['type_cours']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO Cours (titre, description, heures, type_cours) VALUES (%s, %s, %s, %s)', (titre, description, heures, type_cours))
        mysql.connection.commit()
        cursor.close()
        flash('Cours ajouté avec succès', 'success')
    return redirect(url_for('admin'))

@app.route('/add_enseignant', methods=['POST'])
def add_enseignant():
    if 'loggedin' in session and session['type_utilisateur'] == 'secretaire':
        nom = request.form['nom']
        prenom = request.form['prenom']
        fonction = request.form['fonction']
        telephone = request.form['telephone']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO Enseignant (nom, prenom, fonction, telephone) VALUES (%s, %s, %s, %s)', (nom, prenom, fonction, telephone))
        mysql.connection.commit()
        cursor.close()
        flash('Enseignant ajouté avec succès', 'success')
    return redirect(url_for('admin'))

# Route pour supprimer un cours
@app.route('/delete_cours/<int:id>', methods=['GET'])
def delete_cours(id):
    if 'loggedin' in session and session['type_utilisateur'] == 'secretaire':
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM Cours WHERE id = %s', (id,))
        mysql.connection.commit()
        cursor.close()
        flash('Cours supprimé avec succès', 'success')
    return redirect(url_for('admin'))

@app.route('/add_cours_semestriel', methods=['POST'])
def add_cours_semestriel():
    if 'loggedin' in session and session['type_utilisateur'] == 'secretaire':
        id_cours = request.form['id_cours']
        id_enseignant = request.form['id_enseignant']
        semestre = request.form['semestre']
        annee = request.form['annee']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO CoursSemestriel (id_cours, id_enseignant, semestre, annee) VALUES (%s, %s, %s, %s)', (id_cours, id_enseignant, semestre, annee))
        mysql.connection.commit()
        cursor.close()
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
    app.run(debug=True)