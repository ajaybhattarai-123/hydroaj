@echo off
set "PATH=C:\Users\ajayb\.cargo\bin;C:\Users\ajayb\AppData\Local\Microsoft\WinGet\Packages\BrechtSanders.WinLibs.POSIX.MSVCRT_Microsoft.Winget.Source_8wekyb3d8bbwe\winlibs-x86_64-posix-seh-gcc-16.2.0-mingw-w64msvcrt-14.0.0-r3\mingw64\bin;C:\Users\ajayb\AppData\Local\Microsoft\WinGet\Packages\MartinStorsjo.LLVM-MinGW.MSVCRT_Microsoft.Winget.Source_8wekyb3d8bbwe\llvm-mingw-20261006-msvcrt-x86_64\bin;%PATH%"
cd /d E:\python\Water_Resource_Library\hydrocivil
maturin build --release
python -c "import glob, os, subprocess, sys; wheels = glob.glob(r'target\wheels\*.whl'); latest = max(wheels, key=os.path.getmtime); print('Installing', latest); subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--force-reinstall', '--no-deps', latest])"

