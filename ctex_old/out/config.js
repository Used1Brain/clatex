"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const decorations_types_1 = require("./decorations-types");
exports.default = {
    // format: <string>workspace.getConfiguration().get("mathover.format"),
    format: "TeX",
    matchReg: "ꔧ[^ $]+",
    matchRegFlags: "gm",
    wrongReg: "\\$",
    wrongRegFlags: "g",
    forwardSkip: 0,
    backwardSkip: 0,
    cacheSize: 1024,
    updateInterval: 500,
    svgTextColor: "#dddddd",
    svgBackgroundColor: "auto",
    // if you know how to cast objects from configurations, let me know.
    correctDecorationType: decorations_types_1.correctDecorationType,
    wrongDecorationType: decorations_types_1.wrongDecorationType,
    // correctDecorationType: <TextEditorDecorationType>workspace.getConfiguration().get("mathover.correctDecorationType"),
    // wrongDecorationType: <TextEditorDecorationType>workspace.getConfiguration().get("mathover.wrongDecorationType"),
};
//# sourceMappingURL=config.js.map