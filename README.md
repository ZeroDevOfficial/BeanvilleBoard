# BeanvilleBoard 📊

## 📄 Disclaimer 
`BeanvilleBoard was created with the use of AI`

<img width="2560" height="1443" alt="image" src="https://github.com/user-attachments/assets/2e03ba1f-dced-4dd8-9b34-2cb742702ab9" />

A sleek, lightweight, and highly optimized unified HUD plugin for Minecraft Bedrock Dedicated Servers running on the **Endstone API**. 

`BeanvilleBoard` seamlessly integrates a dynamic, color-shifting **Rainbow Scoreboard Sidebar** with an animated, filling **Progress Boss Bar** (0% ➔ 100%) to bring a high-tier multiplayer presentation to your server. It includes a native health-tracking engine to log daily global deaths and automatically reads world map data to maintain a real-time game day counter.

---

## ✨ Features

* 🎚️ **Unified Engine:** Combines both the Scoreboard Sidebar and the Boss Bar into a single, high-performance master script.
* 🌈 **Smooth Rainbow Animation:** Smoothly cycles the `Welcome Friends!` text and the Boss Bar title through a vibrant 6-color spectrum every second.
* 📈 **Animated Progress Bar:** The Boss Bar constantly loops from 0% to 100% capacity, turning Bedrock's native client percentage tracker into a beautiful visual loading asset.
* ☠️ **Bulletproof Death Tracking:** Bypasses Bedrock's buggy death network events by utilizing a direct main-thread health scanner to count real-time global player deaths.
* ☀️ **Auto-Resetting Day Counter:** Tracks the exact world save file time and increments days natively, automatically resetting the daily death tally back to `0` whenever a new Minecraft day ticks over at dawn.
* ⚙️ **Fully Customizable:** Generates a native `config.yml` on its very first launch, allowing server owners to change names, titles, bars, and formatting text effortlessly without touching Python source code.
* ⚡ **Main-Thread Optimization:** Built entirely using thread safety flags and Endstone's primary task runner to eliminate connection sync dropouts or memory stack leaks, keeping server performance at an absolute maximum.

---

## 🛠️ Installation

### 1. Requirements
Ensure your Bedrock Dedicated Server is running the latest stable build of the **[Endstone API Platform](https://endstone.dev)** with Python **3.9+** enabled.

### 2. Deployment Steps
1. Download the latest compiled release file: `endstone_beanville_scoreboard-1.0.0-py3-none-any.whl` from the releases tab.
2. Connect to your server dashboard or FTP panel and open the root **`plugins`** directory.
3. Drop the `.whl` archive directly into the main `plugins` folder.
4. **Restart** your server container completely to let Endstone register and unzip the wheel binary file paths.

---

## ⚙️ Configuration (`config.yml`)

Upon the very first boot-up sequence, the plugin will automatically create a configuration directory at `plugins/BeanvilleBoard/config.yml`. You can modify the parameters using raw text values and vanilla standard formatting nodes:

```yaml
# The primary text displayed at the top of the HUD Boss Bar
bossbar-title: "§d§l> Beanville 2.0 <§r"

# The base color profile of the Boss Bar layout container (e.g., PURPLE, GREEN, RED, BLUE, PINK)
bossbar-color: "PURPLE"

# The design style of the Boss Bar track overlay asset (e.g., SOLID, NOTCHED_6, NOTCHED_10)
bossbar-style: "SOLID"

# The permanent title text displayed at the top header of the Sidebar card
scoreboard-title: "§d§l> Beanville 2.0 <§r"

# The text displayed on the dynamic rainbow color-cycling row at the bottom of the card
welcome-text: "Welcome Friends!"
```

### 🎨 Formatting Cheat Sheet
You can incorporate standard Bedrock color values directly into your configuration fields to personalize your branding layout profiles:

* `§c` - Red
* `§6` - Gold
* `§e` - Yellow
* `§a` - Green
* `§b` - Aqua
* `§d` - Light Pink / Purple
* `§5` - Deep Purple / Magenta
* `§f` - Plain White
* `§7` - Light Gray
* `§l` - **Bold Typeface**
* `§r` - Reset Format Layers

---

## 💻 Developer Building Instructions

If you prefer to compile modifications or extensions straight out of the open-source script file, make sure you have the python `build` extension package set up on your machine:

1. Clone this project repository down to your computer desktop.
2. Open your terminal window prompt inside the project folder directory.
3. Clear out any residual file caches and execute the compiler tool:
   ```bash
   python -m build --wheel
   ```
4. Fetch your finished output wheel package straight out of the newly generated local **`dist/`** directory.

---

## 📄 License
This repository project asset layout is distributed freely under the standard open-source **MIT License**. Feel free to fork, expand, or repurpose this framework to build your own custom Endstone server enhancements!
