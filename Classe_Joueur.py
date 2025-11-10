# On créé la classe Joueur qui nous permettra d'avoir le nom du joueur, le nombre de ses victoires
# et défaites ainsi que les différents grades qu'il a obtenu au cours de ses parties
class Joueur :
    def __init__(self, nom, victoires = 0, defaites = 0, passager_clandestin = 0, matelot = 0, marin = 0, lieutenant = 0, amiral = 0, legende_des_mers = 0) :
        self.nom = nom
        self.victoires = victoires
        self.defaites = defaites
        self.passager_clandestin = passager_clandestin
        self.matelot = matelot
        self.marin = marin
        self.lieutenant = lieutenant
        self.amiral = amiral
        self.legende_des_mers = legende_des_mers

    # Créé un dictionnaire avec toutes les informations du joueur
    def vers_dico(self) :
        return {
            "nom" : self.nom,
            "victoires" : self.victoires,
            "defaites" : self.defaites,
            "passager_clandestin" : self.passager_clandestin,
            "matelot" : self.matelot,
            "marin" : self.marin,
            "lieutenant" : self.lieutenant,
            "amiral" : self.amiral,
            "legende_des_mers" : self.legende_des_mers
        }

    # Prend les informations du dictionnaire
    def depuis_dico(data) :
        return Joueur(
            data["nom"],
            data["victoires"],
            data["defaites"],
            data["passager_clandestin"],
            data["matelot"],
            data["marin"],
            data["lieutenant"],
            data["amiral"],
            data["legende_des_mers"]
        )

# Définition de la classe GestionJoueurs qui gère le fichier Joueurs.txt
class GestionJoueurs :
    def __init__(self, filename) :
        # Prend le nom du document en paramètre
        self.filename = filename

    # Lecture de la liste des joueurs
    def charger_joueurs(self) :
        # Création d'une liste vide qui contiendra les noms des joueurs
        joueurs = []
        # Ouvre le fichier en mode lecture
        with open(self.filename, 'r') as fichier :
            # Prend les joueurs ligne par ligne
            for line in fichier :
                data = eval(line.strip())
                # Ajoute chaque joueur à la liste petit à petit
                joueurs.append(Joueur.depuis_dico(data))
        # return la liste des joueurs pour qu'elle soit utilisable
        return joueurs

    # Enregistre la liste des joueurs
    def enregistrer_joueurs(self, joueurs) :
        # Ouvre le fichier en mode écriture
        with open(self.filename, 'w') as fichier :
            # Ecrit les noms de tous les joueurs pour faire une sauvegarde
            for joueur in joueurs :
                fichier.write(str(joueur.vers_dico()) + "\n")

    # Vérifie si le joueur existe
    def est_enregistre(self, nom) :
        # Prend la liste des joueurs
        joueurs = self.charger_joueurs()
        # Renvoie True si le nom du joueur est dans le fichier
        return any(joueur.nom == nom for joueur in joueurs)

    # Enregistre un nouveau joueur
    def enregistrer_joueur(self, joueur) :
        # Prend la liste des joueurs
        joueurs = self.charger_joueurs()
        # Ajoute le joueur pris en paramètre
        joueurs.append(joueur)
        # Enregistre la nouvelle liste
        self.enregistrer_joueurs(joueurs)

    # Lire un paramètre du joueur
    def lire_parametre(self, nom, parametre) :
        # Prend la liste des joueurs
        joueurs = self.charger_joueurs()
        # Cherche quel joueur a été demandé en paramètre
        for joueur in joueurs :
            if joueur.nom == nom :
                # Renvoie la valeur du paramètre demandé quand il a trouvé le joueur correspondant
                return getattr(joueur, parametre)

    # Modifie un paramètre de la valeur indiquée (+1 a priori)
    def incrementer_parametre(self, nom, parametre, valeur = 1) :
        # Prend la liste des joueurs
        joueurs = self.charger_joueurs()
        # Cherche quel joueur a été demandé en paramètre
        for joueur in joueurs :
            if joueur.nom == nom :
                # Créé une variable "valeur actuelle" qui est le paramètre demandé pour pouvoir y ajouter ensuite la valeur demandée
                valeur_actuelle = self.lire_parametre(nom, parametre)
                # Ajoute la valeur indiquée au paramètre voulu
                setattr(joueur, parametre, valeur_actuelle + valeur)
        # Enregistre la nouvelle liste
        self.enregistrer_joueurs(joueurs)