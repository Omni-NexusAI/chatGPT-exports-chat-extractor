import json
import os
import re
import sys
from pathlib import Path

def split_chat_html(input_file, output_dir, verbose=True):
    """
    Split chat.html into individual HTML files for each conversation
    """
    if verbose:
        print("--- Chat HTML Splitter Starting ---")
        print(f"Input file: {input_file}")
        print(f"Output directory: {output_dir}")

    input_path = Path(input_file)
    if not input_path.exists():
        print(f"ERROR: Input file not found: {input_file}")
        return False

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    if verbose:
        print("Reading HTML file...")

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"ERROR: Failed to read input file: {e}")
        return False

    if verbose:
        print("Searching for JSON data...")

    json_data_lines = []
    in_json = False
    for line in lines:
        if 'var jsonData = ' in line:
            in_json = True
            # Add the part of the line after the declaration
            json_data_lines.append(line.split('var jsonData = ', 1)[1])
            continue
        if 'var assetsJson = ' in line:
            # Remove the trailing comma and semicolon from the last line
            last_line = json_data_lines[-1].strip()
            if last_line.endswith(','):
                last_line = last_line[:-1]
            if last_line.endswith(';'):
                last_line = last_line[:-1]
            json_data_lines[-1] = last_line
            break
        if in_json:
            json_data_lines.append(line)

    if not json_data_lines:
        print("FATAL ERROR: Could not find the 'jsonData' array.")
        return False

    # Reconstruct the HTML template
    with open(input_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # This is a simplified way to get the template. A more robust solution
    # might be needed if the structure is complex.
    try:
        json_start_index = html_content.find(json_data_lines[0])
        # Find the end of the JSON data in the original content
        # This is tricky because the last line might be modified.
        # We'll find the start of assetsJson instead.
        assets_json_start_index = html_content.find('var assetsJson = ')
        html_template_start = html_content[:json_start_index]
        html_template_end = html_content[assets_json_start_index:]
    except (ValueError, IndexError) as e:
        print(f"Error reconstructing HTML template: {e}")
        return False

    json_data_string = "".join(json_data_lines).strip()
    if json_data_string.endswith(';'):
        json_data_string = json_data_string[:-1]

    try:
        all_sessions = json.loads(json_data_string)
    except json.JSONDecodeError as e:
        print(f"FATAL ERROR: Could not parse JSON data: {e}")
        print("Problematic JSON string:", json_data_string)
        return False

    if verbose:
        print(f"Successfully parsed {len(all_sessions)} chat sessions.")

    if verbose:
        print("Creating individual chat files...")

    successful = 0
    for i, session in enumerate(all_sessions, 1):
        session_title = session.get('title', f'Untitled_Chat_{i}')
        safe_title = re.sub(r'[\\/*?:"<>|]', "", session_title).replace(' ', '_')
        safe_title = safe_title[:100] or f'chat_{i}'
        output_filename = output_path / f"{safe_title}.html"

        counter = 1
        original_output = output_filename
        while output_filename.exists():
            counter += 1
            name = original_output.stem
            suffix = original_output.suffix
            output_filename = output_path / f"{name}_{counter}{suffix}"

        if verbose:
            print(f"  -> Writing {output_filename}")

        session_json_string = json.dumps([session], indent=2, ensure_ascii=False)
        new_html_content = html_template_start + session_json_string + '\n' + html_template_end

        try:
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(new_html_content)
            successful += 1
        except Exception as e:
            print(f"ERROR: Failed to write {output_filename}: {e}")

    if verbose:
        print(f"--- Script Finished. {successful}/{len(all_sessions)} sessions processed. ---")

    return successful == len(all_sessions)

def main():
    """Main function with command line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Split chat.html into individual conversation files')
    parser.add_argument('input_file', nargs='?', default='chat.html',
                       help='Path to chat.html file (default: chat.html)')
    parser.add_argument('output_dir', nargs='?', default='split_chats',
                       help='Output directory (default: split_chats)')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Suppress progress messages')
    
    args = parser.parse_args()
    
    success = split_chat_html(args.input_file, args.output_dir, not args.quiet)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()