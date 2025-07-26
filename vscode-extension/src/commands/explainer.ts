import * as vscode from "vscode";



export function createExplainerCommand(EXPLAINER_API: string)
{
    const explainCmd = vscode.commands.registerCommand("codepilot.explainCode", async () =>
    {
        const editor = vscode.window.activeTextEditor;

        if (!editor)
        {
            vscode.window.showErrorMessage("No active editor");
            return;
        }

        const selectedCode = editor.document.getText(editor.selection);
        const fullCode = editor.document.getText();

        if (!selectedCode.trim())
        {
            vscode.window.showErrorMessage("Please select some code to explain.");
            return;
        }

        // Initial loading message
        vscode.window.showInformationMessage("⏳ Analyzing selected code...");

        try
        {
            const response = await fetch(EXPLAINER_API, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    full_code: fullCode,
                    selected_code: selectedCode
                })
            });

            if (!response.ok)
            {
                throw new Error(`Server responded with ${response.status}`);
            }

            const data = await response.json() as { explanation: string };
            const explanation = data.explanation || "No explanation received.";

            vscode.window.showInformationMessage("Code explanation ready!");

            const doc = await vscode.workspace.openTextDocument({
                content: explanation,
                language: "markdown"
            });
            vscode.window.showTextDocument(doc, vscode.ViewColumn.Beside);
        }
        catch (error: any)
        {
            vscode.window.showErrorMessage(`Failed to explain code: ${error.message}`);
        }
    });

    return explainCmd;
}