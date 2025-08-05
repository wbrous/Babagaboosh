# Babagaboosh

## Project Description

Originially created by [DougDoug](https://github.com/DougDougGithub), Babagaboosh is an app that allows a person to interact with an AI Chatbot with a custom system prompt. This allows the AI to fit into whatever personality that such person would like.

## System Requirements

> [!IMPORTANT]
> The Speech-to-Text (STT) library that is in use in this project may need some fine tuning for lower end systems (i.e. read their documentation)

## Setup

### 1. Setup Python (with a [venv](https://docs.python.org/3/library/venv.html))

To begin verify your python version by typing the following command:
```zsh
python --version
```

Make sure you have Python 3.10 or higher installed. If not, download it from [python.org](https://www.python.org/downloads/).

### 2. Create a Virtual Environment
```zsh
python -m venv .venv
```

### 3. Activate the Virtual Environment
- On Windows:
```zsh
.venv\Scripts\activate
```
- On macOS/Linux:
```zsh
source .venv/bin/activate
```

### 4. Install Dependencies
```zsh
pip install -r requirements.txt
```

### 5. Configure Your Environment
Copy the `.env.example` file to `.env` and fill in the required environment variables:
```zsh
cp .env.example .env
```

The next section will help you set up the required environment variables.

## Environment Variables

| Variable                      | Description                                           | Example Value               |
|-------------------------------|-------------------------------------------------------|-----------------------------|
| `GEMINI_API_KEY`             | Your API key for the Gemini AI service               | `your_api_key_here`         |
| `OBS_WEBSOCKET_URL`          | OBS WebSocket server URL                              | `127.0.0.1`                 |
| `OBS_WEBSOCKET_PORT`         | OBS WebSocket server port                             | `4455`                      |
| `USE_OBS_WEBSOCKET_PASSWORD` | Use password for OBS WebSocket (1 or 0)              | `1`                         |
| `OBS_WEBSOCKET_PASSWORD`     | Password for OBS WebSocket connection                 | `your_obs_password_here`    |
| `AMAZON_POLLY_ACCESS_KEY_ID` | Your AWS access key ID for Amazon Polly              | `your_access_key_id_here`   |
| `AMAZON_POLLY_SECRET_ACCESS_KEY` | Your AWS secret access key for Amazon Polly      | `your_secret_access_key_here` |

Edit your `.env` file with the appropriate values for your setup.

### Gemini API Key
To obtain a Gemini API key, you need to sign up for the Gemini API service. Go to Google's [AI Studio](https://aistudio.google.com/apikey) and follow the instructions to create a new project and generate an API key.

### Amazon Polly Configuration
To use Amazon Polly for text-to-speech, you need to set up an [AWS account](https://signin.aws.amazon.com/signup?request_type=register) and create an IAM user with permissions for Amazon Polly. Obtain your access key ID and secret access key from the AWS Management Console and fill in the corresponding environment variables in your `.env` file.

### OBS WebSocket Configuration (optional)
1. If you have OBS Studio v28 or above installed, you need to enable the WebSocket server:
   - Go to `Tools` > `WebSocket Server Settings`.
   - Enable the WebSocket server and set the port (default is 4455).
   - If you want to use a password, set it here as well.
2. If you are using a version of OBS below v28, you will need to install the [OBS WebSocket plugin](https://github.com/Palakis/obs-websocket).

## Configuration

The configuration for the application is stored in the `config.yaml` file. You can customize various settings such as the AI model, language, and other parameters.

### OBS Configuration (optional)
To configure OBS integration:
1. Update scene and filter information in the `config.yaml` file to match your OBS setup.
2. To setup Audio Move, install the [OBS Move plugin](https://obsproject.com/forum/resources/move.913/download).

### RealtimeSTT Configuration (optional)
To update the model used by RealtimeSTT, you can edit the `config.yaml` file (the stt section). You can choose between `small`, `base`, `medium`, `large-v1`, or `large-v2` models. The `base` model is recommended for most users, while the `large` and `large-v2` models provide better accuracy but require more system resources.

### Amazon Polly Configuration (optional)
To use Amazon Polly for text-to-speech, you can configure the `config.yaml` file to specify the voice and language you want to use. The available voices depend on the region you select in your AWS account. You can find the list of available voices in the [Amazon Polly documentation](https://docs.aws.amazon.com/polly/latest/dg/voicelist.html).

## Troubleshooting

<details>
<summary>Having Trouble?</summary>
  
<br/>

> Google Gemini Help: https://ai.google.dev/gemini-api/docs
> 
> RealtimeSTT Help: https://github.com/KoljaB/RealtimeSTT/blob/master/README.md
> 
> Amazon Polly Help: https://docs.aws.amazon.com/polly/

</details>