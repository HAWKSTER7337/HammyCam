# HammyCam Quick Start Guide

## 🚀 Instant Access

Camera auto-starts when container boots!

**Just open:**
```
http://localhost:8080/
```

---

## ⚙️ Configuration

Edit `camera_config.yaml`:

```yaml
camera:
  width: 1280
  height: 720
  fps: 30
  mode: "test_pattern"  # or "image"

display:
  web_port: 8080
```

After editing:
```bash
scripts/stop_camera.sh && python3 scripts/start_camera.py
```

---

## 📱 Access URLs

| Device | URL |
|--------|-----|
| **Your computer** | `http://localhost:8080/` |
| **Phone/tablet** | `http://<container-ip>:8080/` |

Find container IP:
```bash
hostname -I
```

---

## 🎮 Commands

```bash
# Stop
scripts/stop_camera.sh

# Start
python3 scripts/start_camera.py

# Status
ps aux | grep simple_web_camera

# Logs
cat /tmp/hammycam_web.log
```

---

## 🎯 Common Configs

### High Resolution
```yaml
camera:
  width: 1920
  height: 1080
```

### Lower FPS (better for slow connections)
```yaml
camera:
  fps: 15
```

### Custom Image
```yaml
camera:
  mode: "image"
  image_path: "images/myimage.jpg"
```

### Different Port
```yaml
display:
  web_port: 9090
```

---

## 🔥 Pro Tips

1. Bookmark `http://localhost:8080/`
2. Add to mobile home screen for app-like experience
3. Works in multiple browsers simultaneously
4. Lower FPS = less bandwidth

---

## 🐛 Troubleshooting

**Camera not working?**
```bash
scripts/stop_camera.sh
python3 scripts/start_camera.py
```

**Can't connect?**
- Make sure you're using correct URL: `http://localhost:8080/`
- Check logs: `cat /tmp/hammycam_web.log`

**From phone?**
- Same WiFi network required
- Use container IP, not `localhost`

---

## ✨ That's It!

Open `http://localhost:8080/` and enjoy! 🎥
