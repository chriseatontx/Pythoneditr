import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font
import os

class SimpleTextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Text Editor")
        self.root.geometry("800x600")
        self.root.minsize(400, 300)
        
        # Configure the icon (use default Windows icon)
        try:
            self.root.iconbitmap(default=True)
        except:
            pass
        
        # Current file tracking
        self.current_file = None
        self.is_modified = False
        
        # Create the main interface
        self.create_menu()
        self.create_toolbar()
        self.create_text_area()
        self.create_status_bar()
        
        # Bind events
        self.bind_events()
        
        # Set focus to text area
        self.text_area.focus_set()
    
    def create_menu(self):
        """Create the menu bar"""
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        
        # File menu
        file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open...", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self.save_file_as, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_app, accelerator="Alt+F4")
        
        # Edit menu
        edit_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self.redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=self.cut, accelerator="Ctrl+X")
        edit_menu.add_command(label="Copy", command=self.copy, accelerator="Ctrl+C")
        edit_menu.add_command(label="Paste", command=self.paste, accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All", command=self.select_all, accelerator="Ctrl+A")
        edit_menu.add_command(label="Find...", command=self.find, accelerator="Ctrl+F")
        
        # Format menu
        format_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Format", menu=format_menu)
        format_menu.add_command(label="Font...", command=self.choose_font)
        format_menu.add_command(label="Word Wrap", command=self.toggle_word_wrap)
        
        # View menu
        view_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Status Bar", command=self.toggle_status_bar)
        
        # Help menu
        help_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_toolbar(self):
        """Create the toolbar"""
        self.toolbar = ttk.Frame(self.root)
        self.toolbar.pack(side=tk.TOP, fill=tk.X, padx=2, pady=2)
        
        # Toolbar buttons
        ttk.Button(self.toolbar, text="New", command=self.new_file, width=8).pack(side=tk.LEFT, padx=2)
        ttk.Button(self.toolbar, text="Open", command=self.open_file, width=8).pack(side=tk.LEFT, padx=2)
        ttk.Button(self.toolbar, text="Save", command=self.save_file, width=8).pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(self.toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        ttk.Button(self.toolbar, text="Cut", command=self.cut, width=8).pack(side=tk.LEFT, padx=2)
        ttk.Button(self.toolbar, text="Copy", command=self.copy, width=8).pack(side=tk.LEFT, padx=2)
        ttk.Button(self.toolbar, text="Paste", command=self.paste, width=8).pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(self.toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        ttk.Button(self.toolbar, text="Find", command=self.find, width=8).pack(side=tk.LEFT, padx=2)
    
    def create_text_area(self):
        """Create the main text editing area"""
        # Frame for text area and scrollbars
        text_frame = ttk.Frame(self.root)
        text_frame.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        
        # Text widget with scrollbars
        self.text_area = tk.Text(text_frame, wrap=tk.WORD, undo=True, maxundo=50)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.text_area.yview)
        h_scrollbar = ttk.Scrollbar(text_frame, orient=tk.HORIZONTAL, command=self.text_area.xview)
        
        self.text_area.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout
        self.text_area.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Configure grid weights
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)
        
        # Set default font
        default_font = font.nametofont("TkDefaultFont")
        self.text_area.configure(font=(default_font.cget("family"), 11))
    
    def create_status_bar(self):
        """Create the status bar"""
        self.status_bar = ttk.Frame(self.root)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_label = ttk.Label(self.status_bar, text="Ready")
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        # Line and column indicator
        self.line_col_label = ttk.Label(self.status_bar, text="Line 1, Column 1")
        self.line_col_label.pack(side=tk.RIGHT, padx=5)
    
    def bind_events(self):
        """Bind keyboard shortcuts and events"""
        # File operations
        self.root.bind('<Control-n>', lambda e: self.new_file())
        self.root.bind('<Control-o>', lambda e: self.open_file())
        self.root.bind('<Control-s>', lambda e: self.save_file())
        self.root.bind('<Control-Shift-S>', lambda e: self.save_file_as())
        
        # Edit operations
        self.root.bind('<Control-z>', lambda e: self.undo())
        self.root.bind('<Control-y>', lambda e: self.redo())
        self.root.bind('<Control-x>', lambda e: self.cut())
        self.root.bind('<Control-c>', lambda e: self.copy())
        self.root.bind('<Control-v>', lambda e: self.paste())
        self.root.bind('<Control-a>', lambda e: self.select_all())
        self.root.bind('<Control-f>', lambda e: self.find())
        
        # Text modification tracking
        self.text_area.bind('<KeyPress>', self.on_text_change)
        self.text_area.bind('<Button-1>', self.update_cursor_position)
        self.text_area.bind('<KeyRelease>', self.update_cursor_position)
        
        # Window close event
        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)
    
    def new_file(self):
        """Create a new file"""
        if self.check_unsaved():
            self.text_area.delete(1.0, tk.END)
            self.current_file = None
            self.is_modified = False
            self.update_title()
            self.status_label.config(text="New file created")
    
    def open_file(self):
        """Open an existing file"""
        if self.check_unsaved():
            file_path = filedialog.askopenfilename(
                title="Open File",
                filetypes=[
                    ("Text files", "*.txt"),
                    ("Python files", "*.py"),
                    ("All files", "*.*")
                ]
            )
            
            if file_path:
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        self.text_area.delete(1.0, tk.END)
                        self.text_area.insert(1.0, content)
                        
                    self.current_file = file_path
                    self.is_modified = False
                    self.update_title()
                    self.status_label.config(text=f"Opened: {os.path.basename(file_path)}")
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Could not open file:\n{str(e)}")
    
    def save_file(self):
        """Save the current file"""
        if self.current_file:
            try:
                content = self.text_area.get(1.0, tk.END + '-1c')
                with open(self.current_file, 'w', encoding='utf-8') as file:
                    file.write(content)
                
                self.is_modified = False
                self.update_title()
                self.status_label.config(text=f"Saved: {os.path.basename(self.current_file)}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file:\n{str(e)}")
        else:
            self.save_file_as()
    
    def save_file_as(self):
        """Save the file with a new name"""
        file_path = filedialog.asksaveasfilename(
            title="Save As",
            defaultextension=".txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("Python files", "*.py"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                content = self.text_area.get(1.0, tk.END + '-1c')
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                
                self.current_file = file_path
                self.is_modified = False
                self.update_title()
                self.status_label.config(text=f"Saved as: {os.path.basename(file_path)}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file:\n{str(e)}")
    
    def undo(self):
        """Undo last action"""
        try:
            self.text_area.edit_undo()
        except tk.TclError:
            pass
    
    def redo(self):
        """Redo last undone action"""
        try:
            self.text_area.edit_redo()
        except tk.TclError:
            pass
    
    def cut(self):
        """Cut selected text"""
        try:
            self.text_area.event_generate("<<Cut>>")
        except tk.TclError:
            pass
    
    def copy(self):
        """Copy selected text"""
        try:
            self.text_area.event_generate("<<Copy>>")
        except tk.TclError:
            pass
    
    def paste(self):
        """Paste text from clipboard"""
        try:
            self.text_area.event_generate("<<Paste>>")
        except tk.TclError:
            pass
    
    def select_all(self):
        """Select all text"""
        self.text_area.tag_add(tk.SEL, "1.0", tk.END)
        self.text_area.mark_set(tk.INSERT, "1.0")
        self.text_area.see(tk.INSERT)
        return 'break'
    
    def find(self):
        """Open find dialog"""
        find_window = tk.Toplevel(self.root)
        find_window.title("Find")
        find_window.geometry("300x100")
        find_window.resizable(False, False)
        find_window.transient(self.root)
        find_window.grab_set()
        
        ttk.Label(find_window, text="Find:").pack(pady=5)
        
        find_entry = ttk.Entry(find_window, width=30)
        find_entry.pack(pady=5)
        find_entry.focus_set()
        
        def do_find():
            search_text = find_entry.get()
            if search_text:
                # Clear previous search highlights
                self.text_area.tag_remove("search", "1.0", tk.END)
                
                # Find and highlight all occurrences
                start = "1.0"
                while True:
                    pos = self.text_area.search(search_text, start, stopindex=tk.END)
                    if not pos:
                        break
                    
                    end = f"{pos}+{len(search_text)}c"
                    self.text_area.tag_add("search", pos, end)
                    start = end
                
                # Configure search tag
                self.text_area.tag_config("search", background="yellow")
                
                # Move to first occurrence
                first_pos = self.text_area.search(search_text, "1.0", stopindex=tk.END)
                if first_pos:
                    self.text_area.see(first_pos)
                    self.text_area.mark_set(tk.INSERT, first_pos)
        
        ttk.Button(find_window, text="Find All", command=do_find).pack(pady=5)
        
        find_entry.bind('<Return>', lambda e: do_find())
    
    def choose_font(self):
        """Open font selection dialog"""
        current_font = self.text_area.cget("font")
        
        # Simple font dialog (you could use tkinter.font.Font for more advanced options)
        font_window = tk.Toplevel(self.root)
        font_window.title("Font")
        font_window.geometry("300x200")
        font_window.resizable(False, False)
        font_window.transient(self.root)
        font_window.grab_set()
        
        ttk.Label(font_window, text="Font Family:").pack(pady=5)
        family_var = tk.StringVar(value="Consolas")
        family_combo = ttk.Combobox(font_window, textvariable=family_var, 
                                   values=["Consolas", "Courier New", "Arial", "Times New Roman", "Calibri"])
        family_combo.pack(pady=5)
        
        ttk.Label(font_window, text="Font Size:").pack(pady=5)
        size_var = tk.StringVar(value="11")
        size_combo = ttk.Combobox(font_window, textvariable=size_var, 
                                 values=["8", "9", "10", "11", "12", "14", "16", "18", "20", "24"])
        size_combo.pack(pady=5)
        
        def apply_font():
            try:
                self.text_area.configure(font=(family_var.get(), int(size_var.get())))
                font_window.destroy()
            except:
                messagebox.showerror("Error", "Invalid font settings")
        
        ttk.Button(font_window, text="Apply", command=apply_font).pack(pady=10)
    
    def toggle_word_wrap(self):
        """Toggle word wrap"""
        current_wrap = self.text_area.cget("wrap")
        new_wrap = tk.NONE if current_wrap == tk.WORD else tk.WORD
        self.text_area.configure(wrap=new_wrap)
        
        wrap_status = "enabled" if new_wrap == tk.WORD else "disabled"
        self.status_label.config(text=f"Word wrap {wrap_status}")
    
    def toggle_status_bar(self):
        """Toggle status bar visibility"""
        if self.status_bar.winfo_viewable():
            self.status_bar.pack_forget()
        else:
            self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo("About", 
                           "Simple Text Editor\n\n"
                           "A basic text editor built with Python and tkinter.\n"
                           "Features include file operations, editing tools, and basic formatting.")
    
    def on_text_change(self, event=None):
        """Handle text changes"""
        if not self.is_modified:
            self.is_modified = True
            self.update_title()
    
    def update_cursor_position(self, event=None):
        """Update cursor position in status bar"""
        try:
            line, col = self.text_area.index(tk.INSERT).split('.')
            self.line_col_label.config(text=f"Line {line}, Column {int(col) + 1}")
        except:
            pass
    
    def update_title(self):
        """Update window title"""
        filename = os.path.basename(self.current_file) if self.current_file else "Untitled"
        modified_indicator = "*" if self.is_modified else ""
        self.root.title(f"{filename}{modified_indicator} - Simple Text Editor")
    
    def check_unsaved(self):
        """Check for unsaved changes"""
        if self.is_modified:
            response = messagebox.askyesnocancel(
                "Unsaved Changes",
                "You have unsaved changes. Do you want to save before continuing?"
            )
            
            if response is True:  # Yes - save
                self.save_file()
                return not self.is_modified  # Return True if save was successful
            elif response is False:  # No - don't save
                return True
            else:  # Cancel
                return False
        
        return True
    
    def exit_app(self):
        """Exit the application"""
        if self.check_unsaved():
            self.root.destroy()

def main():
    root = tk.Tk()
    editor = SimpleTextEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()
