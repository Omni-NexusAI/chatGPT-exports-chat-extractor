
import json
import os
import re
from pathlib import Path

def extract_claude_chats(input_file, output_dir, verbose=True):
    if verbose:
        print("--- Claude Chat Extractor Starting ---")
        print(f"Input file: {input_file}")
        print(f"Output directory: {output_dir}")

    input_path = Path(input_file)
    if not input_path.exists():
        print(f"ERROR: Input file not found: {input_file}")
        return False

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    if verbose:
        print("Reading JSON file...")

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            conversations = json.load(f)
    except json.JSONDecodeError as e:
        print(f"FATAL ERROR: Could not parse JSON data: {e}")
        return False
    except Exception as e:
        print(f"ERROR: Failed to read input file: {e}")
        return False

    if verbose:
        print(f"Successfully parsed {len(conversations)} chat sessions.")
        print("Creating individual chat files...")

    successful = 0
    for i, convo in enumerate(conversations, 1):
        convo_name = convo.get('name')
        if not convo_name:
            continue

        safe_title = re.sub(r'[\\/*?:",<>|]', "", convo_name).replace(' ', '_')
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

        html_content = "<html><head><title>" + convo_name + "</title></head><body>"
        html_content += f"<h1>{convo_name}</h1>"
        
        for message in convo.get('chat_messages', []):
            sender = message.get('sender')
            text = ""
            if message.get('content'):
                text_parts = []
                for content_part in message.get('content', []):
                    if content_part.get('type') == 'text':
                        text_parts.append(content_part.get('text', ''))
                text = "".join(text_parts)

            # Fallback to the 'text' field if 'content' is empty or not as expected
            if not text and message.get('text'):
                text = message.get('text')

            html_content += f"<p><b>{sender}:</b> {text}</p>"

        html_content += "</body></html>"

        try:
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            successful += 1
        except Exception as e:
            print(f"ERROR: Failed to write {output_filename}: {e}")

    if verbose:
        print(f"--- Script Finished. {successful}/{len(conversations)} sessions processed. ---")

    return True

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Extract Claude conversations into individual HTML files.')
    parser.add_argument('input_file', nargs='?', default='conversations.json',
                       help='Path to conversations.json file (default: conversations.json)')
    parser.add_argument('output_dir', nargs='?', default='claude_chats',
                       help='Output directory (default: claude_chats)')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Suppress progress messages')
    
    args = parser.parse_args()
    
    success = extract_claude_chats(args.input_file, args.output_dir, not args.quiet)
    import sys
    sys.exit(0 if success else 1)
