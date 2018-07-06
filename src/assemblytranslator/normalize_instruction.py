import re


def normalize(instruction):
    normalized_instruction = instruction.lower()

    normalized_instruction = add_ptr_id_needed(normalized_instruction)

    normalized_instruction = remove_consecutive_white_spaces(normalized_instruction)

    normalized_instruction = remove_spaces_between_operands(normalized_instruction)

    normalized_instruction = normalize_operands(normalized_instruction)

    return normalized_instruction


def remove_consecutive_white_spaces(instruction):
    return re.sub("\s+", " ", instruction)


def add_ptr_id_needed(instruction):
    normalized_instruction = instruction

    if "ptr" not in instruction:
        for keyword in ["byte", "word", "dword", "qword"]:
            if keyword in instruction:
                normalized_instruction = normalized_instruction.replace(keyword, keyword + " ptr ")
                break
    else:
        normalized_instruction = normalized_instruction.replace("ptr", " ptr ")

    return normalized_instruction


def remove_spaces_between_operands(instruction):
    normalized_instruction = instruction

    for single_case in [" , ", ", ", " ,"]:
        normalized_instruction = normalized_instruction.replace(single_case, ",")

    return normalized_instruction


def normalize_operands(instruction):
    operands = (" ".join(instruction.split(" ")[1:])).split(",")

    normalized_operands = [normalize_operand(operand) for operand in operands]

    return instruction.split(" ")[0] + " " + ",".join(normalized_operands)


def normalize_operand(operand):
    if "[" in operand:
        tokens = operand.split("[")

        normalized_operand = tokens[0] + "[" + tokens[1].replace(" ", "")
    else:
        normalized_operand = operand

    return normalized_operand
