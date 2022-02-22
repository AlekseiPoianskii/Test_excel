import json
import xlwt


class ColumnTable:
    def __init__(self):
        self.x = None
        self.value = list()

    def get_x(self):
        return self.x

    def set_x(self, x):
        self.x = x

    def add_value(self, value):
        self.value.append(value)

    def get_value(self, i):
        if i > 0:
            return self.value[i]["properties"]["Text"]
        return None

    def get_header(self):
        return self.value[0]["properties"]["QuickInfo"]

    def sort_value(self):
        for j in range(len(self.value)):
            for i in range(len(self.value) - j - 1):
                if self.value[i]["properties"]["Y"] > self.value[i + 1]["properties"]["Y"]:
                    self._change_value(i, i + 1)

    def _change_value(self, i, j):
        temp = self.value[i]
        self.value[i] = self.value[j]
        self.value[j] = temp


class DumpToExcel:
    def __init__(self):
        self.book = xlwt.Workbook()
        self._sheet = list()
        self._name_sheet = list()

    def _get_id_sheet(self, name_sheet):
        i = 0
        name = self._name_sheet[i]
        while name != name_sheet:
            i += 1
            name = self._name_sheet[i]
        return i

    def get_sheet(self, name):
        if name is not self._name_sheet:
            sheet = self.book.add_sheet(name)
            self._name_sheet.append(name)
            self._sheet.append(sheet)
        else:
            sheet = self._sheet[self._get_id_sheet(name)]
        return sheet

    def write_columns(self, columns: list, name_sheet):
        sheet = self.get_sheet(name_sheet)
        col = 0
        for column in columns:
            self._write_column(column, sheet, col)
            col += 1

    def _write_column(self, column: ColumnTable, sheet, col):
        for i in range(0, len(column.value)):
            if i == 0:
                sheet.write(i, col, column.get_header())
                continue
            sheet.write(i, col, column.get_value(i))

    def save(self, name_file):
        self.book.save(name_file)


if __name__ == "__main__":
    book = DumpToExcel()
    for i in range(1, 4):
        with open(f"json_file/test{i}.json", "r") as f:
            dict_json = json.load(f)
        columns = []
        for header in dict_json["headers"]:
            column = ColumnTable()
            column.set_x(header["properties"]["X"])
            column.add_value(header)
            for value in dict_json["values"]:
                if value["properties"]["X"] == column.get_x():
                    column.add_value(value)
            column.sort_value()
            columns.append(column)
        book.write_columns(columns, f"file {i}")
    book.save("test.xls")
