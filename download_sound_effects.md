# Download Free Baseball Sound Effects

To add immersive sound effects to your broadcasts, download these free, royalty-free sounds:

## 📁 Create Sound Effects Directory

```bash
mkdir sound_effects
cd sound_effects
```

## 🎵 Required Sound Files

Download and save these files in the `sound_effects/` directory:

### 1. **catch.mp3** - Glove Catching Ball
Used for: Strikes, balls, foul balls

**Download from:**
- https://pixabay.com/sound-effects/search/baseball%20catch/
- https://freesound.org/search/?q=baseball+glove+catch
- Search for: "baseball glove catch" or "baseball mitt"

**What to look for:** Clean glove pop/smack sound

---

### 2. **hit.mp3** - Bat Hitting Ball
Used for: Balls put in play (ground balls, fly balls, line drives)

**Download from:**
- https://pixabay.com/sound-effects/search/baseball%20hit/
- https://freesound.org/search/?q=baseball+bat+hit
- https://www.zapsplat.com/sound-effect-category/baseball/

**What to look for:** Solid "crack" of bat on ball

---

### 3. **swing_miss.mp3** - Bat Swinging Through Air
Used for: Swinging strikes

**Download from:**
- https://pixabay.com/sound-effects/search/baseball%20swing/
- https://freesound.org/search/?q=baseball+swing+whoosh

**What to look for:** Whoosh/swoosh sound

---

### 4. **crowd_cheer.mp3** - Crowd Celebrating
Used for: Home runs, big hits

**Download from:**
- https://pixabay.com/sound-effects/search/crowd%20cheer/
- https://freesound.org/search/?q=crowd+cheer+baseball
- https://uppbeat.io/sfx/tag/baseball

**What to look for:** Stadium crowd cheering, 2-5 seconds

---

### 5. **crowd_groan.mp3** - Crowd Disappointed (Optional)
Used for: Strikeouts (when home team batting)

**Download from:**
- https://pixabay.com/sound-effects/search/crowd%20groan/
- https://freesound.org/search/?q=crowd+disappointed

**What to look for:** Crowd "awww" or groan, 1-2 seconds

---

## ✅ Quick Download Links

**Best Source (Easiest):**
👉 **Pixabay** (no attribution required, instant download)
- https://pixabay.com/sound-effects/search/baseball/

**Steps:**
1. Click link above
2. Search for each sound type
3. Click download button (MP3 format)
4. Rename to match required filenames above
5. Move to `sound_effects/` directory

---

## 🎯 Expected Directory Structure

```
Baseball broadcast/
├── sound_effects/
│   ├── catch.mp3           # Glove catch sound
│   ├── hit.mp3             # Bat hit sound
│   ├── swing_miss.mp3      # Swing whoosh
│   ├── crowd_cheer.mp3     # Crowd cheering
│   └── crowd_groan.mp3     # Crowd groan (optional)
├── baseball_broadcast_ai.py
├── audio_mixer.py
└── ...
```

---

## 🧪 Test Sound Effects

After downloading, test if they loaded correctly:

```bash
python3 audio_mixer.py
```

You should see:
```
✅ Loaded: catch
✅ Loaded: hit
✅ Loaded: swing_miss
✅ Loaded: crowd_cheer
✅ Loaded: crowd_groan
```

---

## 📝 License Information

All recommended sources provide **royalty-free** sounds that can be used in personal projects:

- **Pixabay:** CC0 license (no attribution required)
- **Freesound:** Various Creative Commons licenses (check individual sounds)
- **Zapsplat:** Free for personal/commercial use with account

Always verify the specific license for each sound you download!

---

## 🚀 Once Downloaded

The audio mixer will automatically:
1. Load all sound effects at startup
2. Add 0.8 second pause after narration (pitcher windup)
3. Play appropriate sound based on pitch result
4. Add 0.3 second pause after sound
5. Continue with next narration

**Result:** Immersive broadcast that lets you imagine the action! ⚾🎙️
