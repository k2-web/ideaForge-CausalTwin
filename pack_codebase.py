import os

def pack_project():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(project_dir, "ideaforge_causaltwin_codebase.md")
    
    files_to_pack = [
        "requirements.txt",
        "graph_db.py",
        "data_ingestion.py",
        "causal_engine.py",
        "agents.py",
        "app.py",
        "test_engine.py",
        "README.md"
    ]
    
    with open(output_file, "w", encoding="utf-8") as out:
        out.write("# ideaForge Causal Digital Twin Codebase Export\n\n")
        out.write("This document aggregates all the code files for the ideaForge Causal Digital Twin project. You can copy and paste this directly into ChatGPT to share the complete context of the application.\n\n")
        
        for filename in files_to_pack:
            filepath = os.path.join(project_dir, filename)
            if os.path.exists(filepath):
                out.write(f"## File: `{filename}`\n")
                
                # Determine language for markdown syntax highlighting
                ext = os.path.splitext(filename)[1]
                lang = "python" if ext == ".py" else "markdown" if ext == ".md" else "text"
                
                out.write(f"```{lang}\n")
                with open(filepath, "r", encoding="utf-8") as f:
                    out.write(f.read())
                out.write("\n```\n\n")
                print(f"Packed {filename}")
            else:
                print(f"Skipping {filename} (not found)")
                
    print(f"Project packed successfully into: {output_file}")

if __name__ == "__main__":
    pack_project()
