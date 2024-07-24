import tkinter as tk
from BiobankApp import BiobankApp

def main():
    root = tk.Tk()
    app = BiobankApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()