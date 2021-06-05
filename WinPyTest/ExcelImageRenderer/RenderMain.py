import time
import win32com.client as win32

def FillRangeYellow(range : str):
    r = ws.Range(range)
    r.Interior.Pattern = win32.constants.xlSolid
    r.Interior.PatternColorIndex = win32.constants.xlAutomatic
    r.Interior.ThemeColor = win32.constants.xlThemeColorAccent2

excel = win32.gencache.EnsureDispatch('Excel.Application')
wb = excel.Workbooks.Add()
ws = wb.Worksheets("Sheet1")

r = ws.Range("a1:v25")
r.Interior.Pattern = win32.constants.xlSolid
r.Interior.PatternColorIndex = win32.constants.xlAutomatic
r.Interior.ThemeColor = win32.constants.xlThemeColorAccent1
r.Interior.TintAndShade = -0.249977111117893
r.Interior.PatternTintAndShade = 0

# Print 'H'

FillRangeYellow("b3:b21")
time.sleep(0.5)
FillRangeYellow("c12:d13")
time.sleep(0.5)
FillRangeYellow("e3:e21")

# Print 'E'

time.sleep(0.5)
FillRangeYellow("h3:j4")
time.sleep(0.5)
FillRangeYellow("h12:j13")
time.sleep(0.5)
FillRangeYellow("h20:j21")
time.sleep(0.5)
FillRangeYellow("g3:g21")

# Print 'J'

time.sleep(0.5)
FillRangeYellow("o5:o21")
time.sleep(0.5)
FillRangeYellow("l3:o4")
FillRangeYellow("l20:n21")
FillRangeYellow("l18:l19")

# Print '!'

time.sleep(0.5)
for x in range(3,17):
    FillRangeYellow("q" + str(x))
    time.sleep(0.2)

time.sleep(0.8)
FillRangeYellow("q19:q21")

# Print some text last
time.sleep(0.5)
ws.Range("l12").Value = "Hello World!"
ws.Range("l14").Value = "By Niclas :)"