import openpyxl as xl
ex_file = xl.load_workbook("Lear_openpyxl.xlsx")
sheet = ex_file.active
for row in sheet.iter_rows(min_row =2 ,values_only=True):
    print(row)

