args = WScript.Arguments.Count

if args <> 2 then
  WScript.Echo "usage: PostHTTP.vbs URL File"
  WScript.Quit
end if

URL = WScript.Arguments.Item(0)
File = WScript.Arguments.Item(1)

Set WshShell = WScript.CreateObject("WScript.Shell")

Const ForReading = 1
Set objFSO = CreateObject("Scripting.FileSystemObject")
Set objFile = objFSO.OpenTextFile(File, ForReading)
strContents = objFile.ReadAll
objFile.Close

Set http = CreateObject("Microsoft.XmlHttp")
http.open "POST", URL, FALSE
http.send strContents
WScript.Echo http.getAllResponseHeaders

set http = nothing
set WshShell= nothing
