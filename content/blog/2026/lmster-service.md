+++
author = "Toni Sagristà Sellés"
title = "LM Studio on systemd linger"
description = "How I set up an old laptop as a persistent inference machine using LM Studio, system-level services, and systemd lingering."
date = 2026-02-27
categories = ["AI"]
tags = ["LLM", "AI", "LM Studio", "RAG", "AI inference", "selfhosting", "systemd"]
featuredpath = "date"
type = "post"
+++ 

The release of **LM Studio 0.4.5** has introduced a much needed feature in this local LLM suite that has it much more attractive with respect to other similar projects. [LM Link](https://lmstudio.ai/docs/lmlink) allows you to connect multiple LM Studio instances across your network to share models and perform inference seamlessly.

<!--more-->

By sheer chance, I was just playing around with setting up an LM Studio server in an old laptop that I planned to use for inference. I would connect AnythingLLM clients to it to make API requests. The timing of 0.4.5 was perfect for me, as I could now use LM Studio for inference directly, and forget about using up my own Tailscale network. But some setup was needed in the laptop. To make this work effectively, the LM Studio server needs to run in the background, start automatically on boot, and persist even when I'm not logged in.

 The LM Studio website provides the source of a [service file](https://lmstudio.ai/docs/developer/core/headless_llmster#create-systemd-service). It suggests creating it as a system-wide service, which is weird, as the default installation method (at least on Linux) sets everything up in the user home directory. I modified it a bit to make things clean, as I want this to be a user `systemd` service. It keeps the process tied to your user environment but, with a little tweak called lingering, allows it to run without an active SSH or GUI session. Here is the setup.

By default, user services stop the moment the user logs out. To prevent this and allow the LM Studio daemon to start at boot and stay alive, run:

```bash
loginctl enable-linger $USERNAME
```

Then, create a directory for your user services if it doesn't exist:

```bash
mkdir -p ~/.config/systemd/user/
```

After that, create a file named `lms.service` in that directory (`~/.config/systemd/user/lms.service`), with the following contents:

```toml
[Unit]
Description=LM Studio Server
After=network.target

[Service]
Type=forking
# This line kills any existing lms processes to prevent the "left-over" error
ExecStartPre=-/home/$USERNAME/.lmstudio/bin/lms daemon down
ExecStartPre=/home/$USERNAME/.lmstudio/bin/lms daemon up
ExecStart=/home/$USERNAME/.lmstudio/bin/lms server start
# Give it a specific PID file if lms supports it, otherwise systemd guesses
ExecStop=/home/$USERNAME/.lmstudio/bin/lms server stop
ExecStopPost=/home/$USERNAME/.lmstudio/bin/lms daemon down

# Ensure systemd doesn't get confused by the CLI exiting
RemainAfterExit=yes

[Install]
WantedBy=default.target
```

Once the file is saved, tell systemd to reload its configuration and enable the service:

```bash
# Reload the user daemon
systemctl --user daemon-reload

# Enable the service to start on boot
systemctl --user enable lms.service

# Start the service now
systemctl --user start lms.service
```

If you want to load a specific model by default, add an additional `ExecStartPre` line, like this:

```toml
ExecStartPre=/home/YOUR_USERNAME/.lmstudio/bin/lms load openai/gpt-oss-20b --yes
```

You can check the service status with `systemctl --user lms.service`. And that is it. You can now use your old hardware for inference with small local LLMs from any of your other machines.
