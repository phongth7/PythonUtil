# coding = utf-8

def CError(
        input=''
):
         print('\033[4:31:40%s\033[m' % input)
         pass

def CKeyInfo(
        input=''
):
         print('\033[1:32:40%s\033[m' % input)
         pass

def CGlobalExit(
         target
):
         try:
                  eval(target)
         except NameError:
                  CError('%s not exit' % target)
                  return False
         return True
         pass

def CLayerInfo(
        name='undefined',
        input=None,
        output=None
):
         assert type(input).__name__ == 'Tensor', CError('input is not a tensor')
         assert type(output).__name__ == 'Tensor', CError('output is not a tensor')
         CKeyInfo(name + str(input.get_shape().as_list()) + str(output.get_shape().as_list()))
         pass




BNEPS = 0.1
def test():
         global BNEPS
         global BNE
         CGlobalExit('BNEPS')
         CGlobalExit('BNE')

if __name__ == '__main__':
         # test()
         pass