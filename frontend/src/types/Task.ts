/**
 * Интерфейс для создания задачи
 */
export interface TaskCreate {
  title: string;
  description?: string;
}

/**
 * Интерфейс для обновления задачи
 */
export interface TaskUpdate {
  title?: string;
  description?: string;
  is_completed?: boolean;
}

/**
 * Интерфейс для ответа с информацией о задаче
 */
export interface Task {
  id: number;
  user_id: number;
  title: string;
  description: string | null;
  is_completed: boolean;
  created_at: string; // date string
  updated_at: string; // date string
}

/**
 * Интерфейс для ответа со списком задач
 */
export interface TaskListResponse {
  tasks: Task[];
  total: number;
}
