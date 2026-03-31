export type SessionStatus = "active" | "closed";

export interface Session {
  id: string;
  clientId: string;
  status: SessionStatus;
  createdAt: string;
  updatedAt: string;
  closedAt?: string;
}
