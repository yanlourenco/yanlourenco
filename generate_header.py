import random

# Dual line grid:
# Line 1: YAN (bold 5x7)
# Line 2: LOURENÇO (4x7)
# Total rows: 7 + 2 (gap) + 7 = 16 rows
rows = 16
cols = 48
sq_size = 11
gap = 3
pad_x = 24
pad_y = 20

font_5x7 = {
    'Y': [
        [1,0,0,0,1],
        [1,0,0,0,1],
        [0,1,0,1,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0],
        [0,0,1,0,0]
    ],
    'A': [
        [0,1,1,1,0],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,1,1,1,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1]
    ],
    'N': [
        [1,0,0,0,1],
        [1,1,0,0,1],
        [1,0,1,0,1],
        [1,0,0,1,1],
        [1,0,0,0,1],
        [1,0,0,0,1],
        [1,0,0,0,1]
    ]
}

font_4x7 = {
    'L': [
        [1,0,0,0],
        [1,0,0,0],
        [1,0,0,0],
        [1,0,0,0],
        [1,0,0,0],
        [1,0,0,0],
        [1,1,1,1]
    ],
    'O': [
        [0,1,1,0],
        [1,0,0,1],
        [1,0,0,1],
        [1,0,0,1],
        [1,0,0,1],
        [1,0,0,1],
        [0,1,1,0]
    ],
    'U': [
        [1,0,0,1],
        [1,0,0,1],
        [1,0,0,1],
        [1,0,0,1],
        [1,0,0,1],
        [1,0,0,1],
        [0,1,1,0]
    ],
    'R': [
        [1,1,1,0],
        [1,0,0,1],
        [1,0,0,1],
        [1,1,1,0],
        [1,0,1,0],
        [1,0,0,1],
        [1,0,0,1]
    ],
    'E': [
        [1,1,1,1],
        [1,0,0,0],
        [1,0,0,0],
        [1,1,1,0],
        [1,0,0,0],
        [1,0,0,0],
        [1,1,1,1]
    ],
    'N': [
        [1,0,0,1],
        [1,1,0,1],
        [1,0,1,1],
        [1,0,0,1],
        [1,0,0,1],
        [1,0,0,1],
        [1,0,0,1]
    ],
    'C': [
        [0,1,1,1],
        [1,0,0,0],
        [1,0,0,0],
        [1,0,0,0],
        [1,0,0,0],
        [1,0,0,0],
        [0,1,1,1]
    ]
}

grid = [[0 for _ in range(cols)] for _ in range(rows)]

# 1. Place "YAN" on rows 0..6
word1 = "YAN"
w1_total = sum(len(font_5x7[ch][0]) for ch in word1) + 2 * (len(word1) - 1)
offset1 = (cols - w1_total) // 2
cur_x = offset1
for ch in word1:
    m = font_5x7[ch]
    w = len(m[0])
    for r in range(7):
        for c in range(w):
            if m[r][c]:
                grid[r][cur_x + c] = 3
    cur_x += w + 2

# 2. Place "LOURENCO" on rows 9..15
word2 = "LOURENCO"
w2_total = sum(len(font_4x7[ch][0]) for ch in word2) + 1 * (len(word2) - 1)
offset2 = (cols - w2_total) // 2
cur_x = offset2
for ch in word2:
    m = font_4x7[ch]
    w = len(m[0])
    for r in range(7):
        for c in range(w):
            if m[r][c]:
                grid[9 + r][cur_x + c] = 3
    cur_x += w + 1

# Random background activity
random.seed(42)
for r in range(rows):
    for c in range(cols):
        if grid[r][c] == 0:
            # Scatter subtle commit tiles around margins
            is_near_text = False
            if r < 8 and (offset1 - 1 <= c <= offset1 + w1_total):
                is_near_text = True
            if r >= 8 and (offset2 - 1 <= c <= offset2 + w2_total):
                is_near_text = True
            
            if not is_near_text:
                p = random.random()
                if p < 0.08:
                    grid[r][c] = 2
                elif p < 0.22:
                    grid[r][c] = 1

width = pad_x * 2 + cols * (sq_size + gap) - gap
height = pad_y * 2 + rows * (sq_size + gap) - gap

rects = []
for r in range(rows):
    for c in range(cols):
        x = pad_x + c * (sq_size + gap)
        y = pad_y + r * (sq_size + gap)
        val = grid[r][c]
        if val == 3:
            fill = '#39d353' # Active bright GitHub green square
        elif val == 2:
            fill = '#26a641' # Medium activity green
        elif val == 1:
            fill = '#0e4429' # Low activity green
        else:
            fill = '#161b22' # Inactive dark tile
        rects.append(f'  <rect x="{x}" y="{y}" width="{sq_size}" height="{sq_size}" rx="2" ry="2" fill="{fill}" />')

svg = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" rx="10" fill="#0d1117" />
{chr(10).join(rects)}
</svg>'''

with open('header.svg', 'w', encoding='utf-8') as f:
    f.write(svg)
print("Dual line YAN LOURENCO header.svg generated successfully!")
