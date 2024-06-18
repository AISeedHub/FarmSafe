# FarmSafe

This repo is for a Smartfarm Alert System

## 📨 The email streams run independently:
1. 📅 Send regularly (daily or weekly) report to customers
2. 🛎️ Send alert email to admin when the sensor data exceeds the threshold (later)
3. 🚨 Send alert email to admin when device is offline: Camera is down or sensor device is not sending data

## Installation

### 1. Install the dependencies

```
pip install -r requirement.txt
```

### 2. Run the application as a background process

```
nohup ./run.sh > email.log >2&1
```

## Development

### Prerequisites

- Establishes the SSH Tunnel to the MongoDB server

```
ssh -L 37017:localhost:27017 andrew@IP -p 2222
```

- Prepare the email configuration file `config.yml` 
