Pushd "%~dp0"
set streamerdir=C:\ProgramData\Alteryx\Tools
for /d %%G in ("C:\ProgramData\Alteryx\Tools\Streamer*") do rd /s /q "%%~G"
mklink /D %streamerdir%\StreamerInterval %CD%\StreamerInterval
mklink /D %streamerdir%\StreamerController %CD%\StreamerController
mklink /D %streamerdir%\StreamerOut %CD%\StreamerOut
mklink /D %streamerdir%\StreamerZip %CD%\StreamerZip
mklink /D %streamerdir%\StreamerCombineLatest %CD%\StreamerCombineLatest
mklink /D %streamerdir%\StreamerCode %CD%\StreamerCode
mklink /D %streamerdir%\StreamerRace %CD%\StreamerRace
mklink /D %streamerdir%\StreamerCalcTest %CD%\StreamerCalcTest
mklink /D %streamerdir%\StreamerSample %CD%\StreamerSample
mklink /D %streamerdir%\StreamerTimeInterval %CD%\StreamerTimeInterval
