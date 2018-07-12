from src.assemblytranslator import translate, ProcessorMode

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

print(translate("mov ebx, [1232]", ProcessorMode.MODE_64))
