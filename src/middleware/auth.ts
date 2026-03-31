import { NextFunction, Request, Response } from "express";
import { AppError } from "./errors";

export const requireBearerAuth = (expectedToken: string) => {
  return (req: Request, _res: Response, next: NextFunction): void => {
    const authHeader = req.header("authorization");

    if (!authHeader) {
      throw new AppError(401, "UNAUTHORIZED", "Authorization header is required.");
    }

    const [scheme, token] = authHeader.split(" ");
    if (scheme?.toLowerCase() !== "bearer" || !token) {
      throw new AppError(401, "UNAUTHORIZED", "Authorization must use Bearer token.");
    }

    if (token !== expectedToken) {
      throw new AppError(401, "UNAUTHORIZED", "Invalid access token.");
    }

    next();
  };
};
