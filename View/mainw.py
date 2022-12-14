import tkinter, os
from tkinter import *
from tkinter.filedialog import *
from tkinter import ttk

current_dir = os.getcwd()
TITRE_FENETRE = 'Lecteur de feuilles d\'abscence'
TAILLE_FENETRE = "600x450"
CHEMIN_ICONE_PDF = f'{current_dir}\\Models\\icone_pdf.png'
TYPES_FICHIERS = [('pdf files', '.pdf')]
NB_LIGNES_DEPOS = 2

fenetre = Tk()
lst_fichiers = []
icone_pdf = tkinter.PhotoImage(file=CHEMIN_ICONE_PDF ).subsample(7, 7)#icone random recup sur https://icon-icons.com/fr/ TODO voir licence ; subsample a addapter si changement d'icone


#
#
#FONCTION DE GESTION DE L'INTERFACE
#
#
def click_souris_sur_image(event):
    """
    Supprimer un fichier de la liste d'attente
    """
    print("supprimer") #supprimer frame, image, label et entrée dans le tableau


def passage_souris_sur_image(event):
    """
    Indications au passage de la souris sur une image
    """
    print("cliquer pour supprimer") #afficher "cliquer pour suprimer"


def ajouter_un_label(nom, index_nom) :
    """
    Afficher le nom d'un fichier et l'iconne de pdf à l'écran
    -----Variables-----
        nom : str
              nom du fichier à ajouter
        ligne : int
                index du nom dans la liste des fichiers (pas tout fait mais vus que c'est le dernier elem de la liste ça passe)
    """
    if len(lst_fichiers) != 0:
        labe_vide.destroy()

    # créer une frame la précedente est remplie sinon recup la derniere frame de frame depos
    if index_nom%NB_LIGNES_DEPOS == 1:
        frame = Frame(frame_depos, border=False)
    else:
        frame = frame_depos.winfo_children()[-1]#recup dernier enfant

    frame.pack(side=LEFT,padx=5, pady=5)

    #jout dans la Frame
    #TODO ne pas jouter l'icone et nom si on a pas selectionné de fichier
    #TODO adapter pour ajout de plusieurs fichiers en symultané ? (clairement pas prioritaire)
    image_label = ttk.Label(frame, image=icone_pdf, padding=5)
    image_label.pack(side=TOP)
    label_depos = Label(frame, text=nom)
    label_depos.pack()

    image_label.bind("<Enter>", passage_souris_sur_image)
    image_label.bind("<Button-1>", click_souris_sur_image)


def ajouter_fichier_a_liste_attente():
    """
    Ajouter un fichier à la liste d'attente
    """
    canva_depos.configure(scrollregion=canva_depos.bbox("all"))
    chemin = askopenfilename(title="Ouvrir une image", filetypes= TYPES_FICHIERS)

    lst_fichiers.append(chemin)
    #ajouterLabel(chemin.split("/")[-1], len(lstFichiers))# Surement a changer pour Windows; Permet de juste afficher le nom du fichier et pas le chemin absolu
    ajouter_un_label(chemin, len(lst_fichiers)) # Surement a changer pour Windows; Permet de juste afficher le nom du fichier et pas le chemin absolu
    #TODO adapter pour une seule ligne

    #MAJ taille scrolling
    #https://openclassrooms.com/forum/sujet/taille-d-une-frame-tkinter
    canva_depos.update_idletasks()#Ligne a ajouter sinon thinker considere qu'on veut màj la taille avant que le depos ne soit fait (ce qui est bien sur faut il est fait et affiché au dessus)
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
frame_aide = LabelFrame(fenetre, text='Aide', font=(30)) #TODO un moyen de cacher l'aide
frame_aide.pack(fill=BOTH)

#Dans Frame Aide
label = Label(frame_aide, text="Decription de l'aide")
label.pack()

#Partie depos de fichier et lancement de l'analyse
frame_analyse = LabelFrame(fenetre, text='Fichiers à analyser', font=(30))
frame_analyse.pack(pady=20, expand= True, fill= BOTH)

canva_depos = Canvas(frame_analyse)
canva_depos.configure(scrollregion=canva_depos.bbox("all"))
canva_depos.pack(expand=True, fill=BOTH)

frame_depos = Frame(canva_depos)
canva_depos.create_window(canva_depos.winfo_rootx(), canva_depos.winfo_rooty(), anchor='nw', window=frame_depos)

#Dans Frame depos
#Creation d'une frame sinon le contenu ne pourra pas etre scrollé
labe_vide = Label(frame_depos, text="Aucun fichiers déposés")
labe_vide.pack()

scroll = Scrollbar(canva_depos, orient=HORIZONTAL)
scroll.pack(side=BOTTOM,fill=X)
scroll.config(command=canva_depos.xview)
canva_depos.config(xscrollcommand=scroll.set)

#Dans frameAnalyse
Button(frame_analyse, text='Analyser').pack(side=RIGHT, padx=5, pady=5)

Button(frame_analyse, text='Deposer un fichier', command=ajouter_fichier_a_liste_attente).pack(side=RIGHT, padx=5, pady=5)

#boutton quitter
Button(fenetre,text='Quitter',command=fenetre.destroy).pack(side=RIGHT,padx=5, pady=5)

#TODO Ajout de la partie sortie/feedback

fenetre.mainloop()
