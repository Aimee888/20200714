# 蓝牙模块
使用VS2017 C++编写  
参考链接：  
https://blog.csdn.net/MaxWoods/article/details/44679679?locationNum=8  
http://blog.sina.com.cn/s/blog_648d306d0102vjq5.html
## 检测蓝牙适配器的数量
函数：check_bluetooth_presence()  
返回值：蓝牙适配器的数量  
举例：  
OS：Windows10 64bit  
无线网卡（带蓝牙）：一个  
* -- 手动打开蓝牙时，读到适配器数为1  
* -- 手动关闭蓝牙时，读到适配器数为0  
~~~
int check_bluetooth_presence() {
	int i = 0;
	HANDLE hRadio = NULL;
	BLUETOOTH_RADIO_INFO LocalRadioInfo = { sizeof(LocalRadioInfo) };
	BLUETOOTH_FIND_RADIO_PARAMS btfrp = { sizeof(btfrp) };
	HBLUETOOTH_RADIO_FIND hFind = BluetoothFindFirstRadio(&btfrp, &hRadio);
	if (hFind != NULL) {
		i++;
		int break_value = 0;
		while (break_value == 0) {
			bool continue_status = BluetoothFindNextRadio(hFind, &hRadio);
			//printf("%d\n", continue_status);  //false--0, true--1
			if (continue_status) {
				i++;
			}
			else {
				break_value = 1;
			}
		}
		BluetoothFindRadioClose(hFind);
	}

	return i;
}
~~~
注意点：一台电脑接多个蓝牙适配器（即多张网卡），还没试过

## 扫描附近蓝牙设备
导入头文件  
~~~
#include <stdio.h>
#include <bluetoothapis.h>
#include <iostream>
using namespace std;

#pragma comment(lib, "Bthprops.lib")
~~~
扫描设备函数
~~~
int scan_bluetooth_device() {
	int i = 0;
	wcout.imbue(locale(""));
	HBLUETOOTH_RADIO_FIND hbf = NULL;
	HANDLE hbr = NULL;
	HBLUETOOTH_DEVICE_FIND hbdf = NULL;
	BLUETOOTH_FIND_RADIO_PARAMS btfrp = {sizeof(BLUETOOTH_FIND_RADIO_PARAMS)};
	BLUETOOTH_RADIO_INFO bri = {sizeof(BLUETOOTH_RADIO_INFO)};
	BLUETOOTH_DEVICE_SEARCH_PARAMS btsp = {sizeof(BLUETOOTH_DEVICE_SEARCH_PARAMS)};
	BLUETOOTH_DEVICE_INFO btdi = {sizeof(BLUETOOTH_DEVICE_INFO)};
	hbf = BluetoothFindFirstRadio(&btfrp, &hbr);
	bool brfind = hbf != NULL;
	while (brfind) {
		if (BluetoothGetRadioInfo(hbr, &bri) == ERROR_SUCCESS) {
			cout << "Class of device:0x" << uppercase << hex << bri.ulClassofDevice << endl;
			wcout << "Name:" << bri.szName << endl;
			cout << "Manufacture:0x" << uppercase << hex << bri.manufacturer << endl;
			cout << "Subversion:0x" << uppercase << hex << bri.lmpSubversion << endl;
			btsp.hRadio = hbr;
			btsp.fReturnAuthenticated = TRUE;
			btsp.fReturnConnected = FALSE;
			btsp.fReturnRemembered = TRUE;
			btsp.fReturnUnknown = TRUE;
			btsp.cTimeoutMultiplier = 30;
			hbdf = BluetoothFindFirstDevice(&btsp, &btdi);
			bool bfind = hbdf != NULL;
			while (bfind)
			{
				i++;
				wcout << "[Name]:" << btdi.szName;
				cout << ",[Address]:0x" << uppercase << hex << btdi.Address.ullLong << endl;
				bfind = BluetoothFindNextDevice(hbdf, &btdi);
			}
			BluetoothFindDeviceClose(hbdf);
		}
		CloseHandle(hbr);
		brfind = BluetoothFindNextRadio(hbf, &hbr);
	}
	BluetoothFindRadioClose(hbf);
	
	return i;
}
~~~
## 通过Bluetooth API调用对话框选择蓝牙设备并显示设备信息
~~~
// 通过Bluetooth API调用对话框选择蓝牙设备并显示设备信息
void select_bluetooth_device() {
	wcout.imbue(locale(""));
	BLUETOOTH_SELECT_DEVICE_PARAMS pbtsdp = { sizeof(BLUETOOTH_SELECT_DEVICE_PARAMS) };
	pbtsdp.fShowAuthenticated = TRUE;
	pbtsdp.fShowRemembered = TRUE;
	pbtsdp.fShowUnknown = TRUE;
	if (BluetoothSelectDevices(&pbtsdp)) {
		BLUETOOTH_DEVICE_INFO *pbtdi = pbtsdp.pDevices;
		BLUETOOTH_ADDRESS_STRUCT addr;
		for (ULONG cDevices = 0; cDevices < pbtsdp.cNumDevices; cDevices++) {
			wcout << "Name: " << pbtdi->szName << endl;
			cout << endl;
			cout << "[Class]:0x" << uppercase << hex << pbtdi->ulClassofDevice;
			addr = pbtdi->Address;
			cout << ",[Adrress]:0x" << uppercase << hex << addr.ullLong << endl;
		}
		BluetoothSelectDevicesFree(&pbtsdp);
	}
}
~~~