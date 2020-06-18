# antitheft
Anti-theft measures for Android which persist after factory reset  

Features
---
* Network access to device via  
Telnet  
SSH  
FTP/SFTP  
ADB  
HTTP (File Server)

* Covert screen captures every 30s in low res which is stored locally and uploaded (if network available) to specified Google Drive folder.

* Pulls a script from a specified URL and runs it on boot completion (at the moment, this is **dumpsys location** to obtain approximate location). Script can be modified at will for example to brick phone once booted or remove password once booted.

Method
---

Entry point is **debuggerd** (debugger daemon for Android present in **/system/bin**).  

The original **debuggerd** is renamed to **debuggerd_real**.  

Modified **debuggerd** becomes a shell script that executes all anti-theft measures before running **/system/bin/debuggerd_real** daemon as last command and Android boot completes as normal.
