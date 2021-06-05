import string
import win32com.client as win32

def GetWorksheetColumn(x : int):
    '''
    Converts an x-value to the corresponding column in excel. Assumes x is 0-indexed.
    '''
    base = int(x/26)
    reminder = x % 26

    if(base == 0):
        return string.ascii_lowercase[reminder]
    else:
        return string.ascii_lowercase[base-1] + GetWorksheetColumn(reminder)

def XYToCellCoordinates(x : int, y : int):
    '''
    Converts a pixel coordinate to a cell in an excel worksheet. Assumes that x and y start at index 0.
    '''
    return GetWorksheetColumn(x) + str(y+1)

def RgbToHex(rgb):
    '''
    Cells.Interior.color uses bgr in hex
    '''
    bgr = (rgb[2], rgb[1], rgb[0])
    strValue = '%02x%02x%02x' % bgr
    # print(strValue)
    iValue = int(strValue, 16)
    return iValue

def FillPixel(worksheet, range, color_rgb):
    r = worksheet.Range(range)
    r.Interior.Pattern = win32.constants.xlSolid
    r.Interior.PatternColorIndex = win32.constants.xlAutomatic
    r.Interior.Color = RgbToHex(color_rgb)

def PrintText(worksheet, cell, text : str):
    worksheet.Range(cell).Value = text

def SetCellSize(worksheet, cell, sizeX: float, sizeY: float):
    selection = worksheet.Range( cell )
    selection.ColumnWidth = sizeX
    selection.RowHeight = sizeY

def GetNewWorkSheet():
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    wb = excel.Workbooks.Add()
    ws = wb.Worksheets("Sheet1")
    ws.ScrollArea = "A1:T22"
    excel.Visible = True
    return ws