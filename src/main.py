from src.assemblytranslator import translate, ProcessorMode
from src.assemblytranslator.parse_error import ParseError


def prettify(machine_code_local):
    new_machine_code = machine_code_local.replace(" ", "")

    answer = ""
    for i in range(int(len(new_machine_code) / 8)):
        hex_value = hex(int(new_machine_code[8 * i: 8 * i + 8], 2))[2:]
        answer += (hex_value if len(hex_value) != 1 else "0" + hex_value) + " "

    return answer


print("Enter instruction: (quit for exit)")
processor_mode = ProcessorMode.MODE_32
print("\t*> processor is in mode 32 bit")

while True:
    instruction = input("\t>> ")
    machine_code = "nop"

    if instruction.startswith("quit"):
        break
    elif instruction.lower().startswith("mode_32"):
        print("\t*> processor changed to mode 32 bit")
        processor_mode = ProcessorMode.MODE_32
    elif instruction.lower().startswith("mode_64"):
        print("\t*> processor changed to mode 64 bit")
        processor_mode = ProcessorMode.MODE_64
    else:
        try:
            machine_code = translate(instruction, processor_mode)
        except ParseError as error:
            print("\t=> ", error)

    print("\t=>", prettify(machine_code) if machine_code != "nop" else machine_code)

