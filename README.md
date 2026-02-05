# Calculator Code

A small calculator library (safe expression evaluator) plus a CLI.

## Install

```bash
npm install
```

## Use as a library

```js
import { evaluate, add, subtract, multiply, divide } from "./src/calculator.js";

console.log(evaluate("2 + 2*(3-1)")); // 6
console.log(add(1, 2)); // 3
```

## Use the CLI

```bash
npm install
npx calc "2 + 2*(3-1)"
```

## Test

```bash
npm test
```
