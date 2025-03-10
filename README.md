# Phone Operator

Phone Operator is an MCP (Mobile Control Protocol) server that enables AI systems or custom clients to automate tasks on Android devices using Tasker. Running on your phone via Termux, it exposes a powerful set of tools that allow you to control phone functions—like sending SMS, taking screenshots, or printing a document—through natural language when paired with an AI assistant.

## What Does This Project Do?

Phone Operator bridges the gap between AI capabilities and Android automation. It transforms your phone into a server that can be controlled via natural language, leveraging Tasker’s extensive automation features. Whether you want to automate daily routines, integrate phone actions with AI models, or build custom clients, Phone Operator provides an extensible, open-source solution.

### Key Features
- **Task Automation**: Perform a wide range of phone actions (e.g., get battery level, play music, set alarms) via predefined tools.
- **AI Integration**: Pair with AI models (e.g., Gemini) to operate your phone using natural language commands.
- **Extensibility**: Add your own custom tools to tailor the system to your needs.
- **Local Execution**: Runs entirely on your device for privacy and performance.

## Setup Instructions

Follow these steps to set up Phone Operator on your Android device:

### 1. Install Termux
- Download [Termux](https://termux.com/) from the Google Play Store or F-Droid and install it on your Android device.

### 2. Set Up Termux Environment
- Open Termux and run the provided setup script to install necessary packages:
  ```bash
  ./setup-termux.sh
  ```
- This script updates Termux, installs Python, Rust, and the Termux API, and sets up the `mcp` library. If you prefer manual installation, run:
  ```bash
  pkg update
  pkg upgrade
  pkg install python rust termux-api
  pip install mcp
  ```

### 3. Install Server Dependencies
- Copy `server/server.py` and `server/requirements.txt` to your Termux environment (e.g., via a file explorer or SSH).
- Install the server dependencies:
  ```bash
  cd server
  pip install -r requirements.txt
  ```

### 4. Configure Tasker
- **Install Tasker**: Download [Tasker](https://tasker.joaoapps.com/) from the Google Play Store.
- **Import Project**: Import the `mcp.prj.xml` file (not included in this repo; create it based on server tools) into Tasker and enable it.
- **Enable Screen Grabbing**: For screenshot functionality, grant Tasker the necessary permission:
  ```bash
  adb shell appops set net.dinglisch.android.taskerm PROJECT_MEDIA allow
  ```
- **Optional Music Playback**: Install the [AutoInput](https://joaoapps.com/autoinput/) plugin for Tasker if you plan to use music-related tools.

### 5. Run the Server
- Start the MCP server:
  ```bash
  python server.py
  ```
- The server will run on `http://0.0.0.0:8000/sse` by default.

## Server Tools

The server (`server/server.py`) defines a variety of tools that map to Tasker tasks. Below is a comprehensive list of available tools, their descriptions, and input parameters:

| Tool Name                  | Description                                      | Input Parameters                                      |
|----------------------------|--------------------------------------------------|-------------------------------------------------------|
| `tasker_get_battery_level` | Returns the current battery percentage.          | None                                                  |
| `tasker_lamp_on`           | Turns the bedroom lamp on.                       | None                                                  |
| `tasker_lamp_off`          | Turns the bedroom lamp off.                      | None                                                  |
| `tasker_toggle_torch`      | Turns flashlight on or off.                      | `state`: `"on"` or `"off"` (required)                 |
| `tasker_flash_text`        | Displays a short message on screen.              | `text`: Message to display (required)                 |
| `tasker_tasker_say`        | Speaks the given text aloud.                     | `speech`: Text to speak (required), `lang`: Language (e.g., `en-usa`) (optional) |
| `tasker_send_sms`          | Sends an SMS message.                            | `number`: Phone number (required), `message`: Text (required) |
| `tasker_call_number`       | Initiates a phone call.                          | `number`: Phone number (required)                     |
| `tasker_toggle_wifi`       | Turns WiFi on or off.                            | `state`: `"on"` or `"off"` (required)                 |
| `tasker_get_location`      | Retrieves current GPS coordinates.               | None                                                  |
| `tasker_get_contacts`      | Retrieves phone contacts.                        | None                                                  |
| `tasker_list_files`        | Lists files in the Documents folder.             | None                                                  |
| `tasker_screenshot`        | Takes a screenshot of the current screen.        | None                                                  |
| `tasker_browse_url`        | Opens a URL in the default browser.              | None
| `tasker_get_volume`        | Retrieves current media volume level.            | None                                                  |
| `tasker_set_volume`        | Sets media volume level (0-15).                  | `level`: Volume (e.g., `"15"`, `"max"`, `"min"`) (required) |
| `tasker_get_clipboard`     | Retrieves current clipboard text.                | None                                                  |
| `tasker_set_clipboard`     | Sets clipboard text.                             | `text`: Text to set (required) |
| `tasker_play_music`        | Plays music on YouTube Music.                    | `query`: Search term for music (required)             |
| `tasker_take_photo`        | Takes a photo with the camera.                   | None                                                  |
| `tasker_print`             | Prints a document.                               | `path`: Path to document (required)                   |
| `tasker_set_alarm`         | Sets an alarm.                                   | `time`: Time in 24:00 format (required) |
| `tasker_create_google_task`| Creates a Google Tasks entry.                    | `text`: Task content (required)                       |

### Notes
- Each tool corresponds to a Tasker task (e.g., `MCP Get Battery Level`). Ensure these tasks are defined in your Tasker project (`mcp.prj.xml`).
- Some tools require specific permissions or plugins (e.g., AutoInput for `tasker_play_music`).

## Usage Examples

### Running the Client
- Use the provided `client/client.py` to connect to the server:
  ```bash
  addr="<localhost o your phones ip address if connecting through LAN>"
  python client.py --endpoint http://$addr --port 8000
  ```
- Chat with it and enter your instructions.
  ```
  > "Send a text to 1234567890 saying Hello"
  [Tool call: tasker_send_sms {"number": "1234567890", "message": "Hello"}]
  ```

### Example Commands
- **Get Battery Level**:
  ```
  tasker_get_battery_level
  ```
- **Toggle Flashlight On**:
  ```
  tasker_toggle_torch {"state": "on"}
  ```
- **Send an SMS**:
  ```
  tasker_send_sms {"number": "1234567890", "message": "Hello!"}
  ```

### Using with other Chat Interfaces
- Any chat interface that understands the MCP protocol with tool support can be used as well.
- Check some of the existing ones [here](https://modelcontextprotocol.io/clients).

## Dependencies

### Server
- Python 3.10
- See `server/requirements.txt` for full list, including:
  - `mcp==1.3.0`
  - `pydantic==2.10.6`
  - `uvicorn==0.34.0`
  - `starlette==0.46.0`

### Client
- Python 3.10
- `asyncio`, `litellm`, `prompt_toolkit` (installed via `client.py` dependencies)

## Troubleshooting

- **Server Fails to Start**: Verify all dependencies are installed and Termux has storage/network permissions.
- **Tasker Tasks Not Running**: Ensure the Tasker project is imported, enabled, and tasks match the `tasker_name` in `server.py`.
- **Permission Issues**: Use ADB to grant permissions if screen grabbing or other features fail.

## Contributing

Want to add new tools or improve Phone Operator?
1. Fork the repository.
2. Create a branch for your feature.
3. Update `server.py` with new tools and corresponding Tasker tasks.
4. Submit a pull request with documentation.


> [!NOTE]
>
> This project was quickly put together during a [hackathon](https://x.com/pulsemcp/status/1897745362388922836).
> For a more polished and actively developed version, please check out [https://github.com/dceluis/tasker-mcp](https://github.com/dceluis/tasker-mcp).

## License

This project is licensed under the [MIT License](LICENSE).
