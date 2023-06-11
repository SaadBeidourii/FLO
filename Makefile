INPUT = $(basename $(notdir $(wildcard input/*.flo)))

flo_vers_exercutable:
	for a in $(INPUT); do echo "compilation: "$${a}; if python3 generation_code.py -nasm input/$${a}.flo > output/$${a}.nasm; then nasm -f elf -g -F dwarf output/$${a}.nasm;  ld -m elf_i386 -o output/$${a} output/$${a}.o; fi done;
