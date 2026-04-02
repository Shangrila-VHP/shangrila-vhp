# How to Run a Python Script in Blender

A quick guide for running `.py` scripts (like the house scene) directly inside Blender.

---

## Prerequisites

- Blender installed (any recent version: 3.x or 4.x works)
- The `.py` script file saved somewhere on your computer

---

## Step-by-Step Instructions

### 1. Open Blender

Launch Blender normally. You'll start on the default splash screen — just click anywhere to dismiss it.

---

### 2. Switch to the Scripting Workspace

At the **top of the screen**, you'll see a row of workspace tabs:

```
Layout | Modeling | Sculpting | UV Editing | Texture Paint | Shading | Animation | Rendering | Compositing | Scripting
```

Click **Scripting**. The layout will change to show a built-in text/code editor on the left and the 3D viewport on the right.

---

### 3. Load the Script

In the **text editor panel** (left side):

1. Click the **Open** button in the header bar of the text editor
2. A file browser will appear — navigate to this folder:
   ```
   design-CAD-scripting-ML/blender/
   ```
3. Select the script you want to run, e.g.:
   ```
   house-with-garage-04-01-2026.py
   ```
4. Click **Open Text Block**

The script will appear in the text editor, ready to run.

---

### 4. Run the Script

Click the **▶ Run Script** button in the text editor header bar.

> **Keyboard shortcut:** `Alt + P` (while your cursor is inside the text editor)

You'll see a progress message in the terminal/info bar at the bottom. When done, the console at the bottom of Blender will print:

```
✅  Scene built successfully!
```

---

### 5. View the Scene

Switch to the **3D Viewport** (right panel, or click the **Layout** workspace tab up top).

You can:
- **Orbit** around the scene: hold `Middle Mouse Button` and drag
- **Zoom**: scroll the `Mouse Wheel`
- **Pan**: hold `Shift + Middle Mouse Button` and drag
- Press **Numpad 0** to look through the camera

---

### 6. Render the Image

Press **F12** to render, or go to **Render > Render Image** from the top menu.

The rendered image will be:
- Displayed in a pop-up render window
- **Automatically saved** to:
  ```
  design-CAD-scripting-ML/blender/renders/house-with-garage-04-01-2026.png
  ```

> **Note:** Rendering uses the **Cycles** engine with 128 samples. This may take a minute or two depending on your hardware. GPU rendering (if available) will be much faster — enable it under **Edit > Preferences > System > Cycles Render Devices**.

---

## Scripts in This Folder

| File | Description |
|------|-------------|
| `house-with-garage-04-01-2026.py` | House with garage, front lawn, trees, lighting & camera |
| `blender-bouncy-ball.py` | Bouncy ball animation |
| `Blender_Windmill_Starts.py` | Windmill scene starter |
| `05-27-2024-Blender-Tent-Started.py` | Tent model |
| `05-27-2024-Blender-Tent-Windmill_Starts-COMBINED.py` | Tent + windmill combined |

---

## Tips

- **Script errors?** Check the **Info** bar at the very bottom of Blender — it shows the last error in red.
- **Scene already has objects?** The house script clears the scene on run (`bpy.ops.object.delete()`), so it's safe to re-run.
- **Want to tweak the design?** Edit values directly in the script (dimensions, colors, positions) and re-run — the scene rebuilds instantly.
