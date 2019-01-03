# SwitchBot HUB

## Overview

This software controll [SwitchBotHub](https://www.switch-bot.com/) with Raspberry Pi Zero W.
The SwitchBot Hub connect to Google Cloud IoT Core for accept event message and send device status.
Thus, this software connect between switch bot and cloud application.


## Install

Checkout this repository and run below command.

```python
pip install -e .
```


## Usage

### 1. setup Google Cloud IoT Core

Google Cloud IoT Core setup and register this software as device.
please record the below information.

| information  | description|
|:-------------|:-----------|
|project id    | your GCP project id|
|Region name   | region name of your project|
|registry name | Google Cloud IoT Core registry name|
|device id     | The device id.|
|private key   | private key of device |

You can define to conf file.

```editorconfig
project_id = YOUR_PROJECT_ID
cloud_region = us-central1 # Your cloud region.
registry_id = YOUR_REGISTRY_ID
device_id = YOUR_DEVICE_ID
```

Othrehand you can using enviroment value for define.


### 2. Run your application

```python
python main.py 
```

* Please see the command help.

```python

python main.py -h

``` 

˚

## Version

* 2018/Dec/31 0.1.0
    * Connect to Google Cloud IoT Core.
    
    
## Author

* Name: masato-ka
* E-mail: jp6uzv at gmail.com
* Twitter: @masato_ka


## LICENSE

This software under the MIT license.

&copy; 2018 masato-ka All Rights Reserved.
