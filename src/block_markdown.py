from functools import reduce
import re

SUBSTRINGS_TO_STRIP = ["\t"]


def normalize_code_block(block_lines):
    """Normalize the indentation of a multi-line code block."""
    if len(block_lines) <= 2:  # If there's no meaningful body, return as-is
        return block_lines
    body_lines = block_lines[1:-1]  # Extract the body (excluding backticks)
    min_indent = min(
        (len(line) - len(line.lstrip()) for line in body_lines if line.strip()),
        default=0,
    )
    normalized_body = [line[min_indent:] for line in body_lines]
    return [block_lines[0].strip()] + normalized_body + [block_lines[-1].strip()]


def markdown_to_blocks(markdown):
    blocks = [block.strip() for block in markdown.split("\n\n") if block.strip()]
    final = []

    for block in blocks:
        if block.startswith("```"):  # It's a code block
            block_lines = block.split("\n")
            final.append("\n".join(normalize_code_block(block_lines)))
        else:  # It's a regular markdown block
            cleaned_block = reduce(
                lambda x, sub: x.replace(sub, ""), SUBSTRINGS_TO_STRIP, block
            )
            cleaned_block = "\n".join(
                re.sub(r"\s{2,}", " ", line).lstrip()
                for line in cleaned_block.split("\n")
            )
            final.append(cleaned_block)

    return final
