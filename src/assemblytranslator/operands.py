from enum import Enum
from .parse_error import ParseError


class Operands(Enum):
    REG = "reg"
    MEM = "mem"
    DATA = "data"


class Registers(Enum):
    AL = "al"
    AH = "ah"
    AX = "ax"
    EAX = "eax"
    RAX = "rax"
    BL = "bl"
    BH = "bh"
    BX = "bx"
    EBX = "ebx"
    RBX = "rbx"
    CL = "cl"
    CH = "ch"
    CX = "cx"
    ECX = "ecx"
    RCX = "rcx"
    DL = "dl"
    DH = "dh"
    DX = "dx"
    EDX = "edx"
    RDX = "rdx"
    CS = "cs"
    DS = "ds"
    SS = "ss"
    ES = "es"
    FS = "fs"
    GS = "gs"
    SPL = "spl"
    SP = "sp"
    ESP = "esp"
    RSP = "rsp"
    BPL = "bpl"
    BP = "bp"
    EBP = "ebp"
    RBP = "rbp"
    SIL = "sil"
    SI = "si"
    ESI = "esi"
    RSI = "rsi"
    DIL = "dil"
    DI = "di"
    EDI = "edi"
    RDI = "rdi"
    IP = "ip"
    EIP = "eip"
    RIP = "rip"
    R8B = "r8b"
    R8W = "r8w"
    R8D = "r8d"
    R8 = "r8"
    R9B = "r9b"
    R9W = "r9w"
    R9D = "r9d"
    R9 = "r9"
    R10B = "r10b"
    R10W = "r10w"
    R10D = "r10d"
    R10 = "r10"
    R11B = "r11b"
    R11W = "r11w"
    R11D = "r11d"
    R11 = "r11"
    R12B = "r12b"
    R12W = "r12w"
    R12D = "r12d"
    R12 = "r12"
    R13B = "r13b"
    R13W = "r13w"
    R13D = "r13d"
    R13 = "r13"
    R14B = "r14b"
    R14W = "r14w"
    R14D = "r14d"
    R14 = "r14"
    R15B = "r15b"
    R15W = "r15w"
    R15D = "r15d"
    R15 = "r15"


regs_8_bit = {
    Registers.AL,
    Registers.AH,
    Registers.BL,
    Registers.BH,
    Registers.CL,
    Registers.CH,
    Registers.DL,
    Registers.DH,
    Registers.SPL,
    Registers.BPL,
    Registers.SIL,
    Registers.DIL,
    Registers.R8B,
    Registers.R9B,
    Registers.R10B,
    Registers.R11B,
    Registers.R12B,
    Registers.R13B,
    Registers.R14B,
    Registers.R15B
}

regs_16_bit = {
    Registers.AX,
    Registers.BX,
    Registers.CX,
    Registers.DX,
    Registers.CS,
    Registers.DS,
    Registers.SS,
    Registers.ES,
    Registers.FS,
    Registers.GS,
    Registers.SP,
    Registers.BP,
    Registers.SI,
    Registers.DI,
    Registers.IP,
    Registers.R8W,
    Registers.R9W,
    Registers.R10W,
    Registers.R11W,
    Registers.R12W,
    Registers.R13W,
    Registers.R14W,
    Registers.R15W
}

regs_32_bit = {
    Registers.EAX,
    Registers.EBX,
    Registers.ECX,
    Registers.EDX,
    Registers.ESP,
    Registers.EBP,
    Registers.ESI,
    Registers.EDI,
    Registers.EIP,
    Registers.R8D,
    Registers.R9D,
    Registers.R10D,
    Registers.R11D,
    Registers.R12D,
    Registers.R13D,
    Registers.R14D,
    Registers.R15D,
}

regs_64_bit = {
    Registers.RAX,
    Registers.RBX,
    Registers.RCX,
    Registers.RDX,
    Registers.RSP,
    Registers.RBP,
    Registers.RSI,
    Registers.RDI,
    Registers.RIP,
    Registers.R8,
    Registers.R9,
    Registers.R10,
    Registers.R11,
    Registers.R12,
    Registers.R13,
    Registers.R14,
    Registers.R15,
}


class MemoryMode(Enum):
    BYTE = "byte"
    WORD = "word"
    DWORD = "dword"
    QWORD = "qword"


class RegisterMode(Enum):
    MODE_8 = "8bit"
    MODE_16 = "16bit"
    MODE_32 = "32bit"
    MODE_64 = "64bit"


def how_many_bits(register):
    if register in regs_8_bit:
        return RegisterMode.MODE_8
    elif register in regs_16_bit:
        return RegisterMode.MODE_16
    elif register in regs_32_bit:
        return RegisterMode.MODE_32
    elif register in regs_64_bit:
        return RegisterMode.MODE_64
    else:
        raise ParseError("invalid register: \"{0}\"".format(register))


reg_op_32_bit = {
    Registers.AL: "000",
    Registers.CL: "001",
    Registers.DL: "010",
    Registers.BL: "011",
    Registers.AH: "100",
    Registers.CH: "101",
    Registers.DH: "110",
    Registers.BH: "111",
    Registers.AX: "000",
    Registers.CX: "001",
    Registers.DX: "010",
    Registers.BX: "011",
    Registers.SP: "100",
    Registers.BP: "101",
    Registers.SI: "110",
    Registers.DI: "111",
    Registers.EAX: "000",
    Registers.ECX: "001",
    Registers.EDX: "010",
    Registers.EBX: "011",
    Registers.ESP: "100",
    Registers.EBP: "101",
    Registers.ESI: "110",
    Registers.EDI: "111"
}

reg_op_64_bit = {
    Registers.RAX: "000",
    Registers.EAX: "000",
    Registers.AX: "000",
    Registers.AL: "000",
    Registers.RCX: "001",
    Registers.ECX: "001",
    Registers.CX: "001",
    Registers.CL: "001",
    Registers.RDX: "010",
    Registers.EDX: "010",
    Registers.DX: "010",
    Registers.DL: "010",
    Registers.RBX: "011",
    Registers.EBX: "011",
    Registers.BX: "011",
    Registers.BL: "011",
    Registers.RSP: "100",
    Registers.ESP: "100",
    Registers.SP: "100",
    Registers.AH: "100",
    Registers.RBP: "101",
    Registers.EBP: "101",
    Registers.BP: "101",
    Registers.CH: "101",
    Registers.RSI: "110",
    Registers.ESI: "110",
    Registers.SI: "110",
    Registers.DH: "110",
    Registers.RDI: "111",
    Registers.EDI: "111",
    Registers.DI: "111",
    Registers.BH: "111",
    Registers.R8: "000",
    Registers.R8D: "000",
    Registers.R8W: "000",
    Registers.R8B: "000",
    Registers.R9: "001",
    Registers.R9D: "001",
    Registers.R9W: "001",
    Registers.R9B: "001",
    Registers.R10: "010",
    Registers.R10D: "010",
    Registers.R10W: "010",
    Registers.R10B: "010",
    Registers.R11: "011",
    Registers.R11D: "011",
    Registers.R11W: "011",
    Registers.R11B: "011",
    Registers.R12: "100",
    Registers.R12D: "100",
    Registers.R12W: "100",
    Registers.R12B: "100",
    Registers.R13: "101",
    Registers.R13D: "101",
    Registers.R13W: "101",
    Registers.R13B: "101",
    Registers.R14: "110",
    Registers.R14D: "110",
    Registers.R14W: "110",
    Registers.R14B: "110",
    Registers.R15: "111",
    Registers.R15D: "111",
    Registers.R15W: "111",
    Registers.R15B: "111",
}
