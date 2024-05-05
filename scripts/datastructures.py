from dataclasses import dataclass


@dataclass
class Commentaire:
    """Classe pour récuppérer les commentaires"""
    id_fichier : int
    sentiment : str
    commentaire : str
   


