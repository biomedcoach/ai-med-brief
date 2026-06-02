with open(r'D:\Qclaw\AiMedbrief\backend\build_index.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Line 176 (0-indexed: 175) has the issue
for i, line in enumerate(lines):
    if 'card-keypoints.open' in line and 'border-top:1px dashed' in line:
        print(f"Found at line {i+1}: {line.strip()[:100]}")
        # Replace the single } with double }}
        if line.rstrip().endswith('}'):
            new_line = line.rstrip()[:-1] + '}}}\n'
            lines[i] = new_line
            print(f"Fixed to: {new_line.strip()[:100]}")

with open(r'D:\Qclaw\AiMedbrief\backend\build_index.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
print('Done')
