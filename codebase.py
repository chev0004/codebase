#!/usr/bin/env python3
import os
import argparse
import time
from pathlib import Path
from tqdm import tqdm
try:
    import pathspec
except ImportError:
    print("Error: 'pathspec' library not found. Please install it using: pip install pathspec")
    exit(1)

# List of file extensions to be cautious about, as they are likely binary.
POTENTIALLY_BINARY_EXTENSIONS = {
    '.pyc', '.pyo', '.o', '.a', '.so', '.dll', '.exe',
    '.DS_Store', '.class', '.jar', '.war', '.ear',
    '.zip', '.tar', '.gz', '.bz2', '.7z', '.rar',
    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.ico',
    '.mp3', '.wav', '.flac', '.ogg',
    '.mp4', '.avi', '.mov', '.wmv', '.mkv',
    '.db', '.sqlite', '.sqlite3', '.dat'
}

def load_gitignore(root_dir: Path) -> pathspec.PathSpec:
    """Loads and parses the .gitignore file, adding default ignore patterns."""
    gitignore_path = root_dir / '.gitignore'
    patterns = []
    if gitignore_path.is_file():
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            patterns = f.readlines()
    
    # Add common nuisance files to the ignore list by default
    default_ignores = ['.git/', '__pycache__/', '*.pyc', '.DS_Store']
    
    return pathspec.PathSpec.from_lines('gitwildmatch', patterns + default_ignores)

def gather_files_to_include(root_dir: Path, spec: pathspec.PathSpec) -> list[tuple[Path, Path]]:
    """Walks the directory and gathers a list of files to include."""
    files_to_include = []
    for path_obj in root_dir.rglob('*'):
        if path_obj.is_file():
            # Get path relative to the root for matching
            relative_path = path_obj.relative_to(root_dir)
            
            # Normalize path for matching (use forward slashes)
            relative_path_str = str(relative_path).replace(os.sep, '/')
            
            if not spec.match_file(relative_path_str):
                files_to_include.append((path_obj, relative_path))
                
    return files_to_include

def write_codebase_to_file(project_name: str, files_list: list, output_filename: str):
    """Writes the content of all included files into a single output file."""
    total_files = len(files_list)
    
    try:
        with open(output_filename, 'w', encoding='utf-8', errors='ignore') as outfile:
            # Write a header
            outfile.write(f"# Codebase for: {project_name}\n")
            outfile.write(f"# Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            outfile.write(f"# Total files: {total_files}\n")
            outfile.write("="*80 + "\n\n")

            # Use tqdm for the progress bar
            for full_path, relative_path in tqdm(files_list, desc="Combining files", unit="file", ncols=100):
                
                # Use Markdown for file headers
                outfile.write("---\n")
                outfile.write(f"### File: `{str(relative_path).replace(os.sep, '/')}`\n")
                outfile.write("---\n\n")
                
                try:
                    with open(full_path, 'r', encoding='utf-8', errors='strict') as infile:
                        content = infile.read()
                        # Use Markdown code blocks with language hints if possible
                        lang = full_path.suffix.lstrip('.')
                        outfile.write(f"```{lang}\n")
                        outfile.write(content)
                        outfile.write("\n```\n\n")
                except UnicodeDecodeError:
                    outfile.write("```\n[Warning: Could not decode file content. It may be binary or have an unsupported encoding.]\n```\n\n")
                except Exception as e:
                    outfile.write(f"```\n[Error: Could not read file. Reason: {e}]\n```\n\n")
                    
    except IOError as e:
        print(f"\nError writing to output file '{output_filename}': {e}")

def main():
    """Main function to parse arguments and run the script."""
    parser = argparse.ArgumentParser(
        description="A tool to combine a codebase into a single file for LLM analysis.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        'directory',
        nargs='?',
        default='.',
        help="The root directory of the codebase to process (defaults to the current directory)."
    )
    parser.add_argument(
        '-o', '--output',
        dest='output_filename',
        default=None,
        help="The name of the output file. If not provided, it defaults to '[project-name]_codebase.md'."
    )
    args = parser.parse_args()
    
    start_time = time.monotonic()
    
    root_dir = Path(args.directory).resolve()
    if not root_dir.is_dir():
        print(f"Error: Directory '{root_dir}' not found.")
        return

    project_name = root_dir.name
    output_filename = args.output_filename or f"{project_name}_codebase.md"

    print(f"Starting to process directory: {root_dir}")
    
    spec = load_gitignore(root_dir)
    files_to_include = gather_files_to_include(root_dir, spec)
    
    if not files_to_include:
        print("No files to include. Check your .gitignore or directory.")
        return
        
    print(f"Found {len(files_to_include)} files to include.")
    
    write_codebase_to_file(project_name, files_to_include, output_filename)
    
    duration = time.monotonic() - start_time
    print("\n" + "="*50)
    print("CODEBASE CONSOLIDATION COMPLETE")
    print("="*50)
    print(f"Success! Combined {len(files_to_include)} files into a single file.")
    print(f"Output file: {output_filename}")
    print(f"Time taken: {duration:.2f} seconds")
    print("="*50)

if __name__ == "__main__":
    main()