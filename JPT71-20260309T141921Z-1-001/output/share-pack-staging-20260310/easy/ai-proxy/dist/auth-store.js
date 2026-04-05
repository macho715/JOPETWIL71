import path from "node:path";
import { loadJsonFile, resolveMyAgentHome, resolveUserPath, saveJsonFile } from "./state.js";
const AUTH_STORE_VERSION = 1;
const DEFAULT_PROFILE_ID = "github-copilot:default";
function createEmptyStore() {
    return {
        version: AUTH_STORE_VERSION,
        defaultProfileId: DEFAULT_PROFILE_ID,
        profiles: {},
    };
}
function coerceTokenCredential(value) {
    if (!value || typeof value !== "object") {
        return null;
    }
    const record = value;
    if (record.type !== "token" || record.provider !== "github-copilot") {
        return null;
    }
    if (typeof record.token !== "string" || record.token.trim().length === 0) {
        return null;
    }
    return {
        type: "token",
        provider: "github-copilot",
        token: record.token.trim(),
        ...(typeof record.expires === "number" ? { expires: record.expires } : {}),
        ...(typeof record.email === "string" && record.email.trim()
            ? { email: record.email.trim() }
            : {}),
    };
}
function coerceAuthStore(raw) {
    if (!raw || typeof raw !== "object") {
        return createEmptyStore();
    }
    const record = raw;
    const profilesRecord = record.profiles && typeof record.profiles === "object"
        ? record.profiles
        : {};
    const profiles = Object.entries(profilesRecord).reduce((acc, [profileId, credential]) => {
        const parsed = coerceTokenCredential(credential);
        if (parsed) {
            acc[profileId] = parsed;
        }
        return acc;
    }, {});
    return {
        version: typeof record.version === "number" && Number.isFinite(record.version)
            ? record.version
            : AUTH_STORE_VERSION,
        defaultProfileId: typeof record.defaultProfileId === "string" && record.defaultProfileId.trim()
            ? record.defaultProfileId.trim()
            : DEFAULT_PROFILE_ID,
        profiles,
    };
}
export function resolveStandaloneAuthStorePath(env = process.env) {
    return path.join(resolveMyAgentHome(env), "auth-profiles.json");
}
export function loadStandaloneAuthStore(env = process.env) {
    return coerceAuthStore(loadJsonFile(resolveStandaloneAuthStorePath(env)));
}
export function saveStandaloneAuthStore(store, env = process.env) {
    saveJsonFile(resolveStandaloneAuthStorePath(env), store);
}
export function upsertStandaloneTokenProfile(params) {
    const env = params.env ?? process.env;
    const profileId = params.profileId?.trim() || DEFAULT_PROFILE_ID;
    const store = loadStandaloneAuthStore(env);
    store.defaultProfileId = profileId;
    store.profiles[profileId] = {
        type: "token",
        provider: "github-copilot",
        token: params.token.trim(),
    };
    saveStandaloneAuthStore(store, env);
    return store;
}
function resolveGithubTokenFromEnv(env) {
    const candidates = [
        "MYAGENT_GITHUB_TOKEN",
        "COPILOT_GITHUB_TOKEN",
        "GH_TOKEN",
        "GITHUB_TOKEN",
    ];
    for (const key of candidates) {
        const value = env[key]?.trim();
        if (value) {
            return { token: value, source: `env:${key}` };
        }
    }
    return null;
}
function isCredentialUsable(credential) {
    if (!credential.token.trim()) {
        return false;
    }
    if (typeof credential.expires === "number" &&
        Number.isFinite(credential.expires) &&
        credential.expires > 0 &&
        Date.now() >= credential.expires) {
        return false;
    }
    return true;
}
function resolveStoreCandidate(store, preferredProfileId) {
    const order = [
        preferredProfileId?.trim(),
        store.defaultProfileId?.trim(),
        ...Object.keys(store.profiles),
    ].filter(Boolean);
    const seen = new Set();
    for (const profileId of order) {
        if (seen.has(profileId)) {
            continue;
        }
        seen.add(profileId);
        const credential = store.profiles[profileId];
        if (!credential || credential.provider !== "github-copilot" || !isCredentialUsable(credential)) {
            continue;
        }
        return {
            token: credential.token,
            source: `store:${profileId}`,
            profileId,
        };
    }
    return null;
}
function resolveOpenClawAuthCandidates(env) {
    const explicit = env.OPENCLAW_AGENT_DIR?.trim();
    if (explicit) {
        return [path.join(resolveUserPath(explicit, env), "auth-profiles.json")];
    }
    const openClawState = env.OPENCLAW_STATE_DIR?.trim()
        ? resolveUserPath(env.OPENCLAW_STATE_DIR.trim(), env)
        : path.join(resolveUserPath("~", env), ".openclaw");
    return [
        path.join(openClawState, "agents", "main", "agent", "auth-profiles.json"),
        path.join(openClawState, "auth-profiles.json"),
    ];
}
function resolveOpenClawCompatAuth(env, preferredProfileId) {
    for (const candidate of resolveOpenClawAuthCandidates(env)) {
        const store = coerceAuthStore(loadJsonFile(candidate));
        const resolved = resolveStoreCandidate(store, preferredProfileId);
        if (resolved) {
            return {
                token: resolved.token,
                source: `openclaw:${candidate}`,
                profileId: resolved.profileId,
            };
        }
    }
    return null;
}
export function resolveStandaloneGithubAuth(params = {}) {
    const env = params.env ?? process.env;
    const envAuth = resolveGithubTokenFromEnv(env);
    if (envAuth) {
        return envAuth;
    }
    const storeAuth = resolveStoreCandidate(loadStandaloneAuthStore(env), params.preferredProfileId);
    if (storeAuth) {
        return storeAuth;
    }
    const openClawFallback = resolveOpenClawCompatAuth(env, params.preferredProfileId);
    if (openClawFallback) {
        return openClawFallback;
    }
    throw new Error("No GitHub Copilot credentials found. Run `pnpm login`, or set MYAGENT_GITHUB_TOKEN / COPILOT_GITHUB_TOKEN / GH_TOKEN / GITHUB_TOKEN.");
}
//# sourceMappingURL=auth-store.js.map