import string
import time
import win32com.client as win32
from PIL import Image

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

def FillPixel(worksheet, range, color_hex):
    r = worksheet.Range(range)
    r.Interior.Pattern = win32.constants.xlSolid
    r.Interior.PatternColorIndex = win32.constants.xlAutomatic
    r.Interior.Color = color_hex

if __name__ == "__main__":
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    wb = excel.Workbooks.Add()
    ws = wb.Worksheets("Sheet1")
    excel.Visible = True

    start_time =time.time()

    with Image.open("Pyramids_M.jpg") as image:
    #with Image.open("Pyramids_200x180.jpg") as image:
    #with Image.open("Mario.jpg") as image:
        if(image.mode != "RGB"):
            print("Error: RGB mode is only supported mode for image.")
            quit()

        size_x, size_y = image.size

        for x in range(size_x):
            for y in range(size_y):
                rgb = image.getpixel( (x,y ))
                color_hex = RgbToHex(rgb)

                ws.Range( GetWorksheetColumn(x) + str(y+1)).RowHeight = 1.5 # 2 px
                ws.Range( GetWorksheetColumn(x) + str(y+1)).ColumnWidth = 0.17 # 2 px

                cell = XYToCellCoordinates(x, y)
                FillPixel(ws, cell, color_hex)
    
    end_time = time.time()
    print("Run complete in %s seconds." % str(end_time - start_time))