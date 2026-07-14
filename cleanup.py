import json
import re

html_path = r'c:\Users\Siddhant\OneDrive\图片\Desktop\scholarship\frontend\pages\scholarships.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract the scholarships array
match = re.search(r'let scholarships = (\[.*?\]);', content, re.DOTALL)
if match:
    json_str = match.group(1)
    # Parse it
    try:
        data = json.loads(json_str)
        # Format it so each object is on one line
        compact_json = "[\n" + ",\n".join("    " + json.dumps(item) for item in data) + "\n]"
        
        # Replace the bloated JSON
        new_content = content[:match.start(1)] + compact_json + content[match.end(1):]
        
        # Now fix the grid to show exactly 3 scholarships per horizontal line in the UI
        # We need to change: grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
        # To: grid-template-columns: repeat(3, 1fr);
        new_content = new_content.replace(
            'grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));',
            'grid-template-columns: repeat(3, 1fr);'
        )
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Success! File compacted and grid updated to 3 per row.")
    except Exception as e:
        print("Error parsing JSON:", e)
else:
    print("Could not find the scholarships array.")
