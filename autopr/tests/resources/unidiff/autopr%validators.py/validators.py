






































































































    elif first_line:
        # Search for the line in the file content
        for offset in range(-search_range, search_range + 1):
            check_line_number = current_line_number + offset
            check_file_line = current_file_content[check_line_number]
            if 0 <= check_line_number < len(current_file_content) and line[1:] == check_file_line:
                current_line_number = check_line_number + 1
                # Fix @@ line
                cleaned_lines[-1] = f"@@ -{check_line_number + 1},1 +{check_line_number + 1},1 @@"
                cleaned_lines.append(line)
                break
 