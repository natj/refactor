from os import listdir
from os.path import isfile, join
from os import walk



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



def read_variables(mode, filename='files.txt'):

    with open(filename) as f:
        s = f.readlines()
    ffiles = split_list(s, mode)
    
    print(ffiles)




if __name__ == '__main__':

    #create file listing
    if False:
        rdir = '../plasmabox/corgi'
        fs = get_files(rdir, ('.py', '.c++', '.h'))
        write_files(fs)

    #create variable name listing
    if True:
        read_variables('cpp', 'files.txt')



