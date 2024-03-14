import os
import fnmatch

def read_ignore_files(root_path, ignore_file_names):
    ignore_patterns = []
    for ignore_file in ignore_file_names:
        ignore_path = os.path.join(root_path, ignore_file)
        if os.path.exists(ignore_path):
            with open(ignore_path, "r") as file:
                patterns = [line.strip() for line in file if line.strip() and not line.startswith("#")]
                ignore_patterns.extend([os.path.join(root_path, pattern) for pattern in patterns])
    return ignore_patterns

def is_excluded(path, ignore_patterns, root_path):
    abs_path = os.path.join(root_path, path)
    for pattern in ignore_patterns:
        if pattern.endswith("/"):
            if abs_path.startswith(pattern) or os.path.commonpath([abs_path, pattern]) == pattern.rstrip("/"):
                return True
        elif fnmatch.fnmatch(abs_path, pattern):
            return True
    return False

def generate_project_summary(root_path, ignore_file_names, output_file):
    ignore_patterns = read_ignore_files(root_path, ignore_file_names)
    summary = "# Project Structure\n\nThis is a representation of the project's folder structure using Markdown notation.\n\n"
    
    for dirpath, dirnames, filenames in os.walk(root_path):
        # Exclude .git folder if it exists
        if ".git" in dirnames:
            dirnames.remove(".git")
        
        # Exclude folders from ignore patterns if provided
        if ignore_patterns:
            dirnames[:] = [d for d in dirnames if not is_excluded(os.path.join(dirpath, d), ignore_patterns, root_path)]
        
        # Add folder structure to summary
        relative_path = os.path.relpath(dirpath, root_path)
        indent = (relative_path.count(os.sep) + 1) * "  "
        summary += f"{indent}- {os.path.basename(dirpath)}/\n"
        
        for filename in filenames:
            # Exclude generate_project_summary.py file and the output file
            if filename in ["generate_project_summary.py", output_file]:
                continue
            
            file_path = os.path.join(dirpath, filename)
            relative_path = os.path.relpath(file_path, root_path)
            
            # Exclude files from ignore patterns if provided
            if ignore_patterns and is_excluded(relative_path, ignore_patterns, root_path):
                continue
            
            # Add file to summary
            indent = (relative_path.count(os.sep) + 2) * "  "
            summary += f"{indent}- {filename}\n"
    
    summary += "\n# File Contents\n\n"
    
    for dirpath, dirnames, filenames in os.walk(root_path):
        # Exclude .git folder if it exists
        if ".git" in dirnames:
            dirnames.remove(".git")
        
        # Exclude folders from ignore patterns if provided
        if ignore_patterns:
            dirnames[:] = [d for d in dirnames if not is_excluded(os.path.join(dirpath, d), ignore_patterns, root_path)]
        
        for filename in filenames:
            # Exclude generate_project_summary.py file and the output file
            if filename in ["generate_project_summary.py", output_file]:
                continue
            
            file_path = os.path.join(dirpath, filename)
            relative_path = os.path.relpath(file_path, root_path)
            
            # Exclude files from ignore patterns if provided
            if ignore_patterns and is_excluded(relative_path, ignore_patterns, root_path):
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
            except UnicodeDecodeError:
                try:
                    with open(file_path, 'r', encoding='shift_jis') as file:
                        content = file.read()
                except UnicodeDecodeError:
                    content = "Error: Unable to decode file content."
            
            summary += f"```{os.path.basename(file_path)}\n{content}\n```\n\n"
            summary += "---\n\n"  # Add a separator between files
    
    return summary

def save_summary_to_file(summary, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(summary)

def main():
    current_path = os.getcwd()
    project_path = input(f"Enter the project path (default: {current_path}): ") or current_path
    
    output_folder = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(output_folder, f"{os.path.basename(project_path)}_project_summary.txt")
    
    ignore_file_names = [".gitignore", ".summaryignore"]
    summary = generate_project_summary(project_path, ignore_file_names, output_file)
    save_summary_to_file(summary, output_file)
    
    print(f"Project summary has been saved to {output_file}")

if __name__ == '__main__':
    main()