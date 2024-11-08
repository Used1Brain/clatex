import { workspace, TextEditorDecorationType } from "vscode";
import { correctDecorationType, wrongDecorationType } from "./decorations-types";
export default {
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
	correctDecorationType: <TextEditorDecorationType>correctDecorationType,
	wrongDecorationType: <TextEditorDecorationType>wrongDecorationType,
	// correctDecorationType: <TextEditorDecorationType>workspace.getConfiguration().get("mathover.correctDecorationType"),
	// wrongDecorationType: <TextEditorDecorationType>workspace.getConfiguration().get("mathover.wrongDecorationType"),
};