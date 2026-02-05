/**
 * Basic calculator helpers + safe expression evaluator.
 *
 * Supported in `evaluate()`:
 * - Numbers: integers and decimals (e.g. 2, 3.14, .5)
 * - Operators: +, -, *, /, ^ (power)
 * - Parentheses: ( )
 * - Unary +/-
 */

export function add(a, b) {
  return toNumber(a) + toNumber(b);
}

export function subtract(a, b) {
  return toNumber(a) - toNumber(b);
}

export function multiply(a, b) {
  return toNumber(a) * toNumber(b);
}

export function divide(a, b) {
  const divisor = toNumber(b);
  if (divisor === 0) throw new Error("Division by zero");
  return toNumber(a) / divisor;
}

export function evaluate(expression) {
  if (typeof expression !== "string") {
    throw new TypeError("Expression must be a string");
  }

  const tokens = tokenize(expression);
  if (tokens.length === 0) throw new Error("Empty expression");
  const rpn = toRpn(tokens);
  return evalRpn(rpn);
}

export const calculate = evaluate;

function toNumber(x) {
  const n = typeof x === "number" ? x : Number(x);
  if (!Number.isFinite(n)) throw new TypeError(`Invalid number: ${String(x)}`);
  return n;
}

function tokenize(input) {
  const tokens = [];
  let i = 0;

  while (i < input.length) {
    const ch = input[i];

    if (isWhitespace(ch)) {
      i += 1;
      continue;
    }

    if (isDigit(ch) || ch === ".") {
      const start = i;
      let sawDot = ch === ".";
      i += 1;
      while (i < input.length) {
        const c = input[i];
        if (isDigit(c)) {
          i += 1;
          continue;
        }
        if (c === ".") {
          if (sawDot) break;
          sawDot = true;
          i += 1;
          continue;
        }
        break;
      }
      const raw = input.slice(start, i);
      if (raw === "." || raw === "+." || raw === "-.") {
        throw new Error(`Invalid number: ${raw}`);
      }
      const value = Number(raw);
      if (!Number.isFinite(value)) throw new Error(`Invalid number: ${raw}`);
      tokens.push({ type: "number", value });
      continue;
    }

    if (ch === "(" || ch === ")") {
      tokens.push({ type: "paren", value: ch });
      i += 1;
      continue;
    }

    if (isOperatorChar(ch)) {
      tokens.push({ type: "op", value: ch });
      i += 1;
      continue;
    }

    throw new Error(`Unexpected character: ${ch}`);
  }

  // Mark unary operators (u+ / u-) based on previous token context.
  const out = [];
  for (let idx = 0; idx < tokens.length; idx += 1) {
    const t = tokens[idx];
    if (t.type === "op" && (t.value === "+" || t.value === "-")) {
      const prev = out[out.length - 1];
      const isUnary =
        !prev ||
        (prev.type === "op") ||
        (prev.type === "paren" && prev.value === "(");
      out.push({
        type: "op",
        value: isUnary ? (t.value === "+" ? "u+" : "u-") : t.value,
      });
    } else {
      out.push(t);
    }
  }

  return out;
}

const OPERATORS = {
  "u+": { precedence: 5, assoc: "right", arity: 1 },
  "u-": { precedence: 5, assoc: "right", arity: 1 },
  "^": { precedence: 4, assoc: "right", arity: 2 },
  "*": { precedence: 3, assoc: "left", arity: 2 },
  "/": { precedence: 3, assoc: "left", arity: 2 },
  "+": { precedence: 2, assoc: "left", arity: 2 },
  "-": { precedence: 2, assoc: "left", arity: 2 },
};

function toRpn(tokens) {
  const output = [];
  const stack = [];

  for (const t of tokens) {
    if (t.type === "number") {
      output.push(t);
      continue;
    }

    if (t.type === "op") {
      const o1 = OPERATORS[t.value];
      if (!o1) throw new Error(`Unknown operator: ${t.value}`);

      while (stack.length > 0) {
        const top = stack[stack.length - 1];
        if (top.type !== "op") break;
        const o2 = OPERATORS[top.value];
        if (!o2) break;

        const shouldPop =
          (o1.assoc === "left" && o1.precedence <= o2.precedence) ||
          (o1.assoc === "right" && o1.precedence < o2.precedence);

        if (!shouldPop) break;
        output.push(stack.pop());
      }

      stack.push(t);
      continue;
    }

    if (t.type === "paren") {
      if (t.value === "(") {
        stack.push(t);
        continue;
      }

      // t.value === ")"
      let foundLeft = false;
      while (stack.length > 0) {
        const top = stack.pop();
        if (top.type === "paren" && top.value === "(") {
          foundLeft = true;
          break;
        }
        output.push(top);
      }
      if (!foundLeft) throw new Error("Mismatched parentheses");
      continue;
    }

    throw new Error(`Unknown token type: ${t.type}`);
  }

  while (stack.length > 0) {
    const top = stack.pop();
    if (top.type === "paren") throw new Error("Mismatched parentheses");
    output.push(top);
  }

  return output;
}

function evalRpn(rpn) {
  const stack = [];

  for (const t of rpn) {
    if (t.type === "number") {
      stack.push(t.value);
      continue;
    }

    if (t.type !== "op") throw new Error("Invalid RPN token");
    const op = OPERATORS[t.value];
    if (!op) throw new Error(`Unknown operator: ${t.value}`);

    if (op.arity === 1) {
      if (stack.length < 1) throw new Error("Invalid expression");
      const a = stack.pop();
      stack.push(t.value === "u-" ? -a : +a);
      continue;
    }

    if (stack.length < 2) throw new Error("Invalid expression");
    const b = stack.pop();
    const a = stack.pop();

    switch (t.value) {
      case "+":
        stack.push(a + b);
        break;
      case "-":
        stack.push(a - b);
        break;
      case "*":
        stack.push(a * b);
        break;
      case "/":
        if (b === 0) throw new Error("Division by zero");
        stack.push(a / b);
        break;
      case "^":
        stack.push(a ** b);
        break;
      default:
        throw new Error(`Unknown operator: ${t.value}`);
    }
  }

  if (stack.length !== 1) throw new Error("Invalid expression");
  const result = stack[0];
  if (!Number.isFinite(result)) throw new Error("Result is not finite");
  return result;
}

function isWhitespace(ch) {
  return ch === " " || ch === "\t" || ch === "\n" || ch === "\r";
}

function isDigit(ch) {
  return ch >= "0" && ch <= "9";
}

function isOperatorChar(ch) {
  return ch === "+" || ch === "-" || ch === "*" || ch === "/" || ch === "^";
}
