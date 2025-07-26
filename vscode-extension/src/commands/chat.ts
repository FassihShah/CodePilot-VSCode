import * as vscode from "vscode";
import * as path from "path";
import * as fs from "fs";



export function createChatCommand(context: vscode.ExtensionContext, EMBEDDER_API: string, CHAT_API: string)
{
    let chatCommand = vscode.commands.registerCommand("codepilot.chatWithCode", async () => 
    {
        const workspaceFolders = vscode.workspace.workspaceFolders;
        if (!workspaceFolders) 
        {
            vscode.window.showErrorMessage("Open a folder to start code-aware chat.");
            return;
        }

        const workspacePath = workspaceFolders[0].uri.fsPath;

        vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: "Embedding codebase for chat...",
            cancellable: false,
        }, async () => 
        {
            try 
            {
                const files = await collectFiles(workspacePath);
                const embedRes = await fetch(EMBEDDER_API, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ files: files })
                });

                if (!embedRes.ok) {
                    vscode.window.showErrorMessage("Embedding failed with status: " + embedRes.status);
                    return;
                }

                vscode.window.showInformationMessage("Codebase embedded. Starting chat...");

                const panel = vscode.window.createWebviewPanel(
                    "codepilotChat",
                    "CodePilot Chat",
                    vscode.ViewColumn.Beside,
                    {
                        enableScripts: true
                    }
                );

                panel.webview.html = getWebviewHTML(panel.webview, context.extensionUri);

                panel.webview.onDidReceiveMessage(async message => 
                {
                    if (message.type === "chat") 
                    {
                        try 
                        {
                            const res = await fetch(CHAT_API, {
                                method: "POST",
                                headers: { "Content-Type": "application/json" },
                                body: JSON.stringify({ query: message.query })
                            });

                            const data = await res.json() as {"answer":string};
                            panel.webview.postMessage({ type: "response", answer: data.answer });
                        } 
                        catch (err) 
                        {
                            panel.webview.postMessage({ type: "response", answer: "❌ Failed to get response." });
                        }
                    }
                });
            } 
            catch (error: any) 
            {
                vscode.window.showErrorMessage("Failed to embed codebase or start chat.");
            }
        });
    });

    return chatCommand;
}



async function collectFiles(dir: string): Promise<Record<string, string>> 
{
    const fileMap: Record<string, string> = {};
    const allowedExt = ['.py', '.ts', '.js', '.java', '.cpp', '.cs', '.swift', '.kt', '.kts', '.dart', '.c', '.razor', '.cshtml'];

    function walk(currentPath: string) 
    {
        const entries = fs.readdirSync(currentPath, { withFileTypes: true });
        for (const entry of entries) 
        {
            const fullPath = path.join(currentPath, entry.name);
            if (entry.isDirectory()) 
            {
                walk(fullPath);
            } 
            else if (allowedExt.includes(path.extname(entry.name))) 
            {
                try 
                {
                    const content = fs.readFileSync(fullPath, "utf-8");
                    fileMap[path.relative(dir, fullPath)] = content;
                } 
                catch { }
            }
        }
    }

    walk(dir);
    return fileMap;
}



function getWebviewHTML(webview: vscode.Webview, extensionUri: vscode.Uri): string 
{
    return `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>CodePilot Chat</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #1e1e1e;
            color: #e0e0e0;
            padding: 16px;
        }

        textarea {
            width: 100%;
            height: 60px;
            background: #2e2d2d;
            color: #ffffff;
            border: 1px solid #555;
            border-radius: 6px;
            padding: 10px;
            font-size: 14px;
            resize: none;
        }

        button {
            margin-top: 8px;
            background-color: #007acc;
            color: white;
            border: none;
            padding: 10px 16px;
            font-size: 14px;
            border-radius: 4px;
            cursor: pointer;
        }

        button:hover {
            background-color: #005f99;
        }

        #chat {
            white-space: pre-wrap;
            margin-top: 16px;
            background: #252526;
            padding: 16px;
            border-radius: 8px;
            border: 1px solid #3c3c3c;
            max-height: 400px;
            overflow-y: auto;
            line-height: 1.6;
        }

        h2 {
            color: #ffffff;
        }
    </style>
</head>
<body>
    <h2>👽 Chat with CodePilot</h2>
    <textarea id="input" placeholder="Ask something about the code..."></textarea><br>
    <button onclick="send()">Send</button>
    <div id="chat"></div>

    <script>
        const vscode = acquireVsCodeApi();

        function send() {
            const input = document.getElementById('input');
            const message = input.value;
            if (!message) return;

            document.getElementById('chat').innerHTML += "<br><b>You:</b> " + message;
            vscode.postMessage({ type: "chat", query: message });
            input.value = "";
        }

        window.addEventListener('message', event => {
            const msg = event.data;
            if (msg.type === "response") {
                document.getElementById('chat').innerHTML += "<br><br>👽 <b>CodePilot:</b> " + msg.answer + "<br><br>";
            }
        });
    </script>
</body>
</html>
`;

}