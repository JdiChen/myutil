from openpyxl import load_workbook


class ExcelRW:
    work_book = None

    def __init__(self, path: str):
        if not path.endswith('.xlsx'):
            print("plese use xlsx file")
            raise FileNotFoundError
        self.work_book = load_workbook(path)

    def get_all_sheet(self):
        return self.work_book.sheetnames

    def get_sheet_row_col(self, sheet_name):
        # return self.work_book[sheet_name].active_cell #当前定位的单元格
        """
        :param sheet_name:
        :return: （有数据的总行数，总列数）
        """
        sheet = self.work_book[sheet_name]
        return sheet.max_row, sheet.max_column

    def get_all_cell_value(self, sheet_name):
        """

        :param sheet_name:
        :return:all test cases list
        """
        cell_list = []
        row, col = self.get_sheet_row_col(sheet_name)
        for r in range(1,row+1):
            tmp_list = []
            tmp_dict = {}
            for c in range(1,col+1):
                cell_value = self.work_book[sheet_name].cell(r, c).value
                if r == 1:
                    tmp_dict.key = cell_value
                    continue

                tmp_list.append(cell_value)
            cell_list.append(tmp_list)
        return cell_list


if __name__ == '__main__':
    path = 'test.xlsx'
    a = ExcelRW(path).get_all_cell_value('主页')
    for i in a:
        print(i)
