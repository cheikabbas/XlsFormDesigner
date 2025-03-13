import string

import wx

caracteristiques = ['list_name', 'value', 'label', 'filter_1', 'filter_2', 'filter_3', 'filter_4', 'filter_5',
                    'filter_6', 'filter_7', 'filter_8', 'filter_9', 'filter_10']

values_type = ["Nombre 1 (0,1,2,...)", "Nombre 2 (1,2,3,...)", "lettres (a,b,c,...)", "LETTRES (A,B,C,...)"]

filter_nb = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']


class ChoiceValues(wx.Dialog):
    def __init__(self, parent, nbval):
        super(ChoiceValues, self).__init__(parent, title="Valeurs du choice", size=(400, 400))

        self.fields = []
        self.values = []
        self.filters = []

        self.scrolled_window = wx.ScrolledWindow(self)
        self.scrolled_window.SetScrollRate(10, 10)

        vbox = wx.BoxSizer(wx.VERTICAL)

        for i in range(nbval):
            label = wx.StaticText(self.scrolled_window, label=f"Valeur {i+1}")
            val = wx.TextCtrl(self.scrolled_window)
            self.fields.append((label, val))
            vbox.Add(label, 0, wx.ALL | wx.EXPAND, 5)
            vbox.Add(val, 0, wx.ALL | wx.EXPAND, 5)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        create_button = wx.Button(self.scrolled_window, label="Créer")
        create_button.SetBackgroundColour("#05f762")
        cancel_button = wx.Button(self.scrolled_window, label="Annuler")
        cancel_button.SetBackgroundColour("#f7052d")

        create_button.Bind(wx.EVT_BUTTON, self.create_action)
        cancel_button.Bind(wx.EVT_BUTTON, self.cancel_action)

        hbox.Add(create_button)
        hbox.Add(cancel_button)

        vbox.Add(hbox)

        self.scrolled_window.SetSizer(vbox)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(self.scrolled_window, 1, wx.EXPAND)
        self.SetSizer(main_sizer)

        self.Centre()

    def create_action(self, event):
        self.values = [field.GetValue() for _, field in self.fields]
        self.EndModal(wx.ID_OK)

    def cancel_action(self, event):
        self.EndModal(wx.ID_CANCEL)


