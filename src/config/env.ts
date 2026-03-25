const DEFAULT_PORT = 3000;
const DEFAULT_AUTH_TOKEN = "dev-connect-token";

function toPort(raw: string | undefined): number {
  if (!raw) {
    return DEFAULT_PORT;
  }

  const parsed = Number.parseInt(raw, 10);
  if (Number.isNaN(parsed) || parsed <= 0) {
    return DEFAULT_PORT;
  }

  return parsed;
}

export interface RuntimeEnv {
  nodeEnv: string;
  port: number;
  connectApiToken: string;
}

export function getEnv(overrides?: Partial<RuntimeEnv>): RuntimeEnv {
  return {
    nodeEnv: overrides?.nodeEnv ?? process.env.NODE_ENV ?? "development",
    port: overrides?.port ?? toPort(process.env.PORT),
    connectApiToken:
      overrides?.connectApiToken ?? process.env.CONNECT_API_TOKEN ?? DEFAULT_AUTH_TOKEN,
  };
}

export const env = getEnv();
