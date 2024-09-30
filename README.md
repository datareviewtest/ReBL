# Introduction
Welcome to the GitHub repository for the paper "**Feedback-Driven Automated Whole Bug Report Reproduction for Android Apps**" which will be published in **ISSTA 2024**. 

In this paper, we introduce **ReBL**, a novel feedback-driven approach that leverages GPT-4.0, a large-scale language model, to automatically reproduce Android bug reports. 

If you have any questions, please do not hesitate to email me at **dbenw96@gmail.com**.  

### Running the Tool
1. `.env`: Provide your API key here
2. Ensure the app is installed and open on your emulator, or you can add a few lines of code to automate the installation and launch process. This is entirely up to your preference.
3. Run the following command in your terminal: python3 reproduction.py [emulator-id] [path_to_bug_report]
- e.g. python3 reproduction.py 5554 ./BRs/k9_3255.txt (assumed that your emulator ID is 'emulator-5554').

### Demo 
[![Watch the video](https://img.youtube.com/vi/Wr8EiwpcFTU/maxresdefault.jpg)](https://www.youtube.com/watch?v=Wr8EiwpcFTU)


### Comparison with Baselines (73 Crash Bug Reports) && Non-Crash Bug Reports

| Bug Report        | ReCDroid | RepRobot | AdbGPT | ReBL |
|------------------|------|------|------|------|
| ActivityDiary#285|  ❌   | ❌ | ✅     | ✅   |
| Acv#12           |  ✅      | ✅      | ✅     | ✅   |
| Aegis#500        |  ❌      | ❌      | ❌     | ✅   |
| Aimsicd#816*    |  ❌      | ✅      | ✅     | ✅   |
| AndOPT#135       | ❌      | ✅      | ❌     | ✅   |
| AndOPT#500       |  ❌      | ❌      | ❌     | ✅   |
| AndOPT#569       |  ❌      | ✅      | ✅      | ✅   |
| AnglersLog#9     |  ❌      | ✅      | ❌      | ✅   |
| Anki#4586        |  ✅      | ✅      | ✅     | ✅   |
| Anki#5638        |  ❌      | ❌      | ✅     | ✅   |
| Anki#6432*    |  ❌      | ❌      | ❌     | ❌   |
| AntennaPod#3245  |  ✅      | ✅      | ✅     | ✅   |
| Anymemo#18        |  ✅      | ✅      | ✅     | ✅   |
| Anymemo#422      |  ✅      | ✅      | ✅     | ✅   |
| Anymemo#440       |  ✅      | ✅      | ✅     | ✅   |
| APhotoMgr#116     |  ✅      | ✅      | ❌    | ✅   |
| AsciiCam#17       | ❌      | ❌      |  ✅      | ✅   |
| Birthdroid#13     | ✅      | ✅      | ✅     | ✅   |
| Calendula#134     |  ❌      | ❌      | ✅     | ✅   |
| CarReport#43      | ❌      | ❌      | ✅     | ✅   |
| Commons#2123      |  ✅      | ✅      | ❌     | ✅   |
| Dagger#46         |  ✅      | ✅      | ✅     | ✅   |
| FamilyFinance#1   | ❌      | ✅      | ✅     | ✅   |
| FastAdapter#394   |  ✅      | ✅      | ✅     | ✅   |
| FastAdapter#113   | ❌      | ❌      | ❌     | ✅   |
| Fastfitness#142   |❌    | ❌      | ✅      | ✅     |
| Fdroid#1821*  |  ❌      | ❌      | ✅     | ✅   |
| Field#Book#145    | ❌      | ✅      | ❌     | ✅   |
| Field#Book#146    |  ❌      | ❌      | ✅     | ✅   |
| FirefoxLite#5085  |  ❌      | ✅      | ✅     | ✅   |
| FlashCards#13     |  ✅      | ✅      | ✅     | ✅   |
| K9#3255           |  ✅      | ✅      | ✅     | ✅   |
| Kiwix#990        |  ❌      | ✅      | ✅     | ✅   |
| LibreNews#22      |  ✅      | ✅      | ✅     | ✅   |
| LibreNews#23      |  ❌      | ✅      | ✅     | ✅   |
| LibreNews#27      |  ✅      | ✅      | ❌     | ✅   |
| Lrk#44            |  ❌      | ❌      | ❌     | ✅   |
| Markor#1698     |  ❌      | ✅      | ✅     | ✅   |
| Markor#194      | ✅      | ✅      | ✅     | ✅   |
| Materialistic#1067| ❌      | ❌      | ✅     | ✅   |
| Memento#169*     |  ❌      | ❌      | ❌     | ❌   |
| MicroMath#39      |  ❌      | ✅      | ✅     | ✅   |
| NewsBlur#1053     |  ✅      | ✅      | ✅     | ✅   |
| NoadPlayer#1      | ❌      | ✅      | ✅     | ✅   |
| Notepad#23        | ✅      | ✅      | ✅     | ✅   |
| Obdreader#22      |✅      | ✅      | ✅     | ✅   |
| ODK#360*        |  ❌      | ❌      | ❌     | ❌   |
| ODK#1402         | ✅      | ✅      | ✅     | ✅   |
| ODK#1796          |  ❌      | ❌      | ❌      | ✅   |
| ODK#2075          | ✅      | ✅      | ✅     | ✅   |
| ODK#2086          |  ✅      | ✅      | ✅     | ✅   |
| ODK#2191          | ✅      | ✅      | ✅     | ✅   |
| ODK#2525          |✅      | ✅      | ✅     | ✅   |
| ODK#3222          | ❌      | ❌      | ✅     | ✅   |
| Olam#1            | ✅      | ✅      | ✅     | ✅   |
| Olam#2            | ✅      | ❌      | ✅     | ✅   |
| Sudoku#173       |  ✅      | ✅      | ✅     | ✅   |
| Osmeditor#637*   |  ❌      | ❌      | ❌     | ❌   |
| PdfViewer#33     |  ❌      | ❌      | ✅      | ✅   |
| Qksms#482        |  ✅      | ✅      | ✅     | ✅   |
| Qksms#585       |  ❌      | ✅      | ✅     | ✅   |
| Screencam#25     |  ✅      | ✅      | ✅     | ✅   |
| Screencam#32     |  ❌      | ✅      | ✅      | ✅   |
| Soen#36          |  ❌      | ❌      | ❌     | ✅   |
| Timetracker#10   |  ❌      | ✅      | ✅     | ✅   |
| Timetracker#138  |  ❌      | ❌      | ❌     | ✅   |
| Timetracker#35   |  ✅      | ✅      | ✅     | ✅  |
| Trainer#7        |  ✅      | ✅      | ❌     | ✅  |
| Transistor#149   |  ❌      | ❌      | ❌    | ✅  |
| Transistor#63    |  ✅      | ✅      | ✅     | ✅  |
| Trickytripper#42 |  ❌      | ❌      | ✅     | ✅  |
| Ultrasonic#187   |  ❌      | ✅      | ✅     | ✅  |
| Weather#61     |  ✅      | ✅      | ✅     | ✅  |
| Success Rate     | 45.21% (33/73)|65.75% (48/73)|73.97%(54/73)|94.52%(69/73)|
|    |
|    |
|    |
|(NC)Aegis#287	 |N/A|N/A|N/A|62.729012|
|(NC)Aegis#415	|N/A|N/A|N/A|58.34102|
|(NC)Aegis#473	|N/A|N/A|N/A|37.56322|
|(NC)andOPT#580	|N/A|N/A|N/A|50.91968|
|(NC)andOPT#638	|N/A|N/A|N/A|83.38809|
|(NC)AndOTP#567	|N/A|N/A|N/A|87.34621|
|(NC)AndrOBD#144	|N/A|N/A|N/A|92.02506|
|(NC)AnglesLog#151	|N/A|N/A|N/A|157.18860|
|(NC)AnglesLog#347*	|N/A|N/A|N/A|❌|
|(NC)AnglesLog#43	|N/A|N/A|N/A|104.9995|
|(NC)Anki#5753|N/A|N/A|N/A|	98.153|
|(NC)FieldBook#137	*|N/A|N/A|N/A|❌|
|(NC)Gpstest#404	|N/A|N/A|N/A|141.94964|
|(NC)Images2PDF#154	|N/A|N/A|N/A|96.92932|
|(NC)K9#3971	|N/A|N/A|N/A|45.34212|
|(NC)KISS#1481*|N/A|N/A|N/A|	❌|
|(NC)LrkFM#34	*|N/A|N/A|N/A|❌|
|(NC)Markor#1020|N/A|N/A|N/A|	64.29208|
|(NC)Markor#331	|N/A|N/A|N/A|78.28462|
|(NC)Memento#7|N/A|N/A|N/A|	84.43842|
|(NC)Qksms#1124	|N/A|N/A|N/A|108.3488|
|(NC)Qksms#1155*	|N/A|N/A|N/A|❌|
|(NC)WiFiAnalyzer#222|N/A|N/A|N/A|	36.47242|
##### * =  summarization applied



