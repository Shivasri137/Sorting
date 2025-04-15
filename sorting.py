import tkinter as tk
from tkinter import ttk, simpledialog
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time
import pygame

pygame.mixer.init()
swap_sound = pygame.mixer.Sound(pygame.mixer.Sound(buffer=b'\x00\x00' * 5000))

# Theories
algorithm_theories = {
    "Bubble Sort": "Bubble Sort is a simple sorting algorithm that repeatedly goes through the list, compares adjacent elements, and swaps them if they are in the wrong order. This process is repeated until the entire list is sorted. In each pass, the largest unsorted element 'bubbles up' to its correct position. The algorithm continues until no more swaps are needed. In Python, it can be implemented as:\ndef bubble_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        for j in range(0, n - i - 1):\n            if arr[j] > arr[j + 1]:\n                arr[j], arr[j + 1] = arr[j + 1], arr[j] \nBubble Sort is one of the simplest sorting algorithms. It repeatedly steps through the list, compares adjacent elements, and swaps them if they are in the wrong order. This process is repeated until the list is sorted. \nTime: O(n^2), Space: O(1), Stable: Yes",
    "Merge Sort": "Merge Sort is a sorting algorithm that works by dividing the array into two halves, recursively sorting each half, and then merging the sorted halves to produce the final sorted array. This divide-and-conquer approach continues until each sub-array contains a single element. Then, during the merge step, elements from the two halves are compared and combined in sorted order. In Python, it can be implemented as:\ndef merge_sort(arr):\n    if len(arr) > 1:\n        mid = len(arr) // 2\n        left = arr[:mid]\n        right = arr[mid:]\n        merge_sort(left)\n        merge_sort(right)\n        i = j = k = 0\n        while i < len(left) and j < len(right):\n            if left[i] < right[j]:\n                arr[k] = left[i]\n                i += 1\n            else:\n                arr[k] = right[j]\n                j += 1\n            k += 1\n        while i < len(left):\n            arr[k] = left[i]\n            i += 1\n            k += 1\n        while j < len(right):\n            arr[k] = right[j]\n            j += 1\n            k += 1 \nMerge Sort is a sorting algorithm that divides the list into smaller parts, sorts each part, and then combines them back together in order to form a sorted list..\nTime: O(n log n), Space: O(n), Stable: Yes",
    "Quick Sort": "Quick Sort is a sorting algorithm that works by selecting a pivot element from the array, then dividing the remaining elements into two sub-arrays: one with elements less than or equal to the pivot and the other with elements greater than the pivot. These sub-arrays are then recursively sorted using the same process. Finally, the sorted sub-arrays are combined with the pivot to form the final sorted array. In Python, this can be written as:\ndef quick_sort(arr):\n    if len(arr) <= 1:\n        return arr\n    else:\n        pivot = arr[0]\n        less = [x for x in arr[1:] if x <= pivot]\n        greater = [x for x in arr[1:] if x > pivot]\n        return quick_sort(less) + [pivot] + quick_sort(greater) \nQuick Sort is a sorting algorithm that works by selecting a 'pivot' element, then rearranging the list so that all elements smaller than the pivot come before it and all greater elements come after it, and then recursively sorting the sublists..\nTime: O(n log n), Space: O(log n), Stable: No",
    "Heap Sort": "Heap Sort is a sorting algorithm that uses a binary heap data structure. It works by first building a max-heap from the input array, where the largest element is at the root. Then, the root is swapped with the last element of the heap and removed from the heap. This process is repeated by heapifying the remaining elements until the entire array is sorted. In Python, it can be implemented as:\ndef heapify(arr, n, i):\n    largest = i\n    left = 2 * i + 1\n    right = 2 * i + 2\n    if left < n and arr[left] > arr[largest]:\n        largest = left\n    if right < n and arr[right] > arr[largest]:\n        largest = right\n    if largest != i:\n        arr[i], arr[largest] = arr[largest], arr[i]\n        heapify(arr, n, largest)\n\ndef heap_sort(arr):\n    n = len(arr)\n    for i in range(n // 2 - 1, -1, -1):\n        heapify(arr, n, i)\n    for i in range(n - 1, 0, -1):\n        arr[i], arr[0] = arr[0], arr[i]\n        heapify(arr, i, 0) \nHeap Sort is a sorting algorithm that builds a special tree-based structure called a heap, then repeatedly removes the largest (or smallest) element from the heap and places it into the sorted part of the list..\nTime: O(n log n), Space: O(1), Stable: No",
}

# Algorithms
def play_swap_sound():
    pygame.mixer.Sound.play(swap_sound)

def bubble_sort(data, draw, speed, log_step):
    n = len(data)
    for i in range(n):
        for j in range(n - i - 1):
            draw(data, [j, j + 1])
            log_step(f"Comparing {j} and {j+1}")
            time.sleep(speed * 1.5)
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                play_swap_sound()
                draw(data, [j, j + 1])
                log_step(f"Swapped {j} and {j+1}")
                time.sleep(speed * 1.5)

