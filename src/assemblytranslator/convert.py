from .instructions import Commands
from .parse_error import ParseError
from .operands import Operands, how_many_bits, MemoryMode, RegisterMode, reg_op_32_bit, reg_op_64_bit, \
    rm_part_16_registers, rm_part_32_registers, Registers, scale_map, rm_part_32_registers_base,\
    rm_part_32_64_registers, rm_part_64_64_registers, has_rex_b, rm_part_32_64_registers_base,\
    rm_part_64_64_registers_base
from .processor_mode import ProcessorMode


def convert(structure, processor_mode):
    if structure["command"] == Commands.MOV:
        return mov(structure, processor_mode)
    else:
        raise ParseError("command not found: \"{0}\"".format(structure["command"]))


def mov(structure, processor_mode):
    try:
        first_operand = structure["first_operand"]
        second_operand = structure["second_operand"]
    except KeyError:
        raise ParseError("MOV command has two operands")
    if first_operand["type"] == Operands.REG and second_operand["type"] == Operands.REG:
        return predict_operand_prefix(first_operand, processor_mode) +\
               "1000100" +\
               predict_w(second_operand, processor_mode) +\
               "11" +\
               predict_reg_op(second_operand["register"], processor_mode) +\
               predict_reg_op(first_operand["register"], processor_mode)
    elif first_operand["type"] == Operands.REG and second_operand["type"] == Operands.MEM:
        print(analyse_memory_operand(second_operand, processor_mode))
        return "asghar"


def predict_w(evidence, processor_mode):
    if evidence["type"] == Operands.REG:
        operand_mode = how_many_bits(evidence["register"])
    else:
        try:
            memory_mode = evidence["memory_mode"]
        except KeyError:
            raise ParseError("operand size unspecified")

        if memory_mode == MemoryMode.BYTE:
            operand_mode = RegisterMode.MODE_8
        elif memory_mode == MemoryMode.WORD:
            operand_mode = RegisterMode.MODE_16
        elif memory_mode == MemoryMode.DWORD:
            operand_mode = RegisterMode.MODE_32
        else:
            operand_mode = RegisterMode.MODE_64

    if processor_mode == ProcessorMode.MODE_32:
        if operand_mode == RegisterMode.MODE_8:
            return "0"
        elif operand_mode == RegisterMode.MODE_16 or operand_mode == RegisterMode.MODE_32:
            return "1"
        else:
            raise ParseError("you are not allowed to use 64 bit mode in 32 bit mode")
    elif processor_mode == ProcessorMode.MODE_64:
        if operand_mode == RegisterMode.MODE_8:
            return "0"
        else:
            return "1"
    else:
        raise ParseError("mode \"{0}\" not supported".format(processor_mode))


def predict_reg_op(register, processor_mode):
    if processor_mode == ProcessorMode.MODE_32:
        try:
            return reg_op_32_bit[register]
        except KeyError:
            raise ParseError("invalid reg/op register: \"{0}\"".format(register))
    else:
        try:
            return reg_op_64_bit[register]
        except KeyError:
            raise ParseError("invalid reg/op register: \"{0}\"".format(register))


def predict_operand_prefix(evidence, processor_mode):
    if evidence["type"] == Operands.REG:
        operand_mode = how_many_bits(evidence["register"])
    else:
        try:
            memory_mode = evidence["memory_mode"]
        except KeyError:
            raise ParseError("operand size unspecified")

        if memory_mode == MemoryMode.BYTE:
            operand_mode = RegisterMode.MODE_8
        elif memory_mode == MemoryMode.WORD:
            operand_mode = RegisterMode.MODE_16
        elif memory_mode == MemoryMode.DWORD:
            operand_mode = RegisterMode.MODE_32
        else:
            operand_mode = RegisterMode.MODE_64

    operand_prefix = "01100110"

    if processor_mode == ProcessorMode.MODE_32:
        if operand_mode == RegisterMode.MODE_16:
            return operand_prefix
    elif processor_mode == ProcessorMode.MODE_64:
        if operand_mode == RegisterMode.MODE_16:
            return operand_prefix
    else:
        raise ParseError("mode \"{0}\" not supported".format(processor_mode))

    return ""


