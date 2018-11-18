from os import listdir
from os.path import isfile, join
from os import walk
import keyword

from constant_symbols import splitsymbols
from constant_symbols import ignorewords
from constant_symbols import ignorewords2

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
            #print("found stop at : ", fl)
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


# read file content, replace string and write back to file
def inplace_change(filename, old_string, new_string):

    with open(filename) as f:
        text = f.read()
        if old_string not in text:
            print('"{old_string}" not found in {filename}'.format(**locals()))
            return
    
    # Safely write the changed content, if found in the file
    filename2 = filename + '_sr'
    with open(filename2, 'w') as f:
        print('Changing "{old_string}" to "{new_string}" in {filename}'.format(**locals()))
        text = text.replace(old_string, new_string)
        f.write(text)

    return


# analyze file content to make sure replacing is possible
def analyze_search_replace(filename, old_string, new_string):

    with open(filename) as f:
        text = f.readlines()

    c_old = 0
    c_new = 0
    linen_old = []
    linen_new = []
    for linen, line in enumerate(text):

        #old string
        c = line.count(old_string)
        if c > 0:
            linen_old.append(linen)
        c_old += c

        #new string
        c = line.count(new_string)
        if c > 0:
            linen_new.append(linen)
        c_new += c

    if c_old + c_new > 0:
        print("    {} hits ({} new hits)".format(c_old, c_new))
        
        #print(linen_old)
        #print(linen_new)

    if c_old + c_new > 0:
        print("*********")
        for linen in linen_old:
            print("{}: {}".format(linen, text[linen].strip() ))

        for linen in linen_new:
            print("{}: {}".format(linen, text[linen].strip() ))
        print("*********")
    


def search_and_replace(
        files = 'files.txt',
        replace_filename='replace.txt',
        ):

    # read search and replace list
    wordreplaces={}
    with open(replace_filename) as f:
        for line in f.readlines():
            both = line.split('=>')
            try:
                orig, new = both
                orig = orig.strip()
                new  = new.strip()
            except:
                continue
            wordreplaces[orig] = new


    # read project file listing
    with open(files) as f:
        filelist = f.readlines()
    ffiles = split_list(filelist, 'py')
    

    modes = ['py', 'cpp']
    for k,v in wordreplaces.items():
        print("-------------------------------------------------- ")
        print("replacing:")
        print("  {} => {}".format(k,v))

        #loop over different file types
        for mode in modes:
            print("[{}]".format(mode))
            ffiles = split_list(filelist, mode)
            for filename in ffiles:
                print(filename)
                analyze_search_replace(filename, k, v)
                

        print("\n")


if __name__ == '__main__':

    #create file listing
    if False:
        rdir = '../plasmabox/corgi'
        fs = get_files(rdir, ('.py', '.c++', '.h'))
        write_files(fs)

    #create variable name listing
    if False:
        #read_variables('cpp', 'files.txt')
        read_variables('cpp', 'files.txt', detect_only_camelcase=True)
        #read_variables('cpp', 'files.txt', detect_only_underscore=True)

    if True:
        search_and_replace('files.txt', 'replace.txt')



