# 蓝牙模块
使用python编写  
参考链接：  
https://mlog.club/article/2968364  
https://superuser.com/tags/powershell/info
### 打开蓝牙 -- BT_on.py
以管理员程序运行py文件
Bluetooth.ps1
~~~
[CmdletBinding()] Param (
    [Parameter(Mandatory=$true)][ValidateSet('Off', 'On')][string]$BluetoothStatus
)
If ((Get-Service bthserv).Status -eq 'Stopped') { Start-Service bthserv }
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$asTaskGeneric = ([System.WindowsRuntimeSystemExtensions].GetMethods() | ? { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' })[0]
Function Await($WinRtTask, $ResultType) {
    $asTask = $asTaskGeneric.MakeGenericMethod($ResultType)
    $netTask = $asTask.Invoke($null, @($WinRtTask))
    $netTask.Wait(-1) | Out-Null
    $netTask.Result
}
[Windows.Devices.Radios.Radio,Windows.System.Devices,ContentType=WindowsRuntime] | Out-Null
[Windows.Devices.Radios.RadioAccessStatus,Windows.System.Devices,ContentType=WindowsRuntime] | Out-Null
Await ([Windows.Devices.Radios.Radio]::RequestAccessAsync()) ([Windows.Devices.Radios.RadioAccessStatus]) | Out-Null
$radios = Await ([Windows.Devices.Radios.Radio]::GetRadiosAsync()) ([System.Collections.Generic.IReadOnlyList[Windows.Devices.Radios.Radio]])
$bluetooth = $radios | ? { $_.Kind -eq 'Bluetooth' }
[Windows.Devices.Radios.RadioState,Windows.System.Devices,ContentType=WindowsRuntime] | Out-Null
Await ($bluetooth.SetStateAsync($BluetoothStatus)) ([Windows.Devices.Radios.RadioAccessStatus]) | Out-Null


~~~
~~~
powershell.exe -command .\Bluetooth.ps1 -BluetoothStatus On
~~~
### 关闭蓝牙 -- BT_off.py
以管理员程序运行py文件
~~~
powershell.exe -command .\Bluetooth.ps1 -BluetoothStatus Off
~~~
### 检查蓝牙driver -- checkdriver.py
使用wmi检查蓝牙driver
### 扫描附近蓝牙 -- bluetooth_test.py
~~~
from bluetooth import *
found_devs = discover_devices(lookup_names=True)
~~~
特别注意取py名字时不要直接取bluetooth.py，否则会报错哦。