import fs from "node:fs";
import os from "node:os";
import path from "node:path";
function resolveHomeBase(env) {
    const home = env.USERPROFILE?.trim() || env.HOME?.trim() || os.homedir();
    if (!home) {
        throw new Error("Unable to resolve home directory.");
    }
    return home;
}
export function resolveUserPath(input, env = process.env) {
    const trimmed = input.trim();
    if (!trimmed) {
        return trimmed;
    }
    if (trimmed.startsWith("~")) {
        return path.resolve(path.join(resolveHomeBase(env), trimmed.slice(1)));
    }
    return path.resolve(trimmed);
}
export function resolveMyAgentHome(env = process.env) {
    const override = env.MYAGENT_HOME?.trim();
    if (override) {
        return resolveUserPath(override, env);
    }
    return path.join(resolveHomeBase(env), ".myagent-copilot");
}
export function ensureDirectory(pathname) {
    fs.mkdirSync(pathname, { recursive: true });
}
export function loadJsonFile(pathname) {
    try {
        if (!fs.existsSync(pathname)) {
            return undefined;
        }
        return JSON.parse(fs.readFileSync(pathname, "utf8"));
    }
    catch {
        return undefined;
    }
}
export function saveJsonFile(pathname, data) {
    ensureDirectory(path.dirname(pathname));
    fs.writeFileSync(pathname, `${JSON.stringify(data, null, 2)}\n`, "utf8");
    try {
        fs.chmodSync(pathname, 0o600);
    }
    catch {
        // Windows may ignore chmod semantics; best effort only.
    }
}
//# sourceMappingURL=state.js.map