import path from "node:path";
import { loadJsonFile, resolveMyAgentHome, saveJsonFile } from "./state.js";
const COPILOT_TOKEN_URL = "https://api.github.com/copilot_internal/v2/token";
const DEFAULT_COPILOT_API_BASE_URL = "https://api.individual.githubcopilot.com";
const TOKEN_REFRESH_MARGIN_MS = 5 * 60 * 1000;
function resolveTokenCachePath(env = process.env) {
    return path.join(resolveMyAgentHome(env), "cache", "github-copilot.token.json");
}
function parseCopilotTokenResponse(value) {
    if (!value || typeof value !== "object") {
        throw new Error("Unexpected response from Copilot token exchange.");
    }
    const record = value;
    const token = record.token;
    const expiresAt = record.expires_at;
    if (typeof token !== "string" || token.trim().length === 0) {
        throw new Error("Copilot token response is missing token.");
    }
    let expiresAtMs;
    if (typeof expiresAt === "number" && Number.isFinite(expiresAt)) {
        expiresAtMs = expiresAt > 10_000_000_000 ? expiresAt : expiresAt * 1000;
    }
    else if (typeof expiresAt === "string" && expiresAt.trim()) {
        const parsed = Number.parseInt(expiresAt, 10);
        if (!Number.isFinite(parsed)) {
            throw new Error("Copilot token response has invalid expires_at.");
        }
        expiresAtMs = parsed > 10_000_000_000 ? parsed : parsed * 1000;
    }
    else {
        throw new Error("Copilot token response is missing expires_at.");
    }
    return { token: token.trim(), expiresAt: expiresAtMs };
}
function isTokenUsable(cache, now = Date.now()) {
    return cache.expiresAt - now > TOKEN_REFRESH_MARGIN_MS;
}
export function deriveCopilotApiBaseUrlFromToken(token) {
    const match = token.match(/(?:^|;)\s*proxy-ep=([^;\s]+)/i);
    const proxyEndpoint = match?.[1]?.trim();
    if (!proxyEndpoint) {
        return DEFAULT_COPILOT_API_BASE_URL;
    }
    const host = proxyEndpoint.replace(/^https?:\/\//, "").replace(/^proxy\./i, "api.");
    return host ? `https://${host}` : DEFAULT_COPILOT_API_BASE_URL;
}
export function clearCachedRuntimeToken(env = process.env) {
    const cachePath = resolveTokenCachePath(env);
    saveJsonFile(cachePath, {});
}
export async function resolveCopilotRuntimeToken(params) {
    const env = params.env ?? process.env;
    const cachePath = resolveTokenCachePath(env);
    if (!params.forceRefresh) {
        const cached = loadJsonFile(cachePath);
        if (cached && typeof cached.token === "string" && typeof cached.expiresAt === "number") {
            if (isTokenUsable(cached)) {
                return {
                    token: cached.token,
                    expiresAt: cached.expiresAt,
                    source: `cache:${cachePath}`,
                    baseUrl: deriveCopilotApiBaseUrlFromToken(cached.token),
                };
            }
        }
    }
    const fetchFn = params.fetchFn ?? fetch;
    const response = await fetchFn(COPILOT_TOKEN_URL, {
        method: "GET",
        headers: {
            Accept: "application/json",
            Authorization: `Bearer ${params.githubToken}`,
        },
    });
    if (!response.ok) {
        throw new Error(`Copilot token exchange failed: HTTP ${response.status}`);
    }
    const parsed = parseCopilotTokenResponse(await response.json());
    const payload = {
        token: parsed.token,
        expiresAt: parsed.expiresAt,
        updatedAt: Date.now(),
    };
    saveJsonFile(cachePath, payload);
    return {
        token: payload.token,
        expiresAt: payload.expiresAt,
        source: `fetched:${COPILOT_TOKEN_URL}`,
        baseUrl: deriveCopilotApiBaseUrlFromToken(payload.token),
    };
}
//# sourceMappingURL=runtime-token.js.map