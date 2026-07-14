import json
import re

html_path = r'c:\Users\Siddhant\OneDrive\图片\Desktop\scholarship\frontend\pages\scholarships.html'
txt_path = r'c:\Users\Siddhant\OneDrive\图片\Desktop\scholarship\reqs.txt'

with open(txt_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Parse requirements. Format: * Name [URL]\n  - Requirement: text
req_dict = {}
blocks = text.split('* ')
for block in blocks[1:]:
    lines = block.split('\n')
    if len(lines) >= 2:
        name_url_line = lines[0].strip()
        req_line = lines[1].strip()
        
        # Extract name and url
        m = re.search(r'(.*?) \[(.*?)\]', name_url_line)
        if m:
            name = m.group(1).strip()
            url = m.group(2).strip()
            
            # Extract req
            if req_line.startswith('- Requirement:'):
                req_text = req_line.replace('- Requirement:', '').strip()
                req_dict[url] = req_text

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'let scholarships = (\[.*?\]);', content, re.DOTALL)
if match:
    json_str = match.group(1)
    try:
        data = json.loads(json_str)
        # update data with requirements
        for s in data:
            url = s.get('url', '')
            if url in req_dict:
                s['requirement'] = req_dict[url]
            else:
                s['requirement'] = "विवरण उपलब्ध नहीं।" # Description not available
                
        compact_json = "[\n" + ",\n".join("    " + json.dumps(item, ensure_ascii=False) for item in data) + "\n]"
        new_content = content[:match.start(1)] + compact_json + content[match.end(1):]
        
        # Now update the UI in scholarships.html to show requirements
        # Find where the card is built
        # `<div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">...</div>`
        # We'll inject a requirement div before the View Details button.
        
        ui_injection = """
        <div style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1.5rem; line-height: 1.5; background: rgba(0,0,0,0.2); padding: 10px; border-radius: 8px; border-left: 3px solid var(--primary);">
            <strong>Requirement:</strong> ${s.requirement || 'Not specified'}
        </div>
        """
        
        # Replace the old button block and inject our requirement text above it
        # The button block looks like: `<a href="${s.url || '#'}" target="_blank" class="btn btn-outline" ...`
        if '<strong>Requirement:</strong>' not in new_content:
            new_content = new_content.replace(
                '<a href="${s.url || \'#\'}" target="_blank" class="btn btn-outline"',
                ui_injection.strip() + '\\n            ' + '<a href="${s.url || \'#\'}" target="_blank" class="btn btn-outline"'
            )

        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Successfully added requirements to {len(req_dict)} scholarships.")
    except Exception as e:
        print("Error:", e)
else:
    print("Could not find scholarships array")
