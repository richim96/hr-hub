/**
 * TypeScript interfaces the backend Python DTOs.
 * Keep in sync with: backend/src/hr_hub/model/dto/
 */

// ---------------------------------------------------------------------------
// Enums / literals
// ---------------------------------------------------------------------------

export type Department =
	| 'accounting'
	| 'engineering'
	| 'hr'
	| 'IT'
	| 'management'
	| 'marketing'
	| 'product_management'
	| 'r&d'
	| 'sales'
	| 'support';

export type SalaryTier = 'low' | 'medium' | 'high';

export type Gender = 'M' | 'F';

export type Status = 'Pending' | 'Completed' | 'Canceled';

export type RequestType = 'new_hire' | 'employee_change' | 'prediction';

export type ActionType =
	| 'create_employee'
	| 'update_employee'
	| 'delete_employee'
	| 'create_task'
	| 'create_ticket'
	| 'update_ticket'
	| 'close_ticket'
	| 'delete_ticket'
	| 'score_attrition';

// ---------------------------------------------------------------------------
// Employee DTOs
// ---------------------------------------------------------------------------

/** Mirrors backend EmployeeDTO */
export interface Employee {
	employee_id: string;
	first_name: string;
	last_name: string;
	gender?: Gender | null;
	email: string;
	manager_email?: string | null;
}

/** Mirrors backend EmployeeEquipmentDTO */
export interface EmployeeEquipment {
	laptop?: string | null;
	monitor?: boolean | null;
	headset?: boolean | null;
}

/** Mirrors backend EmployeeInfoDTO */
export interface EmployeeInfo {
	department: Department;
	salary: SalaryTier;
	active_projects?: number | null;
	avg_monthly_hours?: number | null;
	years_at_company?: number | null;
	work_accidents?: boolean | null;
	received_promotion?: boolean | null;
	last_evaluation?: number | null;
	satisfaction_score?: number | null;
	attrition?: boolean | null;
	attrition_risk?: number | null;
}

/** Full employee record for display (joins Employee + EmployeeEquipment + EmployeeInfo) */
export interface FullEmployee extends Employee, EmployeeEquipment, EmployeeInfo {}

// ---------------------------------------------------------------------------
// IT Task (mirrors the it_task ORM table — no dedicated DTO in backend yet)
// ---------------------------------------------------------------------------

export interface ITTask {
	task_id: string;
	employee_id: string;
	employee_email?: string | null;
	title: string;
	description?: string | null;
	assignee?: string | null;
	due_date?: string | null;
	status?: Status | null;
	task_metadata?: Record<string, unknown> | null;
}

// ---------------------------------------------------------------------------
// Request payloads
// ---------------------------------------------------------------------------

/**
 * Mirrors backend NewHireRequest.
 */
export interface NewHireRequest {
	request_id: string;
	request_type: 'new_hire';
	employee: Employee;
	equipment: EmployeeEquipment;
	info: EmployeeInfo;
}

/**
 * Mirrors backend UpdateEmployeeRequest.
 * All fields optional — only non-null values are written by the backend.
 */
export interface UpdateEmployeeRequest {
	// Identity
	first_name?: string;
	last_name?: string;
	gender?: Gender | null;
	email?: string;
	manager_email?: string | null;
	// Equipment
	laptop?: string | null;
	monitor?: boolean | null;
	headset?: boolean | null;
	// Employment info
	department?: Department;
	salary?: SalaryTier;
	active_projects?: number | null;
	avg_monthly_hours?: number | null;
	years_at_company?: number | null;
	work_accidents?: boolean | null;
	received_promotion?: boolean | null;
	last_evaluation?: number | null;
	satisfaction_score?: number | null;
	attrition?: boolean | null;
	attrition_risk?: number | null;
}

/** Mirrors backend UpdateTicketRequest. */
export interface UpdateTicketRequest {
	title?: string | null;
	text?: string | null;
}

/**
 * Mirrors backend NewTicketRequest.
 */
export interface TicketRequest {
	request_id: string;
	request_type: 'people_ticket';
	submitted_by: string;
	title: string;
	text: string;
}

// ---------------------------------------------------------------------------
// APIResponse (mirrors backend APIResponse + nested classes)
// ---------------------------------------------------------------------------

export interface APIAction {
	action: ActionType;
	success: boolean;
	details: string;
}

export interface LLMResult {
	topics: string[];
	summary?: string;
	confidence?: number;
	extracted_info?: Record<string, unknown>;
	draft_response?: string;
}

export interface APIResponse {
	request_id: string;
	request_type: RequestType;
	status: Status;
	actions: APIAction[];
}

/** Mirrors backend TicketDTO. */
export interface Ticket {
	request_id: string;
	request_type: string;
	status: Status;
	submitted_by: string;
	title: string;
	text: string;
	actions: APIAction[];
	llm_result?: LLMResult | null;
	created_at: string;
}

/** Mirrors backend ScoreAllAttritionRequest */
export interface ScoreAllRequest {
	request_id: string;
	request_type: 'prediction';
}

// ---------------------------------------------------------------------------
// Frontend-only helpers
// ---------------------------------------------------------------------------

/** Wraps an API call result with loading/error state for components. */
export interface AsyncState<T> {
	data: T | null;
	loading: boolean;
	error: string | null;
}

export type ToastType = 'success' | 'error' | 'warning' | 'info';

export interface Toast {
	id: string;
	type: ToastType;
	message: string;
}
