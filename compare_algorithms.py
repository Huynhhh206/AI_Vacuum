import time
import threading
import tkinter as tk

from tkinter import ttk
from algorithm.A_star_10_12_nearest_first import *
from algorithm.bfs_in_AI import *
from algorithm.dfs_AI1 import *
from algorithm.bfs_AI import *
from algorithm.dfs_AI import *




def run_benchmark_window(matrix, start):
    """
    Chạy benchmark trong thread riêng và hiển thị kết quả trên cửa sổ Tkinter
    """

    # =========================
    # Tạo cửa sổ kết quả
    # =========================
    result_window = tk.Toplevel()
    result_window.title("So sánh thuật toán")
    result_window.geometry("500x250")

    columns = ("Algorithm", "Steps", "Time (s)")
    tree = ttk.Treeview(result_window, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=150)

    tree.pack(fill="both", expand=True, padx=10, pady=10)

    # =========================
    # Hàm benchmark chạy nền
    # =========================
    def benchmark_task():
        algorithms = [
            ("A*", benchmark_a_star),
            ("BFS", benchmark_bfs),
            ("DFS", benchmark_dfs),
            ("BFS Full", benchmark_bfs_full),
            ("DFS Full", benchmark_dfs_full),
        ]

        for name, func in algorithms:
            matrix_copy = [row[:] for row in matrix]

            start_time = time.perf_counter()
            steps = func(matrix_copy, start)
            end_time = time.perf_counter()

            elapsed = round(end_time - start_time, 6)

            result_window.after(
                0,
                lambda n=name, s=steps, t=elapsed:
                tree.insert("", "end", values=(n, s, t))
            )

    # chạy thread benchmark
    threading.Thread(target=benchmark_task, daemon=True).start()


# ==================================================
# Các hàm benchmark riêng cho từng thuật toán
# ==================================================

def benchmark_a_star(matrix, start):
    dust_positions = [(i, j) for i in range(len(matrix))
                    for j in range(len(matrix[0]))
                    if matrix[i][j] == 2]

    current = tuple(start)
    total_steps = 0

    for dust in dust_positions:
        path = find_path_to_closest_goal(matrix, current, dust_positions)
        total_steps += len(path)
        current = dust

    return total_steps


def benchmark_bfs(matrix, start):
    dust_positions = [(i, j) for i in range(len(matrix))
                    for j in range(len(matrix[0]))
                    if matrix[i][j] == 2]

    current = start
    total_steps = 0

    for dust in dust_positions:
        path = initialize_bfs(matrix, current, dust)
        total_steps += len(path)
        current = dust

    return total_steps


def benchmark_dfs(matrix, start):
    dust_positions = [(i, j) for i in range(len(matrix))
                    for j in range(len(matrix[0]))
                    if matrix[i][j] == 2]

    current = start
    total_steps = 0

    for dust in dust_positions:
        path = initialize_dfs1(matrix, current, dust)
        total_steps += len(path)
        current = dust

    return total_steps



def benchmark_bfs_full(matrix, start):
    path = initialize_B(matrix, start)
    return len(path)



def benchmark_dfs_full(matrix, start):
    path = initialize_D(matrix, start)
    return len(path)



