# AssistsChecker

Il s’agit d’une application qui s’exécute sur l’ordinateur du personnel administratif de l’école. Le client scanne les feuilles de présence les drag and drop sur le logiciel puis clique sur le bouton « analyser » pour activer l’algorithme. Écrit avec le langage python
L’OCR va analyser les documents pour les « traduire » et retranscrire numériquement qui est présent et absent. De là il va créer une archive où il va ranger les documents. 
ARCHIVE DES FDP -> <Nom de la filière> -> <Nom de la promotion> -> <Nom+Prénom du professeur> -> <Nom ecue ou UE> 
Où il met le document final avec pour nom <Date + Salle>
Si le document ou dossier existe déjà il n’en crée pas, s’il n’existe pas il va le créer.

## Pour lancer depuis votre Ordinateur

### Attention
1. Cette application utilise une API de google cloud pour fonctionner. Il est indispensable de créer un projet dans google cloud avec l'api google-vision activée.
Une fois vous avez créé votre application dans le cloud, dans un terminal, lancez :
```
gcloud auth application-default login
```

1.1. Cela va vous générer un fichier appelé <<application_default_credentials.json>> (il se trouve normalement dans le chemin %APPDATA%\gcloud\)
Vous devez déplacer ce fichier dans le dossier controllers/miagepackage/


2. Téléchargez poppler depuis le lien suivant : https://github.com/oschwartz10612/poppler-windows/releases/tag/v23.01.0-0
Déplacez le fichier bin au chemin C:\Program Files\poppler-22.11.0\Library\


3. Il est recommandé de créer un environnement virtuel.

- Si vous n'avez pas le module venv
```
pip install venv
```
- Pour créer l'environnement
```
python3 -m venv <<myenv_name>>
```

3.1. À partir de maintenant, il faudra compiler avec myenv_name, faire :
```
./myenv_name/Scripts/activate
```

4. Nous avons créé un fichier appelé "requirements.txt" avec les librairies nécessaires pour lancer l'application.
- Pour installer toutes les dépendances
```
pip3 install -r controllers/requierements.txt
```

5. Il reste juste à lancer le programme en mode DEBBUG avec l'aide du fichier launch.json
