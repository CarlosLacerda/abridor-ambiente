import os
import subprocess
import webbrowser
import json
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from datetime import datetime

# ==================== CONFIGURAÇÕES ====================
def find_vscode_path():
    """Tenta encontrar o caminho do VS Code automaticamente"""
    possible_paths = [
        "code",  # Se estiver no PATH
        r"C:\Program Files\Microsoft VS Code\Code.exe",
        r"C:\Program Files (x86)\Microsoft VS Code\Code.exe",
        str(Path.home() / "AppData" / "Local" / "Programs" / "Microsoft VS Code" / "Code.exe"),
    ]
    
    # Testar se 'code' funciona
    try:
        subprocess.run(["code", "--version"], capture_output=True, timeout=2)
        return "code"
    except:
        pass
    
    # Procurar nos caminhos comuns
    for path in possible_paths[1:]:
        if Path(path).exists():
            return path
    
    return None

CONFIG = {
    "vscode_path": find_vscode_path(),
    "base_projects_dir": str(Path.home() / "Documents" / "Projetos"),
    "browser": "default",
}

# ==================== TEMPLATES DE LINGUAGENS ====================
LANGUAGES = {
    "JavaScript": {
        "color": "#f7df1e",
        "icon": "🟨",
        "files": {
            "index.html": '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Projeto JavaScript</title>
</head>
<body>
    <h1>Olá, JavaScript!</h1>
    <script src="script.js"></script>
</body>
</html>''',
            "script.js": '''// Projeto JavaScript
console.log("Ambiente iniciado!");

// Seu código aqui
''',
            "style.css": '''/* Estilos do projeto */
body {
    font-family: Arial, sans-serif;
    margin: 20px;
    background: #f0f0f0;
}

h1 {
    color: #333;
}'''
        },
        "urls": [
            "https://developer.mozilla.org/pt-BR/docs/Web/JavaScript",
            "https://www.npmjs.com/",
            "https://github.com"
        ],
        "terminal_commands": ["node --version", "npm --version"],
        "extensions": ["ms-vscode.vscode-typescript-next"]
    },
    
    "Python": {
        "color": "#3776ab",
        "icon": "🐍",
        "files": {
            "main.py": '''# Projeto Python
def main():
    print("Ambiente Python iniciado!")
    
    # Seu código aqui

if __name__ == "__main__":
    main()
''',
            "requirements.txt": '''# Dependências do projeto
# requests==2.31.0
# pandas==2.0.0
''',
            ".gitignore": '''# Python
__pycache__/
*.py[cod]
*$py.class
venv/
env/
.env
*.so
.Python
'''
        },
        "urls": [
            "https://docs.python.org/pt-br/3/",
            "https://pypi.org/",
            "https://stackoverflow.com/questions/tagged/python"
        ],
        "terminal_commands": ["python --version", "pip --version"],
        "venv": True,
        "extensions": ["ms-python.python"]
    },
    
    "Java": {
        "color": "#007396",
        "icon": "☕",
        "files": {
            "src/Main.java": '''public class Main {
    public static void main(String[] args) {
        System.out.println("Ambiente Java iniciado!");
        
        // Seu código aqui
    }
}
''',
            ".gitignore": '''# Java
*.class
*.jar
*.war
*.ear
target/
.idea/
*.iml
'''
        },
        "urls": [
            "https://docs.oracle.com/en/java/",
            "https://www.geeksforgeeks.org/java/",
            "https://stackoverflow.com/questions/tagged/java"
        ],
        "terminal_commands": ["java --version", "javac --version"],
        "extensions": ["vscjava.vscode-java-pack"]
    },
    
    "C/C++": {
        "color": "#00599c",
        "icon": "⚙️",
        "files": {
            "main.cpp": '''#include <iostream>
using namespace std;

int main() {
    cout << "Ambiente C++ iniciado!" << endl;
    
    // Seu código aqui
    
    return 0;
}
''',
            "Makefile": '''CC = g++
CFLAGS = -Wall -std=c++17
TARGET = main

all: $(TARGET)

$(TARGET): main.cpp
\t$(CC) $(CFLAGS) -o $(TARGET) main.cpp

clean:
\trm -f $(TARGET) *.o

run: $(TARGET)
\t./$(TARGET)
'''
        },
        "urls": [
            "https://en.cppreference.com/",
            "https://www.geeksforgeeks.org/c-plus-plus/",
            "https://stackoverflow.com/questions/tagged/c++"
        ],
        "terminal_commands": ["g++ --version", "gcc --version"],
        "extensions": ["ms-vscode.cpptools"]
    },
    
    "HTML/CSS/JS": {
        "color": "#e34c26",
        "icon": "🌐",
        "files": {
            "index.html": '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Meu Projeto Web</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>Bem-vindo ao Projeto Web</h1>
    </header>
    <main>
        <p>Comece a criar algo incrível!</p>
    </main>
    <script src="script.js"></script>
</body>
</html>''',
            "style.css": '''* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #333;
}

header {
    background: rgba(255, 255, 255, 0.95);
    padding: 2rem;
    text-align: center;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

main {
    max-width: 1200px;
    margin: 2rem auto;
    padding: 2rem;
    background: white;
    border-radius: 10px;
}''',
            "script.js": '''// Projeto Web
console.log('Site carregado!');

// Adicione interatividade aqui
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM pronto!');
});'''
        },
        "urls": [
            "https://developer.mozilla.org/pt-BR/",
            "https://www.w3schools.com/",
            "https://css-tricks.com/"
        ],
        "terminal_commands": [],
        "live_server": True
    }
}

