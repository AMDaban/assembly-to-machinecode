from .instructions import Commands
from .parse_error import ParseError
from .operands import Operands, how_many_bits, MemoryMode, RegisterMode, reg_op_32_bit, reg_op_64_bit
from .processor_mode import ProcessorMode


def convert(structure, processor_mode):
    if structure["command"] == Commands.MOV:
        print(mov(structure, processor_mode))
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
        return "1000100" +\
               predict_w(second_operand, processor_mode) +\
               "11" +\
               predict_reg_op(second_operand["register"], processor_mode) +\
               predict_reg_op(first_operand["register"], processor_mode)


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

