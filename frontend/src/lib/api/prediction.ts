/**
 * Prediction API service — attrition risk scoring.
 *
 * Implemented backend endpoints:
 *   POST /hr-hub/api/v0.1/prediction/attrition/score-all    ✅ re-score all current employees
 */

import { apiFetch } from './client';
import type { APIResponse, ScoreAllRequest } from '$lib/types';

const PREFIX = '/hr-hub/api/v0.1/prediction';

/**
 * Re-score attrition risk for all current (non-attrited) employees and persist the results.
 */
export async function scoreAll(payload: ScoreAllRequest): Promise<APIResponse> {
	return apiFetch<APIResponse>(`${PREFIX}/attrition/score-all`, {
		method: 'POST',
		json: payload
	});
}
