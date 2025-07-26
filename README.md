# 👽 CodePilot – AI Coding Agent for VS Code

**CodePilot** is a powerful, agent-based AI extension for VS Code that enhances your productivity by assisting with code editing, explanation, generation, and intelligent codebase conversations—all directly from your editor.

## ✨ Features

CodePilot provides four main AI-powered commands that you can access via **Right Click** on your code or through the **Command Palette** (`Ctrl+Shift+P`):

| Command | Description |
|---------|-------------|
| 🛠️ **Generate Boilerplate** | Automatically generates starter code files with boilerplate based on your specified project type |
| ✍️ **Edit Code** | Select any part of your code and ask CodePilot to edit or refactor it according to your instructions |
| 📘 **Explain Code** | Get clear and concise explanations of what selected code does |
| 💬 **Chat With Codebase** | Ask natural language questions about your entire codebase using RAG (Retrieval-Augmented Generation) |

All features are powered by specialized AI agents built with LangGraph workflows.

## Demo Video


https://github.com/user-attachments/assets/4eb5eef4-7464-4b5d-94c0-3b9f59dc0329


## 🗂️ Project Structure

```
CodePilot-VSCode/
├── 📁 backend/                    # FastAPI backend
│   ├── 📁 agents/                 # AI agent implementations
│   │   ├── 🐍 boilerplate_agent.py    # Template generation agent
│   │   ├── 🐍 chat_agent.py            # RAG-powered chat agent
│   │   ├── 🐍 code_editor_agent.py     # Code editing agent
│   │   ├── 🐍 code_explainer_agent.py  # Code explanation agent
│   │   └── 🐍 embed_saver_agent.py     # Vector embedding agent
│   └── 🐍 main.py                      # FastAPI application entry
├── 📁 vscode-extension/           # Extension source code
│   ├── 📁 src/
│   │   └── 📁 commands/           # VS Code command implementations
│   │       ├── 📄 boilerplates.ts     # Boilerplate generation
│   │       ├── 📄 chat.ts             # Codebase chat functionality  
│   │       ├── 📄 editor.ts           # Code editing command
│   │       └── 📄 explainer.ts        # Code explanation command
│   ├── 📄 extension.ts            # Main extension entry point
│   ├── 🎨 icon.png                # Extension icon
│   ├── 📄 package.json            # Extension manifest
│   ├── 📄 package-lock.json       # Dependency lock file
│   ├── 📄 README.md               # Extension documentation
├── 📄 LICENSE                     # MIT License
├── 📄 README.md                   # This File
└── 📄 requirements.txt            # Python dependencies
```


## 🧠 Architecture - Agents and Backend

CodePilot uses a sophisticated multi-agent architecture where each command is handled by a specialized **LangGraph agent**:

| Agent Type | Functionality |
|------------|---------------|
| **Code Editor Agent** | Intelligently edits and refactors selected code blocks |
| **Code Explainer Agent** | Summarizes and explains code in human-readable format |
| **Chat Agent** | Enables conversations with your entire codebase using Retrieval-Augmented Generation (RAG) for contextual understanding |
| **Boilerplate Generator Agent** | Creates project-specific boilerplate files and templates |

### Backend Technology Stack
- **FastAPI** - High-performance web framework for the API backend
- **LangGraph** - Agent orchestration and workflow management
- **Gemini AI** - Large language model for code understanding and generation
- **RAG System** - Retrieval-Augmented Generation for codebase context in chat functionality
- **Railway** - Cloud deployment platform (for demo environment)

The Chat Agent specifically uses RAG to provide contextual responses by:
1. Indexing your codebase into a vector database
2. Retrieving relevant code snippets based on your questions
3. Using the retrieved context to provide accurate, project-specific answers


## 🛠️ Installation & Usage

### 🔌 Install from VS Code Marketplace

1. Open **VS Code**
2. Navigate to **Extensions** tab
3. Search for: `CodePilot-AI`
4. Click **Install** or [Install directly from Marketplace](https://marketplace.visualstudio.com/items?itemName=Fassih.codepilot-ai)
5. Reload VS Code

 ⚠️ Note: The demo backend is temporarily deployed for testing purposes and may not always be available.

### 🚀 Using CodePilot

Once installed, you can access CodePilot commands through:

- **Right-click context menu** on any code selection
- **Command Palette** (`Ctrl+Shift+P`) - search for `CodePilot: <Command Name>`

#### Example Usage:

1. **Edit Code**: Select a function, right-click → "CodePilot: Edit Code" → Describe your changes
2. **Explain Code**: Highlight complex code → "CodePilot: Explain Code" → Get instant explanation
3. **Chat With Codebase**: Right click and start Chat → Ask "Where is user authentication handled?"
4. **Generate Boilerplate**: Create new files with boilerplates by telling your need

## 🧪 Local Development Setup

If you want to run the backend locally or contribute to development:

### Prerequisites
- Python 3.8+
- Node.js (for VS Code extension development)
- Git

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/FassihShah/CodePilot-VSCode.git
   cd CodePilot-VSCode
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

4. **Start the FastAPI server**
   ```bash
   uvicorn backend.main:app --reload
   ```
   
   The server will start at `http://localhost:8000`

### Extension Configuration for Local Backend

To use your local backend instead of the production server:

1. Open the extension source code
2. In `extension.ts`, update the API endpoints:

```typescript
const EDITOR_API = "http://localhost:8000/edit-code/";
const EXPLAINER_API = "http://localhost:8000/explain-code/";
const BOILERPLATE_API = "http://localhost:8000/generate-boilerplate/";
const CHAT_API = "http://localhost:8000/chat-with-code/";
const EMBED_API = "http://localhost:8000/embed-and-store/";
```

## 🌟 Why Choose CodePilot?

- **Open Source Foundation**: Built with LangGraph, Gemini, and FastAPI
- **Fully Customizable**: Extend and modify agents for your specific needs
- **Contextual Intelligence**: RAG-powered chat understands your entire codebase
- **Seamless Integration**: Works directly within VS Code workflow
- **Privacy-Focused**: Run locally or use your own deployment

## ⚠️ Known Limitations

- **Demo Backend**: The production backend is hosted temporarily and may experience downtime
- **Output Stability**: Some commands may occasionally produce inconsistent results
- **Rate Limits**: Demo deployment may have usage restrictions

## Contributing

Pull requests are welcome! If you want to contribute new commands, backend enhancements, or fix bugs, feel free to fork the repo.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
