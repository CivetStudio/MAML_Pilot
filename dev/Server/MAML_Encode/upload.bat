@echo off

rem 检查是否提供了文件路径参数
if "%~1" == "" (
    echo No file path provided. Drag and drop a file onto this batch file to upload.
    echo "请拖入一个文件并命名为 maml.xml 上传至服务器"
    pause>nul
    exit /b
)

rem 提取拖放的文件路径
set "file_path=%~1"

rem 检查文件名是否为 maml.xml
for %%I in ("%file_path%") do set "file_name=%%~nxI"
if /i "%file_name%" neq "maml.xml" (
    echo Invalid file name. Please ensure the file name is 'maml.xml'.
    echo "文件名无效，请确保文件名为 'maml.xml'。"
    pause>nul
    exit /b
)

rem 使用 FOR 命令获取文件大小
for %%F in ("%file_path%") do set "file_size=%%~zF"

rem 检查文件大小是否小于等于 1MB
if %file_size% LEQ 1048576 (
    rem 使用 curl 将文件上传到服务器
    REM curl -X POST -F "file=@%file_path%" http://192.168.0.19:9975/api/send_text_data > manifest.xml
    curl -X POST -F "file=@%file_path%" http://31ds6tk49329.vicp.fun/api/send_text_data > manifest.xml

    rem 提示上传完成
    echo File uploaded successfully.
    echo "文件上传成功"
) else (
    echo File size exceeds 1MB limit. Please upload a file with size less than or equal to 1MB.
    echo "文件大小超过了1MB的限制，请上传大小小于或等于1MB的文件。"
)

pause>nul

