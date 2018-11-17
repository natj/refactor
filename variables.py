from os import listdir
from os.path import isfile, join
from os import walk
import keyword


def get_files(mypath, suffix):

    f = []
    for (dirpath, dirnames, filenames) in walk(mypath):

        filtered_filenames = []
        for fname in filenames:

            # remove dot files
            if fname[0] == '.':
                continue

            #match only given suffix
            if not(fname.lower().endswith(suffix)):
                continue

            #make it into full path
            fname = dirpath + '/' + fname

            filtered_filenames.append(fname)

        f.extend(filtered_filenames)
        #break
    return f


def write_files(fs):

    with open('files.txt', 'a') as ffile:
        ffile.write('[py]\n')
        for m in fs:
            if m.lower().endswith('.py'):
                ffile.write(m + '\n')

        ffile.write('\n')
        ffile.write('[cpp]\n')
        for m in fs:
            if m.lower().endswith( ('.c++', '.cpp', '.h') ):
                ffile.write(m + '\n')


# split file listing into different modes
def split_list(s, mode):
    fs = []

    readmode = False
    for f in s:
        fl = f.strip()

        #start reading when correct mode is detected
        if fl == '['+mode+']':
            readmode = True
            continue

        #stop reading when other mode is detected
        if  fl.startswith('['): 
            print("found stop at : ", fl)
            readmode = False

        #filename matches, append
        if readmode:
            if not(fl == ''):
                fs.append(fl)

    return fs


def analyze(text):
    wordcount={}
    for word in text.split():
        if word not in wordcount:
            wordcount[word] = 1
        else:
            wordcount[word] += 1
    
    for k,v in wordcount.items():
        print(k, v)


# common split symbols in code
splitsymbols = (
        ' ',':','::','.',',',';','(',')','[', ']','\n',
        '<','>','+','-','/','*','"','{','}',
        '&','!','@','%','?','#',
        )

ignorewords = [
'size_t',  'array', 'enable_if_t', 'vector', 'tuple', 'enable_if', 'tuple_of', 'size', 'uint64_t', 'noexcept',
'def_readwrite', 'make_tuple', 'push_back', 'constexpr', 'shared_ptr', 'first', 'second', 'move',
'size_type', 'type', 'pybind11', 'https', 'object', 'NOTE', 'TODO', 'FIXME', 'clear', 'const_iterator', 'iterator',
'module', 'float_type', '==',
'auto'       ,'const'        ,'double'    ,'float'            ,'int'      ,'short'  ,'struct'  ,'unsigned',
'break'      ,'continue'     ,'else'      ,'for'              ,'long'     ,'signed' ,'switch'  ,'void',
'case'       ,'default'      ,'enum'      ,'goto'             ,'register' ,'sizeof' ,'typedef' ,'volatile',
'char'       ,'do'           ,'extern'    ,'if'               ,'return'   ,'static' ,'union'   ,'while',
'asm'        ,'dynamic_cast' ,'namespace' ,'reinterpret_cast' ,'try',
'bool'       ,'explicit'     ,'new'       ,'static_cast'      ,'typeid',
'catch'      ,'false'        ,'operator'  ,'template'         ,'typename',
'class'      ,'friend'       ,'private'   ,'this'             ,'using',
'const_cast' ,'inline'       ,'public'    ,'throw'            ,'virtual',
'delete'     ,'mutable'      ,'protected' ,'true'             ,'wchar_t',
'and'        ,'bitand'       ,'compl'     ,'not_eq'           ,'or_eq'    ,'xor_eq',
'and_eq'     ,'bitor'        ,'not'       ,'or'               ,'xor',
'cin'        ,'endl'         ,'INT_MIN'   ,'iomanip'          ,'main'     ,'npos' ,'std',
'cout'       ,'include'      ,'INT_MAX'   ,'iostream'         ,'MAX_RAND' ,'NULL' ,'string',
]


