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
mklink /D %streamerdir%\StreamerScan %CD%\StreamerScan
mklink /D %streamerdir%\StreamerScanFromField %CD%\StreamerScanFromField
mklink /D %streamerdir%\StreamerReduce %CD%\StreamerReduce
mklink /D %streamerdir%\StreamerTwitter %CD%\StreamerTwitter
mklink /D %streamerdir%\StreamerEventHubsIn %CD%\StreamerEventHubsIn
mklink /D %streamerdir%\StreamerEventHubsOut %CD%\StreamerEventHubsOut
mklink /D %streamerdir%\StreamerBuffer %CD%\StreamerBuffer
mklink /D %streamerdir%\StreamerRabbitMqIn %CD%\StreamerRabbitMqIn
mklink /D %streamerdir%\StreamerRabbitMqOut %CD%\StreamerRabbitMqOut
mklink /D %streamerdir%\StreamerEmitFile %CD%\StreamerEmitFile
