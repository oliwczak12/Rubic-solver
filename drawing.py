

def gridDrawRec(canvas, x, y, cell_size, rows, cols):
    rec_list = canvas.grid.rec_list
    for i in range(rows):
        for j in range(cols):
            if len(rec_list) > 8:
                canvas.delete(rec_list.pop(0))
            rec_list.append(canvas.create_rectangle(x + (cell_size * i), y + (cell_size * j), x + (cell_size * (i + 1)), y + (cell_size * (j + 1)), outline="green", width=4))
