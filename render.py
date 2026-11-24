"""Render the front page of THE WORLD TODAY for Tuesday 24 November 2026.

Draws a 1024x1024 newspaper front page with Pillow from the verified facts
in news_data.md. Purely deterministic: no network, no clock, no randomness,
so every run writes identical bytes.
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "news_image.png")

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (20, 20, 20)
GREY = (90, 86, 76)
RED = (164, 30, 34)
GREEN = (11, 110, 63)
BLUE = (29, 78, 137)
ORANGE = (214, 96, 20)
PANEL = (238, 233, 220)
STRIP = (232, 236, 240)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap returning a list of lines that fit max_width."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for word in words[1:]:
            trial = cur + " " + word
            if draw.textlength(trial, font=fnt) <= max_width:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_width, fill=INK, leading=6):
    """Draw wrapped text; return the y just below the last line."""
    for line in wrap(draw, text, fnt, max_width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + leading
    return y


def centred(draw, cx, y, text, fnt, fill=INK):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size


def rule(draw, x0, x1, y, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_chip(draw, x0, y0, x1, y1):
    """Stylised green processor chip with pins and an NVDA label."""
    draw.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=GREEN)
    draw.rounded_rectangle(
        [x0 + 26, y0 + 26, x1 - 26, y1 - 26], radius=8,
        outline=(255, 255, 255), width=3)
    # pins on all four sides
    for i in range(5):
        t = y0 + 30 + i * ((y1 - y0 - 60) // 4)
        draw.line([(x0 - 12, t), (x0, t)], fill=GREEN, width=5)
        draw.line([(x1, t), (x1 + 12, t)], fill=GREEN, width=5)
        s = x0 + 30 + i * ((x1 - x0 - 60) // 4)
        draw.line([(s, y0 - 12), (s, y0)], fill=GREEN, width=5)
        draw.line([(s, y1), (s, y1 + 12)], fill=GREEN, width=5)
    label = font(SANS_B, 30)
    w = draw.textlength("NVDA", font=label)
    draw.text((x0 + (x1 - x0 - w) / 2, y0 + (y1 - y0) / 2 - 18),
              "NVDA", font=label, fill=(255, 255, 255))


def draw_chart(draw, x0, y0, x1, y1):
    """Rising line chart with an arrowhead and a +30% label."""
    draw.line([(x0, y1), (x1, y1)], fill=GREY, width=2)
    draw.line([(x0, y0), (x0, y1)], fill=GREY, width=2)
    pts = [(x0 + 6, y1 - 14), (x0 + 60, y1 - 30), (x0 + 110, y1 - 22),
           (x0 + 160, y1 - 58), (x0 + 210, y1 - 78), (x1 - 8, y0 + 10)]
    draw.line(pts, fill=GREEN, width=5, joint="curve")
    tip = pts[-1]
    draw.polygon([(tip[0] + 2, tip[1] - 12), (tip[0] + 14, tip[1] + 2),
                  (tip[0] - 6, tip[1] + 6)], fill=GREEN)
    pct = font(SANS_B, 34)
    draw.text((x0 + 8, y0 - 4), "+30%", font=pct, fill=GREEN)


def draw_burst(draw, cx, cy, r):
    """Orange starburst for the Kyiv strike story."""
    import math
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=ORANGE)


def draw_dome(draw, x0, y0, x1, y1):
    """Small blue capitol dome for the US midterms story."""
    mid = (x0 + x1) // 2
    draw.pieslice([x0 + 18, y0, x1 - 18, y0 + (x1 - x0) - 36],
                  start=180, end=360, fill=BLUE)
    draw.rectangle([x0 + 8, y0 + (x1 - x0) // 2 - 6, x1 - 8,
                    y0 + (x1 - x0) // 2 + 4], fill=BLUE)
    for i in range(4):
        cx = x0 + 22 + i * ((x1 - x0 - 44) // 3)
        draw.rectangle([cx - 6, y0 + (x1 - x0) // 2 + 6, cx + 6, y1 - 12],
                       fill=BLUE)
    draw.rectangle([x0, y1 - 12, x1, y1], fill=BLUE)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 36  # margin
    rx = W - mx

    # ---- Masthead ----
    title = font(SERIF_B, 86)
    centred(d, W // 2, 26, "THE WORLD TODAY", title)
    rule(d, mx, rx, 132, 3)
    date = font(SANS_B, 21)
    centred(d, W // 2, 144, "TUESDAY, 24 NOVEMBER 2026  ·  No. 329", date,
            fill=GREY)
    rule(d, mx, rx, 178, 1)

    # ---- Lead story (left) + illustration (right) ----
    ly = 196
    kick = font(SANS_B, 20)
    d.text((mx, ly), "TECHNOLOGY  ·  CHIPS", font=kick, fill=RED)
    head = font(SERIF_B, 52)
    y = ly + 34
    y = para(d, mx, y, "HUANG RETURNS\nTO NVIDIA", head, 600, leading=2)
    stand = font(SANS, 23)
    y = para(d, mx, y + 8,
             "Board reinstates chief executive 11 days after resignation; "
             "shares jump 30% in a day.",
             stand, 600, leading=5)
    body = font(SANS, 21)
    y = para(d, mx, y + 8,
             "Nvidia's board voted unanimously on Monday to restore Jensen "
             "Huang as chief executive, president and director, saying it "
             "had taken advice from senior US officials and found no "
             "national security risk.",
             body, 600, leading=5)
    assert y <= 516, f"lead body overflows into second row: ends at {y}"

    # illustration panel
    px0, py0, px1, py1 = 668, 196, 988, 500
    d.rounded_rectangle([px0, py0, px1, py1], radius=10, fill=PANEL,
                        outline=GREY, width=1)
    draw_chip(d, 700, 214, 850, 340)
    draw_chart(d, 700, 360, 956, 470)
    cap = font(SANS, 17)
    centred(d, (px0 + px1) // 2, 476, "Nvidia shares on Monday", cap,
            fill=GREY)

    # ---- Second row: two stories ----
    rule(d, mx, rx, 516, 1)
    sy = 532
    # Kyiv (left)
    draw_burst(d, mx + 30, sy + 26, 26)
    kh = font(SERIF_B, 29)
    d.text((mx + 68, sy + 8), "KYIV HIT AS STRIKES", font=kh, fill=INK)
    d.text((mx + 68, sy + 40), "KILL 14", font=kh, fill=INK)
    kb = font(SANS, 20)
    y2 = para(d, mx, sy + 84,
              "Russian air strikes on the Kyiv region killed at least 14 "
              "people, officials said. President Zelensky urged four-way "
              "talks soon.",
              kb, 448, leading=4)
    assert y2 <= 700, f"Kyiv body overflows: ends at {y2}"
    # Democrats (right)
    dx = 528
    draw_dome(d, dx, sy + 6, dx + 62, sy + 62)
    d.text((dx + 76, sy + 8), "DEMOCRATS' BIGGEST", font=kh, fill=INK)
    d.text((dx + 76, sy + 40), "HOUSE WIN IN DECADES", font=kh, fill=INK)
    y2 = para(d, dx, sy + 84,
              "Democrats won their largest House majority in decades. US "
              "stocks rebounded on Monday, recovering the post-election "
              "losses.",
              kb, 460, leading=4)
    assert y2 <= 700, f"Democrats body overflows: ends at {y2}"

    # ---- COP31 strip ----
    rule(d, mx, rx, 700, 1)
    d.rectangle([mx, 714, rx, 792], fill=STRIP)
    strip_h = font(SERIF_B, 24)
    d.text((mx + 14, 724), "COP31 AFTERMATH", font=strip_h, fill=BLUE)
    strip_b = font(SANS, 20)
    para(d, mx + 14, 758,
         "Antalya talks collapsed on Sunday — the longest climate summit "
         "ever — as the EU and 130 nations rejected a text with no "
         "fossil-fuel phase-out.",
         strip_b, 920, leading=3)

    # ---- In brief ----
    rule(d, mx, rx, 808, 1)
    brief_h = font(SANS_B, 19)
    d.text((mx, 820), "IN BRIEF", font=brief_h, fill=RED)
    briefs = [
        ("MANCHESTER — ", "12,000 evacuated from arena after substance "
         "scare."),
        ("INDIA–NEPAL — ", "Modi, Shah open rail link; India pledges aid."),
        ("INDONESIA — ", "Factory fire kills at least 24; 30 missing."),
        ("ESTONIA — ", "Russia threatens \"open war\"; border to shut."),
        ("EU — ", "New Russia sanctions proposed on banks, crypto."),
        ("SPORT — ", "Pant's 128 in drawn Test; Verstappen wins Vegas GP."),
    ]
    bf = font(SANS, 19)
    bfb = font(SANS_B, 19)
    col_w = 464
    for i, (lead, rest) in enumerate(briefs):
        col = i % 2
        row = i // 2
        bx = mx + col * (col_w + 24)
        by = 850 + row * 40
        d.text((bx, by), lead, font=bfb, fill=INK)
        lw = d.textlength(lead, font=bfb)
        lines = wrap(d, rest, bf, col_w - lw)
        assert len(lines) <= 2, f"brief wraps to {len(lines)} lines: {lead}{rest}"
        d.text((bx + lw, by), lines[0], font=bf, fill=INK)
        # second line, if any, starts at the column edge
        if len(lines) > 1:
            d.text((bx, by + 21), lines[1], font=bf, fill=INK)

    # ---- Footer ----
    rule(d, mx, rx, 978, 1)
    foot = font(SANS, 15)
    centred(d, W // 2, 986,
            "THE WORLD TODAY  ·  Tuesday 24 November 2026  ·  Stories first "
            "reported 24 November 2026",
            foot, fill=GREY)

    img.save(OUT, format="PNG")
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
