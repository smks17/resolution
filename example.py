import pprint

from resolution import prove

pp = pprint.PrettyPrinter(indent=4)

data = [
    #   premises            conclusion                      status
    # -----------------------------------------------------------------
    (['p -> q', 'p'],           'q'),                       # provable
    ([' p /\\ q', 'q'],         'p'),                       # provable
    (['p -> q', 'q'],           'p'),                       # not provable
    (['p -> q', 'r -> s'],'( p \\/ r ) -> ( q \\/ s )')     # provable
]

def runExample(premises, conclusion):
    pp.pprint(f'premises: {", ".join(premises)}')
    pp.pprint(f'conclusion: {conclusion}')
    result = prove(premises, conclusion)
    if(result[0]):
        print('\x1b[6;30;42m' + 'provable!' + '\x1b[0m')
    else:
        print('\x1b[6;30;41m' + 'not provable!' + '\x1b[0m')
    print("result:")
    pp.pprint(result[1])

if __name__ == "__main__":
    for n in range(len(data)):
        print('\x1b[1;35;40m' + f'example {int(n+1)}:' + '\x1b[0m')
        eval(f'runExample({data[n][0]}, \'{data[n][1]}\')')    #run nth example
        print()