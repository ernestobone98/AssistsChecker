# coding: utf-8
import tkinter
import os
from tkinter import *
from tkinter.filedialog import *
from tkinter import ttk
from platform import system

current_dir = os.getcwd()
sep = os.path.sep

TITRE_FENETRE = 'Lecteur de feuilles d\'abscence'
TEXTE_AIDE = 'Cliquez sur \'Déposer un fichier\' pour ajouter un fichier à la liste d\'attente d\'analyse.\nPassez la ' \
             'souris sur un fichier dans la liste d\'attente.\nCliquez sur la croix pour retirer un fichier de la ' \
             'liste d\'attente.\nCliquez sur \'Analiser\' pour Commencer l\'analise des fichiers déposés dans la ' \
             'liste d\'attente.\nCliquez n\'importe ou sur le texte de l\'aide pour la cacher ou la faire apparaitre'
TAILLE_FENETRE = "700x650"
CHEMIN_ICONE_PDF = f'{current_dir}{sep}Models{sep}icone_pdf.png'
CHEMIN_ICONE_CROIX = f'{current_dir}{sep}Models{sep}croix_cercle.png'
TYPES_FICHIERS = [('pdf files', '.pdf')]
NB_LIGNES_DEPOS = 3

fenetre = Tk()
lst_fichiers = []
icone_pdf = tkinter.PhotoImage(file=CHEMIN_ICONE_PDF ).subsample(7, 7)
# icone random recup sur https://icon-icons.com/fr/
# TODO voir licence ; subsample a addapter si changement d'icone
icone_croix = tkinter.PhotoImage(file=CHEMIN_ICONE_CROIX )#idem


#
#
#FONCTION DE GESTION DE L'INTERFACE
#
#
def apparaitre_aide(event):
    label_aide=event.widget

    label_aide.winfo_children()[0].pack(side = LEFT)
    label_aide.configure(text="Aide")
    label_aide.unbind("<Button-1>")


def cacher_aide(event):
    """
    Fait disparaitre le texte d'aide de la fenetre
    """
    label_aide = event.widget.master

    event.widget.pack_forget()
    label_aide.configure(text="Cliquez pour faire apparaitre l'aide", height=25)
    label_aide.bind("<Button-1>", apparaitre_aide)



def sortie_souris_frame(event):
    """
    Suppression de la croix d'une frame quand la souris sort de celle-ci
    """
    event.widget.winfo_children()[1].winfo_children()[0].destroy()


def click_souris_sur_image(event):
    """
    Supprimer un fichier de la liste d'attente et retire l'affichage du fichier de l'interface
    """
    frame_depos = event.widget.master.master.master.master
    colonne_depos = event.widget.master.master.master
    frame_fichier = event.widget.master.master

    numero_colonne = 0
    numero_fichier_dans_colonne = 0
    for colonne in  frame_depos.winfo_children():
        numero_colonne += 1
        if colonne == colonne_depos :
            for fichier in colonne.winfo_children() :
                numero_fichier_dans_colonne += 1
                if fichier == frame_fichier :
                    break
            break
    numero_fichier = numero_colonne*NB_LIGNES_DEPOS - (NB_LIGNES_DEPOS-numero_fichier_dans_colonne)

    #supprimer le fichier dans lst fichier
    lst_fichiers.pop(numero_fichier - 1)
    #supprimer les affichages
    for colonne in frame_depos.winfo_children() :
        colonne.destroy()
    #refaire tout les affichages
    cpt = 1
    for chemin in lst_fichiers :
        ajouter_un_label(nom_fichier(chemin),cpt)
        cpt += 1

def passage_souris_sur_frame(event):
    """
    Indications au passage de la souris sur une image
    """
    #label_depos = Label(event, text="cliquer sur l'icone pour supprimer")
    #ajouter la croix de suppression
    image_label_suppression = ttk.Label(event.widget.winfo_children()[1], image=icone_croix, padding=5)
    image_label_suppression.pack(anchor=NE)


    #ajout des evenements surlabel supression
    image_label_suppression.bind("<Button-1>", click_souris_sur_image)


