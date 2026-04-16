/**
 * Chat / LLM Agent API service.
 *
 * The ChatWidget uses this function and handles errors gracefully.
 * Endpoint: POST /hr-hub/api/v0.1/agent/chat
 */

import { apiFetch } from './client';

export interface ChatMessage {
	role: 'user' | 'assistant';
	content: string;
}

export interface ChatRequest {
	message: string;
	context?: Record<string, unknown>;
	request_id: string;
}

export interface ChatResponse {
	reply: string;
}

/** Send a natural-language query to the HR agent. */
export async function sendChatMessage(payload: ChatRequest): Promise<ChatResponse> {
	return apiFetch<ChatResponse>('/hr-hub/api/v0.1/agent/chat', {
		method: 'POST',
		json: payload
	});
}
