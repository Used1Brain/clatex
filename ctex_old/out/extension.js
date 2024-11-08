"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.activate = activate;
const config_1 = __importDefault(require("./config"));
const vscode = __importStar(require("vscode"));
const tex2svg_1 = require("./tex2svg");
function activate(context) {
    const matchRegEx = new RegExp(config_1.default.matchReg, config_1.default.matchRegFlags);
    const wrongRegEx = new RegExp(config_1.default.wrongReg, config_1.default.wrongRegFlags);
    const tex2Svg = new tex2svg_1.Tex2Svg(config_1.default.cacheSize);
    let timeout = undefined;
    let activeEditor = vscode.window.activeTextEditor;
    async function updateDecorations() {
        if (!activeEditor) {
            return;
        }
        const text = activeEditor.document.getText();
        const wrongUsage = [];
        const correctUsage = [];
        let match;
        while ((match = matchRegEx.exec(text))) {
            const start = match.index + config_1.default.forwardSkip;
            const end = match.index + match[0].length - config_1.default.backwardSkip;
            const startPos = activeEditor.document.positionAt(start);
            const endPos = activeEditor.document.positionAt(end);
            const range = new vscode.Range(startPos, endPos);
            const latex = match[0].substring(config_1.default.forwardSkip, match[0].length - config_1.default.backwardSkip);
            // console.log(`Match: ${match[0]}, match index: ${match.index}, match length: ${match[0].length}, processed: ${latex}`);
            const hoverUri = await tex2Svg.render(latex);
            const decoration = { range: range, hoverMessage: hoverUri.text };
            if (hoverUri.error || wrongRegEx.test(match[0])) {
                wrongUsage.push(decoration);
            }
            else {
                correctUsage.push(decoration);
            }
        }
        activeEditor.setDecorations(config_1.default.wrongDecorationType, wrongUsage);
        activeEditor.setDecorations(config_1.default.correctDecorationType, correctUsage);
    }
    function triggerUpdateDecorations() {
        if (timeout) {
            clearTimeout(timeout);
            timeout = undefined;
        }
        timeout = setTimeout(updateDecorations, config_1.default.updateInterval);
    }
    if (activeEditor) {
        triggerUpdateDecorations();
    }
    vscode.window.onDidChangeActiveTextEditor(editor => {
        activeEditor = editor;
        if (editor) {
            triggerUpdateDecorations();
        }
    }, null, context.subscriptions);
    vscode.workspace.onDidChangeTextDocument(event => {
        if (activeEditor && event.document === activeEditor.document) {
            triggerUpdateDecorations();
        }
    }, null, context.subscriptions);
}
//# sourceMappingURL=extension.js.map