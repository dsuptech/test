import { v4 as uuidv4 } from "uuid";
import { Session } from "../types/session";

export class SessionStore {
  private readonly sessions = new Map<string, Session>();

  create(clientId: string): Session {
    const now = new Date().toISOString();
    const session: Session = {
      id: uuidv4(),
      clientId,
      status: "active",
      createdAt: now,
      updatedAt: now,
    };

    this.sessions.set(session.id, session);
    return session;
  }

  findById(sessionId: string): Session | null {
    return this.sessions.get(sessionId) ?? null;
  }

  getById(sessionId: string): Session | null {
    return this.findById(sessionId);
  }

  close(sessionId: string): Session | null {
    const current = this.sessions.get(sessionId);
    if (!current) {
      return null;
    }

    const now = new Date().toISOString();
    const updated: Session = {
      ...current,
      status: "closed",
      updatedAt: now,
      closedAt: now,
    };

    this.sessions.set(sessionId, updated);
    return updated;
  }
}
