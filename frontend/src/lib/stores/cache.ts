/**
 * In-memory-first cache with optional localStorage persistence.
 *
 * Primary store: module-level Map (_mem).
 *   - Lives as long as the JS module = browser tab session.
 *   - Resets automatically on full page refresh → triggers cold-start re-fetch.
 *   - No quota issues — suitable for large datasets.
 *
 * Secondary store: localStorage.
 *   - Written opportunistically after each network fetch.
 *   - Silently skipped on QuotaExceededError (common with large datasets).
 *   - Not read back in this session — _mem is always the read path.
 *
 * Flow:
 *   Cold start  → fetch from backend → writeCache (populates _mem + tries LS) → store
 *   Warm nav    → isWarm check → readCache from _mem → store  (zero network)
 *   Full reload → _mem cleared → cold start again
 *   Mutations   → call backend → patch _mem + LS in-place → update store
 */

const LS_KEY: Record<string, string> = {
	employees: 'hr_hub:employees',
	tasks: 'hr_hub:tasks',
	tickets: 'hr_hub:tickets'
};

// Primary in-memory cache. No size limit.
const _mem = new Map<string, unknown[]>();

// ---------------------------------------------------------------------------
// Warm / cold detection
// ---------------------------------------------------------------------------

/** True after the domain has been fetched at least once this page session. */
export function isWarm(domain: string): boolean {
	return _mem.has(domain);
}

// ---------------------------------------------------------------------------
// Read / write
// ---------------------------------------------------------------------------

/**
 * Read cached items.
 * Returns the array (possibly empty) when the domain is warm, null when cold.
 */
export function readCache<T>(domain: string): T[] | null {
	if (!_mem.has(domain)) return null;
	return _mem.get(domain) as T[];
}

/**
 * Persist items for a domain.
 * Always writes to _mem. Also attempts localStorage (fails gracefully on quota).
 */
export function writeCache<T>(domain: string, items: T[]): void {
	_mem.set(domain, items as unknown[]);

	if (typeof localStorage === 'undefined') return;
	try {
		localStorage.setItem(LS_KEY[domain], JSON.stringify(items));
	} catch {
		// QuotaExceededError — _mem still serves warm reads this session.
	}
}

// ---------------------------------------------------------------------------
// Granular in-place mutations (called after backend writes)
// ---------------------------------------------------------------------------

/** Mark a domain cold so the next fetch* call hits the backend. */
export function invalidateCache(domain: string): void {
	_mem.delete(domain);
	if (typeof localStorage !== 'undefined' && LS_KEY[domain]) {
		localStorage.removeItem(LS_KEY[domain]);
	}
}
