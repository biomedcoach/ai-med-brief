# Fix the f-string syntax error in build_index.py
with open(r'D:\Qclaw\AiMedbrief\backend\build_index.py', 'r', encoding='utf-8') as f:
    content = f.read()

# The problem: inside an f-string, a single } closes it. Need to double it.
old = '.card-keypoints.open{{max-height:200px;margin-top:12px;padding-top:12px;border-top:1px dashed var(--border-light)}}'
new = ".card-keypoints.open{{max-height:200px;margin-top:12px;padding-top:12px;border-top:1px dashed var(--border-light)}}}}"

if old in content:
    content = content.replace(old, new)
    with open(r'D:\Qclaw\AiMedbrief\backend\build_index.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Fixed')
else:
    print('Pattern not found, checking...')
    # Find the problematic line
    for i, line in enumerate(content.split('\n'), 1):
        if 'card-keypoints' in line and 'open' in line:
            print(f'Line {i}: {line[:120]}')
