"""CPU functionality."""

import sys
import re
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram=[0x00] * 256        
        self.reg=[0x00] * 8
        self.reg[7] = 0xF4
        self.pc = 0
        self.fl = 0
        self.hlt = 0b00000001
        self.ldi = 0b10000010
        self.prn = 0b01000111
        self.add =  0b10100000
        self.mul = 0b10100010
        self.push = 0b01000101
        self.pop = 0b01000110
        self.call = 0b01010000
        self.ret = 0b00010001
        self.branchtable = {}
        self.branchtable[self.hlt]=self.handle_htl
        self.branchtable[self.ldi]=self.handle_ldi
        self.branchtable[self.prn]=self.handle_prn
        self.branchtable[self.add]=self.handle_add
        self.branchtable[self.mul]=self.handle_mul
        self.branchtable[self.push]=self.handle_push
        self.branchtable[self.pop]=self.handle_pop
        self.branchtable[self.call]=self.handle_call
        self.branchtable[self.ret]=self.handle_ret
    
    def handle_htl(self):
        print("exit")
        exit()
    
    def handle_ldi(self):
        operand_a = self.pc+1
        operand_b = self.pc+2
        reg_a = self.ram_read(operand_a)              
        value = self.ram_read(operand_b)
        self.reg[reg_a]=value
        self.pc += 3

    def handle_prn(self):
        operand_a = self.pc+1
        reg_a = self.ram_read(operand_a)
        print(self.reg[reg_a])
        self.pc += 2

    def handle_mul(self):
        operand_a = self.pc+1
        operand_b = self.pc+2
        reg_a = self.ram_read(operand_a)
        reg_b = self.ram_read(operand_b)
        self.alu("MUL", reg_a, reg_b)
        self.pc += 3
    
    def handle_add(self):
        operand_a = self.pc+1
        operand_b = self.pc+2
        reg_a = self.ram_read(operand_a)
        reg_b = self.ram_read(operand_b)
        self.alu("ADD", reg_a, reg_b)
        self.pc += 3

    def handle_push(self):
        self.reg[7] -= 1
        operand_a = self.pc+1
        reg_a = self.ram_read(operand_a)
        value = self.reg[reg_a]
        self.ram_write(value, self.reg[7])
        self.pc += 2

    def handle_pop(self):
        operand_a = self.pc+1
        reg_a = self.ram_read(operand_a)
        value = self.ram_read(self.reg[7])
        self.reg[reg_a] = value
        self.reg[7] += 1
        self.pc += 2 

    def handle_call(self):
        operand_a = self.pc+1
        operand_b = self.pc+2
        return_address = operand_b
        self.reg[7] -= 1
        self.ram_write(return_address, self.reg[7])
        reg_a = self.ram_read(operand_a)
        subroutine_address = self.reg[reg_a]
        self.pc = subroutine_address

    def handle_ret(self):
        top_of_stack_addr = self.reg[7]
        return_addr = self.ram_read(top_of_stack_addr)
        self.reg[7] += 1
        self.pc = return_addr

    def load(self):
        """Load a program into memory."""
        address = 0
        path = "sctest.ls8"
        # try:
        #      path += sys.argv[1]
        # except IndexError:
        #      print("file is required")
        
        with open(path) as file:
            pattern = re.compile("[01]{8}")
            for line in file:
                result = pattern.findall(line)
                if result:
                     self.ram[address] = int(result.pop(), base=2)
                     address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")
    
    # _Memory Address Register_ (MAR)
    def ram_read(self, MAR):
        return self.ram[MAR]

    # _Memory Data Register_ (MDR) _Memory Address Register_ (MAR)
    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR 

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        ir = 0
        while ir != self.hlt:
            ir = self.ram_read(self.pc)
            # self.trace()
            try:
                 self.branchtable[ir]()
            except:
                exit()
            # operand_a = self.pc+1
            # operand_b = self.pc+2

            # if ir == self.hlt:
            #     exit()
            # elif ir == self.ldi:
            #     reg_a = self.ram_read(operand_a)              
            #     value = self.ram_read(operand_b)
            #     self.reg[reg_a]=value
            #     self.pc += 3
            # elif ir == self.prn:
            #     reg_a = self.ram_read(operand_a)
            #     print(self.reg[reg_a])
            #     self.pc += 2
            # elif ir == self.mul:
            #     reg_a = self.ram_read(operand_a)
            #     reg_b = self.ram_read(operand_b)
            #     self.alu("MUL", reg_a, reg_b)
            #     self.pc += 3
            # else:
            #     exit()
