import wx
import wx.grid

# Liste des caractéristiques
caracteristiques = ["type", "name", "label", "hint", "relevant", "constraint", "constraint_message", "appearance",
                    "required", "calculation", "choice_filter", "repeat_count", "default", "read_only",
                    "image", "comment", "required_message", "body::accuracyThreshold"]

types = ["acknowledge",	"audio",	"background-audio",	"barcode",	"calculate",	"date",	"dateTime",	"decimal",
         "file",	"geopoint",	"geoshape",	"geotrace",	"hidden",	"image",	"integer",	"note",	"range",	"rank",
         "select_multiple",	"select_multiple_from_file",	"select_one",	"select_one_from_file",	"text",	"time",
         "video",	"xml-external"]

appearances = ["compact",	"draw",	"field-list",	"horizontal",	"horizontal-compact",	"label",	"likert",
               "list-nolabel",	"minimal",	"month-year",	"multiline",	"no-calendar",	"quick",	"quickcompact",
               "signature",	"table-list",	"year"]


booleens = ["yes", "no"]


class NewItem(wx.Dialog):
    """ Formulaire de remplissage de caractéristiques """

    def __init__(self, parent):
        super(NewItem, self).__init__(parent, title="Nouvel item", size=(400, 800))

        # Créer une fenêtre défilable
        self.values = None
        self.scrolled_window = wx.ScrolledWindow(self)
        self.scrolled_window.SetScrollRate(10, 10)  # Vitesse de défilement

        # Vertical container
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Creating fields
        self.fields = []
        for i in caracteristiques:
            if i == "type":
                label = wx.StaticText(self.scrolled_window, label=i)
                text_ctrl = wx.ComboBox(self.scrolled_window, choices=types)
                self.fields.append((label, text_ctrl))
                vbox.Add(label, 0, wx.ALL | wx.EXPAND, 5)
                vbox.Add(text_ctrl, 0, wx.ALL | wx.EXPAND, 5)
            elif i == "appearance":
                label = wx.StaticText(self.scrolled_window, label=i)
                text_ctrl = wx.ComboBox(self.scrolled_window, choices=appearances)
                self.fields.append((label, text_ctrl))
                vbox.Add(label, 0, wx.ALL | wx.EXPAND, 5)
                vbox.Add(text_ctrl, 0, wx.ALL | wx.EXPAND, 5)
            elif i == "read_only":
                label = wx.StaticText(self.scrolled_window, label=i)
                text_ctrl = wx.ComboBox(self.scrolled_window, choices=booleens)
                text_ctrl.SetSelection(1)
                self.fields.append((label, text_ctrl))
                vbox.Add(label, 0, wx.ALL | wx.EXPAND, 5)
                vbox.Add(text_ctrl, 0, wx.ALL | wx.EXPAND, 5)
            elif i == "required":
                label = wx.StaticText(self.scrolled_window, label=i)
                text_ctrl = wx.ComboBox(self.scrolled_window, choices=booleens)
                text_ctrl.SetSelection(0)
                self.fields.append((label, text_ctrl))
                vbox.Add(label, 0, wx.ALL | wx.EXPAND, 5)
                vbox.Add(text_ctrl, 0, wx.ALL | wx.EXPAND, 5)
            else:
                label = wx.StaticText(self.scrolled_window, label=i)
                text_ctrl = wx.TextCtrl(self.scrolled_window)
                self.fields.append((label, text_ctrl))
                vbox.Add(label, 0, wx.ALL | wx.EXPAND, 5)
                vbox.Add(text_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        # Buttons
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
        """Fonction appelée lors de l'enregistrement."""
        self.values = [field.GetValue() for _, field in self.fields]
        self.EndModal(wx.ID_OK)

    def cancel_action(self, event):
        """Fonction appelée lors de l'annulation."""
        self.EndModal(wx.ID_CANCEL)


class Survey(wx.Panel):
    """ Onglet survey """

    def __init__(self, parent):
        super(Survey, self).__init__(parent)

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
        dialog = NewItem(self)
        if dialog.ShowModal() == wx.ID_OK:
            # Ajouter une nouvelle ligne au tableau
            row = self.grid.GetNumberRows()
            self.grid.AppendRows(1)  # Ajouter une nouvelle ligne
            for col, value in enumerate(dialog.values):
                self.grid.SetCellValue(row, col, value)  # Remplir les cellules
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
        choices = wx.Panel(notebook)
        notebook.AddPage(choices, "choices")

        settings = wx.Panel(notebook)
        notebook.AddPage(settings, "settings")

        # Afficher le notebook
        self.Centre()
        self.Show()
