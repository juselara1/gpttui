# GPTTUI
---

<a href="https://pypi.python.org/pypi/gpttui"><img src="https://img.shields.io/pypi/v/gpttui.svg"/></a>
<a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg"/></a>

TUI to interact with GPT models.

![example](./docs/img/example.gif)

`gpttui` provides a terminal frontend that allows sessions (conversations) with LLMs, stores all the information in a centralized database, and provides vi-like keybindings.

> **Note**: It currently supports **OpenAI**, **ChatSonic**, and **ColossalAI** (it seems like they terminated the server, so you'll need to use other deployed endpoint).

## Installation

You can install `gpttui` with `pip`:

```sh
pip install gpttui
```

## Basic Concepts

- `session`: a conversation (chat).
- `context`: specifies a topic or a specialization for the assistant.
- `user`: the person that uses `gpttui`.
- `assistant`: the AI assistant.

## Usage

You can get more information using the help page:

```sh
gpttui --help
```

You have the following options:

### OpenAI

First, you need to set up the configuration files:

```sh
gpttui init --model_kind OPENAI --model_config openai.json
```

This will generate the configuration files in the default configuration folder `$HOME/.config/gpttui`:

```sh
.config/gpttui
├── keybindings.json
├── openai.json
└── style.css
```

- `keybindings.json` specifies the keybindings to use in the app.
- `style.css` defines the app's theme.
- `openai.json` is the configuration file for OpenAI models.

For OpenAI, you need to generate an API key and extract the organization ID; you must replace these values in the `openai.json` file:

```javascript
{
  "timeout": 30,
  "max_retries": 3,
  "model_name": "gpt-3.5-turbo",
  "organization": "ORGANIZATION ID",
  "api_key": "API KEY"
}
```

You can also specify the maximum `timeout` for a response, the maximum number of retries `max_retries`, and which model to use `model_name`.

Use the following command to launch `gpttui` using the OpenAI configuration:

```sh
gpttui front \
    --model_kind OPENAI \
    --model_config openai.json \
    --database_kind SQLITE \
    --database_name db.sqlite \
    --context "You're an expert python developer." \
    --session python_dev
```

In this case, we create the `db.sqlite` database in `SQLite`, the session (conversation) `python_dev` is initialized for the given context.

> **Note**: You can recover the conversation by using the same session name. By default, the `SQLite` database is created in the default config folder.

### Colossal

First, you need to set up the configuration files:

```sh
gpttui init --model_kind COLOSSAL --model_config colossal.json
```

This will generate the configuration files in the default configuration folder `$HOME/.config/gpttui`:

```sh
.config/gpttui
├── keybindings.json
├── colossal.json
└── style.css
```

For Colossal, you can configure the following values in the `colossal.json` file:

```javascript
{
  "url": "https://service.colossalai.org/generate",
  "repetition_penalty": 1.2,
  "top_k": 40,
  "top_p": 0.5,
  "temperature": 0.7,
  "max_new_tokens": 512,
  "timeout": 30
}
```

Use the following command to launch `gpttui` using the OpenAI configuration:

```sh
gpttui front \
    --model_kind COLOSSAL \
    --model_config colossal.json \
    --database_kind SQLITE \
    --database_name db.sqlite \
    --session colossal_test
```

In this case, the `db.sqlite` database is created (or reused if already created) in `SQLite`, and the session (conversation) `colossal_test` is initialized for the given context.

> **Note**: You can recover the conversation by using the same session name. By default, the `SQLite` database is created in the default configuration folder.

### ChatSonic

First, you need to set up the configuration files:

```sh
gpttui init --model_kind CHATSONIC --model_config chatsonic.json
```

This will generate the configuration files in the default configuration folder `$HOME/.config/gpttui`:

```sh
.config/gpttui
├── keybindings.json
├── chatsonic.json
└── style.css
```

For ChatSonic, you can configure the following values in the `chatsonic.json` file:

```javascript
{
  "url": "https://api.writesonic.com/v2/business/content/chatsonic?engine=premium",
  "api_key": "",
  "enable_memory": true,
  "enable_google_results": true
}
```

You must insert your ChatSonic API KEY into the `api_key` value.

Use the following command to launch `gpttui` using the ChatSonic configuration:

```sh
gpttui front \
    --model_kind CHATSONIC \
    --model_config chatsonic.json \
    --database_kind SQLITE \
    --database_name db.sqlite
    --session chatsonic_test
``` 

In this case, the `db.sqlite` database is created (or reused if already created) in `sqlite`, and the session (conversation) `chatsonic_test` is initialized for the given context.

> **Note**: You can recover the conversation by using the same session name. By default, the `sqlite` database is created in the default configuration folder.

## Configuration

### Keybindings

`gpttui` has two modes:

- `NORMAL`: In this mode, you can perform global operations. By default, the `NORMAL` mode has the following keybindings:
    - `c`: Clear messages.
    - `d`: Delete prompt.
    - `q`: Quit.
    - `y`: Yank/copy the last message from the assistant.
    - `p`: Paste some text from the clipboard into the prompt.
    - `i`: Switch to insert mode.

- `INSERT`: In this mode, you can enter text in the prompt. By default, the `INSERT` mode has the following keybindings:
    - `esc`: Switch to normal mode.
    - `enter`: Send text to the assistant.

You can modify the keybindings in the `keybindings.json` file located at `.config/gpttui/`.

## Style

`gpttui` is stylized through [textual css](https://textual.textualize.io/guide/CSS/). You can modify the `style.css` file located at `.config/gpttui`.
