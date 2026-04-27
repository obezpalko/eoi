import re
import sys

def transform_table(content, folder_name):
    lines = content.split('\n')
    new_lines = []
    in_table = False
    
    # Common headers in this project
    headers = ["Característica", "Tipo", "Parte", "Elemento", "Relación", "Español", "Adjetivo", "Palabra", "Término"]
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('|') and '|' in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) < 3:
                new_lines.append(line)
                continue
            
            # Header row check
            is_header = any(h in line for h in headers)
            
            if is_header and "Imagen" not in line:
                new_lines.append("| Imagen " + line)
                in_table = True
                continue
            elif "Imagen" in line:
                new_lines.append(line)
                in_table = True
                continue
            
            # Separator row
            if "---" in line:
                if in_table:
                    new_lines.append("| :--- " + line)
                else:
                    new_lines.append(line)
                continue
            
            # Content row
            if in_table:
                # Extract first word as image name
                # Part 0 is empty (before first |), Part 1 is the first column
                char = parts[1].replace('**', '').strip()
                # If there are multiple (e.g. El padre / La madre), take the first one
                char = char.split('/')[0].strip()
                char = char.split(',')[0].strip()
                char = char.split('(')[0].strip()
                
                # Safe filename
                safe_name = re.sub(r'[^\w\s-]', '', char.lower())
                safe_name = re.sub(r'[-\s]+', '_', safe_name)
                
                # Check if it already has an image link
                if '![' in line:
                    new_lines.append(line)
                else:
                    new_lines.append(f"| ![[{folder_name}/{safe_name}.jpg]] " + line)
            else:
                new_lines.append(line)
        else:
            in_table = False
            new_lines.append(line)
            
    return '\n'.join(new_lines)

if __name__ == "__main__":
    file_path = sys.argv[1]
    folder = sys.argv[2]
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = transform_table(content, folder)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
