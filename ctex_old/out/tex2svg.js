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
exports.Tex2Svg = void 0;
const config_1 = __importDefault(require("./config"));
const vscode = __importStar(require("vscode"));
const mathjax_full_1 = __importDefault(require("mathjax-full"));
const parser_1 = __importDefault(require("datauri/parser"));
const cache_1 = require("./cache");
class Tex2Svg {
    constructor(cacheLimit = 1024, color = "white") {
        this.svgTextColor = config_1.default.svgTextColor || color;
        this.svgBackgroundColor = config_1.default.svgBackgroundColor || "auto";
        this.cache = new cache_1.LRUCache(cacheLimit);
        this.mathJax = mathjax_full_1.default;
        this.mathJax.start();
        this.parser = new parser_1.default();
    }
    async render(tex) {
        const found = this.cache.get(tex);
        if (found) {
            return { text: found, error: false };
        }
        let data;
        try {
            data = await this.mathJax.typeset({
                math: tex,
                format: config_1.default.format, // [ "TeX" | "inline-TeX" | "MathML" ]
                svg: true // [ svg:true | html:true ]
            });
        }
        catch (err) {
            // vscode.window.showWarningMessage(err);
            return { text: err, error: true }; // return the string
        }
        let svg = data?.svg;
        if (this.svgTextColor !== "auto") {
            svg = svg.replace(/"currentColor"/g, `"${this.svgTextColor}"`);
        }
        if (this.svgBackgroundColor !== "auto") {
            svg = svg.replace("style=\"", `style="background-color:${this.svgBackgroundColor};`);
        }
        const dataUri = this.parser.format(".svg", svg).content || "";
        if (dataUri.length === 0) {
            // throw Error(`cannot parse svg: ${svg}`);
            vscode.window.showWarningMessage(`cannot parse svg: ${svg}`);
        }
        const uri = `![](${dataUri})`; // as markdown image
        this.cache.set(tex, uri);
        return { text: uri, error: false };
    }
}
exports.Tex2Svg = Tex2Svg;
//# sourceMappingURL=tex2svg.js.map