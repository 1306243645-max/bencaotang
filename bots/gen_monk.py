"""Generate a cute Buddhist monk SVG"""
import sys
from pathlib import Path
sys.path.insert(0,'.')
from agents.base import BaseAgent

agent = BaseAgent(system='你是佛教艺术插画师，专画可爱小沙弥。只输出SVG代码。')

prompt = """Draw a cute cartoon Buddhist young monk meditating. SVG only, 256x256 viewBox.
Requirements:
- Round bald head with 3 small dots (ordination scars) on top
- Gentle closed smiling eyes, peaceful expression
- Grey robe with red kasaya sash draped diagonally
- Hands in meditation mudra (dhyana mudra)
- Sitting cross-legged on a pink lotus
- Soft golden halo behind head
- Warm cream background circle
- Simple clean lines, kawaii style
- Use gradient fills for depth
Only output SVG code, no markdown, no explanation."""

resp = agent.chat(prompt)
svg = resp.content
# Clean up
for tag in ['svg','SVG']:
    if f'<{tag}' in svg:
        start = svg.find(f'<{tag}')
        end = svg.find(f'</{tag}>') + len(f'</{tag}>')
        if end > start:
            svg = svg[start:end]
            break

Path('web/static/orange_cat.svg').write_text(svg, encoding='utf-8')
print('SVG saved!')
print(svg[:300])
