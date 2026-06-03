"""Replace text logo with image logo in all article detail pages."""
import glob

files = glob.glob(r'D:\Qclaw\AiMedbrief\articles\*.html')
old = '<a href="../index.html" class="top-bar-brand">AiMedbrief</a>'
new = '<a href="../index.html" class="top-bar-brand"><img src="../images/logo.png" alt="AiMedbrief" style="height:28px;width:auto"></a>'

for f in sorted(files):
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    if old in content:
        content = content.replace(old, new)
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(content)
        print(f'Updated: {f}')
    else:
        print(f'NOT FOUND in: {f}')
        # Debug: find actual match
        idx = content.find('top-bar-brand')
        if idx >= 0:
            print(f'  Context: ...{content[idx:idx+80]}...')
