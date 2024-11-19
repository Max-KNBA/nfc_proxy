# NFC Reader Proxy Application

Due to the lack of support for the ACR122U NFC reader by the webUSB API in browsers like Chrome, Edge, and Safari, this application adopts a strategy of sending NFC card UID via WebSocket. This application is a WebSocket server that monitors NFC card events using a smart card reader. It detects card insertions and removals and sends the card information to connected WebSocket clients.

## Features

- Monitors NFC card insertions and removals.
- Sends card UID and ATR information to WebSocket clients.
- Closes WebSocket connection after sending card information.

## Hardware Support

This application supports the [ACR122U USB NFC Reader](https://www.acs.com.hk/en/products/3/acr122u-usb-nfc-reader/). Ensure that the reader is properly connected to your system before running the application.

## Requirements

- Python 3.7+
- `websockets` library
- `pyscard` library
- `py122u` library

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Max-KNBA/nfc_proxy.git
   cd nfc_proxy
   ```

2. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

3. Activate the virtual environment:

   On Windows:
   ```bash
   .venv\Scripts\activate
   ```

   On macOS and Linux:
   ```bash
   source .venv/bin/activate
   ```

4. Install the required Python packages:

   ```bash
   pip install websockets pyscard py122u
   ```

## Usage

1. Connect your ACR122U NFC reader to the system.

2. Run the server:

   ```bash
   python nfc_server.py
   ```

3. The server will start and listen for WebSocket connections on `ws://localhost:8865`.

4. Connect a WebSocket client to `ws://localhost:8865/nfc` to receive NFC card events.

## Web Client

The `templates/index.html` file provides a simple web interface to interact with the NFC server. It uses WebSockets to receive NFC card events and allows users to input a PIN after a card is detected.

### How to Use the Web Client

1. Open `templates/index.html` in a web browser.

2. When an NFC card is detected, the message "請輸入PIN" will be displayed, and a PIN input field will appear.

3. Enter the PIN and click "提交" to submit it. The application will log the submitted PIN and redirect to a logged-in interface if the PIN is correct.

## Code Overview

- **NFCObserver**: A class that observes NFC card events and handles card insertions and removals.
- **RFID_monitor**: An asynchronous function that manages WebSocket connections and card monitoring.
- **main**: The entry point of the application that starts the WebSocket server.

## Notes

- The server will close the WebSocket connection after sending the card information.
- The application currently supports only one WebSocket connection at a time.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
