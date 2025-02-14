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
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Cours')
        cours = cursor.fetchall()
        cursor.execute('SELECT * FROM Enseignant')
        enseignants = cursor.fetchall()
        cursor.execute('SELECT * FROM CoursSemestriel')
        cours_semestriels = cursor.fetchall()
        return render_template('admin.html', cours=cours, enseignants=enseignants, cours_semestriels=cours_semestriels)
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

# Déconnexion
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('type_utilisateur', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)