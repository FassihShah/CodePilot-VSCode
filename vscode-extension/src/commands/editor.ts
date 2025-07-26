import * as vscode from "vscode";



export function createCodeEditorCommand(EDITOR_API: string)
{
    let editCodeCmd = vscode.commands.registerCommand("codepilot.editCode", async () => 
    {
    const editor = vscode.window.activeTextEditor;
    if (!editor) 
    {
        vscode.window.showErrorMessage("No active editor.");
        return;
    }

    const fullCode = editor.document.getText();
    const selectedText = editor.document.getText(editor.selection);

    if (!selectedText) 
    {
        vscode.window.showWarningMessage("Please select the code you want to edit.");
        return;
    }

    const instruction = await vscode.window.showInputBox({
        prompt: "Describe the edit you want (e.g. fix bug, rename variable)",
    });

    if (!instruction) 
    {
        vscode.window.showWarningMessage("Edit instruction is required.");
        return;
    }

    vscode.window.withProgress(
    {
        location: vscode.ProgressLocation.Notification,
        title: "Editing code with CodePilot...",
        cancellable: false,
    },
    async () => 
    {
        try 
        {
            const res = await fetch(EDITOR_API, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    full_code: fullCode,
                    selected_code: selectedText,
                    instruction: instruction
                })
            });

            const result = await res.json() as { updated_code: string, full_updated_code: string, explanation?: string };

            const updatedSelection = result.updated_code;
            const updatedFullFile = result.full_updated_code;
            const explanation = result.explanation || "No explanation provided.";

            const doc = await vscode.workspace.openTextDocument({ content: explanation, language: "markdown" });
            vscode.window.showTextDocument(doc, vscode.ViewColumn.Beside);

            // Apply selected code change
            await editor.edit(editBuilder => {
                editBuilder.replace(editor.selection, updatedSelection);
            });

            // Ask if user also wants to update full file
            const applyFullFile = await vscode.window.showQuickPick(["Yes", "No"], {
                placeHolder: "Do you want to replace the entire file with updated version?",
            });

            if (applyFullFile === "Yes") 
            {
                const fullRange = new vscode.Range(
                    editor.document.positionAt(0),
                    editor.document.positionAt(fullCode.length)
                );

                await editor.edit(editBuilder => {
                    editBuilder.replace(fullRange, updatedFullFile);
                });

                vscode.window.showInformationMessage("Full file updated with AI edits.");
            } 
            else 
            {
                vscode.window.showInformationMessage("Selected code updated successfully.");
            }
        } 
        catch (error: any) 
        {
            console.error(error);
            vscode.window.showErrorMessage("Code editing failed.");
        }
    });
});

return editCodeCmd;
}