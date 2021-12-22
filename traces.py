import os
from datetime import datetime


class Traces:

    def __init__(self):
        self.dossier = "Parties"
        if not os.path.exists(self.dossier):
            os.makedirs(self.dossier, mode=0o777, exist_ok=False)  # création de trace dossier s'il n'existe pas encore
            print("dossier bien crée")
        self.nomFichier = ""

    def createFile(self, name):
        """ Méthode de création du fichier de trâce du jeu, le format du nom du fichier sera donc
            YYYY-MM-DD_HH-MM-SS_name

            Parameters
            ---------
            :param name : str
                nom de celui qui a lancé la partie
        """
        now = datetime.now()

        # YYYY-MM-DD H:M:S
        dt_string = now.strftime("%Y-%m-%d_%H-%M-%S")
        self.nomFichier = dt_string + "_" + name
        try:
            with open('{0}/{1}.txt'.format(self.dossier, self.nomFichier), 'a', encoding="utf-8") as target:
                target.write("# --- Davy Back Fight ---#\n")
                target.write("Session lancée par: {0}\n\n".format(name))
        except FileNotFoundError:
            print("Le dossier {} ou le fichier {} n'existe pas".format(self.dossier, self.nomFichier))
        finally:
            target.close()
        return

    def numberPlayer(self, tabPlayer: [str]):
        """ Méthode de sauvegarde des joueurs de la partie
                YYYY-MM-DD_HH:MM:SS_name

                Parameters
                ---------
                :param tabPlayer : [str]
                    tableau contenant le nom des joueurs
        """
        try:
            with open('{0}/{1}.txt'.format(self.dossier, self.nomFichier), 'a', encoding="utf-8") as target:
                target.write("# --- JOUEURS ---#\n")
                target.write("# --- [EQUIPE 1] ---#\n")
                for playerTeam1 in range(len(tabPlayer[0])):
                    target.write("#{0} - {1}\n".format(playerTeam1 + 1, tabPlayer[0][playerTeam1]))
                target.write("# --- [EQUIPE 2] ---#\n")
                for playerTeam2 in range(len(tabPlayer[1])):
                    target.write("#{0} - {1}\n".format(playerTeam2 + 1, tabPlayer[1][playerTeam2]))
                target.write("\n")
        except FileNotFoundError:
            print("Le dossier {} ou le fichier {} n'existe pas".format(self.dossier, self.nomFichier))
        finally:
            target.close()
        return

    def traceQuestionQuiz(self):
        """ Méthode d'annone que l'on est sur la partie quiz des questions
              YYYY-MM-DD_HH:MM:SS_name

        """
        try:
            with open('{0}/{1}.txt'.format(self.dossier, self.nomFichier), 'a', encoding="utf-8") as target:
                target.write("# ---*** [QUIZ] ***---#\n")
                target.write("\n")
        except FileNotFoundError:
            print("Le dossier {} ou le fichier {} n'existe pas".format(self.dossier, self.nomFichier))
        finally:
            target.close()
        return

    def traceQuestionImage(self):
        """ Méthode d'annone que l'on est sur la partie quiz des questions
              YYYY-MM-DD_HH:MM:SS_name

        """
        try:
            with open('{0}/{1}.txt'.format(self.dossier, self.nomFichier), 'a', encoding="utf-8") as target:
                target.write("# ---*** [IMAGES] ***---#\n")
                target.write("\n")
        except FileNotFoundError:
            print("Le dossier {} ou le fichier {} n'existe pas".format(self.dossier, self.nomFichier))
        finally:
            target.close()
        return

    def saveTraceQuestions(self, numQuestion, question, answer, typeQuestion):
        """ Méthode de sauvegarde des questions de la partie
                YYYY-MM-DD_HH:MM:SS_name

                Parameters
                ---------
                :param numQuestion : int
                    numéro de la question en cours
                :param question : str
                    question
                :param answer : [str]
                    réponse de la question
                :param typeQuestion : int
                    type de question
        """
        try:
            with open('{0}/{1}.txt'.format(self.dossier, self.nomFichier), 'a', encoding="utf-8") as target:
                target.write("# --- [Question {}] ---#\n".format(numQuestion + 1))
                target.write("# --- Question: {} ---#\n".format(question))
                target.write("# --- Réponse(s): {} ---#\n".format(answer))
                target.write("# --- type de questions: {} ---#\n".format(typeQuestion))
        except FileNotFoundError:
            print("Le dossier {} ou le fichier {} n'existe pas".format(self.dossier, self.nomFichier))
        finally:
            target.close()
        return

    def saveTraceAnswer(self, namePlayer, answer):
        """ Méthode de sauvegarde des questions de la partie
                YYYY-MM-DD_HH:MM:SS_name

            Parameters
            ---------
            :param namePlayer : str
                nom du joueur
            :param answer : str
                réponse de la question
        """
        try:
            with open('{0}/{1}.txt'.format(self.dossier, self.nomFichier), 'a', encoding="utf-8") as target:
                target.write("Joueur : {} , réponse : {} namePlayer".format(namePlayer, answer))
                target.write("\n")
        except FileNotFoundError:
            print("Le dossier {} ou le fichier {} n'existe pas".format(self.dossier, self.nomFichier))
        finally:
            target.close()
        return
