
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
,'dynamic_pointer_cast','define','send','element'
,'begin','pragma','owner','length','request'
,'elem','once','index_type','number','time'
,'into','are_integral','class_','that','container'
,'init','base','local','mins','maxs','value'
]
