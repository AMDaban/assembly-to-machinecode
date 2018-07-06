from .normalize_instruction import normalize
from .processor_mode import ProcessorMode
from .extract_structure import extract_structure
from pprint import pprint


def translate(instruction, processor_mode=ProcessorMode.MODE_32):
    normalized_instruction = normalize(instruction)

    pprint(extract_structure(normalized_instruction))

    return normalized_instruction

