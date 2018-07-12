from src.assemblytranslator import translate, ProcessorMode


def pretty_print(machine_code):
    new_machine_code = machine_code.replace(" ", "")

    answer = ""
    for i in range(int(len(new_machine_code) / 8)):
        hex_value = hex(int(new_machine_code[8 * i: 8 * i + 8], 2))[2:]
        answer += (hex_value if len(hex_value) != 1 else "0" + hex_value) + " "

    print(answer)

# print("Enter instruction: (quit for exit)")
#
# while True:
#     instruction = input("\t>> ")
#
#     if instruction.startswith("quit"):
#         break
#
#     machine_code = translate(instruction, ProcessorMode.MODE_32)
#
#     print("\t=>", machine_code)


pretty_print(translate("mov r8b, 1", ProcessorMode.MODE_64))
