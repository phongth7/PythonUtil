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
         CKeyInfo('LayerInfo:' + name + str(input.get_shape().as_list()) + str(output.get_shape().as_list()))
         pass


def AddToCollectionInfo(collection_name, value):
    """
    该信息输出添加value到colection的信息''
    :param collection_name: string
    :param value: tf.Tensor/tf.Variable/tf.Operation
    :return: 
    """
    print('AddToCollection: add \033[1:32:40m %s \033[mto \033[1:32:40m%s\033[m' % (collection_name, value.name()))
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