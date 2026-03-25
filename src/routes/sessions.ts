import { Router } from "express";
import { SessionStore } from "../domain/sessionStore";
import { AppError } from "../middleware/errors";

interface CreateSessionBody {
  clientId?: string;
}

export const sessionsRouter = (store: SessionStore): Router => {
  const router = Router();

  router.post("/sessions", (req, res) => {
    const body = req.body as CreateSessionBody;
    if (!body.clientId?.trim()) {
      throw new AppError(400, "VALIDATION_ERROR", "clientId is required.");
    }

    const session = store.create(body.clientId.trim());
    res.status(201).json(session);
  });

  router.get("/sessions/:id", (req, res) => {
    const session = store.findById(req.params.id);
    if (!session) {
      throw new AppError(404, "SESSION_NOT_FOUND", "Session not found.");
    }
    res.status(200).json(session);
  });

  router.delete("/sessions/:id", (req, res) => {
    const session = store.close(req.params.id);
    if (!session) {
      throw new AppError(404, "SESSION_NOT_FOUND", "Session not found.");
    }
    res.status(200).json(session);
  });

  return router;
};
