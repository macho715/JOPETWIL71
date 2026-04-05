Attribute VB_Name = "mod_JPT71_RefreshAll"
Option Explicit

'==========================================================
' JPT71 - One Button Refresh
' - Reads current workbook path
' - Runs Python to rebuild Cross_Gantt into a NEW output file
' - Opens refreshed file
'
' IMPORTANT:
' 1) Update SCRIPT_PATH to the real path on your PC
' 2) Python must be installed (py command available) or set PY_EXE full path
'==========================================================

Private Const PY_EXE As String = "py"
Private Const SCRIPT_PATH As String = "C:\Path\jpt71_refresh_all.py"

Public Sub Refresh_All_OneButton()
    On Error GoTo EH

    Dim inPath As String, outPath As String
    inPath = ThisWorkbook.FullName
    outPath = Left(inPath, InStrRev(inPath, ".") - 1) & "_REFRESHED.xlsx"

    ' Save current changes first
    ThisWorkbook.Save

    Dim cmd As String
    cmd = """" & PY_EXE & """ """ & SCRIPT_PATH & """ """ & inPath & """ """ & outPath & """"

    ' Run and wait
    Dim sh As Object, ex As Object
    Set sh = CreateObject("WScript.Shell")
    Set ex = sh.Exec(cmd)

    Do While ex.Status = 0
        DoEvents
    Loop

    If ex.ExitCode <> 0 Then
        MsgBox "Python failed:" & vbCrLf & ex.StdErr.ReadAll, vbExclamation
        Exit Sub
    End If

    ' Open refreshed file
    Application.Workbooks.Open outPath
    MsgBox "Refreshed file created & opened:" & vbCrLf & outPath, vbInformation
    Exit Sub

EH:
    MsgBox "Refresh_All_OneButton Error: " & Err.Description, vbExclamation
End Sub
