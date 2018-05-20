class X10():
    houseCodes     = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']
    devices        = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']
    codedValues    = ['6', 'E', '2', 'A', '1', '9', '5', 'D', '7', 'F', '3', 'B', '0', '8', '4', 'C']
    codedCommands  = {'ALLUOFF': '0', 'ALLLON': '1', 'ON': '2', 'OFF': '3', 'DIM': '4', 'BRIGHT': '5', 'ALLLOFF': '6'}
    
    @staticmethod
    def encodeAddress(value, hexadecimal = False):
        if len(value) == 1:
            if hexadecimal:
                return(int(X10.codedValues[X10.houseCodes.index(value)], 16))
            else:
                return(X10.codedValues[X10.houseCodes.index(value)])
        elif len(value) < 4:
            if hexadecimal:
                return(int(X10.codedValues[X10.houseCodes.index(value[0])] + X10.codedValues[X10.devices.index(value[1:])], 16))
            else:
                return(X10.codedValues[X10.houseCodes.index(value[0])] + X10.codedValues[X10.devices.index(value[1:])])
        else:
            raise ValueError('Incorrect X10 address')
    
    @staticmethod
    def decodeAddress(value):
        if len(value) == 1:
            return(X10.houseCodes[X10.codedValues.index(value)])
        elif len(value) == 2:
            return(X10.houseCodes[X10.codedValues.index(value[0])] + X10.devices[X10.codedValues.index(value[1])])
        else:
            raise ValueError('Incorrect X10 encoded address')

    @staticmethod
    def getCommand(command, hexadecimal = False):
        if hexadecimal:
            return int(X10.codedCommands[command], 16)
        else:
            return X10.codedCommands[command]
    
    @staticmethod
    def encodeCommand(house_code, command):
        return int(X10.encodeAddress(house_code) + X10.getCommand(command), 16)
