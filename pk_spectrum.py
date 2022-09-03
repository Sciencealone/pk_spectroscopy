from openpyxl import load_workbook


class pKSpectrum():
    def __init__(self, source_file):
        self.source_file = source_file
        self.sample_name = None
        self.comment = None
        self.date = None
        self.time = None
        self.sample_volume = None
        self.alkaline_concentration = None
        self.alkaline_volumes = None
        self.ph_values = None

        self._load_data()

    def _load_data(self):
        wb = load_workbook(self.source_file)
        ws = wb.active

        self.sample_name = ws['A1'].value
        self.comment = ws['A2'].value
        self.date = ws['A3'].value
        self.time = ws['A4'].value
        self.sample_volume = ws['A5'].value
        self.alkaline_concentration = ws['A6'].value
