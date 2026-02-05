#!/usr/bin/env node
import { evaluate } from "../src/calculator.js";

function main() {
  const args = process.argv.slice(2);
  if (args.length === 0 || args.includes("-h") || args.includes("--help")) {
    printHelp();
    process.exit(0);
  }

  const expr = args.join(" ");

  try {
    const result = evaluate(expr);
    // Print as-is; Node will render integers without trailing .0
    process.stdout.write(String(result) + "\n");
  } catch (err) {
    process.stderr.write((err instanceof Error ? err.message : String(err)) + "\n");
    process.exit(1);
  }
}

function printHelp() {
  process.stdout.write(
    [
      "Usage:",
      '  calc "2 + 2*(3-1)"',
      "",
      "Supported operators: + - * / ^ and parentheses ().",
    ].join("\n") + "\n",
  );
}

main();
