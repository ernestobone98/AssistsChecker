# coding: utf-8
from menu_rules import *

fenetre.title(TITRE_FENETRE)
fenetre.geometry(TAILLE_FENETRE)
photo = PhotoImage(file=APP_ICON)
fenetre.iconphoto(False, photo)

# Dans la fenetre
# Aide utilisateur
frame_aide = LabelFrame(fenetre, text="Cliquez pour faire apparaitre l'aide", height=25, font=(30))
frame_aide.pack(fill=BOTH)

# Dans Frame Aide
label_aide = Label(frame_aide, text=TEXTE_AIDE, justify=LEFT)
label_aide.pack(side=LEFT)
label_aide.bind("<Button-1>", cacher_aide)

# cacher l'aide lors de l'apparition de la fenetre
label_aide.pack_forget()
frame_aide.bind("<Button-1>", apparaitre_aide)

# Partie depos de fichier et lancement de l'analyse
frame_analyse = LabelFrame(fenetre, text='Fichiers à analyser', font=(30))
frame_analyse.pack(pady=20, expand=True, fill=BOTH)

canva_depos = Canvas(frame_analyse)
canva_depos.configure(scrollregion=canva_depos.bbox("all"))
canva_depos.pack(expand=True, fill=BOTH)

# Dans Frame depos
# Creation d'une frame sinon le contenu ne pourra pas etre scrollé
frame_depos = Frame(canva_depos)
canva_depos.create_window(canva_depos.winfo_rootx(), canva_depos.winfo_rooty(), anchor='nw', window=frame_depos)

label_vide = Label(frame_depos, text="Aucun fichiers déposés", padx=20, pady=20)
label_vide.pack()

scroll = Scrollbar(canva_depos, orient=HORIZONTAL)
scroll.pack(side=BOTTOM, fill=X)
scroll.config(command=canva_depos.xview)
canva_depos.config(xscrollcommand=scroll.set)

# Dans frameAnalyse
Button(frame_analyse, text='Analyser', command=analyserFichiers).pack(side=RIGHT, padx=5, pady=5)

Button(frame_analyse, text='Déposer un fichier', command=lambda: ajouter_fichier_a_liste_attente(canva_depos, label_vide, frame_depos)).pack(
    side=RIGHT, padx=5, pady=5)

# boutton quitter
Button(fenetre, text='Quitter', command=fenetre.destroy).pack(side=RIGHT, padx=5, pady=5)

canva_depos.drop_target_register(DND_FILES)
canva_depos.dnd_bind('<<Drop>>', lambda event : drop(event,label_vide, frame_depos))

# TODO Pandant le traitement si une signature est au delà de la marge le programme met en pose l'analyse, affiche le
#  fichier et demande confirmation
#  TODO Ajout de la partie sortie/feedback

fenetre.mainloop()
