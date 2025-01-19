def extract_sections(input_file, output_file_1, output_file_2,
                     title1="capital-common-countries",
                     title2="gram7-past-tense"):
    """
    Extract sections from a file based on specific titles and save them to separate files.

    Args:
        input_file (str): Path to the input file.
        output_file_1 (str): Path to save the first section.
        output_file_2 (str): Path to save the second section.
        title1 (str): The title of the first section to extract.
        title2 (str): The title of the second section to extract.
    """
    current_section = None
    sections = {title1: [], title2: []}

    # Read the file and categorize lines into sections
    with open(input_file, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith(":"):  # Title line
                title = line[1:].strip()  # Remove leading ":" and spaces
                current_section = title if title in sections else None
            elif current_section in sections:
                sections[current_section].append(line)

    # Write the extracted sections to separate files
    with open(output_file_1, 'w') as file1:
        file1.write("\n".join(sections[title1]))

    with open(output_file_2, 'w') as file2:
        file2.write("\n".join(sections[title2]))

    print(f"Data extracted successfully:\n- {title1} saved to {output_file_1}\n- {title2} saved to {output_file_2}")

# File paths
input_file = "test_data/word-test.v1.txt"  # Input file path
output_file_1 = "test_data/capital-common-countries.txt"  # Output file for capital-common-countries
output_file_2 = "test_data/past-tense.txt"  # Output file for past-tense

# Run the extraction
extract_sections(input_file, output_file_1, output_file_2)
