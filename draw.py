import math
from PIL import Image, ImageDraw

def draw_entry():
    # Supersampling at 2048x2048 for high craft and clean antialiasing
    W, H = 2048, 2048
    im = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(im)

    # 1. Sky: soft radial / gradient warm peach-orange sky
    # Draw horizontal bands from warm peach (#FFE5D0) at top to golden hour orange (#FFB07C) at horizon
    sky_top = (255, 235, 210)
    sky_mid = (255, 195, 150)
    sky_bot = (255, 160, 110)
    
    steps = 1200
    for y in range(steps):
        t = y / float(steps)
        # quadratic transition
        r = int(sky_top[0] * (1 - t)**2 + sky_mid[0] * 2 * (1 - t) * t + sky_bot[0] * t**2)
        g = int(sky_top[1] * (1 - t)**2 + sky_mid[1] * 2 * (1 - t) * t + sky_bot[1] * t**2)
        b = int(sky_top[2] * (1 - t)**2 + sky_mid[2] * 2 * (1 - t) * t + sky_bot[2] * t**2)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # 2. Distant gentle rolling hills (warm amber/ochre)
    hill_color_back = (242, 175, 105)
    # create a smooth curve for the back hill
    back_points = [(0, 1300), (400, 1220), (1000, 1180), (1600, 1240), (W, 1300), (W, H), (0, H)]
    draw.polygon(back_points, fill=hill_color_back)

    # 3. Main grassy foreground hill (rich warm spring green / golden green)
    hill_color_front = (135, 190, 85)
    front_points = [(0, 1450), (300, 1380), (800, 1320), (1400, 1360), (W, 1420), (W, H), (0, H)]
    draw.polygon(front_points, fill=hill_color_front)

    # 4. Sun kite in the upper left (warm yellow-orange with rays and a happy face)
    kite_center = (600, 550)
    kite_radius = 220
    
    # Kite rays
    ray_color = (255, 220, 100)
    for i in range(12):
        angle = i * (2 * math.pi / 12)
        x1 = kite_center[0] + int((kite_radius + 20) * math.cos(angle))
        y1 = kite_center[1] + int((kite_radius + 20) * math.sin(angle))
        x2 = kite_center[0] + int((kite_radius + 90) * math.cos(angle))
        y2 = kite_center[1] + int((kite_radius + 90) * math.sin(angle))
        draw.line([(x1, y1), (x2, y2)], fill=ray_color, width=14)

    # Kite body (circle)
    kite_body_color = (255, 204, 51)
    draw.ellipse([
        (kite_center[0] - kite_radius, kite_center[1] - kite_radius),
        (kite_center[0] + kite_radius, kite_center[1] + kite_radius)
    ], fill=kite_body_color, outline=(230, 160, 20), width=8)

    # Kite face (simple joyful dot eyes and curved smile)
    eye_color = (120, 70, 20)
    draw.ellipse([
        (kite_center[0] - 70, kite_center[1] - 40),
        (kite_center[0] - 30, kite_center[1])
    ], fill=eye_color)
    draw.ellipse([
        (kite_center[0] + 30, kite_center[1] - 40),
        (kite_center[0] + 70, kite_center[1] + 0)
    ], fill=eye_color)
    
    # Smile arc
    draw.arc([
        (kite_center[0] - 80, kite_center[1] - 20),
        (kite_center[0] + 80, kite_center[1] + 90)
    ], start=15, end=165, fill=eye_color, width=12)

    # Kite bow tails (colorful playful bows hanging from the bottom of the kite)
    tail_start = (kite_center[0], kite_center[1] + kite_radius)
    tail_end = (kite_center[0] - 80, kite_center[1] + kite_radius + 350)
    # draw string
    draw.line([tail_start, tail_end], fill=(240, 190, 80), width=6)
    # bows
    for b_pos in [0.3, 0.6, 0.9]:
        bx = int(tail_start[0] + (tail_end[0] - tail_start[0]) * b_pos)
        by = int(tail_start[1] + (tail_end[1] - tail_start[1]) * b_pos)
        draw.ellipse([(bx-25, by-15), (bx+25, by+15)], fill=(255, 90, 90))

    # 5. Kite string curving from kite to child's hand
    child_hand = (1220, 1260)
    # Polyline for smooth curve
    curve_points = []
    num_pts = 40
    for i in range(num_pts + 1):
        t = i / float(num_pts)
        # Bezier-like interpolation with a sag
        x = (1 - t) * kite_center[0] + t * child_hand[0]
        y = (1 - t) * kite_center[1] + t * child_hand[1] + int(200 * math.sin(t * math.pi))
        curve_points.append((x, y))
    draw.line(curve_points, fill=(180, 130, 70), width=5)

    # 6. Small child in bright yellow raincoat and golden puppy in center-right
    # Child body / raincoat (yellow)
    coat_color = (255, 230, 50)
    # Legs (boots)
    boot_color = (90, 130, 190)
    draw.rectangle([1170, 1340, 1210, 1430], fill=boot_color) # left leg
    draw.rectangle([1230, 1340, 1270, 1430], fill=boot_color) # right leg

    # Raincoat body (trapezoid / rounded rect)
    draw.rounded_rectangle([1140, 1180, 1300, 1360], radius=40, fill=coat_color)

    # Child head & hat
    head_center = (1220, 1110)
    head_radius = 55
    skin_color = (255, 215, 185)
    draw.ellipse([
        (head_center[0] - head_radius, head_center[1] - head_radius),
        (head_center[0] + head_radius, head_center[1] + head_radius)
    ], fill=skin_color)

    # Raincoat hood
    draw.arc([
        (head_center[0] - head_radius - 10, head_center[1] - head_radius - 10),
        (head_center[0] + head_radius + 10, head_center[1] + head_radius + 10)
    ], start=180, end=360, fill=(230, 200, 30), width=18)

    # Happy face (dot eyes, rosy cheeks, smile)
    draw.ellipse([(head_center[0] - 22, head_center[1] - 8), (head_center[0] - 12, head_center[1] + 2)], fill=(80, 50, 30))
    draw.ellipse([(head_center[0] + 12, head_center[1] - 8), (head_center[0] + 22, head_center[1] + 2)], fill=(80, 50, 30))
    # Cheeks
    draw.ellipse([(head_center[0] - 32, head_center[1] + 4), (head_center[0] - 14, head_center[1] + 16)], fill=(255, 140, 140))
    draw.ellipse([(head_center[0] + 14, head_center[1] + 4), (head_center[0] + 32, head_center[1] + 16)], fill=(255, 140, 140))
    # Smile
    draw.arc([
        (head_center[0] - 18, head_center[1] - 2),
        (head_center[0] + 18, head_center[1] + 24)
    ], start=0, end=180, fill=(120, 60, 30), width=6)

    # Raised arm holding string
    draw.line([(1200, 1220), child_hand], fill=coat_color, width=22)
    draw.ellipse([(child_hand[0]-12, child_hand[1]-12), (child_hand[0]+12, child_hand[1]+12)], fill=skin_color)

    # Golden Puppy next to child
    puppy_body_color = (220, 150, 70)
    # Body
    draw.rounded_rectangle([1020, 1280, 1140, 1370], radius=35, fill=puppy_body_color)
    # Head
    draw.ellipse([1100, 1230, 1180, 1310], fill=puppy_body_color)
    # Floppy ear
    draw.ellipse([1105, 1225, 1145, 1285], fill=(190, 120, 50))
    # Tail wagging up
    draw.arc([1000, 1240, 1040, 1310], start=180, end=360, fill=puppy_body_color, width=14)
    # Puppy face dots & happy open tongue
    draw.ellipse([1150, 1255, 1160, 1265], fill=(50, 30, 10)) # eye
    # Happy tongue
    draw.ellipse([1165, 1280, 1185, 1300], fill=(255, 100, 100))

    # 7. Foreground details: Wildflowers and grass tufts
    flower_colors = [(255, 255, 255), (255, 120, 180), (255, 230, 100), (200, 150, 255)]
    stem_color = (90, 140, 50)
    
    import random
    rng = random.Random(42) # reproducible flowers
    for _ in range(35):
        fx = rng.randint(50, W - 50)
        fy = rng.randint(1460, H - 40)
        # stem
        draw.line([(fx, fy + 30), (fx, fy)], fill=stem_color, width=4)
        # petals
        fc = flower_colors[rng.randrange(len(flower_colors))]
        for pet_angle in range(0, 360, 72):
            rad = math.radians(pet_angle)
            px = fx + int(12 * math.cos(rad))
            py = fy + int(12 * math.sin(rad))
            draw.ellipse([(px-8, py-8), (px+8, py+8)], fill=fc)
        # center
        draw.ellipse([(fx-6, fy-6), (fx+6, fy+6)], fill=(255, 200, 50))

    # 8. Birds in the sky (gentle soaring V shapes)
    bird_color = (220, 130, 90)
    for bx, by, scale in [(350, 320, 1.0), (450, 280, 0.7), (1500, 400, 1.2), (1600, 350, 0.8)]:
        # draw a graceful curved bird wing shape
        draw.arc([bx - int(30*scale), by - int(20*scale), bx, by + int(10*scale)], start=0, end=180, fill=bird_color, width=int(6*scale))
        draw.arc([bx, by - int(20*scale), bx + int(30*scale), by + int(10*scale)], start=0, end=180, fill=bird_color, width=int(6*scale))

    # Downscale using LANCZOS to 1024x1024 for clean high-craft output
    final_im = im.resize((1024, 1024), Image.Resampling.LANCZOS)
    final_im.save("entry.png", "PNG", optimize=True, compress_level=9)
    print("Successfully generated entry.png (1024x1024)")

if __name__ == "__main__":
    draw_entry()
