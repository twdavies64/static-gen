def markdown_to_blocks(markdown):
    """
    Split markdown text into blocks based on blank lines.
    Strips leading/trailing whitespace from each line.
    """
    if not markdown:
        return []

    # Split into lines
    lines = markdown.splitlines()
    blocks = []
    current_block_lines = []

    for line in lines:
        if line.strip():  # Line has content after stripping
            current_block_lines.append(line.strip())  # Strip each line
        elif current_block_lines:  # Empty line and we have a block to finish
            block = "\n".join(current_block_lines)
            blocks.append(block)
            current_block_lines = []

    # Process the last block if any
    if current_block_lines:
        block = "\n".join(current_block_lines)
        blocks.append(block)

    return blocks
