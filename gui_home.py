import wx

from gui_choices import Choices
from gui_survey import Survey


class Home(wx.Frame):
    """ Accueil """

    def __init__(self):
        super(Home, self).__init__(None, title="XlsForm Designer", size=(1200, 600))

        # Créer un notebook (onglets)
        notebook = wx.Notebook(self)

        # Ajouter l'onglet Survey
        survey_tab = Survey(notebook)
        notebook.AddPage(survey_tab, "survey")

        # Ajouter d'autres onglets (exemples)
        choices = Choices(notebook)
        notebook.AddPage(choices, "choices")

        settings = wx.Panel(notebook)
        notebook.AddPage(settings, "settings")

        # Afficher le notebook
        self.Centre()
        self.Show()
