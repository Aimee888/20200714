#wifi_test.py
定义了一个wifi功能类，里面包含以下功能  
* 开启wifi
* 关闭wifi
* 检查wifi driver
* 扫描附近wifi
* 检查特定wifi的信号强度

##开启wifi
~~~
netsh interface set interface "Wi-Fi 3" enabled
~~~

##关闭wifi
~~~
netsh interface set interface "Wi-Fi 3" disabled
~~~

##打印wifi接口
~~~
netsh interface show interface
~~~

## 查询特定interface的状态
~~~
netsh interface show interface "Wi-Fi 3"
~~~

##wifitest.ini
~~~
[WIFI]
wlanname = Wi-Fi 3
wifiname = yhkvfbv
drivername = Realtek RTL8821CE 802.11ac PCIe Adapter
max = 0
min = -65
~~~
wlanname就是wifi的接口名字  
wifiname就是附近随便一个wifi的名称  
drivername就是网卡的名称  
max是信号强度的最大值  
min是信号强度的最小值