class NewChoice(wx.Dialog):
    """ Formulaire de remplissage pour nouveau choice"""

    def __init__(self, parent):
        super(NewChoice, self).__init__(parent, title="Nouveau choice", size=(400, 400))

        self.values = []
        self.scrolled_window = wx.ScrolledWindow(self)
        self.scrolled_window.SetScrollRate(10, 10)

        vbox = wx.BoxSizer(wx.VERTICAL)

        self.fields = []
        # for i in caracteristiques:
        # Champs list_name
        label = wx.StaticText(self.scrolled_window, label="list_name")
        self.text_ctrl = wx.TextCtrl(self.scrolled_window)
        vbox.Add(label, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(self.text_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        # Champs Type de valeurs
        label_type = wx.StaticText(self.scrolled_window, label="Type de valeurs")
        self.type_val = wx.ComboBox(self.scrolled_window, choices=values_type)
        self.type_val.SetSelection(0)
        vbox.Add(label_type, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(self.type_val, 0, wx.ALL | wx.EXPAND, 5)

        # Champs nombre de valeurs
        label_nb = wx.StaticText(self.scrolled_window, label="Nombre de valeurs")
        self.text_ctrl_nb = wx.TextCtrl(self.scrolled_window, value="1")
        vbox.Add(label_nb, 0, wx.ALL | wx.EXPAND, 5)
        vbox.Add(self.text_ctrl_nb, 0, wx.ALL | wx.EXPAND, 5)

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        create_button = wx.Button(self.scrolled_window, label="Valider")
        create_button.SetBackgroundColour("#05f762")
        cancel_button = wx.Button(self.scrolled_window, label="Annuler")
        cancel_button.SetBackgroundColour("#f7052d")

        create_button.Bind(wx.EVT_BUTTON, self.create_action)
        cancel_button.Bind(wx.EVT_BUTTON, self.cancel_action)

        hbox.Add(create_button)
        hbox.Add(cancel_button)

        vbox.Add(hbox)

        self.scrolled_window.SetSizer(vbox)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(self.scrolled_window, 1, wx.EXPAND)
        self.SetSizer(main_sizer)

        self.Centre()

    def first_vals(self):
        nb_val = int(self.text_ctrl_nb.GetValue())

        # Ajout des list_name
        for i in range(nb_val):
            self.values.append([self.text_ctrl.GetValue()])

        # Ajout des valeurs
        if self.type_val.GetValue() == "Nombre 1 (0,1,2,...)":
            for i in range(nb_val):
                self.values[i].append(str(i))
        elif self.type_val.GetValue() == "Nombre 2 (1,2,3,...)":
            for i in range(1, nb_val+1):
                self.values[i-1].append(str(i))
        elif self.type_val.GetValue() == "lettres (a,b,c,...)":
            for i in range(nb_val):
                self.values[i].append(list(string.ascii_lowercase)[i])
        else:
            for i in range(nb_val):
                self.values[i].append(list(string.ascii_uppercase)[i])

    def create_action(self, event):
        """Fonction appelée lors de l'enregistrement."""
        nb_val = self.text_ctrl_nb.GetValue()
        if nb_val.isdigit():
            self.first_vals()
            dialog = ChoiceValues(self, int(nb_val))
            if dialog.ShowModal() == wx.ID_OK:
                for i in range(len(dialog.values)):
                    self.values[i].append(dialog.values[i])
            dialog.Destroy()
            self.EndModal(wx.ID_OK)
        else:
            wx.MessageBox("Veuillez entrer uniquement des chiffres entiers pour les nombres de valeurs et de filtres.",
                          "Erreur", wx.OK | wx.ICON_ERROR)

    def cancel_action(self, event):
        """Fonction appelée lors de l'annulation."""
        self.EndModal(wx.ID_CANCEL)


class Choices(wx.Panel):
    """ Onglet survey """

    def __init__(self, parent):
        super(Choices, self).__init__(parent)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        new_item_btn = wx.Button(self, label="Nouveau")
        new_item_btn.SetBackgroundColour("#05f762")
        del_item_btn = wx.Button(self, label="Supprimer")
        del_item_btn.SetBackgroundColour("#f7052d")

        new_item_btn.Bind(wx.EVT_BUTTON, self.newItem)
        del_item_btn.Bind(wx.EVT_BUTTON, self.delItem)

        hbox.Add(new_item_btn, 0, wx.ALL, 5)
        hbox.Add(del_item_btn, 0, wx.ALL, 5)

        vbox.Add(hbox, 0, wx.ALL | wx.EXPAND, 10)

        # Créer un tableau (wx.grid.Grid) pour afficher les objets
        self.grid = wx.grid.Grid(self)
        self.grid.CreateGrid(0, len(caracteristiques))  # 0 lignes initiales, 18 colonnes
        for i in range(len(caracteristiques)):
            self.grid.SetColLabelValue(i, caracteristiques[i])
            self.grid.AutoSizeColLabelSize(i)
        vbox.Add(self.grid, 1, wx.ALL | wx.EXPAND, 10)

        self.SetSizer(vbox)

    def newItem(self, event):
        dialog = NewChoice(self)
        if dialog.ShowModal() == wx.ID_OK:
           for i in range(len(dialog.values)):
               # Ajouter une nouvelle ligne au tableau
               row = self.grid.GetNumberRows()
               self.grid.AppendRows(1)  # Ajouter une nouvelle ligne
               for col, value in enumerate(dialog.values[i]):
                   self.grid.SetCellValue(row, col, str(value))  # Remplir les cellules
               self.grid.AutoSizeColumns()
        dialog.Destroy()

    def delItem(self, event):
        """Fonction appelée pour supprimer un objet."""
        selected_row = self.grid.GetGridCursorRow()
        if selected_row >= 0:
            dialog = wx.MessageDialog(self, f'Voulez-vous vraiment supprimer cette ligne ?', 'Suppression',
                                      wx.YES_NO)
            answer = dialog.ShowModal()
            dialog.Destroy()
            if answer == wx.ID_YES:
                self.grid.DeleteRows(selected_row, 1)  # Supprimer la ligne sélectionnée
        else:
            wx.MessageBox("Veuillez sélectionner une ligne à supprimer.", "Erreur", wx.OK | wx.ICON_WARNING)
