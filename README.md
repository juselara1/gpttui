# GPTTUI
---

<a href="https://pypi.python.org/pypi/gpttui"><img src="https://img.shields.io/pypi/v/gpttui.svg"/></a>

TUI to interact with gpt models.

![example](./docs/img/example.gif)

`gpttui` provides a terminal frontend that allows sessions (conversations) with LLMs, stores all the information in a centralized database, and provides vi-like keybindings.

> **Note**: At the moment it only supports **OpenAI** models, but other LLMs can be easily integrated. Same with the databases, currently supporting `sqlite`.

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

Likewise, you can get help of the different frontend options with the following command:

```sh
gpttui front --help
```

For example, to launch the TUI:

```sh
gpttui front\
    --database_kind SQLITE \
    --session first_chat \
    --model_kind OPENAI \
    --model_name "gpt-3.5-turbo" \
    --context 'You are an expert software developer'
```

### OpenAI

To use OpenAI models you need to specify the following environment variables:

```sh
export OPENAI_ORG=""
export OPENAI_API_KEY=""
```

### Keybindings

`gpttui` has two modes:

- `NORMAL`: in this mode you can do global operations. By default, `NORMAL` mode has the following bindings:
    - `c`: clear messages.
    - `d`: delete prompt.
    - `q`: quit.
    - `y`: yank/copy the last message from the assistant.
    - `p`: paste some text from the clipboard into the prompt.
    - `i`: switch to insert mode.

- `INSERT`: in this mode you can prompt text. By default, `INSERT` mode has the following bindings:
    - `esc`: switch to normal mode.
    - `enter`: send text to the assistant.

### Customization

- If you want custom keybindings, you can modify the `$HOME/.config/gpttui/keybindings.json` file.
- If you want to change the app style, you can modify the `$HOME/.config/gpttui/style.css` file.