def merge_sort(data, draw, speed, log_step):
    def merge_sort_rec(arr, left, right):
        if left < right:
            mid = (left + right) // 2
            merge_sort_rec(arr, left, mid)
            merge_sort_rec(arr, mid + 1, right)
            merge(arr, left, mid, right)

    def merge(arr, left, mid, right):
        L = arr[left:mid+1]
        R = arr[mid+1:right+1]
        i = j = 0
        k = left
        while i < len(L) and j < len(R):
            if L[i] <= R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            play_swap_sound()
            draw(arr, list(range(left, right+1)))
            log_step(f"Merging index {k}")
            time.sleep(speed * 1.5)
            k += 1
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

    merge_sort_rec(data, 0, len(data)-1)

def quick_sort(data, draw, speed, log_step):
    def partition(low, high):
        pivot = data[high]
        i = low - 1
        for j in range(low, high):
            draw(data, [j, high])
            time.sleep(speed * 1.5)
            if data[j] < pivot:
                i += 1
                data[i], data[j] = data[j], data[i]
                play_swap_sound()
                draw(data, [i, j])
                log_step(f"Swapped {i} and {j}")
                time.sleep(speed * 1.5)
        data[i+1], data[high] = data[high], data[i+1]
        play_swap_sound()
        return i + 1

    def quick_sort_rec(low, high):
        if low < high:
            pi = partition(low, high)
            quick_sort_rec(low, pi - 1)
            quick_sort_rec(pi + 1, high)

    quick_sort_rec(0, len(data)-1)

def heap_sort(data, draw, speed, log_step):
    def heapify(n, i):
        largest = i
        l = 2*i + 1
        r = 2*i + 2
        if l < n and data[l] > data[largest]:
            largest = l
        if r < n and data[r] > data[largest]:
            largest = r
        if largest != i:
            data[i], data[largest] = data[largest], data[i]
            play_swap_sound()
            draw(data, [i, largest])
            log_step(f"Swapped {i} and {largest}")
            time.sleep(speed * 1.5)
            heapify(n, largest)

    n = len(data)
    for i in range(n//2 - 1, -1, -1):
        heapify(n, i)
    for i in range(n-1, 0, -1):
        data[i], data[0] = data[0], data[i]
        play_swap_sound()
        draw(data, [i, 0])
        log_step(f"Swapped root with index {i}")
        time.sleep(speed * 1.5)
        heapify(i, 0)

# GUI App
class SortingVisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔍 Shiva's Sorting Visualizer")
        self.algorithms = {
            "Bubble Sort": bubble_sort,
            "Merge Sort": merge_sort,
            "Quick Sort": quick_sort,
            "Heap Sort": heap_sort,
        }
        self.speed = 0.3
        self.num_values = 10
        self.selected_algo = tk.StringVar(value="Bubble Sort")
        self.data = []
        self.setup_ui()

    def setup_ui(self):
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        ttk.Label(self.control_frame, text="Algorithm:", font=("poppins", 30, "bold")).pack(pady=(15, 5))
        algo_menu = ttk.Combobox(self.control_frame, values=list(self.algorithms.keys()), textvariable=self.selected_algo)
        algo_menu.pack()

        ttk.Button(self.control_frame, text="🎬 Visualize", command=self.start_sorting).pack(pady=20)
        ttk.Button(self.control_frame, text="📘 Show Theory", command=self.show_theory).pack(pady=10)
        ttk.Button(self.control_frame, text="⌨️ Enter Value Count", command=self.prompt_value_count).pack(pady=5)

        self.fig, self.ax = plt.subplots()
        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.text_area = tk.Text(self.root, height=10, font=("Helvetica", 20), bg="#2A2F4F", fg="#f9fafb", insertbackground="white")
        self.text_area.pack(fill=tk.X, padx=10, pady=5)
        self.text_area.insert(tk.END, "🧠 Step-by-step explanation will appear here...")

    def draw_data(self, data, color_indices=[]):
        self.ax.clear()
        bar_colors = ["#917FB3" if i not in color_indices else "#E5BEEC" for i in range(len(data))]
        self.ax.bar(range(len(data)), data, color=bar_colors)
        self.canvas.draw()

    def show_theory(self):
        theory = algorithm_theories.get(self.selected_algo.get(), "No theory available.")
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, theory)

    def prompt_value_count(self):
        value = simpledialog.askinteger("Enter Number", "Enter number of bars (10 - 100):", minvalue=10, maxvalue=100)
        if value:
            self.num_values = value

    def log_step(self, step_text):
        self.text_area.insert(tk.END, f"\n{step_text}")
        self.text_area.see(tk.END)

    def start_sorting(self):
        self.data = [random.randint(1, 100) for _ in range(self.num_values)]
        self.draw_data(self.data)
        algo_func = self.algorithms[self.selected_algo.get()]
        self.text_area.delete("1.0", tk.END)
        threading.Thread(target=lambda: algo_func(self.data, self.draw_data, self.speed, self.log_step)).start()

# Run
if __name__ == "__main__":
    root = tk.Tk()
    app = SortingVisualizerApp(root)
    root.mainloop()
