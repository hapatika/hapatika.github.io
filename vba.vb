Sub RunPythonAndImportCSV()
    Dim shell As Object
    Dim pythonExe As String
    Dim pythonScript As String
    Dim csvFile As String
    Dim ws As Worksheet
    Dim csvLine As String
    Dim csvContents As Variant
    Dim rowNum As Long
    Dim fso As Object
    Dim ts As Object

    ' --- EDIT THESE ---
    pythonExe = "C:\Users\YourUser\Anaconda3\python.exe"
    pythonScript = "C:\path\to\your_script.py"
    csvFile = "C:\path\to\output.csv"
    ' -------------------

    Set ws = ActiveSheet

    ' Run the Python script
    Set shell = CreateObject("WScript.Shell")
    shell.Run """" & pythonExe & """" & " " & """" & pythonScript & """", 0, True

    ' Wait for CSV to be created (optional: add error handling or check for file existence)
    Application.Wait (Now + TimeValue("0:00:02"))

    ' Read the CSV file
    Set fso = CreateObject("Scripting.FileSystemObject")
    If Not fso.FileExists(csvFile) Then
        MsgBox "CSV file not found: " & csvFile, vbCritical
        Exit Sub
    End If

    Set ts = fso.OpenTextFile(csvFile, 1)
    rowNum = 1
    Do While Not ts.AtEndOfStream
        csvLine = ts.ReadLine
        ' Split CSV line by comma
        csvContents = Split(csvLine, ",")
        ' Write each cell to column AP (col 42)
        Dim i As Integer
        For i = LBound(csvContents) To UBound(csvContents)
            ws.Cells(rowNum, 42 + i).Value = csvContents(i)
        Next i
        rowNum = rowNum + 1
    Loop
    ts.Close

    MsgBox "Import complete!", vbInformation
End Sub

' 2

        Sub ImportAndProcessTickers()
    Dim wbA As Workbook
    Dim wbB As Workbook
    Dim wsA As Worksheet
    Dim wsB As Worksheet
    Dim filePath As String
    Dim lastRowB As Long
    Dim outputRow As Long
    Dim tickerCol As Long, reqdCol As Long, locCol As Long
    Dim r As Long
    Dim ticker As String, qtyReqd As Double, qtyLoc As Double, diff As Double
    Dim header As Range

    ' Set references
    Set wbA = ThisWorkbook
    Set wsA = wbA.Sheets(1) ' Change to your output sheet name or index

    ' Prompt for Workbook B path
    filePath = Application.GetOpenFilename("Excel Files (*.xls*),*.xls*", , "Select Workbook B")
    If filePath = "False" Then Exit Sub ' User cancelled

    ' Open Workbook B
    Set wbB = Workbooks.Open(filePath)
    Set wsB = wbB.Sheets(1) ' Change if needed

    ' Find columns by header in Workbook B
    Set header = wsB.Rows(1)
    For Each cell In header.Cells
        If Trim(cell.Value) = "QTY (Reqd)" Then reqdCol = cell.Column
        If Trim(cell.Value) = "QTY (Loc)" Then locCol = cell.Column
        If InStr(1, cell.Value, "CODE", vbTextCompare) > 0 Or InStr(1, cell.Value, "TICKER", vbTextCompare) > 0 Then tickerCol = cell.Column
    Next cell

    If tickerCol = 0 Or reqdCol = 0 Or locCol = 0 Then
        MsgBox "Could not find all necessary columns in Workbook B!", vbCritical
        wbB.Close False
        Exit Sub
    End If

    ' Output headers in Workbook A
    wsA.Cells(1, 1).Value = "Ticker"
    wsA.Cells(1, 2).Value = "QTY (Reqd)"
    wsA.Cells(1, 3).Value = "QTY (Loc)"
    wsA.Cells(1, 4).Value = "Diff (Reqd-Loc)"

    outputRow = 2

    lastRowB = wsB.Cells(wsB.Rows.Count, tickerCol).End(xlUp).Row

    For r = 2 To lastRowB
        ticker = Trim(wsB.Cells(r, tickerCol).Value)
        If ticker <> "" And (Right(ticker, 3) = ".SH" Or Right(ticker, 3) = ".SS") Then
            qtyReqd = wsB.Cells(r, reqdCol).Value
            qtyLoc = wsB.Cells(r, locCol).Value
            If Right(ticker, 3) = ".SH" Then
                ticker = Left(ticker, Len(ticker) - 3) & ".SS"
            End If
            diff = qtyReqd - qtyLoc

            wsA.Cells(outputRow, 1).Value = ticker
            wsA.Cells(outputRow, 2).Value = qtyReqd
            wsA.Cells(outputRow, 3).Value = qtyLoc
            wsA.Cells(outputRow, 4).Value = diff

            outputRow = outputRow + 1
        End If
    Next r

    wbB.Close False
    MsgBox "Done!"
End Sub
        
