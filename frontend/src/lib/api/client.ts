/**
 * Base HTTP client for the HR Hub API.
 *
 * All domain API files go through `apiFetch`. Never call `fetch` directly.
 */

import { env } from '$env/dynamic/public';

const BASE_URL = env.PUBLIC_API_BASE_URL ?? 'http://localhost:8000';

export class ApiError extends Error {
	constructor(
		public readonly status: number,
		message: string
	) {
		super(message);
		this.name = 'ApiError';
	}
}

interface FetchOptions extends RequestInit {
	json?: unknown;
}

/**
 * Thin wrapper around fetch.
 * - Sets `Content-Type: application/json` when `options.json` is provided.
 * - Throws `ApiError` on non-2xx responses.
 */
export async function apiFetch<T>(path: string, options: FetchOptions = {}): Promise<T> {
	const { json, ...rest } = options;

	const headers: Record<string, string> = {
		Accept: 'application/json',
		...(json !== undefined ? { 'Content-Type': 'application/json' } : {}),
		...(rest.headers as Record<string, string> | undefined)
	};

	const response = await fetch(`${BASE_URL}${path}`, {
		...rest,
		headers,
		body: json !== undefined ? JSON.stringify(json) : rest.body
	});

	if (!response.ok) {
		let message = `HTTP ${response.status}`;
		try {
			const body = await response.json();
			message = body?.detail ?? body?.message ?? message;
		} catch {
			// ignore parse errors — keep the default message
		}
		throw new ApiError(response.status, message);
	}

	// 204 No Content
	if (response.status === 204) {
		return undefined as T;
	}

	return response.json() as Promise<T>;
}
