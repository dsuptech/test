import request from "supertest";
import { createApp } from "../src/app";

describe("Connect server", () => {
  const token = "dev-connect-token";

  it("responds health check without authentication", async () => {
    const app = createApp();
    const response = await request(app).get("/health");

    expect(response.status).toBe(200);
    expect(response.body).toEqual({
      status: "ok",
      service: "connect-server",
    });
  });

  it("creates, fetches, and closes a session", async () => {
    const app = createApp(token);

    const createResponse = await request(app)
      .post("/api/v1/sessions")
      .set("Authorization", `Bearer ${token}`)
      .send({ clientId: "client-A" });

    expect(createResponse.status).toBe(201);
    expect(createResponse.body.clientId).toBe("client-A");
    expect(createResponse.body.status).toBe("active");
    expect(createResponse.body.id).toBeDefined();
    const sessionId = createResponse.body.id as string;

    const fetchResponse = await request(app)
      .get(`/api/v1/sessions/${sessionId}`)
      .set("Authorization", `Bearer ${token}`);
    expect(fetchResponse.status).toBe(200);
    expect(fetchResponse.body.id).toBe(sessionId);
    expect(fetchResponse.body.status).toBe("active");

    const closeResponse = await request(app)
      .delete(`/api/v1/sessions/${sessionId}`)
      .set("Authorization", `Bearer ${token}`);
    expect(closeResponse.status).toBe(200);
    expect(closeResponse.body.id).toBe(sessionId);
    expect(closeResponse.body.status).toBe("closed");
    expect(closeResponse.body.closedAt).toBeDefined();
  });

  it("returns 401 for missing auth header on protected endpoints", async () => {
    const app = createApp(token);
    const response = await request(app)
      .post("/api/v1/sessions")
      .send({ clientId: "client-A" });

    expect(response.status).toBe(401);
    expect(response.body.error.code).toBe("UNAUTHORIZED");
  });

  it("returns 404 for unknown session", async () => {
    const app = createApp(token);
    const response = await request(app)
      .get("/api/v1/sessions/unknown")
      .set("Authorization", `Bearer ${token}`);

    expect(response.status).toBe(404);
    expect(response.body.error.code).toBe("SESSION_NOT_FOUND");
  });

  it("returns 409 when closing an already closed session", async () => {
    const app = createApp(token);

    const createResponse = await request(app)
      .post("/api/v1/sessions")
      .set("Authorization", `Bearer ${token}`)
      .send({ clientId: "client-B" });
    const sessionId = createResponse.body.id as string;

    const firstClose = await request(app)
      .delete(`/api/v1/sessions/${sessionId}`)
      .set("Authorization", `Bearer ${token}`);
    expect(firstClose.status).toBe(200);
    expect(firstClose.body.status).toBe("closed");

    const secondClose = await request(app)
      .delete(`/api/v1/sessions/${sessionId}`)
      .set("Authorization", `Bearer ${token}`);

    expect(secondClose.status).toBe(409);
    expect(secondClose.body.error.code).toBe("SESSION_ALREADY_CLOSED");
  });
});
