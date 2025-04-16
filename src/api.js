// api.js
const API_URL = "http://localhost:8000"; // Your backend base URL

export const getTodos = async () => {
  const res = await fetch(`${API_URL}/todos`);
  if (!res.ok) throw new Error("Failed to fetch todos");
  return res.json();
};

export const addTodo = async (todo) => {
  const res = await fetch(`${API_URL}/todos`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(todo),
  });
  if (!res.ok) throw new Error("Failed to add todo");
  return res.json();
};

export const updateTodo = async (id, todo) => {
  const res = await fetch(`${API_URL}/todos/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(todo),
  });
  if (!res.ok) throw new Error("Failed to update todo");
  return res.json();
};

export const deleteTodo = async (id) => {
  const res = await fetch(`${API_URL}/todos/${id}`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error("Failed to delete todo");
};

export const filterTodos = async (status) => {
  const res = await fetch(`${API_URL}/todos/filter/${status}`);
  if (!res.ok) throw new Error("Failed to filter todos");
  return res.json();
};
