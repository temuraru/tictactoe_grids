from reportlab.lib.pagesizes import letter, landscape, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak, Spacer
from reportlab.lib import colors


# Function to create a Tic Tac Toe grid
def create_tic_tac_toe_grid(cell_size=20):
    data = [[' ' for _ in range(3)] for _ in range(3)]
    table = Table(data, colWidths=cell_size, rowHeights=cell_size)
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 20),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER')
    ]))
    return table


# Function to generate the PDF document with the grid layout
def generate_pdf_with_grids(filename, pages, rows, cols, grid_elements_nr, side_space):
    print("pages:", pages)
    page_width, page_height = A4
    # Calculate the available width and height for the grids and also margins
    available_width = page_width - 2 * side_space
    available_height = page_height - 2 * side_space
    grid_element_size_h = int(available_width / (cols * (grid_elements_nr + 1)))
    grid_element_size_v = int(available_height / (rows * (grid_elements_nr + 1)))
    cell_size = min(grid_element_size_h, grid_element_size_v)
    margin_h = side_space + int(grid_element_size_h / 2)
    margin_v = side_space - int(grid_element_size_v / 2)

    doc = SimpleDocTemplate(filename, pagesize=A4, leftMargin=margin_h, bottomMargin=margin_v, topMargin=margin_v)
    elements = []
    for page in range(pages):
        if page > 0:
            elements.append(PageBreak())  # Add a page break between pages
        for _ in range(rows):
            row_elements = []
            for _ in range(cols):
                tic_tac_toe_grid = create_tic_tac_toe_grid(cell_size)
                row_elements.append(tic_tac_toe_grid)

            # Combine the grids into a single row
            col_widths = [grid_element_size_h * (grid_elements_nr + 1)] * cols
            row_heights = [grid_element_size_v * grid_elements_nr]
            combined_grid = Table([row_elements], colWidths=col_widths, rowHeights=row_heights)

            # Add current row to the document
            elements.append(combined_grid)
            # elements.append(PageBreak())  # Add a page break between rows
            elements.append(Spacer(1, grid_element_size_v))  # Add space between rows
        # elements.append(Spacer(1, grid_element_size_v))  # Add space between pages

    doc.build(elements)


if __name__ == "__main__":
    rows = 6  # Number of rows
    cols = 3  # Number of columns
    pages = 4  # Number of pages in the document
    grid_elements_nr = 3  # nr of cells in a grid (same for horizontal and vertical)
    side_space = 50
    if pages > 1:
        output_filename = f"tic_tac_toe_grid_{pages}pages_x_{rows}x{cols}_x_{grid_elements_nr}x{grid_elements_nr}.pdf"
    else:
        output_filename = f"tic_tac_toe_grid_{rows}x{cols}_x_{grid_elements_nr}x{grid_elements_nr}.pdf"
    generate_pdf_with_grids(output_filename, pages, rows, cols, grid_elements_nr, side_space)
