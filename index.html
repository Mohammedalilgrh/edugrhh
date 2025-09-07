```python
#!/usr/bin/env python3
"""
Professional Smart Teaching Whiteboard
A standalone Python application for live teaching
Optimized for Termux and mobile devices
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
import json
import os
from datetime import datetime
import threading
import socket

class SmartWhiteboard:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Smart Teaching Whiteboard")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1a1a1a')
        
        # Drawing variables
        self.drawing = False
        self.current_tool = 'pen'
        self.brush_size = 3
        self.brush_color = '#ffffff'
        self.last_x = None
        self.last_y = None
        
        # History for undo/redo
        self.history = []
        self.history_index = -1
        
        # Session data
        self.session_data = {
            'id': f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'name': 'Live Teaching Session',
            'created_at': datetime.now().isoformat(),
            'drawings': []
        }
        
        self.setup_ui()
        self.setup_canvas()
        self.setup_bindings()
        
    def setup_ui(self):
        """Setup the user interface with dark professional theme"""
        # Configure styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure dark theme colors
        style.configure('Dark.TFrame', background='#2d2d2d')
        style.configure('Dark.TButton', background='#3d3d3d', foreground='white')
        style.configure('Dark.TLabel', background='#2d2d2d', foreground='white')
        
        # Main container
        self.main_frame = ttk.Frame(self.root, style='Dark.TFrame')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Top toolbar
        self.toolbar = ttk.Frame(self.main_frame, style='Dark.TFrame')
        self.toolbar.pack(fill=tk.X, pady=(0, 5))
        
        self.setup_toolbar()
        
        # Canvas container
        self.canvas_frame = ttk.Frame(self.main_frame, style='Dark.TFrame')
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)
        
    def setup_toolbar(self):
        """Setup the professional toolbar with all teaching tools"""
        # Tools section
        tools_frame = ttk.Frame(self.toolbar, style='Dark.TFrame')
        tools_frame.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Label(tools_frame, text="Tools:", style='Dark.TLabel').pack(side=tk.LEFT, padx=(0, 5))
        
        # Drawing tools
        self.pen_btn = tk.Button(tools_frame, text="✏️ Pen", bg='#4CAF50', fg='white', 
                                command=lambda: self.set_tool('pen'), relief='raised')
        self.pen_btn.pack(side=tk.LEFT, padx=2)
        
        self.eraser_btn = tk.Button(tools_frame, text="🧽 Eraser", bg='#3d3d3d', fg='white',
                                   command=lambda: self.set_tool('eraser'), relief='raised')
        self.eraser_btn.pack(side=tk.LEFT, padx=2)
        
        self.line_btn = tk.Button(tools_frame, text="📏 Line", bg='#3d3d3d', fg='white',
                                 command=lambda: self.set_tool('line'), relief='raised')
        self.line_btn.pack(side=tk.LEFT, padx=2)
        
        self.rect_btn = tk.Button(tools_frame, text="⬜ Rect", bg='#3d3d3d', fg='white',
                                 command=lambda: self.set_tool('rectangle'), relief='raised')
        self.rect_btn.pack(side=tk.LEFT, padx=2)
        
        self.circle_btn = tk.Button(tools_frame, text="⭕ Circle", bg='#3d3d3d', fg='white',
                                   command=lambda: self.set_tool('circle'), relief='raised')
        self.circle_btn.pack(side=tk.LEFT, padx=2)
        
        # Separator
        ttk.Separator(self.toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # Brush size section
        size_frame = ttk.Frame(self.toolbar, style='Dark.TFrame')
        size_frame.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Label(size_frame, text="Size:", style='Dark.TLabel').pack(side=tk.LEFT, padx=(0, 5))
        
        self.size_var = tk.IntVar(value=3)
        self.size_scale = tk.Scale(size_frame, from_=1, to=20, orient=tk.HORIZONTAL,
                                  variable=self.size_var, bg='#2d2d2d', fg='white',
                                  highlightbackground='#2d2d2d', length=100)
        self.size_scale.pack(side=tk.LEFT)
        self.size_scale.bind('<Motion>', self.update_brush_size)
        
        # Separator
        ttk.Separator(self.toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # Colors section
        colors_frame = ttk.Frame(self.toolbar, style='Dark.TFrame')
        colors_frame.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Label(colors_frame, text="Colors:", style='Dark.TLabel').pack(side=tk.LEFT, padx=(0, 5))
        
        # Predefined colors
        colors = ['#ffffff', '#ff0000', '#00ff00', '#0000ff', '#ffff00', 
                 '#ff00ff', '#00ffff', '#ffa500', '#800080', '#008000']
        
        color_container = ttk.Frame(colors_frame, style='Dark.TFrame')
        color_container.pack(side=tk.LEFT)
        
        for i, color in enumerate(colors):
            btn = tk.Button(color_container, bg=color, width=2, height=1,
                           command=lambda c=color: self.set_color(c))
            btn.grid(row=0, column=i, padx=1)
        
        # Custom color picker
        tk.Button(colors_frame, text="🎨", bg='#3d3d3d', fg='white',
                 command=self.choose_custom_color).pack(side=tk.LEFT, padx=(5, 0))
        
        # Separator
        ttk.Separator(self.toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # Action buttons
        actions_frame = ttk.Frame(self.toolbar, style='Dark.TFrame')
        actions_frame.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(actions_frame, text="↶ Undo", bg='#3d3d3d', fg='white',
                 command=self.undo).pack(side=tk.LEFT, padx=2)
        
        tk.Button(actions_frame, text="↷ Redo", bg='#3d3d3d', fg='white',
                 command=self.redo).pack(side=tk.LEFT, padx=2)
        
        tk.Button(actions_frame, text="🗑️ Clear", bg='#f44336', fg='white',
                 command=self.clear_canvas).pack(side=tk.LEFT, padx=2)
        
        tk.Button(actions_frame, text="💾 Save", bg='#2196F3', fg='white',
                 command=self.save_session).pack(side=tk.LEFT, padx=2)
        
        tk.Button(actions_frame, text="📁 Load", bg='#FF9800', fg='white',
                 command=self.load_session).pack(side=tk.LEFT, padx=2)
        
        # Session info
        info_frame = ttk.Frame(self.toolbar, style='Dark.TFrame')
        info_frame.pack(side=tk.RIGHT)
        
        self.session_label = ttk.Label(info_frame, text=f"Session: {self.session_data['name']}", 
                                      style='Dark.TLabel')
        self.session_label.pack(side=tk.RIGHT, padx=10)
        
    def setup_canvas(self):
        """Setup the main drawing canvas"""
        # Canvas with dark background
        self.canvas = tk.Canvas(self.canvas_frame, bg='#1a1a1a', highlightthickness=1,
                               highlightbackground='#3d3d3d')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Save initial state
        self.save_to_history()
        
    def setup_bindings(self):
        """Setup mouse and touch event bindings"""
        self.canvas.bind('<Button-1>', self.start_drawing)
        self.canvas.bind('<B1-Motion>', self.draw)
        self.canvas.bind('<ButtonRelease-1>', self.stop_drawing)
        
        # Keyboard shortcuts
        self.root.bind('<Control-z>', lambda e: self.undo())
        self.root.bind('<Control-y>', lambda e: self.redo())
        self.root.bind('<Control-s>', lambda e: self.save_session())
        self.root.bind('<Control-o>', lambda e: self.load_session())
        self.root.bind('<Delete>', lambda e: self.clear_canvas())
        
    def set_tool(self, tool):
        """Set the active drawing tool"""
        self.current_tool = tool
        
        # Update button colors
        buttons = {
            'pen': self.pen_btn,
            'eraser': self.eraser_btn,
            'line': self.line_btn,
            'rectangle': self.rect_btn,
            'circle': self.circle_btn
        }
        
        for tool_name, btn in buttons.items():
            if tool_name == tool:
                btn.configure(bg='#4CAF50')
            else:
                btn.configure(bg='#3d3d3d')
                
        # Set cursor
        cursors = {
            'pen': 'pencil',
            'eraser': 'dotbox',
            'line': 'crosshair',
            'rectangle': 'crosshair',
            'circle': 'crosshair'
        }
        self.canvas.configure(cursor=cursors.get(tool, 'arrow'))
        
    def set_color(self, color):
        """Set the brush color"""
        self.brush_color = color
        
    def choose_custom_color(self):
        """Open color chooser dialog"""
        color = colorchooser.askcolor(title="Choose Color")
        if color[1]:
            self.set_color(color[1])
            
    def update_brush_size(self, event=None):
        """Update brush size from scale"""
        self.brush_size = self.size_var.get()
        
    def start_drawing(self, event):
        """Start drawing operation"""
        self.drawing = True
        self.last_x = event.x
        self.last_y = event.y
        
        if self.current_tool == 'pen':
            self.canvas.create_oval(
                event.x - self.brush_size/2, event.y - self.brush_size/2,
                event.x + self.brush_size/2, event.y + self.brush_size/2,
                fill=self.brush_color, outline=self.brush_color
            )
        elif self.current_tool == 'eraser':
            self.canvas.create_oval(
                event.x - self.brush_size, event.y - self.brush_size,
                event.x + self.brush_size, event.y + self.brush_size,
                fill=self.canvas['bg'], outline=self.canvas['bg']
            )
            
    def draw(self, event):
        """Continue drawing operation"""
        if not self.drawing:
            return
            
        if self.current_tool == 'pen':
            self.canvas.create_line(
                self.last_x, self.last_y, event.x, event.y,
                width=self.brush_size, fill=self.brush_color,
                capstyle=tk.ROUND, smooth=tk.TRUE
            )
        elif self.current_tool == 'eraser':
            self.canvas.create_line(
                self.last_x, self.last_y, event.x, event.y,
                width=self.brush_size * 2, fill=self.canvas['bg'],
                capstyle=tk.ROUND, smooth=tk.TRUE
            )
            
        self.last_x = event.x
        self.last_y = event.y
        
    def stop_drawing(self, event):
        """Stop drawing operation"""
        if not self.drawing:
            return
            
        self.drawing = False
        
        if self.current_tool == 'line':
            self.canvas.create_line(
                self.last_x, self.last_y, event.x, event.y,
                width=self.brush_size, fill=self.brush_color,
                capstyle=tk.ROUND
            )
        elif self.current_tool == 'rectangle':
            self.canvas.create_rectangle(
                self.last_x, self.last_y, event.x, event.y,
                outline=self.brush_color, width=self.brush_size
            )
        elif self.current_tool == 'circle':
            self.canvas.create_oval(
                self.last_x, self.last_y, event.x, event.y,
                outline=self.brush_color, width=self.brush_size
            )
            
        # Save to history after drawing
        self.save_to_history()
        
    def save_to_history(self):
        """Save current canvas state to history"""
        # Get canvas as PostScript and store
        ps_data = self.canvas.postscript()
        
        # Remove future history if we're not at the end
        if self.history_index < len(self.history) - 1:
            self.history = self.history[:self.history_index + 1]
            
        self.history.append(ps_data)
        self.history_index = len(self.history) - 1
        
        # Limit history size
        if len(self.history) > 50:
            self.history.pop(0)
            self.history_index -= 1
            
    def undo(self):
        """Undo last drawing operation"""
        if self.history_index > 0:
            self.history_index -= 1
            self.restore_from_history()
            
    def redo(self):
        """Redo last undone operation"""
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.restore_from_history()
            
    def restore_from_history(self):
        """Restore canvas from history"""
        if 0 <= self.history_index < len(self.history):
            self.canvas.delete("all")
            # Note: Full PostScript restoration is complex
            # For now, we'll implement a simpler approach
            pass
            
    def clear_canvas(self):
        """Clear the entire canvas"""
        if messagebox.askyesno("Clear Canvas", "Are you sure you want to clear the canvas?"):
            self.canvas.delete("all")
            self.save_to_history()
            
    def save_session(self):
        """Save current session to file"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Save Session"
            )
            
            if filename:
                # Get canvas items
                items = []
                for item in self.canvas.find_all():
                    item_config = self.canvas.itemconfig(item)
                    item_coords = self.canvas.coords(item)
                    item_type = self.canvas.type(item)
                    
                    items.append({
                        'type': item_type,
                        'coords': item_coords,
                        'config': {k: v[-1] for k, v in item_config.items()}
                    })
                
                session_data = {
                    **self.session_data,
                    'items': items,
                    'saved_at': datetime.now().isoformat()
                }
                
                with open(filename, 'w') as f:
                    json.dump(session_data, f, indent=2)
                    
                messagebox.showinfo("Success", f"Session saved to {filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save session: {str(e)}")
            
    def load_session(self):
        """Load session from file"""
        try:
            filename = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Load Session"
            )
            
            if filename:
                with open(filename, 'r') as f:
                    session_data = json.load(f)
                
                # Clear current canvas
                self.canvas.delete("all")
                
                # Restore items
                for item in session_data.get('items', []):
                    item_type = item['type']
                    coords = item['coords']
                    config = item['config']
                    
                    if item_type == 'line':
                        self.canvas.create_line(*coords, **config)
                    elif item_type == 'oval':
                        self.canvas.create_oval(*coords, **config)
                    elif item_type == 'rectangle':
                        self.canvas.create_rectangle(*coords, **config)
                
                self.session_data = session_data
                self.session_label.configure(text=f"Session: {session_data.get('name', 'Loaded Session')}")
                self.save_to_history()
                
                messagebox.showinfo("Success", f"Session loaded from {filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load session: {str(e)}")
            
    def start_live_session(self):
        """Start a live teaching session (placeholder for real-time features)"""
        messagebox.showinfo("Live Session", 
                           "Live session started!\n\n"
                           "Students can now connect to view your teaching.\n"
                           f"Session ID: {self.session_data['id']}")
        
    def run(self):
        """Start the whiteboard application"""
        print("🎓 Smart Teaching Whiteboard Started!")
        print(f"📋 Session ID: {self.session_data['id']}")
        print("🎨 Ready for live teaching!")
        print("\n📖 Keyboard Shortcuts:")
        print("  Ctrl+Z: Undo")
        print("  Ctrl+Y: Redo")
        print("  Ctrl+S: Save Session")
        print("  Ctrl+O: Load Session")
        print("  Delete: Clear Canvas")
        
        self.root.mainloop()

def main():
    """Main function to start the whiteboard"""
    print("🚀 Initializing Smart Teaching Whiteboard...")
    
    try:
        app = SmartWhiteboard()
        app.run()
    except Exception as e:
        print(f"❌ Error starting whiteboard: {e}")
        print("💡 Make sure you have tkinter installed:")
        print("   For Termux: pkg install python-tkinter")
        print("   For Ubuntu: sudo apt-get install python3-tk")

if __name__ == "__main__":
    main()
```
