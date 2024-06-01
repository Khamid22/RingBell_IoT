# RingBell

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Eligible Users](#eligible-users)
- [Contributing](#contributing)

## Introduction

RingBell is a Telegram bot that interacts with an MQTT broker to control a bell. It allows authorized users to send commands to ring the bell, check its status, and play audio files through the MQTT protocol. This project demonstrates the integration of Telegram bot functionality with MQTT for IoT applications.

## Features

- **Ring the Bell**: Authorized users can send a command to ring the bell.
- **Check Status**: Users can check the current status of the bell.
- **Play Audio**: Users can play an audio file through the bell.
- **Send Audio/Voice Messages**: Users can send audio or voice messages that will be processed and sent to the MQTT broker.

## Installation

### Prerequisites

- Python 3.x
- Required Python packages (install via `requirements.txt`)

### Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/ringbell.git
    ```
2. Navigate to the project directory:
    ```bash
    cd ringbell
    ```
3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Create a `.env` file in the project root directory and add your configuration details:
    ```
    BOT_TOKEN=your-telegram-bot-token
    DB_HOST=your-database-host
    DB_USER=your-database-username
    DB_PASS=your-database-password
    DB_NAME=your-database-name
    ```
5. Start the bot:
    ```bash
    python start.py
    ```

## Usage

1. Start the bot:
    ```bash
    python start.py
    ```
2. Use the following commands in Telegram:
    - `/start`: Welcome message and initial instructions.
    - `/ring`: Ring the bell.
    - `/status`: Check the status of the bell.
    - `/play`: Play audio through the bell.

## Eligible Users

The list of eligible users can be modified to include new users. By default, the `AUTHORIZED_USERS` list is empty. To add new users, simply update the `AUTHORIZED_USERS` list in `start.py`.

Example:
```python
AUTHORIZED_USERS = [1081721793, 1114820537, 1270439555]
```

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.
