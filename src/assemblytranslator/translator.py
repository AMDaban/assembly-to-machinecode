from .normalize_instruction import normalize
from .processor_mode import ProcessorMode
from .extract_structure import extract_structure
from .convert import convert


def translate(instruction, processor_mode=ProcessorMode.MODE_32):
    normalized_instruction = normalize(instruction)

    instruction_structure = extract_structure(normalized_instruction)

    convert(instruction_structure, processor_mode)

    return normalized_instruction

