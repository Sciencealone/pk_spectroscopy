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
        self.alkaline_volumes = []
        self.ph_values = []

        self._load_data()

    def _load_data(self):

        # Load workbook
        wb = load_workbook(self.source_file)
        ws = wb.active

        # Get sample information
        self.sample_name = ws['A1'].value
        self.comment = ws['A2'].value
        self.timestamp = ws['A3'].value
        self.sample_volume = ws['A4'].value
        self.alkaline_concentration = ws['A5'].value

        # Get titration data
        shift = 0
        while True:
            volume = ws[f'A{6 + shift}'].value
            ph = ws[f'B{6 + shift}'].value

            if self._check_number(volume) and self._check_number(ph):
                self.alkaline_volumes.append(volume)
                self.ph_values.append(ph)
                shift += 1
            else:
                break

    @staticmethod
    def _check_number(a):
        return type(a) == int or type(a) == float
