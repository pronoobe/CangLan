from Debugger import *

formatter = CangLan_MicroDsp()

formatter.add_new_command('cmd0', 0b0, (int, int, int, int,), ['i1', 'i2', 'i3', 'i4',])
formatter.add_new_command('cmd1', 0b1, (float, float,), ['f1', 'f2',])
formatter.add_new_command('cmd2', 0b10, (int, float,), ['i1', 'f1',])
formatter.add_new_command('cmd3', 0b11, (int, float,), ['i2', 'f2',])
formatter.add_new_command('cmd4', 0b100, (str,), ['s1',])
formatter.add_new_command('cmd5', 0b101, (str,), ['s2',])


if __name__ == "__main__":
    debugger = CangLan_Debugger(formatter)
    debugger.run()
        