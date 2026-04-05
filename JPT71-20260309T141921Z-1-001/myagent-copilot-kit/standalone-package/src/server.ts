import express from "express";
import {
  createChatProxyHandler,
  createPreSendDlpMiddleware,
  createRoutingGateMiddleware,
} from "./proxy-middleware.js";
import type { ProxyOperationalLogger } from "./ops-log.js";

export type StandaloneServerOptions = {
  host?: string;
  port?: number;
  enableOpsLogs?: boolean;
  allowSanitizedToCopilot?: boolean;
  corsOrigins?: string[];
  authToken?: string;
};

const DEFAULT_ALLOWED_ORIGINS = ["http://127.0.0.1:4173", "http://127.0.0.1:18789"];

function readCsvList(value: string | undefined): string[] {
  if (!value?.trim()) {
    return [];
  }
  return value
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

function getRequestAuthToken(req: express.Request): string {
  const direct = req.header("x-ai-proxy-token");
  if (typeof direct === "string" && direct.trim()) {
    return direct.trim();
  }
  const authorization = req.header("authorization");
  const match = authorization?.match(/^Bearer\s+(.+)$/i);
  return match?.[1]?.trim() || "";
}

export function resolveServerOptionsFromEnv(
  env: NodeJS.ProcessEnv = process.env,
): Required<StandaloneServerOptions> {
  const host = env.MYAGENT_PROXY_HOST?.trim() || "127.0.0.1";
  const port = Number.parseInt(env.MYAGENT_PROXY_PORT ?? "3010", 10);
  const enableOpsLogs = env.MYAGENT_PROXY_OPS_LOGS?.trim() !== "0";
  const allowSanitizedToCopilot =
    env.MYAGENT_PROXY_ALLOW_SANITIZED_TO_COPILOT?.trim() === "1";
  const authToken = env.MYAGENT_PROXY_AUTH_TOKEN?.trim() || "";
  const corsOrigins = Array.from(
    new Set([...DEFAULT_ALLOWED_ORIGINS, ...readCsvList(env.MYAGENT_PROXY_CORS_ORIGINS)]),
  );
  return {
    host,
    port: Number.isFinite(port) ? port : 3010,
    enableOpsLogs,
    allowSanitizedToCopilot,
    corsOrigins,
    authToken,
  };
}

export function createStandaloneServer(opts?: StandaloneServerOptions) {
  const resolved = {
    ...resolveServerOptionsFromEnv(),
    ...(opts ?? {}),
  };
  const allowedOrigins = new Set(resolved.corsOrigins.map((origin) => origin.trim()).filter(Boolean));
  const requireAuthToken = resolved.authToken.trim().length > 0;
  const logger: ProxyOperationalLogger | undefined = resolved.enableOpsLogs
    ? (entry) => {
        console.log(JSON.stringify(entry));
      }
    : undefined;

  const app = express();
  app.use(express.json({ limit: "1mb" }));

  app.use((req, res, next) => {
    const origin = req.header("origin");
    const hasOrigin = typeof origin === "string" && origin.trim().length > 0;
    const isAllowedOrigin = hasOrigin && allowedOrigins.has(origin.trim());

    if (hasOrigin && !isAllowedOrigin) {
      res.status(403).json({
        error: "CORS_ORIGIN_DENIED",
        detail: "Origin is not allowed for this proxy.",
      });
      return;
    }

    if (isAllowedOrigin && origin) {
      res.setHeader("Access-Control-Allow-Origin", origin.trim());
      res.setHeader("Vary", "Origin");
    }

    res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
    res.setHeader(
      "Access-Control-Allow-Headers",
      "Content-Type, x-request-id, x-ai-sensitivity, x-ai-proxy-token, ngrok-skip-browser-warning, Authorization",
    );

    if (req.method.toUpperCase() === "OPTIONS") {
      res.status(204).end();
      return;
    }

    next();
  });

  app.get("/api/ai/health", (_req, res) => {
    res.json({
      ok: true,
      service: "myagent-copilot-standalone",
      host: resolved.host,
      port: resolved.port,
      authTokenRequired: requireAuthToken,
      origins: Array.from(allowedOrigins),
    });
  });

  app.post(
    "/api/ai/chat",
    (req, res, next) => {
      if (!requireAuthToken) {
        next();
        return;
      }
      const providedToken = getRequestAuthToken(req);
      if (!providedToken || providedToken !== resolved.authToken) {
        res.status(401).json({
          error: "PROXY_AUTH_REQUIRED",
          detail: "Missing or invalid AI proxy token.",
        });
        return;
      }
      next();
    },
    createPreSendDlpMiddleware({
      policy: {
        sanitizeAtOrAbove: "medium",
        blockAtOrAbove: "high",
      },
      logger,
    }),
    createRoutingGateMiddleware({
      policy: {
        defaultSensitivity: "internal",
        minSensitivityForLocalOnly: "secret",
        allowSanitizedToCopilot: resolved.allowSanitizedToCopilot,
      },
      logger,
    }),
    createChatProxyHandler({
      defaultModel: "github-copilot/gpt-5-mini",
      logger,
    }),
  );

  return {
    app,
    options: resolved,
    start() {
      return new Promise<express.Express["listen"] extends (...args: never[]) => infer T ? T : never>(
        (resolve) => {
          const server = app.listen(resolved.port, resolved.host, () => {
            console.log(`myagent standalone proxy listening: http://${resolved.host}:${resolved.port}`);
            console.log(
              `allow sanitized to copilot: ${resolved.allowSanitizedToCopilot ? "on" : "off"}`,
            );
            console.log(`allowed origins: ${Array.from(allowedOrigins).join(", ")}`);
            console.log(`auth token required: ${requireAuthToken ? "on" : "off"}`);
            console.log("POST /api/ai/chat");
            console.log("GET  /api/ai/health");
            resolve(server);
          });
        },
      );
    },
  };
}
