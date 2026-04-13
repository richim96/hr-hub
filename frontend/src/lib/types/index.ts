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

export type TaskStatus = 'Pending' | 'Completed' | 'Canceled';

export type RequestType = 'new_hire' | 'employee_change' | 'people_ticket';

export type ResponseStatus = 'completed' | 'pending' | 'failed';

export type ActionType =
	| 'create_employee'
	| 'update_employee'
	| 'create_task'
	| 'create_ticket'
	| 'update_ticket'
	| 'close_ticket';

export type EmployeeField =
	| 'first_name'
	| 'last_name'
	| 'email'
	| 'start_date'
	| 'team'
	| 'role'
	| 'manager'
	| 'location';

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
	manager_email: string;
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
	salary?: SalaryTier | null;
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
	status?: TaskStatus | null;
	task_metadata?: Record<string, unknown> | null;
}

// ---------------------------------------------------------------------------
// Change DTO
// ---------------------------------------------------------------------------

export interface ChangeField {
	from_value: string;
	to: string;
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
 * Mirrors backend EmployeeChangeRequest.
 */
export interface EmployeeChangeRequest {
	request_id: string;
	request_type: 'employee_change';
	employee_email: string;
	changes: Partial<Record<EmployeeField, ChangeField>>;
	effective_date: string; // ISO date string YYYY-MM-DD
}

/**
 * Mirrors backend TicketRequest.
 */
export interface TicketRequest {
	request_id: string;
	request_type: 'people_ticket';
	submitted_by: string;
	subject: string;
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
	confidence: number;
	extracted_info: Record<string, unknown>;
	draft_response: string;
}

export interface APIResponse {
	request_id: string;
	request_type: RequestType;
	status: ResponseStatus;
	actions: APIAction[];
	llm_result?: LLMResult | null;
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
