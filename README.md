# HammyCam - Web-Based Camera System

A Python-based camera system with auto-starting web viewer. View your camera feed in any web browser - **no installation required!**

## 🚀 Quick Start

The camera **auto-starts** when you open the container and is viewable in your browser!

### Open in Browser

```
http://localhost:8080/
```

That's it! The camera displays in your browser automatically. 🎥

---

## ⚙️ Configuration

Edit `camera_config.yaml` to customize settings:

```yaml
camera:
  width: 1280           # Resolution width
  height: 720           # Resolution height
  fps: 30               # Frame rate
  mode: "test_pattern"  # or "image"
  image_path: "images/black.jpg"  # if mode is "image"

display:
  web_port: 8080        # Web server port

autostart:
  enabled: true         # Auto-start on boot
  delay: 2              # Delay before starting (seconds)
```

After editing, restart:
```bash
scripts/stop_camera.sh
python3 scripts/start_camera.py
```

Or rebuild the container.

---

## 📱 Access from Any Device

### From Your Computer
```
http://localhost:8080/
```

### From Phone/Tablet (same network)
```
http://<container-ip>:8080/
```

Find container IP:
```bash
hostname -I
```

---

## 🎮 Manual Control

```bash
# Stop camera
scripts/stop_camera.sh

# Start camera
python3 scripts/start_camera.py

# Check if running
ps aux | grep simple_web_camera

# View logs
cat /tmp/hammycam_web.log
```

---

## 📁 Project Structure

```
HammyCam/
├── camera_config.yaml         # ⚙️  Configuration
├── requirements.txt           # 📦 Python dependencies
├── scripts/                   # 🔧 Core scripts
│   ├── start_camera.py        #    🚀 Auto-start script
│   ├── stop_camera.sh         #    🛑 Stop script
│   └── simple_web_camera.sh   #    📹 Camera script
├── web/                       # 🌐 Web interface
│   ├── simple_web_viewer.html #    Web viewer
│   └── current_frame.jpg      #    Live frame (generated)
├── examples/                  # 📖 Example scripts
│   ├── example_motion_detector.py
│   └── process_image.py
├── images/                    # 📁 Sample images
└── README.md                  # 📄 This file
```

---

## 🎯 Features

- ✅ **Auto-start** - Camera starts when container boots
- ✅ **Web-based** - View in any browser (desktop, mobile, tablet)
- ✅ **No installation** - Just open the URL
- ✅ **Configurable** - Edit YAML file to customize
- ✅ **Network accessible** - View from any device
- ✅ **Test pattern or custom image** - Your choice

---

## 📖 Usage Examples

### Default Setup (Test Pattern)
```bash
# Just rebuild container - camera starts automatically!
# Open: http://localhost:8080/
```

### Custom Image
```yaml
# In camera_config.yaml
camera:
  mode: "image"
  image_path: "images/myimage.jpg"
```

### Different Resolution
```yaml
camera:
  width: 1920
  height: 1080
  fps: 15
```

### Different Port
```yaml
display:
  web_port: 9090
```
Then access at: `http://localhost:9090/`

---

## 🔧 Dev Container Setup

This project uses a Dev Container for consistent development.

### Prerequisites
- Docker Desktop
- Visual Studio Code with Dev Containers extension

### Getting Started
1. Open this folder in VS Code
2. Click "Reopen in Container" when prompted
3. Wait for container to build
4. Camera starts automatically!
5. Open `http://localhost:8080/` in your browser

---

## 🎨 Web Viewer Features

- **Live camera feed** with auto-refresh
- **FPS selector** - Choose 10, 15, or 30 FPS
- **Refresh button** - Force immediate update
- **FPS counter** - See actual frame rate
- **Responsive design** - Works on any screen size
- **Beautiful UI** - Modern, gradient design

---

## 🐛 Troubleshooting

### Camera not starting?
```bash
# Check logs
cat /tmp/hammycam_web.log

# Restart manually
scripts/stop_camera.sh
python3 scripts/start_camera.py
```

### Can't access from browser?
1. Make sure you're using the correct URL: `http://localhost:8080/`
2. Check if port 8080 is in use: `lsof -i :8080`
3. Try a different port in `camera_config.yaml`

### Can't access from phone?
1. Ensure phone is on same WiFi network
2. Find container IP: `hostname -I`
3. Check firewall allows port 8080

### Image not updating?
```bash
# Check if FFmpeg is running
ps aux | grep ffmpeg

# Check frame file
ls -lh web/current_frame.jpg

# Restart camera
scripts/stop_camera.sh && python3 scripts/start_camera.py
```

---

## 📚 Documentation

- **camera_config.yaml** - Configuration file with comments
- **QUICKSTART.md** - Quick reference guide
- **examples/example_motion_detector.py** - Motion detection code example
- **examples/process_image.py** - Image processing utilities

---

## 💡 Tips

1. **Lower FPS for slower connections**: Set `fps: 15` in config
2. **Bookmark the URL** for instant access
3. **Add to home screen** on mobile for app-like experience
4. **Multiple viewers** - Open in multiple browsers simultaneously
5. **Background operation** - Container runs independently

---

## ✨ Summary

**HammyCam is a simple, web-based camera system:**

1. ✅ Auto-starts on container boot
2. ✅ View in any web browser
3. ✅ Works on desktop, mobile, tablet
4. ✅ Configure via simple YAML file
5. ✅ No installation or setup needed

**Just open `http://localhost:8080/` and enjoy!** 🎥

---

## License

MIT
