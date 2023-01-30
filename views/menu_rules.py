# coding: utf-8
import os
import tkinter
import tkinter.filedialog as fd
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as MessageBox
from tkinter.filedialog import askopenfilenames
from tkinterdnd2 import DND_FILES, TkinterDnD
from miagepackage.testing_tabula import check_presence
from miagepackage.testing_tabula import preprocessing
from miagepackage.handw_ext import trating_text

current_dir = os.getcwd()
sep = os.path.sep

TITRE_FENETRE = 'Lecteur de feuilles d\'abscence'
TEXTE_AIDE = 'Cliquez sur \'Déposer un fichier\' pour ajouter un fichier à la liste d\'attente d\'analyse.\nPassez la ' \
             'souris sur un fichier dans la liste d\'attente.\nCliquez sur la croix pour retirer un fichier de la ' \
             'liste d\'attente.\nCliquez sur \'Analiser\' pour Commencer l\'analise des fichiers déposés dans la ' \
             'liste d\'attente.\nCliquez n\'importe ou sur le texte de l\'aide pour la cacher ou la faire apparaitre'
TAILLE_FENETRE = "700x650"
CHEMIN_ICONE_PDF = f'{current_dir}{sep}views{sep}img{sep}icone_pdf.png'
CHEMIN_ICONE_CROIX = f'{current_dir}{sep}views{sep}img{sep}croix_cercle.png'
TYPES_FICHIERS = [('pdf files', '.pdf')]
NB_LIGNES_DEPOS = 3
APP_ICON = f'{current_dir}{sep}views{sep}img{sep}logo.png'

fenetre = TkinterDnD.Tk()
lst_fichiers = []
icone_pdf = tkinter.PhotoImage(file=CHEMIN_ICONE_PDF).subsample(7, 7)
# icone random recup sur https://icon-icons.com/fr/
# TODO voir licence ; subsample a addapter si changement d'icone
icone_croix = tkinter.PhotoImage(file=CHEMIN_ICONE_CROIX)  # idem


def analyserFichiers():
    """
    Fonction qui lance l'analyse de chaque fichiers dans la liste d'attente
    """
    for fichier in lst_fichiers:
        nom_du_fichier = nom_fichier(fichier)[:-4]
        preprocessing(fichier, nom_du_fichier)
        file_info = trating_text(nom_du_fichier + '.jpg')
        nom_du_fichier_json = file_info[-1]
        path = file_info[0] + sep + file_info[1] + sep + file_info[2] + sep + file_info[3] + sep + file_info[4] + sep
        check_presence(nom_du_fichier + '.pdf', nom_du_fichier_json, path)
    
    MessageBox.showinfo("Analyse terminée", "L'analyse des fichiers a été terminée")


def apparaitre_aide(event):
    """
    Faire apparaitre l'aide dans la fenetre
    """
    label_aide = event.widget

    label_aide.winfo_children()[0].pack(side=LEFT)
    label_aide.configure(text="Aide")


def cacher_aide(event):
    """
    Fait disparaitre le texte d'aide de la fenetre
    """
    label_aide = event.widget.master

    event.widget.pack_forget()
    label_aide.configure(text="Cliquez pour faire apparaitre l'aide", height=25)


def sortie_souris_frame(event):
    """
    Suppression de la croix d'une frame quand la souris sort de celle-ci
    """
    event.widget.winfo_children()[1].winfo_children()[0].destroy()


def click_souris_sur_image(event, label_vide):
    """
    Supprimer un fichier de la liste d'attente et retire l'affichage du fichier de l'interface
    """
    frame_depos = event.widget.master.master.master.master
    colonne_depos = event.widget.master.master.master
    frame_fichier = event.widget.master.master

    numero_colonne = 0
    numero_fichier_dans_colonne = 0
    for colonne in frame_depos.winfo_children():
        numero_colonne += 1
        if colonne == colonne_depos:
            for fichier in colonne.winfo_children():
                numero_fichier_dans_colonne += 1
                if fichier == frame_fichier:
                    break
            break
    numero_fichier = numero_colonne * NB_LIGNES_DEPOS - (NB_LIGNES_DEPOS - numero_fichier_dans_colonne)

    # supprimer le fichier dans lst fichier
    lst_fichiers.pop(numero_fichier - 1)
    # supprimer les affichages
    for colonne in frame_depos.winfo_children():
        colonne.destroy()
    # refaire tout les affichages
    cpt = 1
    for chemin in lst_fichiers:
        ajouter_un_label(nom_fichier(chemin), cpt, label_vide, frame_depos)
        cpt += 1