def ajouter_un_label(nom, index_nom) :
    #TODO si aucun fichier replacer label vide
    """
    Afficher le nom d'un fichier et l'iconne de pdf à l'écran
    -----Variables-----
        nom : str
              nom du fichier à ajouter
        ligne : int
                index du nom dans la liste des fichiers (pas tout fait mais vus que c'est le dernier elem de la liste ça passe)
    """
    #détruire l'indication 'aucun fichier déposé'
    if len(lst_fichiers) != 0:
        labe_vide.destroy()

    # créer une frame la précedente est remplie sinon recup la derniere frame de frame depos
    if index_nom%NB_LIGNES_DEPOS == 1 or NB_LIGNES_DEPOS == 1:
        frame = Frame(frame_depos, border=False)
    else:
        frame = frame_depos.winfo_children()[-1]#recupère le dernier enfant

    frame.pack(expand=True, fill=BOTH, side=LEFT,padx=5, pady=5)

    #jout dans la Frame récupérée
    frame_fichier = Frame(frame)
    label_depos = Label(frame_fichier, text=nom)
    label_depos.pack(side=BOTTOM)
    image_label = ttk.Label(frame_fichier, image=icone_pdf, padding=10)
    image_label.pack(side=BOTTOM)
    image_label.propagate(False)
    frame_fichier.pack()

    #ajout des evenements sur frame_fichier
    frame_fichier.bind("<Enter>", passage_souris_sur_frame)
    frame_fichier.bind("<Leave>", sortie_souris_frame)

def nom_fichier(chemin):
    """
    Donne le nom d'un fichier a partir de son chemin
    :param chemin: (str) le chemin vers un fichier
    :return: (str) le nom du fichier
    """
    #separateur = "\\" if system() == "Windows" else "/"
    return chemin.split("/")[-1]


def ajouter_fichier_a_liste_attente():
    """
    Ouvre une fenetre de recherche de fichier pdf
    Ajoute un fichier à la liste d'attente
    Ajoute l'icone d'un pdf et le chemin du fichier ajouté
    """
    canva_depos.configure(scrollregion=canva_depos.bbox("all"))
    chemin = askopenfilename(title="Ouvrir une image", filetypes= TYPES_FICHIERS)

    if len(chemin) != 0:
        lst_fichiers.append(chemin)
        ajouter_un_label(nom_fichier(chemin), len(lst_fichiers))

        #MAJ taille scrolling
        #https://openclassrooms.com/forum/sujet/taille-d-une-frame-tkinter
        canva_depos.update_idletasks()#Ligne à ajouter sinon thinker considere qu'on veut màj la taille avant que le dépos ne soit fait (ce qui est faux il est fait et affiché au dessus)
        canva_depos.configure(scrollregion=canva_depos.bbox("all"))


#
#
#AFFICHAGE DE L'INTERFACE
#
#

fenetre.title(TITRE_FENETRE)
fenetre.geometry(TAILLE_FENETRE)

#Dans la fenetre
#Aide utilisateur
frame_aide = LabelFrame(fenetre, text='Aide', font=(30))
frame_aide.pack(fill=BOTH)

#Dans Frame Aide
label_aide = Label(frame_aide, text= TEXTE_AIDE, justify=LEFT)
label_aide.pack(side=LEFT)

label_aide.bind("<Button-1>", cacher_aide)

#Partie depos de fichier et lancement de l'analyse
frame_analyse = LabelFrame(fenetre, text='Fichiers à analyser', font=(30))
frame_analyse.pack(pady=20, expand= True, fill= BOTH)

canva_depos = Canvas(frame_analyse)
canva_depos.configure(scrollregion=canva_depos.bbox("all"))
canva_depos.pack(expand=True, fill=BOTH)

#Dans Frame depos
#Creation d'une frame sinon le contenu ne pourra pas etre scrollé
frame_depos = Frame(canva_depos)
canva_depos.create_window(canva_depos.winfo_rootx(), canva_depos.winfo_rooty(), anchor='nw', window=frame_depos)

labe_vide = Label(frame_depos, text="Aucun fichiers déposés", padx=20, pady=20)
labe_vide.pack()

scroll = Scrollbar(canva_depos, orient=HORIZONTAL)
scroll.pack(side=BOTTOM,fill=X)
scroll.config(command=canva_depos.xview)
canva_depos.config(xscrollcommand=scroll.set)

#Dans frameAnalyse
Button(frame_analyse, text='Analyser').pack(side=RIGHT, padx=5, pady=5)

Button(frame_analyse, text='Déposer un fichier', command=ajouter_fichier_a_liste_attente).pack(side=RIGHT, padx=5, pady=5)

#boutton quitter
Button(fenetre, text='Quitter', command=fenetre.destroy).pack(side=RIGHT, padx=5, pady=5)

#TODO Pandant le traitement si une signature est au delà de la marge le programme met en pose l'analyse, affiche le fichier et demande confirmation
#TODO Ajout de la partie sortie/feedback

fenetre.mainloop()