def analyse_memory_operand(mem_operand, processor_mode):
    mode = "00"
    displacement = None

    reg_1 = None
    reg_2 = None
    scale = 0
    scale_index = 0

    for part in mem_operand["values"]:
        if part["type"] == Operands.DATA:
            if part["value"].startswith("0x"):
                value = int(part["value"], 16)
            else:
                value = int(part["value"], 10)

            binary_value = bin(value)[2:]

            if binary_value.startswith("1"):
                binary_value = "0" + binary_value

            true_mem_op = binary_value
            if mem_operand["is_displacement_negative"]:
                toggled_mem_op = ""
                for char in binary_value:
                    if char == "0":
                        toggled_mem_op += "1"
                    else:
                        toggled_mem_op += "0"

                true_mem_op = ""
                reversed_toggled_mem_op = toggled_mem_op[::-1]
                for index, char in enumerate(reversed_toggled_mem_op):
                    if char == "1":
                        true_mem_op += "0"
                    else:
                        true_mem_op += "1"
                        true_mem_op += reversed_toggled_mem_op[index + 1:]
                        break

                true_mem_op = true_mem_op[::-1]

            padding_bit = "1" if mem_operand["is_displacement_negative"] else "0"

            if processor_mode == ProcessorMode.MODE_32:
                if len(true_mem_op) > 16:
                    raise ParseError("displacement larger than 16 bit")
                elif len(true_mem_op) <= 8:
                    mode = "01"
                    displacement = padding_bit * (8 - len(true_mem_op)) + true_mem_op
                else:
                    mode = "10"
                    displacement = padding_bit * (16 - len(true_mem_op)) + true_mem_op
            else:
                if len(true_mem_op) > 32:
                    raise ParseError("displacement larger than 32 bit")
                elif len(true_mem_op) <= 8:
                    mode = "01"
                    displacement = padding_bit * (8 - len(true_mem_op)) + true_mem_op
                else:
                    mode = "10"
                    displacement = padding_bit * (32 - len(true_mem_op)) + true_mem_op

            final_displacement = ""
            for i in range(int(len(displacement) / 8) + 1):
                final_displacement = displacement[i * 8: i * 8 + 8] + final_displacement

            displacement = final_displacement

        if part["type"] == Operands.REG:
            if reg_1 is None:
                reg_1 = part["register"]
                if "scale" in part:
                    scale = int(part["scale"])
                    scale_index = 1
            else:
                reg_2 = part["register"]
                if "scale" in part:
                    scale = int(part["scale"])
                    scale_index = 2

    has_address_prefix = False
    rm_part = ""
    has_sib = False
    scale_part = ""
    base_part = ""
    index_part = ""
    has_rex = False
    rex_x = "0"
    rex_b = "0"

    if reg_1 is None and reg_2 is None:
        mode = "00"
        if processor_mode == ProcessorMode.MODE_32:
            rm_part = "101"
        else:
            rm_part = "100"
            has_sib = True
            scale_part = "00"
            base_part = "101"
            index_part = "100"
    else:
        if scale not in [0, 1, 2, 4, 8]:
            raise ParseError("scale is not allowed: \"{0}\"".format(scale))

        if processor_mode == ProcessorMode.MODE_32:
            if reg_1 is not None:
                if how_many_bits(reg_1) in [RegisterMode.MODE_8, RegisterMode.MODE_64]:
                    raise ParseError("register not allowed: \"{0}\"".format(reg_1))
            if reg_2 is not None:
                if how_many_bits(reg_2) in [RegisterMode.MODE_8, RegisterMode.MODE_64]:
                    raise ParseError("register not allowed: \"{0}\"".format(reg_2))

            if reg_2 is None:
                if reg_1 == Registers.ESP:
                    rm_part = "100"
                    has_sib = True
                    scale_part = "00"
                    index_part = "100"
                    base_part = "100"
                else:
                    if how_many_bits(reg_1) == RegisterMode.MODE_16:
                        has_address_prefix = True
                        try:
                            rm_part = rm_part_16_registers[(reg_1, "")]
                        except KeyError:
                            raise ParseError("invalid base/index")
                    else:
                        try:
                            rm_part = rm_part_32_registers[reg_1]
                        except KeyError:
                            raise ParseError("invalid base/index")
            else:
                if how_many_bits(reg_1) == RegisterMode.MODE_16:
                    if how_many_bits(reg_2) != RegisterMode.MODE_16:
                        raise ParseError("invalid base/index")

                    has_address_prefix = True
                    try:
                        rm_part = rm_part_16_registers[(reg_1, reg_2)]
                        print(rm_part)
                    except KeyError:
                        raise ParseError("invalid base/index")
                else:
                    if how_many_bits(reg_2) != RegisterMode.MODE_32:
                        raise ParseError("invalid base/index")

                    rm_part = "100"
                    has_sib = True

                    if scale == 0:
                        scale = 1
                        if reg_1 != Registers.ESP:
                            scale_index = 1
                        else:
                            scale_index = 2

                    scale_part = scale_map[scale]

                    try:
                        if scale_index == 1:
                            index_part = rm_part_32_registers[reg_1]
                            base_part = rm_part_32_registers_base[reg_2]
                        else:
                            index_part = rm_part_32_registers[reg_2]
                            base_part = rm_part_32_registers_base[reg_1]
                    except KeyError:
                        raise ParseError("invalid index or base register")
        else:
            if reg_1 is not None:
                if how_many_bits(reg_1) in [RegisterMode.MODE_8, RegisterMode.MODE_16]:
                    raise ParseError("register not allowed: \"{0}\"".format(reg_1))
            if reg_2 is not None:
                if how_many_bits(reg_2) in [RegisterMode.MODE_8, RegisterMode.MODE_16]:
                    raise ParseError("register not allowed: \"{0}\"".format(reg_2))

            if reg_2 is None:
                if reg_1 == Registers.RSP:
                    rm_part = "100"
                    has_sib = True
                    scale_part = "00"
                    index_part = "100"
                    base_part = "100"
                elif reg_1 == Registers.ESP:
                    has_address_prefix = True
                    rm_part = "100"
                    has_sib = True
                    scale_part = "00"
                    index_part = "100"
                    base_part = "100"
                else:
                    if how_many_bits(reg_1) == RegisterMode.MODE_32:
                        has_address_prefix = True
                        try:
                            rm_part = rm_part_32_64_registers[reg_1]
                            if reg_1 in has_rex_b:
                                has_rex = True
                                rex_b = "1"
                        except KeyError:
                            raise ParseError("invalid base/index")
                    else:
                        try:
                            rm_part = rm_part_64_64_registers[reg_1]
                            if reg_1 in has_rex_b:
                                has_rex = True
                                rex_b = "1"
                        except KeyError:
                            raise ParseError("invalid base/index")
            else:
                if how_many_bits(reg_1) == RegisterMode.MODE_32:
                    if how_many_bits(reg_2) == RegisterMode.MODE_32:
                        has_address_prefix = True
                        rm_part = "100"
                        has_sib = True

                        if scale == 0:
                            scale = 1
                            if reg_1 != Registers.ESP and reg_1 != Registers.RSP:
                                scale_index = 1
                            else:
                                scale_index = 2

                        scale_part = scale_map[scale]

                        try:
                            if scale_index == 1:
                                index_part = rm_part_32_64_registers[reg_1]
                                if reg_1 in has_rex_b:
                                    has_rex = True
                                    rex_x = "1"
                                base_part = rm_part_32_64_registers_base[reg_2]
                                if reg_2 in has_rex_b:
                                    has_rex = True
                                    rex_b = "1"
                            else:
                                index_part = rm_part_32_64_registers[reg_2]
                                if reg_2 in has_rex_b:
                                    has_rex = True
                                    rex_x = "1"
                                base_part = rm_part_32_64_registers_base[reg_1]
                                if reg_1 in has_rex_b:
                                    has_rex = True
                                    rex_b = "1"
                        except KeyError:
                            raise ParseError("invalid index or base register")

                    else:
                        raise ParseError("invalid base/index")
                else:
                    if how_many_bits(reg_2) == RegisterMode.MODE_32:
                        raise ParseError("invalid base/index")
                    else:
                        rm_part = "100"
                        has_sib = True

                        if scale == 0:
                            scale = 1
                            if reg_1 != Registers.ESP and reg_1 != Registers.RSP:
                                scale_index = 1
                            else:
                                scale_index = 2

                        scale_part = scale_map[scale]

                        try:
                            if scale_index == 1:
                                index_part = rm_part_64_64_registers[reg_1]
                                if reg_1 in has_rex_b:
                                    has_rex = True
                                    rex_x = "1"
                                base_part = rm_part_64_64_registers_base[reg_2]
                                if reg_2 in has_rex_b:
                                    has_rex = True
                                    rex_b = "1"
                            else:
                                index_part = rm_part_64_64_registers[reg_2]
                                if reg_2 in has_rex_b:
                                    has_rex = True
                                    rex_x = "1"
                                base_part = rm_part_64_64_registers_base[reg_1]
                                if reg_1 in has_rex_b:
                                    has_rex = True
                                    rex_b = "1"
                        except KeyError:
                            raise ParseError("invalid base/index")

    return {
        "address_prefix": "01100111" if has_address_prefix else "",
        "mode": mode,
        "rm_part": rm_part,
        "has_sib": has_sib,
        "scale_part": scale_part,
        "index_part": index_part,
        "base_part": base_part,
        "has_displacement": True if displacement is not None else False,
        "displacement": displacement,
        "has_rex": has_rex,
        "rex_x": rex_x,
        "rex_b": rex_b
    }
