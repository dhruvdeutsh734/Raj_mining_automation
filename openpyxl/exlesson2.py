import openpyxl as xl
excel_file = xl.load_workbook("Lear_openpyxl.xlsx")
sheet = excel_file.active
print(sheet["A1"].value ,"-" ,sheet["A2"].value)
print(sheet["B1"].value ,"-" ,sheet["B2"].value)
print(sheet["C1"].value ,"-" ,sheet["C2"].value)