def passage_souris_sur_frame(event,label_vide):
    """
    Indications au passage de la souris sur une image
    """
    # label_depos = Label(event, text="cliquer sur l'icone pour supprimer")
    # ajouter la croix de suppression
    image_label_suppression = ttk.Label(event.widget.winfo_children()[1], image=icone_croix, padding=5)
    image_label_suppression.pack(anchor=NE)

    # ajout des evenements surlabel supression
    image_label_suppression.bind("<Button-1>", lambda eff: click_souris_sur_image(eff, label_vide))


def ajouter_un_label(nom, index_nom, label_vide, frame_depos):
    # TODO si aucun fichier replacer label vide
    """
    Afficher le nom d'un fichier et l'iconne de pdf à l'écran
    -----Variables-----
        nom : str
              nom du fichier à ajouter
        ligne : int
                index du nom dans la liste des fichiers (pas tout fait mais vus que c'est le dernier elem de la liste ça passe)
    """
    # détruire l'indication 'aucun fichier déposé'
    detruire_label_vide(label_vide)

    # créer une frame la précedente est remplie sinon recup la derniere frame de frame depos
    frame = recuperer_frame_de_depos(index_nom,frame_depos)
    frame.pack(expand=True, fill=BOTH, side=LEFT, padx=5, pady=5)

    # jout dans la Frame récupérée
    frame_fichier = Frame(frame)
    label_depos = Label(frame_fichier, text=nom)
    label_depos.pack(side=BOTTOM)
    image_label = ttk.Label(frame_fichier, image=icone_pdf, padding=10)
    image_label.pack(side=BOTTOM)
    image_label.propagate(False)
    frame_fichier.pack()

    # ajout des evenements sur frame_fichier
    #frame_fichier.bind("<Enter>", passage_souris_sur_frame(label_vide))
    frame_fichier.bind("<Enter>", lambda eff: passage_souris_sur_frame(eff, label_vide))
    frame_fichier.bind("<Leave>", sortie_souris_frame)

def detruire_label_vide(label_vide):
    if len(lst_fichiers) != 0:
        label_vide.destroy()

def recuperer_frame_de_depos(index_nom,frame_depos):
    if index_nom % NB_LIGNES_DEPOS == 1 or NB_LIGNES_DEPOS == 1:
        return Frame(frame_depos, border=False)
    else:
        return frame_depos.winfo_children()[-1]  # recupère le dernier enfant


def nom_fichier(chemin):
    """
    Donne le nom d'un fichier a partir de son chemin
    :param chemin: (str) le chemin vers un fichier
    :return: (str) le nom du fichier
    """
    return chemin.split("/")[-1]

def drop(event, label_vide, frame_depos):
    file_path = event.data
    if not file_path.endswith(".pdf"):
        MessageBox.showerror("Erreur", "Le fichier n'est pas au format pdf")
    else:
        lst_fichiers.append(file_path)
        ajouter_un_label(nom_fichier(file_path), len(lst_fichiers), label_vide, frame_depos)
    

def ajouter_fichier_a_liste_attente(canva_depos, label_vide, frame_depos):
    """
    Ouvre une fenetre de recherche de fichier pdf
    Ajoute un fichier à la liste d'attente
    Ajoute l'icone d'un pdf et le chemin du fichier ajouté
    """

    canva_depos.configure(scrollregion=canva_depos.bbox("all"))
    chemins = askopenfilenames(title="Ouvrir une image", filetypes=TYPES_FICHIERS)

    for chemin in chemins:
        if len(chemin) != 0:
            lst_fichiers.append(chemin)
            ajouter_un_label(nom_fichier(chemin), len(lst_fichiers), label_vide, frame_depos)

            # MAJ taille scrolling
            # https://openclassrooms.com/forum/sujet/taille-d-une-frame-tkinter
            canva_depos.update_idletasks()
            # Ligne à ajouter sinon thinker considere qu'on veut màj la taille avant que le dépos ne soit fait
            canva_depos.configure(scrollregion=canva_depos.bbox("all"))
