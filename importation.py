import os

import wx
import pandas as pd


class Import(wx.Panel):
    """Onglet d'exportation"""

    def __init__(self, parent, survey, choices, settings):
        super(Import, self).__init__(parent)

        self.survey = survey
        self.choices = choices
        self.settings = settings

        self.path = ""

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.ctrl_dir = wx.TextCtrl(self, style=wx.TE_READONLY, value="Aucun fichier choisi")

        self.btn_select_dir = wx.Button(self, label="Choisir un fichier")
        self.btn_select_dir.Bind(wx.EVT_BUTTON, self.on_choose_file)

        hbox.Add(self.ctrl_dir, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        hbox.Add(self.btn_select_dir, flag=wx.ALL, border=5)

        vbox.Add(hbox, 0, wx.ALL | wx.EXPAND, 5)

        self.import_btn = wx.Button(self, label="Importer le fichier")
        self.import_btn.SetBackgroundColour("#05f762")
        self.import_btn.Bind(wx.EVT_BUTTON, self.on_import)

        vbox.Add(self.import_btn, 0, wx.ALL, 5)

        self.SetSizer(vbox)

    def on_choose_file(self, event):
        """Ouvre un sélecteur de fichier et met à jour le TextCtrl avec le chemin du fichier choisi."""
        with wx.FileDialog(self, "Choisir un fichier", wildcard="Fichiers Excel (*.xlsx)|*.xlsx",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return  # L'utilisateur a annulé

            # Récupération du chemin sélectionné et mise à jour du TextCtrl
            self.path = file_dialog.GetPath()
            self.ctrl_dir.SetValue(self.path)

    def on_import(self, event):
        """Importer les données d'un fichier Excel dans les grids."""

        # Lire les feuilles du fichier Excel avec pandas
        try:
            survey_df = pd.read_excel(self.path, sheet_name="survey", keep_default_na=False)
            choices_df = pd.read_excel(self.path, sheet_name="choices", keep_default_na=False)
            settings_df = pd.read_excel(self.path, sheet_name="settings", keep_default_na=False)
        except Exception as e:
            wx.MessageBox("Erreur lors de la lecture du fichier Excel", "Erreur", wx.OK | wx.ICON_ERROR)
            return

        # Importer les données dans les grids
        self.import_data_to_grid(self.survey.grid, survey_df)
        self.import_data_to_grid(self.choices.grid, choices_df)
        self.import_data_to_grid(self.settings.grid, settings_df)

        wx.MessageBox("Importation réussie !", "Succès", wx.OK | wx.ICON_INFORMATION)

    def import_data_to_grid(self, grid, dataframe):
        """Importer les données d'un DataFrame pandas dans un wx.grid.Grid."""
        # Remplir le grid avec les données du DataFrame
        for row in range(dataframe.shape[0]):
            grid.AppendRows(1)
            for col in range(dataframe.shape[1]):
                value = str(dataframe.iat[row, col])  # Convertir la valeur en chaîne
                grid.SetCellValue(row, col, value)
        grid.AutoSizeColumns()

        # Ajouter les en-têtes de colonnes
        for col, column_name in enumerate(dataframe.columns):
            grid.SetColLabelValue(col, str(column_name))
