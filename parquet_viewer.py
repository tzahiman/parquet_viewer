import pyarrow.parquet as pq
import tkinter 
from tkinter import *
import tkinter.ttk as ttk
from tkinter import filedialog

def create_window():
    # Create a window
    root = Tk()
    root.title("Parquet File Viewer")
    return root

def choose_file(root):
    # Ask user to choose a parquet file to open
    parquet_file = filedialog.askopenfilename(title = 'Choose a parquet file to open')
    return parquet_file

def read_file(parquet_file):
    # Read the parquet file
    df = pq.read_table(parquet_file).to_pandas()
    return df

def create_view(root, df):
    # Create a dataframe that can be viewed in a GUI window
    df_view = LabelFrame(root, text='Data', padx=5, pady=5, width=5000, height=5000)
    df_view.pack(padx=10, pady=10, expand=True,fill=BOTH)

    # Create the table view
    tree = ttk.Treeview(df_view, columns=tuple(df.columns), show='headings', height=40)
    return tree,df_view

def create_headers(tree, df):
    # Create the table headers
    for col in df.columns:
        tree.heading(col, text=col)

def insert_data(tree, df):
    # Add the table data
    for index, row in df.iterrows():
        tree.insert('', 'end', values=tuple(row))

def add_table(tree):
    # Add the table to the window
    tree.pack(fill=BOTH)
        
        
def sortby(tree, col, descending):
    data = [(tree.set(child, col), child) for child in tree.get_children('')]
    # Sort by the column
    data.sort(reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)
    # Reverse sort to ascending order
    tree.heading(col, command=lambda col=col: sortby(tree, col, int(not descending)))

def add_sort_headers(tree, df):
    # Add column heading to enable sorting
    for col in df.columns:
        tree.heading(col, text=col, command=lambda col=col: sortby(tree, col, False))

# def add_buttons(root, df_view, tree):
#     # Add plus and minus buttons that resize the table view
#     plus_button = Button(root, text='+', command= lambda: plus(tree))
#     minus_button = Button(root, text='-', command= lambda: minus(tree))
#     plus_button.pack(side=TOP, anchor=S)
#     minus_button.pack(side=TOP, anchor=S)

# def plus(tree):
#     # Make the table view bigger
#     tree.config(height=tree.winfo_height()+5)


# def minus(tree):
#     # Make the table view smaller
#     tree.config(height=tree.winfo_height()-5)

def show_table(root):
    # Show the window
    root.mainloop()

# Main Program
root = create_window()
parquet_file = choose_file(root)
df = read_file(parquet_file)
tree,df_view = create_view(root, df)
create_headers(tree, df)
insert_data(tree, df)
add_table(tree)
add_sort_headers(tree, df)
# add_buttons(root, df_view, tree)
show_table(root)