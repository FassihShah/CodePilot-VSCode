import * as vscode from "vscode";

import { createBoilerPlateCommand } from "./commands/boilerplate";
import { createCodeEditorCommand } from "./commands/editor";
import { createExplainerCommand } from "./commands/explainer";
import { createChatCommand } from "./commands/chat";

const BOILERPLATE_API = "https://codepilot-production.up.railway.app/generate-boilerplate/";
const EMBEDDER_API = "https://codepilot-production.up.railway.app/embed-and-store/";
const CHAT_API = "https://codepilot-production.up.railway.app/chat-with-code/";
const EDITOR_API = "https://codepilot-production.up.railway.app/edit-code/";
const EXPLAINER_API = "https://codepilot-production.up.railway.app/explain-code/";


export function activate(context: vscode.ExtensionContext) 
{
    context.subscriptions.push(createBoilerPlateCommand(BOILERPLATE_API));
    context.subscriptions.push(createCodeEditorCommand(EDITOR_API));
    context.subscriptions.push(createExplainerCommand(EXPLAINER_API));
    context.subscriptions.push(createChatCommand(context,EMBEDDER_API,CHAT_API));
};