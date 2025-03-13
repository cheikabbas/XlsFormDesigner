import wx

from export import Export
from gui_choices import Choices
from gui_settings import Settings
from gui_survey import Survey


class Home(wx.Frame):
    """ Accueil """

    def __init__(self):
        super(Home, self).__init__(None, title="XlsForm Designer", size=(1200, 600))

        # Créer un notebook (onglets)
        notebook = wx.Notebook(self)

        # Ajouter l'onglet Survey
        survey = Survey(notebook)
        notebook.AddPage(survey, "survey")

        # Ajouter d'autres onglets (exemples)
        choices = Choices(notebook)
        notebook.AddPage(choices, "choices")

        settings = Settings(notebook)
        notebook.AddPage(settings, "settings")

        export = Export(notebook, survey, choices, settings)
        notebook.AddPage(export, "Exportation")

        # Afficher le notebook
        self.Centre()
        self.Show()
