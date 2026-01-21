---
name: transparent-background
description: Extract true alpha transparency from images using the two-pass technique with image editing. Use this skill when creating transparent PNGs for icons, logos, sprites, or any image assets that need genuine alpha channels. Triggers on requests for: (1) transparent background images, (2) PNG icons/logos with transparency, (3) sprite sheets, (4) overlay graphics, or (5) any image where "remove background" or "transparent" is mentioned.
---

# Transparent Background Extraction

This skill enables creation of images with true alpha transparency using the **two-pass extraction technique**. AI image generators cannot produce genuine transparency, so this technique generates two versions and mathematically derives the alpha channel.

> [!NOTE]
> **Requirements:** This skill requires an AI image generation tool with **edit/inpainting capability** (ability to modify existing images). Compatible tools include Antigravity and similar services that support the `ImagePaths` parameter for image editing.

## The Two-Pass Workflow

### Step 1: Generate Image on White Background

Generate the first version with a pure white background:

```
[Original prompt], on a solid pure white background (#FFFFFF), no gradients, no shadows on background, centered composition
```

**Example:**

```
A modern minimalist microphone icon, purple-blue gradient, flat design, on a solid pure white background (#FFFFFF), no gradients on background, no shadows, centered
```

### Step 2: Edit to Black Background (Using ImagePaths)

Use the `generate_image` tool with the **`ImagePaths`** parameter to edit the first image, changing only the background:

```
ImagePaths: ["/path/to/first_image.png"]
Prompt: "Change the background to solid pure black (#000000), keep the subject exactly the same, no other changes"
```

> [!IMPORTANT]
> Using `ImagePaths` ensures the second image maintains the same subject, pose, and styling as the first. Only the background color changes.

### Step 3: Run the Extraction Script

After generating both images, run the extraction script:

```bash
python3 .agent/skills/transparent-background/scripts/extract_transparency.py \
  <image_on_white> \
  <image_on_black> \
  <output.png>
```

**Example:**

```bash
python3 .agent/skills/transparent-background/scripts/extract_transparency.py \
  logo_white.png \
  logo_black.png \
  logo_transparent.png
```

### Step 4: Deliver the Result

Provide the user with the final PNG that contains true alpha transparency.

---

## How It Works

The algorithm exploits how transparency affects colors over different backgrounds:

| Pixel Type        | On White     | On Black     | Distance     | Alpha |
| ----------------- | ------------ | ------------ | ------------ | ----- |
| Fully opaque      | Same color   | Same color   | 0            | 1.0   |
| Fully transparent | White (#FFF) | Black (#000) | Max (~442)   | 0.0   |
| Semi-transparent  | Lighter      | Darker       | Proportional | 0-1   |

**Formula:** `alpha = 1 - (pixel_distance / max_background_distance)`

---

## Prompt Engineering Tips

For best results when generating the source images:

### Good Prompts

```
A cute cartoon fox mascot, simple flat design, on a solid pure white background, no shadows, centered composition
```

```
Modern minimalist app icon of a camera, flat design, solid pure white background, no gradients or shadows
```

### Avoid

- Complex backgrounds (forests, gradients)
- Soft drop shadows touching background edges
- Environmental elements that blend with background

---

## Fallback: AI Background Removal

If the two-pass technique produces artifacts (e.g., ImagePaths doesn't preserve the subject well), use the rembg fallback:

```bash
python3 .agent/skills/transparent-background/scripts/remove_background.py \
  <input_image> \
  <output.png>
```

This uses AI (U2-Net model) to detect and remove backgrounds from a single image.

---

## Troubleshooting

| Issue          | Cause                   | Solution                                               |
| -------------- | ----------------------- | ------------------------------------------------------ |
| Ghosting/halos | Images not well-aligned | Re-edit with clearer instruction or use rembg fallback |
| Dark artifacts | Shadows on background   | Re-generate with "no shadows" in prompt                |
| Wrong colors   | Low alpha areas         | Increase `--threshold` parameter                       |
| Script fails   | Missing Pillow          | Run `pip install Pillow`                               |

---

## Requirements

```bash
# For two-pass extraction
pip install Pillow

# For fallback AI removal
pip install rembg Pillow
```