#these are less strict and might need to be changed
ignorewords2 = [
'MPI_UNSIGNED_CHAR','MPI_UNSIGNED_SHORT','MPI_UNSIGNED','MPI_UNSIGNED_LONG'
,'MPI_Type_create_struct','MPI_Type_commit','StackOverflow','MPI_Bcast'
,'MPI_COMM_WORLD','MPI_Iprobe','MPI_IProbe','__getitem__','__setitem__'
,'PYBIND11_DECLARE_HOLDER_TYPE','stdexcept','overwrite','MPI_UINT64_T'
,'MPI_UNSIGNED_LONG_LONG','MPI_DOUBLE','operator=','variadic','make_unique'
,'optional','http','trait','result','binary'
,'call','slice','range_error','match','c_str'
,'pybind','without','either','were','endif'
,'python','will','MPI_Datatype','MPI_Aint','real'
,'format','algorithm','unordered_map','some','does'
,'erase','already','invalid_argument','entry','found'
,'pop_back','must','others','could','also'
,'accumulate','PYBIND11_MODULE','override','extend','which'
,'github','reverse_iterator','\begin','\end','tuples'
,'method','count','wait','print','`std'
,'tuple_size','forward','attr','pyclass_name','methods'
,'SIZE_MAX','MPI_SIZE_T','should','where','function'
,'unique_ptr','Return','sort','find','back'
,'there','resize','cast','types','elements'
,'each','create','reference','\text','make'
,'unique','only','This','have','xmin'
,'xmax','what','many','MPI_INT','avoid'
,'emplace','internal','\brief','same','stackoverflow'
,'decltype','communications','const_reverse_iterator','lens','make_index_sequence'
,'apply','MPI_Get_address','copy','list','Args'
,'dynamic_pointer_cast','define','send','send_queue','element'
,'begin','pragma','owner','length','request'
,'elem','once','index_type','number','time'
,'into','are_integral','class_','that','container'
,'init','base','local','mins','maxs','value'
]



def tsplit(s, sep):
    stack = [s]
    for char in sep:
        pieces = []
        for substr in stack:
            pieces.extend(substr.split(char))
        stack = pieces
    return stack


def read_variables(
        mode, 
        filename='files.txt',
        detect_only_camelcase=False,
        detect_only_underscore=False,
        ):

    with open(filename) as f:
        s = f.readlines()
    ffiles = split_list(s, mode)
    
    wordcount={}
    for codefile in ffiles:
        print("analyzing {}......".format(codefile))
        with open(codefile) as f:
            for word in tsplit(f.read(), splitsymbols):
                word = word.strip()
                if len(word) < 4:
                    continue

                if word in ignorewords:
                    continue

                #less strict ignore words
                if word in ignorewords2:
                    continue

                #ignore python keywords
                if keyword.iskeyword(word):
                    continue

                if detect_only_camelcase:
                    if word.lower() == word:
                        continue

                if detect_only_underscore:
                    if not(word.match('_')):
                        continue

                if word not in wordcount:
                    wordcount[word] = 1
                else:
                    wordcount[word] += 1

    print("--------------------------------------------------")
    print("analysis result:")

    #for k,v in wordcount.items():
    for k,v, in sorted(wordcount.items(), key=lambda words: words[1], reverse = False):
        #if v > 1:
        print(k, v)

    with open('variables.txt', 'a') as ffile:
        for k,v, in sorted(wordcount.items(), key=lambda words: words[1], reverse = False):
            ffile.write(k +'\n')


if __name__ == '__main__':

    #create file listing
    if False:
        rdir = '../plasmabox/corgi'
        fs = get_files(rdir, ('.py', '.c++', '.h'))
        write_files(fs)

    #create variable name listing
    if True:
        #read_variables('cpp', 'files.txt')
        read_variables('cpp', 'files.txt', detect_only_camelcase=True)
        #read_variables('cpp', 'files.txt', detect_only_underscore=True)



