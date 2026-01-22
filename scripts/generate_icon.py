#!/usr/bin/env python3
"""Generate the FavApp Starter icon."""

from PIL import Image, ImageDraw
import os


def create_icon(size=256):
    """Create a bookmark-style icon with gradient and plus sign."""
    # Create image with transparency
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Define colors for gradient (blue to teal)
    color_top = (0, 122, 255)      # Blue
    color_bottom = (0, 230, 180)   # Teal/Cyan

    # Bookmark dimensions
    margin = int(size * 0.1)
    bookmark_width = size - 2 * margin
    bookmark_height = size - margin
    notch_height = int(size * 0.15)

    # Create gradient background for bookmark shape
    for y in range(margin, size):
        # Calculate gradient color
        progress = (y - margin) / (size - margin)
        r = int(color_top[0] + (color_bottom[0] - color_top[0]) * progress)
        g = int(color_top[1] + (color_bottom[1] - color_top[1]) * progress)
        b = int(color_top[2] + (color_bottom[2] - color_top[2]) * progress)

        # Draw horizontal line for this y position
        for x in range(margin, size - margin):
            # Check if this pixel is within the bookmark shape
            if y < size - notch_height:
                # Regular rectangle part
                img.putpixel((x, y), (r, g, b, 255))
            else:
                # Notch part (V-shape at bottom)
                center_x = size // 2
                notch_y = size - notch_height
                dist_from_center = abs(x - center_x)
                notch_progress = (y - notch_y) / notch_height
                max_dist = (bookmark_width // 2) * (1 - notch_progress)

                if dist_from_center <= max_dist:
                    img.putpixel((x, y), (r, g, b, 255))

    # Draw circle with plus sign
    circle_radius = int(size * 0.22)
    circle_center = (size // 2, int(size * 0.38))
    circle_thickness = int(size * 0.03)

    # Draw white circle outline
    for angle in range(360):
        import math
        for r_offset in range(-circle_thickness, circle_thickness + 1):
            rad = math.radians(angle)
            x = int(circle_center[0] + (circle_radius + r_offset) * math.cos(rad))
            y = int(circle_center[1] + (circle_radius + r_offset) * math.sin(rad))
            if 0 <= x < size and 0 <= y < size:
                img.putpixel((x, y), (255, 255, 255, 255))

    # Fill circle interior with white
    for y in range(circle_center[1] - circle_radius, circle_center[1] + circle_radius + 1):
        for x in range(circle_center[0] - circle_radius, circle_center[0] + circle_radius + 1):
            dist = ((x - circle_center[0]) ** 2 + (y - circle_center[1]) ** 2) ** 0.5
            if dist <= circle_radius - circle_thickness and 0 <= x < size and 0 <= y < size:
                img.putpixel((x, y), (255, 255, 255, 255))

    # Draw plus sign in center of circle (using gradient color at that position)
    plus_size = int(circle_radius * 0.6)
    plus_thickness = int(size * 0.06)

    # Calculate color at circle center
    progress = (circle_center[1] - margin) / (size - margin)
    plus_r = int(color_top[0] + (color_bottom[0] - color_top[0]) * progress)
    plus_g = int(color_top[1] + (color_bottom[1] - color_top[1]) * progress)
    plus_b = int(color_top[2] + (color_bottom[2] - color_top[2]) * progress)
    plus_color = (plus_r, plus_g, plus_b, 255)

    # Horizontal bar of plus
    for y in range(circle_center[1] - plus_thickness // 2, circle_center[1] + plus_thickness // 2 + 1):
        for x in range(circle_center[0] - plus_size, circle_center[0] + plus_size + 1):
            if 0 <= x < size and 0 <= y < size:
                img.putpixel((x, y), plus_color)

    # Vertical bar of plus
    for x in range(circle_center[0] - plus_thickness // 2, circle_center[0] + plus_thickness // 2 + 1):
        for y in range(circle_center[1] - plus_size, circle_center[1] + plus_size + 1):
            if 0 <= x < size and 0 <= y < size:
                img.putpixel((x, y), plus_color)

    return img


def main():
    """Generate icons in multiple sizes and save as ICO."""
    # Create assets directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    assets_dir = os.path.join(project_dir, "assets")
    os.makedirs(assets_dir, exist_ok=True)

    # Generate icons at different sizes
    sizes = [16, 32, 48, 64, 128, 256]
    icons = []

    for size in sizes:
        print(f"Generating {size}x{size} icon...")
        icon = create_icon(size)
        icons.append(icon)

    # Save as ICO with multiple sizes
    ico_path = os.path.join(assets_dir, "icon.ico")
    icons[0].save(
        ico_path,
        format='ICO',
        sizes=[(s, s) for s in sizes],
        append_images=icons[1:]
    )
    print(f"Saved: {ico_path}")

    # Also save as PNG for other uses
    png_path = os.path.join(assets_dir, "icon.png")
    icons[-1].save(png_path, format='PNG')
    print(f"Saved: {png_path}")

    # Copy to project root as well
    root_ico_path = os.path.join(project_dir, "icon.ico")
    icons[0].save(
        root_ico_path,
        format='ICO',
        sizes=[(s, s) for s in sizes],
        append_images=icons[1:]
    )
    print(f"Saved: {root_ico_path}")


if __name__ == "__main__":
    main()
