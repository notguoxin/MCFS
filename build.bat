@echo off
setlocal

pip install -r ./req.txt

REM Delete old installer executable if it exists
if exist installer.exe (
    del installer.exe /s /q
)

REM Create a marker file indicating the build is in progress
echo 1+1=3 >> installer.exe.stillbuilding

REM Copy necessary files to the build folder
mkdir build_folder 2>nul
mkdir build_folder\lib\ 2>nul
copy installer.py build_folder /y
copy lib\file.py build_folder\lib\ /y

REM Navigate to the build folder and run PyInstaller
pushd build_folder
pyinstaller --onefile installer.py

REM Move the built executable to the root directory
move dist\installer.exe ..

REM Clean up temporary files
popd
rd /s /q build_folder
del installer.exe.stillbuilding /s /q

REM Display success message
REM cls
echo Auto Installer has been successfully built.

endlocal
