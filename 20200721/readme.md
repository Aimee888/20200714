# 蓝牙模块
使用python编写  
参考链接：  
https://mlog.club/article/2968364  
https://superuser.com/tags/powershell/info  
https://jingyan.baidu.com/article/36d6ed1f6e18b61bcf4883de.html
## BT_test.py
整合了BT_on.py，BT_off.py，checkdriver.py，bluetooth_test.py  
功能：
* 打开蓝牙 -- bt_on()
* 关闭蓝牙 -- bt_off()
* 检查蓝牙driver -- bt_check_driver()
* 扫描附近蓝牙 -- bt_scan_nearby_device() 
* 检测特定蓝牙是否存在 -- check_certain_device_by_name(device_name) 

将这些功能集中在一个py文件中，变成一个测试蓝牙的工具。
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
remotesigned：  
可以运行脚本，但要求从网络上下载的脚本和配置文件由可信发布者签名；  
不要求对已经运行和已在本地计算机编写的脚本进行数字签名。  
Restricted:  
禁止运行任何脚本和配置文件。  
AllSigned:  
可以运行脚本，但要求所有脚本和配置文件由可信发布者签名，包括在本地计算机上编写的脚本。  
Unrestricted:  
可以运行未签名脚本。（危险！）
~~~
Powershell.exe -executionpolicy remotesigned -command .\Bluetooth.ps1  -BluetoothStatus On
# Powershell.exe -executionpolicy Restricted -command .\Bluetooth.ps1  -BluetoothStatus On
# Powershell.exe -executionpolicy AllSigned -command .\Bluetooth.ps1  -BluetoothStatus On
# Powershell.exe -executionpolicy Unrestricted -command .\Bluetooth.ps1  -BluetoothStatus On
~~~
### 关闭蓝牙 -- BT_off.py
以管理员程序运行py文件
~~~
cmd_off = "Powershell.exe -executionpolicy remotesigned -command .\Bluetooth.ps1  -BluetoothStatus Off"
# cmd_off = "Powershell.exe -executionpolicy Restricted -command .\Bluetooth.ps1  -BluetoothStatus Off"
# cmd_off = "Powershell.exe -executionpolicy AllSigned -command .\Bluetooth.ps1  -BluetoothStatus Off"
# cmd_off = "Powershell.exe -executionpolicy Unrestricted -command .\Bluetooth.ps1  -BluetoothStatus Off"
~~~
### 检查蓝牙driver -- checkdriver.py
使用wmi检查蓝牙driver
### 扫描附近蓝牙 -- bluetooth_test.py
~~~
from bluetooth import *
found_devs = discover_devices(lookup_names=True)
~~~
特别注意取py名字时不要直接取bluetooth.py，否则会报错哦。