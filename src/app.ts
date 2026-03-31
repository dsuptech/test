import express from "express";
import { env } from "./config/env";
import { SessionStore } from "./domain/sessionStore";
import { requireBearerAuth } from "./middleware/auth";
import { errorHandler, notFoundHandler } from "./middleware/errors";
import { healthRouter } from "./routes/health";
import { sessionsRouter } from "./routes/sessions";

export const createApp = (authToken: string = env.connectApiToken): express.Express => {
  const app = express();
  const sessionStore = new SessionStore();

  app.use(express.json());
  app.use("/health", healthRouter);
  app.use("/api/v1", requireBearerAuth(authToken), sessionsRouter(sessionStore));
  app.use(notFoundHandler);
  app.use(errorHandler);

  return app;
};