# ==================== FUNÇÕES AUXILIARES ====================

def create_project_structure(language, project_name, base_dir):
    """Cria a estrutura de pastas e arquivos do projeto"""
    project_path = Path(base_dir) / project_name
    
    try:
        project_path.mkdir(parents=True, exist_ok=True)
        
        # Criar arquivos do template
        for file_path, content in LANGUAGES[language]["files"].items():
            full_path = project_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content, encoding='utf-8')
        
        # Criar README
        readme = f"""# {project_name}

**Linguagem:** {language}
**Criado em:** {datetime.now().strftime('%d/%m/%Y às %H:%M')}

## Descrição
Projeto criado automaticamente pelo Abridor de Ambiente de Estudo.

## Como usar
[Adicione instruções aqui]

## Tecnologias
- {language}

## Autor
Seu nome aqui
"""
        (project_path / "README.md").write_text(readme, encoding='utf-8')
        
        # Inicializar Git
        subprocess.run(["git", "init"], cwd=project_path, shell=True, capture_output=True)
        
        return str(project_path)
    except Exception as e:
        raise Exception(f"Erro ao criar projeto: {e}")

def open_vscode(project_path, language):
    """Abre o VS Code no projeto"""
    try:
        vscode_path = CONFIG["vscode_path"]
        
        # Se não encontrou o VS Code, mostrar erro amigável
        if not vscode_path:
            raise Exception("VS Code não encontrado!\n\nPor favor:\n1. Instale o VS Code em: https://code.visualstudio.com/\n2. Ou edite o código e defina o caminho manualmente")
        
        # Tentar abrir
        subprocess.Popen([vscode_path, project_path], stderr=subprocess.PIPE)
        
        # Sugerir extensões (opcional)
        if "extensions" in LANGUAGES[language]:
            for ext in LANGUAGES[language]["extensions"]:
                subprocess.Popen([vscode_path, "--install-extension", ext], 
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        raise Exception(f"VS Code não encontrado em: {vscode_path}\n\nInstale em: https://code.visualstudio.com/")
    except Exception as e:
        raise Exception(f"Erro ao abrir VS Code: {e}")

def open_browser_tabs(urls):
    """Abre as URLs no navegador"""
    try:
        for url in urls:
            webbrowser.open(url)
    except Exception as e:
        raise Exception(f"Erro ao abrir navegador: {e}")

def setup_python_venv(project_path):
    """Cria ambiente virtual Python"""
    try:
        venv_path = Path(project_path) / "venv"
        subprocess.run(["python", "-m", "venv", "venv"], cwd=project_path, shell=True, check=True)
        return str(venv_path)
    except Exception as e:
        raise Exception(f"Erro ao criar venv: {e}")

def open_terminal(project_path, language):
    """Abre o terminal no diretório do projeto"""
    try:
        commands = LANGUAGES[language].get("terminal_commands", [])
        
        if os.name == 'nt':  # Windows
            # Criar script batch temporário
            batch_script = f"""@echo off
cd /d "{project_path}"
echo ========================================
echo Ambiente {language} iniciado!
echo ========================================
echo.
"""
            if LANGUAGES[language].get("venv"):
                batch_script += "call venv\\Scripts\\activate.bat\necho Ambiente virtual ativado!\necho.\n"
            
            for cmd in commands:
                batch_script += f"{cmd}\n"
            
            batch_script += "echo.\necho Pronto para programar!\ncmd /k"
            
            batch_path = Path(project_path) / "start_env.bat"
            batch_path.write_text(batch_script, encoding='utf-8')
            
            subprocess.Popen(["cmd", "/c", "start", "cmd", "/k", str(batch_path)], shell=True)
        else:  # Linux/Mac
            subprocess.Popen(["gnome-terminal", "--working-directory", project_path])
    except Exception as e:
        print(f"Aviso: Não foi possível abrir terminal: {e}")

# ==================== INTERFACE GRÁFICA ====================

class DevEnvironmentLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 Abridor de Ambiente de Estudo")
        
        # Calcular tamanho ideal da janela (80% da tela)
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = min(900, int(screen_width * 0.8))
        window_height = min(650, int(screen_height * 0.85))
        
        # Centralizar na tela
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.resizable(True, True)  # Permitir redimensionar
        self.root.minsize(750, 600)  # Tamanho mínimo
        self.root.configure(bg="#f5f5f5")
        
        # Variáveis
        self.selected_language = tk.StringVar()
        self.project_name = tk.StringVar(value=f"projeto_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        self.base_dir = tk.StringVar(value=CONFIG["base_projects_dir"])
        self.open_browser = tk.BooleanVar(value=True)
        self.open_terminal = tk.BooleanVar(value=True)
        self.init_git = tk.BooleanVar(value=True)
        
        self.setup_ui()
    
    def setup_ui(self):
        # Verificar se VS Code foi encontrado
        if not CONFIG["vscode_path"]:
            messagebox.showwarning("⚠️ VS Code não encontrado",
                                 "VS Code não foi encontrado automaticamente.\n\n"
                                 "O programa ainda funcionará, mas você precisará:\n"
                                 "• Instalar o VS Code: https://code.visualstudio.com/\n"
                                 "• Ou abrir a pasta do projeto manualmente\n\n"
                                 "Pressione OK para continuar...")
        
        # Header - Mais compacto
        header = tk.Frame(self.root, bg="#667eea", height=70)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title = tk.Label(header, text="🚀 Abridor de Ambiente", 
                        font=("Arial", 22, "bold"), bg="#667eea", fg="white")
        title.pack(expand=True)
        
        # Container principal SEM scroll - tudo visível
        main_frame = tk.Frame(self.root, bg="#f5f5f5")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Seleção de linguagem - Mais compacta
        lang_label = tk.Label(main_frame, text="Escolha a linguagem:", 
                             font=("Arial", 12, "bold"), bg="#f5f5f5")
        lang_label.pack(anchor=tk.W, pady=(0, 8))
        
        # Botões de linguagem - Layout em grid 3x2
        lang_frame = tk.Frame(main_frame, bg="#f5f5f5")
        lang_frame.pack(fill=tk.X, pady=(0, 12))
        
        for idx, (lang, config) in enumerate(LANGUAGES.items()):
            btn = tk.Button(lang_frame, text=f"{config['icon']} {lang}",
                          font=("Arial", 10, "bold"), width=13, height=1,
                          bg=config['color'], fg="white",
                          activebackground=config['color'],
                          activeforeground="white",
                          command=lambda l=lang: self.select_language(l),
                          cursor="hand2", relief=tk.RAISED, bd=2)
            btn.grid(row=idx//3, column=idx%3, padx=4, pady=4, sticky=tk.NSEW, ipady=8)
        
        # Configurar grid
        for i in range(3):
            lang_frame.columnconfigure(i, weight=1)
        
        # Nome do projeto - Mais compacto
        name_label = tk.Label(main_frame, text="Nome do projeto:", 
                             font=("Arial", 10, "bold"), bg="#f5f5f5")
        name_label.pack(anchor=tk.W, pady=(8, 3))
        
        name_entry = tk.Entry(main_frame, textvariable=self.project_name, 
                             font=("Arial", 10), width=50)
        name_entry.pack(fill=tk.X, pady=(0, 10), ipady=3)
        
        # Diretório base - Mais compacto
        dir_label = tk.Label(main_frame, text="Pasta de projetos:", 
                            font=("Arial", 10, "bold"), bg="#f5f5f5")
        dir_label.pack(anchor=tk.W, pady=(3, 3))
        
        dir_frame = tk.Frame(main_frame, bg="#f5f5f5")
        dir_frame.pack(fill=tk.X, pady=(0, 10))
        
        dir_entry = tk.Entry(dir_frame, textvariable=self.base_dir, 
                            font=("Arial", 9), width=45)
        dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=2)
        
        dir_btn = tk.Button(dir_frame, text="📁", 
                           font=("Arial", 10),
                           command=self.choose_directory, width=3)
        dir_btn.pack(side=tk.LEFT, padx=(4, 0))
        
        # Opções - Mais compactas
        options_frame = tk.LabelFrame(main_frame, text="  Opções  ", 
                                     font=("Arial", 10, "bold"), bg="#f5f5f5",
                                     relief=tk.GROOVE, bd=2)
        options_frame.pack(fill=tk.X, pady=(8, 12))
        
        tk.Checkbutton(options_frame, text="Abrir navegador com documentação", 
                      variable=self.open_browser, bg="#f5f5f5", 
                      font=("Arial", 9)).pack(anchor=tk.W, padx=12, pady=4)
        
        tk.Checkbutton(options_frame, text="Abrir terminal configurado", 
                      variable=self.open_terminal, bg="#f5f5f5", 
                      font=("Arial", 9)).pack(anchor=tk.W, padx=12, pady=4)
        
        tk.Checkbutton(options_frame, text="Inicializar Git", 
                      variable=self.init_git, bg="#f5f5f5", 
                      font=("Arial", 9)).pack(anchor=tk.W, padx=12, pady=4)
        
        # BOTÃO DE AÇÃO - GRANDE E VISÍVEL
        btn_frame = tk.Frame(main_frame, bg="#f5f5f5")
        btn_frame.pack(fill=tk.X, pady=(12, 8))
        
        self.launch_btn = tk.Button(btn_frame, 
                                    text="🚀 INICIAR AMBIENTE", 
                                    font=("Arial", 16, "bold"), 
                                    bg="#4CAF50", 
                                    fg="white",
                                    activebackground="#45a049",
                                    activeforeground="white",
                                    command=self.launch_environment,
                                    cursor="hand2", 
                                    state=tk.DISABLED,
                                    relief=tk.RAISED, 
                                    bd=3,
                                    height=2)
        self.launch_btn.pack(fill=tk.BOTH, expand=True, ipady=8)
        
        # Status - Mais compacto
        self.status_label = tk.Label(main_frame, 
                                     text="👆 Selecione uma linguagem para começar", 
                                     font=("Arial", 9, "italic"), 
                                     bg="#f5f5f5", 
                                     fg="#666")
        self.status_label.pack(pady=(8, 0))
    
    def select_language(self, language):
        self.selected_language.set(language)
        self.launch_btn.config(state=tk.NORMAL, bg="#4CAF50")
        self.status_label.config(text=f"✓ {language} selecionado - Pronto para iniciar!", fg="#4CAF50")
    
    def choose_directory(self):
        directory = filedialog.askdirectory(initialdir=self.base_dir.get())
        if directory:
            self.base_dir.set(directory)
    
    def launch_environment(self):
        if not self.selected_language.get():
            messagebox.showerror("Erro", "Selecione uma linguagem!")
            return
        
        if not self.project_name.get():
            messagebox.showerror("Erro", "Digite um nome para o projeto!")
            return
        
        self.launch_btn.config(state=tk.DISABLED, text="⏳ INICIANDO...", bg="#FF9800")
        self.root.update()
        
        try:
            language = self.selected_language.get()
            project_name = self.project_name.get()
            base_dir = self.base_dir.get()
            
            # Criar projeto
            self.status_label.config(text="📁 Criando estrutura do projeto...", fg="#2196F3")
            self.root.update()
            project_path = create_project_structure(language, project_name, base_dir)
            
            # Ambiente virtual Python
            if LANGUAGES[language].get("venv"):
                self.status_label.config(text="🐍 Criando ambiente virtual Python...", fg="#2196F3")
                self.root.update()
                setup_python_venv(project_path)
            
            # Abrir VS Code
            self.status_label.config(text="💻 Abrindo VS Code...", fg="#2196F3")
            self.root.update()
            open_vscode(project_path, language)
            
            # Abrir navegador
            if self.open_browser.get():
                self.status_label.config(text="🌐 Abrindo documentação...", fg="#2196F3")
                self.root.update()
                open_browser_tabs(LANGUAGES[language]["urls"])
            
            # Abrir terminal
            if self.open_terminal.get():
                self.status_label.config(text="⌨️ Abrindo terminal...", fg="#2196F3")
                self.root.update()
                open_terminal(project_path, language)
            
            messagebox.showinfo("✅ Sucesso!", 
                              f"Ambiente {language} iniciado com sucesso!\n\n📂 Projeto criado em:\n{project_path}")
            
            self.launch_btn.config(state=tk.NORMAL, text="🚀 INICIAR AMBIENTE", bg="#4CAF50")
            self.status_label.config(text=f"✅ Ambiente {language} pronto para usar!", fg="#4CAF50")
            
        except Exception as e:
            messagebox.showerror("❌ Erro", f"Erro ao iniciar ambiente:\n\n{str(e)}")
            self.launch_btn.config(state=tk.NORMAL, text="🚀 INICIAR AMBIENTE", bg="#4CAF50")
            self.status_label.config(text="❌ Erro ao iniciar ambiente", fg="red")

# ==================== EXECUÇÃO ====================

if __name__ == "__main__":
    root = tk.Tk()
    app = DevEnvironmentLauncher(root)
    root.mainloop()