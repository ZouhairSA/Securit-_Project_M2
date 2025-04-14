# 🔐 Application Sécurisée de Gestion des Cours Universitaires

> Un projet académique complet intégrant **Flask**, **MySQL** et les **bonnes pratiques de sécurité** pour la gestion des cours dans un environnement universitaire.

---

## 🧑‍💻 Réalisé par

**SABYOUD Zohair**  
Master 2 – Réseaux & Télécommunications  
Parcours **Cybersécurité – Défense des Systèmes d’Information**  
INSA Hauts-de-France – Année universitaire 2024/2025

Encadré par **M. RATLI Mustapha**

---

## 🎯 Objectifs du Projet

Ce projet vise à :

- Développer une **application web complète** pour la gestion des cours universitaires.
- Implémenter des **interfaces distinctes** pour chaque type d’utilisateur (secrétaire, enseignant, étudiant).
- **Sécuriser la base de données** contre les attaques SQL (injections).
- Tester l'application avec l'outil **SQLMap** pour valider la robustesse du système.
- Appliquer les principes de **séparation des rôles** et de **gestion des privilèges** dans MySQL.

---

## 🛠️ Technologies Utilisées

| Composant          | Description |
|--------------------|-------------|
| Python             | Langage principal |
| Flask              | Framework web léger |
| MySQL              | Base de données relationnelle |
| Flask-MySQLdb      | Connexion Flask ↔ MySQL |
| HTML / CSS / Bootstrap | Interfaces utilisateurs |
| SQLMap             | Tests de sécurité contre les injections SQL |
| XAMPP              | Environnement serveur local (Apache + MySQL) |
| GitHub             | Versionnage de code |
| Kali Linux         | Outils de test d’intrusion |

---

## 🧑‍🏫 Rôles Utilisateurs

- **👩‍💼 Secrétaire (Administrateur)** :
    - Créer, modifier, supprimer des cours
    - Gérer les enseignants
    - Visualiser les inscriptions et messages

- **👨‍🏫 Enseignant** :
    - Planifier des séances
    - Noter les étudiants
    - Répondre aux questions

- **👨‍🎓 Étudiant** :
    - S’inscrire à des cours
    - Déposer des exercices
    - Poser des questions

---

## 🔐 Sécurité Intégrée

✅ Utilisation de requêtes **préparées**  
✅ Validation des **entrées utilisateur**  
✅ Chiffrement du mot de passe dans la base  
✅ Tests avec **SQLMap** pour détecter les injections SQL  
✅ Gestion des **rôles MySQL** avec privilèges limités

---

## 🖼️ Captures d’écran

- Tableau de bord dynamique
- Interfaces personnalisées selon le rôle
- Gestion des cours et utilisateurs
- Messages de contact, inscription, exercices...

---

## ⚙️ Structure du Projet

