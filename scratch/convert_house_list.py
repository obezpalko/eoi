import re
import sys

def convert_list_to_table(content):
    lines = content.split('\n')
    new_lines = []
    current_list = []
    
    def flush_list():
        if not current_list:
            return
        
        # Determine section header or something
        new_lines.append("| Imagen | Término | Traducción |")
        new_lines.append("| :--- | :--- | :--- |")
        for item in current_list:
            # Match - **Word** - Definition / Translation
            match = re.match(r'^- \*\*([^*]+)\*\* - ([^/]+) / (.+)$', item)
            if match:
                term = f"**{match.group(1)}**"
                trans = f"{match.group(2).strip()} / {match.group(3).strip()}"
                
                # Safe filename
                char = match.group(1).replace('**', '').strip()
                char = char.split('/')[0].strip()
                char = char.split(',')[0].strip()
                char = char.split('(')[0].strip()
                if char.lower().startswith('el '): char = char[3:]
                if char.lower().startswith('la '): char = char[3:]
                if char.lower().startswith('los '): char = char[4:]
                if char.lower().startswith('las '): char = char[4:]
                
                safe_name = re.sub(r'[^\w\s-]', '', char.lower())
                safe_name = re.sub(r'[-\s]+', '_', safe_name)
                
                new_lines.append(f"| ![[La Casa/{safe_name}.jpg]] | {term} | {trans} |")
            else:
                # Handle cases without Russian translation or different format
                match2 = re.match(r'^- \*\*([^*]+)\*\* - (.+)$', item)
                if match2:
                    term = f"**{match2.group(1)}**"
                    trans = match2.group(2).strip()
                    
                    char = match2.group(1).replace('**', '').strip()
                    char = char.split('/')[0].strip()
                    if char.lower().startswith('el '): char = char[3:]
                    if char.lower().startswith('la '): char = char[3:]
                    
                    safe_name = re.sub(r'[^\w\s-]', '', char.lower())
                    safe_name = re.sub(r'[-\s]+', '_', safe_name)
                    new_lines.append(f"| ![[La Casa/{safe_name}.jpg]] | {term} | {trans} |")
                else:
                    new_lines.append(item)
        current_list.clear()

    for line in lines:
        if line.strip().startswith('- **'):
            current_list.append(line)
        else:
            flush_list()
            new_lines.append(line)
    
    flush_list()
    return '\n'.join(new_lines)

if __name__ == "__main__":
    file_path = "/home/alexb/src/github.com/obezpalko/eoi/30-Vocabulario/Temas/La Casa.md"
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = convert_list_to_table(content)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
