@echo off

rem ����Ƿ��ṩ���ļ�·������
if "%~1" == "" (
    echo No file path provided. Drag and drop a file onto this batch file to upload.
    echo "������һ���ļ�������Ϊ maml.xml �ϴ���������"
    pause>nul
    exit /b
)

rem ��ȡ�Ϸŵ��ļ�·��
set "file_path=%~1"

rem ����ļ����Ƿ�Ϊ maml.xml
for %%I in ("%file_path%") do set "file_name=%%~nxI"
if /i "%file_name%" neq "maml.xml" (
    echo Invalid file name. Please ensure the file name is 'maml.xml'.
    echo "�ļ�����Ч����ȷ���ļ���Ϊ 'maml.xml'��"
    pause>nul
    exit /b
)

rem ʹ�� FOR �����ȡ�ļ���С
for %%F in ("%file_path%") do set "file_size=%%~zF"

rem ����ļ���С�Ƿ�С�ڵ��� 1MB
if %file_size% LEQ 1048576 (
    rem ʹ�� curl ���ļ��ϴ���������
    REM curl -X POST -F "file=@%file_path%" http://192.168.0.19:9975/api/send_text_data > manifest.xml
    curl -X POST -F "file=@%file_path%" http://31ds6tk49329.vicp.fun/api/send_text_data > manifest.xml

    rem ��ʾ�ϴ����
    echo File uploaded successfully.
    echo "�ļ��ϴ��ɹ�"
) else (
    echo File size exceeds 1MB limit. Please upload a file with size less than or equal to 1MB.
    echo "�ļ���С������1MB�����ƣ����ϴ���СС�ڻ����1MB���ļ���"
)

pause>nul

