#!/usr/bin/env python3
"""Fix missing closing </div> tags for nav-section-body elements."""

FILEPATH = r'static\dashboard\index.html'

with open(FILEPATH, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Section body IDs and the comment that starts the NEXT section after each
# Structure: after closing last nav-sub in section, we need:
#     </div>   <- close nav-section-body
#   </div>     <- close nav-section
#
# Currently only: </div> (nav-section), so we need to insert one more </div> before

# Find lines where section body divs were opened
section_bodies = [
    'sec-inicio', 'sec-red', 'sec-ops', 'sec-fin', 'sec-cfg', 'sec-sec', 'sec-me'
]

# Find the line indices for each section body opening
body_open_lines = {}
for i, line in enumerate(lines):
    for sec_id in section_bodies:
        if f'id="{sec_id}"' in line and 'nav-section-body' in line:
            body_open_lines[sec_id] = i
            break

print("Section body openings found:")
for k, v in body_open_lines.items():
    print(f"  {k}: line {v+1}")

# Find the next <!-- ② ... comment lines
next_section_comments = []
for i, line in enumerate(lines):
    stripped = line.strip()
    if stripped.startswith('<!-- ②') or stripped.startswith('<!-- ③') or \
       stripped.startswith('<!-- ④') or stripped.startswith('<!-- ⑤') or \
       stripped.startswith('<!-- ⑥') or stripped.startswith('<!-- ⑦') or \
       'sidebar-footer' in stripped:
        next_section_comments.append(i)

print("\nNext section markers at lines:")
for i in next_section_comments:
    print(f"  {i+1}: {lines[i].rstrip()}")

# For each section start comment (except the first section),
# 2 lines before should be </div> (nav-section), 
# 3 lines before should be </div> (nav-section-body that's missing)
# Let's verify and insert

# Strategy: before each section comment (and sidebar-footer),
# go back to find the </div> that closes the nav-section.
# Then insert another </div> for nav-section-body just before it.

new_lines = list(lines)
insertions = 0

for marker_line in reversed(next_section_comments):
    # Walk backwards from marker to find closing </div> of nav-section
    for j in range(marker_line - 1, max(0, marker_line - 5), -1):
        stripped = new_lines[j].strip()
        if stripped == '</div>':
            # This is the nav-section closer; insert nav-section-body closer before it
            # Get indentation of this </div>
            indent = len(new_lines[j]) - len(new_lines[j].lstrip())
            inner_indent = '    ' + new_lines[j][:indent]
            new_lines.insert(j, inner_indent + '</div>\n')
            insertions += 1
            print(f"Inserted </div> at line {j+1} (before section marker at {marker_line+2})")
            break

print(f"\nTotal insertions: {insertions}")

with open(FILEPATH, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("File saved successfully.")
