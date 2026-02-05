import { describe, expect, it } from "vitest";
import { add, subtract, multiply, divide, evaluate } from "../src/calculator.js";

describe("basic operations", () => {
  it("adds", () => {
    expect(add(2, 3)).toBe(5);
  });

  it("subtracts", () => {
    expect(subtract(10, 4)).toBe(6);
  });

  it("multiplies", () => {
    expect(multiply(6, 7)).toBe(42);
  });

  it("divides", () => {
    expect(divide(8, 2)).toBe(4);
  });

  it("throws on division by zero", () => {
    expect(() => divide(1, 0)).toThrow(/Division by zero/);
  });
});

describe("evaluate()", () => {
  it("evaluates simple expressions", () => {
    expect(evaluate("2+2")).toBe(4);
    expect(evaluate(" 12 / 3 ")).toBe(4);
  });

  it("respects operator precedence", () => {
    expect(evaluate("2+3*4")).toBe(14);
    expect(evaluate("2*3+4")).toBe(10);
  });

  it("handles parentheses", () => {
    expect(evaluate("(2+3)*4")).toBe(20);
    expect(evaluate("2*(3+(4-1))")).toBe(12);
  });

  it("handles unary +/-", () => {
    expect(evaluate("-3 + 5")).toBe(2);
    expect(evaluate("2 * -3")).toBe(-6);
    expect(evaluate("-(2+3) * 4")).toBe(-20);
    expect(evaluate("+5")).toBe(5);
  });

  it("handles exponentiation (right associative)", () => {
    expect(evaluate("2^3")).toBe(8);
    expect(evaluate("2^3^2")).toBe(512); // 2^(3^2)
  });

  it("handles decimals", () => {
    expect(evaluate(".5 * 8")).toBe(4);
    expect(evaluate("1.5 + 2.25")).toBeCloseTo(3.75, 10);
  });

  it("throws on empty expression", () => {
    expect(() => evaluate("   ")).toThrow(/Empty expression/);
  });

  it("throws on invalid characters", () => {
    expect(() => evaluate("2 + a")).toThrow(/Unexpected character/);
  });

  it("throws on mismatched parentheses", () => {
    expect(() => evaluate("(2+3")).toThrow(/Mismatched parentheses/);
    expect(() => evaluate("2+3)")).toThrow(/Mismatched parentheses/);
  });

  it("throws on division by zero", () => {
    expect(() => evaluate("1/0")).toThrow(/Division by zero/);
  });
});

