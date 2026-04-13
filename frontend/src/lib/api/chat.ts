/**
 * Chat / LLM Agent API service.
 *
 * NOTE: No chat endpoint exists on the backend yet.
 * The ChatWidget uses this function and handles errors gracefully.
 * Expected endpoint (once implemented): POST /hr-hub/api/v0.1/agent/query
 */

import { apiFetch } from './client';

export interface ChatMessage {
	role: 'user' | 'assistant';
	content: string;
}

export interface ChatRequest {
	message: string;
	context?: Record<string, unknown>;
}

export interface ChatResponse {
	reply: string;
}

/** Send a natural-language query to the HR agent. */
export async function sendChatMessage(payload: ChatRequest): Promise<ChatResponse> {
	return apiFetch<ChatResponse>('/hr-hub/api/v0.1/agent/query', {
		method: 'POST',
		json: payload
	});
}
