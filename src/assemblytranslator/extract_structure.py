from .instructions import Commands
from .parse_error import ParseError
from .operands import Operands, Registers, MemoryMode
import re


def extract_structure(instruction):
    extracted_command = instruction.split(" ")[0]

    instruction_without_command = instruction.replace(extracted_command, "")

    first_operand = instruction_without_command.split(",")[0]

    second_operand = None
    if "," in instruction:
        second_operand = instruction_without_command.split(",")[1]

    structure = {
        "command": get_command(extracted_command),
        "first_operand": get_operand_structure(first_operand)
    }

    if second_operand is not None:
        structure.update({
            "second_operand": get_operand_structure(second_operand)
        })

    return structure


def get_command(command_str):
    try:
        return Commands(command_str)
    except ValueError:
        raise ParseError("command not found: \"{0}\"".format(command_str))


def get_operand_structure(operand):
    if "[" in operand:
        return get_mem_operand_structure(operand)
    else:
        operand_without_space = operand.replace(" ", "")

        pattern_1 = re.compile("[0-9]+$")
        pattern_2 = re.compile("0x([0-9a-f]+)$")

        if re.match(pattern_1, operand_without_space)\
                or re.match(pattern_2, operand_without_space):
            return {
                "type": Operands.DATA,
                "value": operand_without_space
            }
        else:
            try:
                return {
                    "type": Operands.REG,
                    "register": Registers(operand_without_space)
                }
            except ValueError:
                raise ParseError("invalid operand: \"{0}\"".format(operand_without_space))


def get_mem_operand_structure(m_operand):
    is_displacement_negative = False
    if "-" in m_operand:
        is_displacement_negative = True
        m_operand = m_operand.replace("-", "+")

    main_exp_parts = (m_operand[m_operand.find("[") + 1:m_operand.find("]")]).split("+")

    mem_operand_parse_results = []
    for part in main_exp_parts:
        pattern_1 = re.compile("[0-9]+$")
        pattern_2 = re.compile("0x([0-9a-f]+)$")

        if re.match(pattern_1, part) \
                or re.match(pattern_2, part):
            mem_operand_parse_results.append({
                "type": Operands.DATA,
                "value": part
            })
        elif "*" not in part:
            try:
                target_register = Registers(part)
            except ValueError:
                raise ParseError("register not found: \"{0}\"".format(part))

            mem_operand_parse_results.append({
                "type": Operands.REG,
                "register": target_register
            })
        else:
            exp_parts = part.split("*")

            try:
                if exp_parts[0].isdigit():
                    reg_index = 1
                else:
                    reg_index = 0

                mem_operand_parse_results.append({
                    "type": Operands.REG,
                    "register": Registers(exp_parts[reg_index]),
                    "scale": exp_parts[(reg_index + 1) % 2]
                })
            except ValueError:
                raise ParseError("register not found: \"{0}\"".format(part))

        mem_structure = {
            "values": mem_operand_parse_results,
            "type": Operands.MEM,
            "is_displacement_negative": is_displacement_negative
        }

        for mode in ["byte", "word", "dword", "qword"]:
            if mode in m_operand:
                mem_structure.update({
                    "memory_mode": MemoryMode(mode)
                })

    return mem_structure
