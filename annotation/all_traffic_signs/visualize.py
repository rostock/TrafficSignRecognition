#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def txt_to_grid_markdown(input_file, output_file, columns=3):
    try:
        with open(input_file, "r", encoding="utf-8") as infile:
            lines = [line.strip() for line in infile if line.strip()]
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found!")
        return

    cells = []
    for line in lines:
        parts = line.split('_', 1)
        if len(parts) != 2:
            continue
        number = parts[0]
        name = parts[1]
        cell_content = (
            f"<img src='https://raw.githubusercontent.com/rostock/3DModels/main/Thumbnails/Verkehrszeichen/{number}.jpg' width='50px' /><br>"
            f"{number}<br>{name}"
        )
        cells.append(cell_content)

    table_lines = []
    table_lines.append("<table>")
    for i in range(0, len(cells), columns):
        table_lines.append("  <tr>")
        row_cells = cells[i : i + columns]
        if len(row_cells) < columns:
            row_cells.extend([""] * (columns - len(row_cells)))
        for cell in row_cells:
            table_lines.append(f"    <td align='center'>{cell}</td>")
        table_lines.append("  </tr>")
    table_lines.append("</table>")

    with open(output_file, "w", encoding="utf-8") as outfile:
        outfile.write("# All Traffic Sign Classes\n[About](About.md)"+("\n".join(table_lines)))

if __name__ == "__main__":
    txt_to_grid_markdown("all_traffic_sign_names.txt", "Readme.md")
