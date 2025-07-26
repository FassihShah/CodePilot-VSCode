import * as vscode from "vscode";
import * as path from "path";
import * as fs from "fs";




export function createBoilerPlateCommand(BOILERPLATE_API: string)
{

    let boilerplateCmd = vscode.commands.registerCommand("codepilot.generateBoilerplate", async () => 
    {
        const userInput = await vscode.window.showInputBox({
            prompt: "Enter a short prompt (e.g. 'fastapi crud')",
        });

        if (!userInput) 
        {
            vscode.window.showWarningMessage("Prompt is required.");
            return;
        }

        vscode.window.withProgress(
        {
            location: vscode.ProgressLocation.Notification,
            title: "Generating boilerplate...",
            cancellable: false,
        },
        async () => 
        {
            try 
            {
                const response = await fetch(BOILERPLATE_API, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ prompt: userInput }),
                });

                const result = await response.json() as { files: Record<string, string> };
                const files = result.files;

                if (!files || Object.keys(files).length === 0) 
                {
                    vscode.window.showErrorMessage("No files generated.");
                    return;
                }

                const workspaceFolders = vscode.workspace.workspaceFolders;
                if (!workspaceFolders) 
                {
                    vscode.window.showErrorMessage("No workspace folder open.");
                    return;
                }

                const workspacePath = workspaceFolders[0].uri.fsPath;

                for (const [filePath, fileContent] of Object.entries(files)) 
                {
                    const fullPath = path.join(workspacePath, filePath);
                    const dir = path.dirname(fullPath);
                    fs.mkdirSync(dir, { recursive: true });
                    fs.writeFileSync(fullPath, fileContent, "utf-8");
                }

                vscode.window.showInformationMessage("Boilerplate generated successfully.");
            } 
            catch (error: any) 
            {
                console.error(error);
                vscode.window.showErrorMessage("Failed to generate boilerplate.");
            }
        });
    });

    return boilerplateCmd;
}