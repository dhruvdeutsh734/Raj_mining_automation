import openpyxl as xl
excel_sheet = xl.load_workbook("RAJ_MINING_DEVICES.xlsx")
sheet = excel_sheet.active
print(sheet["A1"].value)
for i in sheet:
    print(sheet[i].value)

