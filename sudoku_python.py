import tkinter as tk
from tkinter import messagebox, ttk

class SudokuSolver:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.root.configure(bg='#f0f0f0')  # Light gray background
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        
        # Use ttk Style for better-looking widgets
        style = ttk.Style()
        style.configure('TEntry', font=('Arial', 18), padding=5)
        style.configure('TButton', font=('Arial', 12, 'bold'), padding=10)
        style.configure('TLabel', font=('Arial', 10), background='#f0f0f0')

        self.create_grid()

        # Add import string feature
        import_frame = tk.Frame(self.root, bg='#f0f0f0')
        import_frame.grid(row=11, column=0, columnspan=9, pady=10, sticky='ew')
        
        tk.Label(import_frame, text="Import 81-char string (0 or . for empty):", bg='#f0f0f0', font=('Arial', 10)).pack(side='left', padx=5)
        self.import_entry = tk.Entry(import_frame, width=50, font=('Arial', 10))
        self.import_entry.pack(side='left', expand=True, fill='x', padx=5)

        load_button = ttk.Button(self.root, text="Load String", command=self.load_from_string, style='TButton')
        load_button.grid(row=12, column=0, columnspan=9, pady=5)

        solve_button = ttk.Button(self.root, text="Solve", command=self.solve_sudoku, style='TButton')
        solve_button.grid(row=9, column=0, columnspan=9, pady=10)

        clear_button = ttk.Button(self.root, text="Clear", command=self.clear_grid, style='TButton')
        clear_button.grid(row=10, column=0, columnspan=9, pady=5)

    def create_grid(self):
        grid_frame = tk.Frame(self.root, bg='#ffffff', bd=2, relief='ridge')  # White frame with border
        grid_frame.grid(row=0, column=0, columnspan=9, rowspan=9, padx=20, pady=20)

        for i in range(9):
            for j in range(9):
                frame = tk.Frame(grid_frame, bg='#ffffff', bd=1, relief='solid')  # Cell frame for borders
                frame.grid(row=i, column=j, sticky='nsew')
                
                entry = ttk.Entry(frame, width=3, justify='center', style='TEntry')
                entry.pack(fill='both', expand=True)
                self.entries[i][j] = entry

                # Thicker borders for 3x3 subgrids
                if i % 3 == 0:
                    frame.grid(pady=(2, 0))
                if j % 3 == 0:
                    frame.grid(padx=(2, 0))
                if i % 3 == 2:
                    frame.grid(pady=(0, 2))
                if j % 3 == 2:
                    frame.grid(padx=(0, 2))

        # Make grid responsive
        for i in range(9):
            grid_frame.rowconfigure(i, weight=1)
            grid_frame.columnconfigure(i, weight=1)

    def load_from_string(self):
        s = self.import_entry.get().strip()
        if len(s) != 81:
            messagebox.showerror("Invalid String", "String must be exactly 81 characters long.")
            return

        board = []
        try:
            for i in range(9):
                row = []
                for j in range(9):
                    char = s[i*9 + j]
                    if char in '123456789':
                        row.append(int(char))
                    elif char in '0.':
                        row.append(0)
                    else:
                        raise ValueError
                board.append(row)
            self.set_board(board)
            messagebox.showinfo("Success", "Sudoku loaded from string!")
        except ValueError:
            messagebox.showerror("Invalid String", "String must contain only 0-9 or '.' for empty cells.")

    def get_board(self):
        board = []
        for i in range(9):
            row = []
            for j in range(9):
                val = self.entries[i][j].get()
                if val == '':
                    row.append(0)
                else:
                    try:
                        num = int(val)
                        if 1 <= num <= 9:
                            row.append(num)
                        else:
                            raise ValueError
                    except ValueError:
                        messagebox.showerror("Invalid Input", f"Invalid number at row {i+1}, column {j+1}. Must be 1-9 or empty.")
                        return None
            board.append(row)
        return board

    def set_board(self, board):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                if board[i][j] != 0:
                    self.entries[i][j].insert(0, str(board[i][j]))
                    self.entries[i][j].configure(state='disabled')  # Lock pre-filled cells
                else:
                    self.entries[i][j].configure(state='normal')

    def clear_grid(self):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].configure(state='normal')
                self.entries[i][j].delete(0, tk.END)
        self.import_entry.delete(0, tk.END)

    def solve_sudoku(self):
        board = self.get_board()
        if board is None:
            return

        # Unlock all cells before solving
        for i in range(9):
            for j in range(9):
                self.entries[i][j].configure(state='normal')

        if self.solve(board):
            self.set_board(board)  # This will lock pre-filled, but since solved, maybe lock all?
            messagebox.showinfo("Success", "Sudoku solved!")
        else:
            messagebox.showerror("Error", "No solution exists for this Sudoku.")

    def find_empty(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None

    def is_valid(self, board, num, pos):
        row, col = pos

        # Check row
        for j in range(9):
            if board[row][j] == num and col != j:
                return False

        # Check column
        for i in range(9):
            if board[i][col] == num and row != i:
                return False

        # Check 3x3 box
        box_x = col // 3
        box_y = row // 3
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if board[i][j] == num and (i, j) != pos:
                    return False

        return True

    def solve(self, board):
        empty = self.find_empty(board)
        if not empty:
            return True  # Solved

        row, col = empty
        for num in range(1, 10):
            if self.is_valid(board, num, (row, col)):
                board[row][col] = num
                if self.solve(board):
                    return True
                board[row][col] = 0  # Backtrack
        return False

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x700")  # Set a fixed size for better appearance
    app = SudokuSolver(root)
    root.mainloop()