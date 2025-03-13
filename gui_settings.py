import wx

caracteristiques = ['form_title', 'form_id', 'instance_name', 'version', 'public_key', 'submission_url',
                    'default_language']


class Settings(wx.Panel):
    """ Onglet survey """

    def __init__(self, parent):
        super(Settings, self).__init__(parent)

        self.fields = []
        self.values = []

        vbox = wx.BoxSizer(wx.VERTICAL)

        for i in caracteristiques:
            label = wx.StaticText(self, label=i)
            text_ctrl = wx.TextCtrl(self)
            self.fields.append((label, text_ctrl))
            vbox.Add(label, 0, wx.ALL | wx.EXPAND, 5)
            vbox.Add(text_ctrl, 0, wx.ALL | wx.EXPAND, 5)

        create_button = wx.Button(self, label="Ok")
        create_button.SetBackgroundColour("#05f762")

        create_button.Bind(wx.EVT_BUTTON, self.create_action)

        vbox.Add(create_button)

        # Créer un tableau (wx.grid.Grid) pour afficher les objets
        self.grid = wx.grid.Grid(self)
        self.grid.CreateGrid(0, len(caracteristiques))  # 0 lignes initiales, 18 colonnes
        for i in range(len(caracteristiques)):
            self.grid.SetColLabelValue(i, caracteristiques[i])
            self.grid.AutoSizeColLabelSize(i)
        self.grid.AppendRows(1)
        vbox.Add(self.grid, 1, wx.ALL | wx.EXPAND, 10)

        self.SetSizer(vbox)

    def getValues(self):
        self.values = [field.GetValue() for _, field in self.fields]

    def create_action(self, event):
        self.getValues()
        for col, value in enumerate(self.values):
            self.grid.SetCellValue(0, col, value)  # Remplir les cellules
        self.grid.AutoSizeColumns()
