# -*- coding: utf-8 -*-
import os
import sets

#import find

# Current directory
os.chdir('/Users/marissagemma/Dropbox/Colloquial style study 13-14/texts')
print os.getcwd()

dir = os.getcwd()
punctuations = ':;,?!-&§\'"”“‘.%$*-`—”“'
white = ' \n\t\r'
    
taille_fenetre = 21
MAXIMUM_PHRASE_LENGTH = 15


tr = []


def words(string):
    LString = segmenter_nr(string)
    return wordsListe_iter(LString, [])
                
def segmenter_nr(string):
    S = string
    N = 0
    A = ''
    R = []
    while not S == '':
        if N > 700 and S[0] in white:
            R = R + [A]
            A = ''
            N = 0
            S = S[1:]
        else:
            N = N + 1
            A = A + S[0]
            S = S[1:]
    if A == '':
        return R
    else: 
        return R + [A]
        
def wordsListe(Lstring, R):
    if Lstring == []:
        return R
    else:
        NR = R + words_(Lstring[0], '', [])
        return wordsListe(Lstring[1:], NR)
        
def wordsListe_iter(Lstring, R):
    while not Lstring == []:
        R = R + words_iteratif(Lstring[0], '', [])
        Lstring = Lstring[1:]
    return R
            
    
def words_(string, A, R):
    if A == '':
        NR = R
    else:
        NR = R + [A]
    if string == '':
        return NR
    elif string[0] in white:
       return words_(string[1:], '', NR)
    elif string[0] in punctuations:
        if A == '' or A[0] in punctuations:
            return words_(string[1:], A + string[0], R)
        else:
            return words_(string[1:], string[0], NR)
    else:
        if A == '' or A[0] in punctuations:
            return words_(string[1:], string[0], NR)
        else:
            return words_(string[1:], A + string[0], R)
            
def add_chaine(LC, S):
    if S == '':
        return LC
    else:
        return LC + [S]

def words_iteratif(string, A, R):
    #NR = add_chaine(R, A)
    while string <> '':
        if string[0] in white:
            R = add_chaine(R, A)
            A = ''
        elif string[0] in punctuations:
            if A == '' or A[0] in punctuations:
                A = A + string[0]
            else:
                R = add_chaine(R, A)
                A = string[0]
        else:
            if not A == '' and A[0] in punctuations:
                R = add_chaine(R, A)
                A = string[0]
            else:
                A = A + string[0]
        string = string[1:]
        #R = add_chaine(R, A)
    return add_chaine(R, A)       
                                    
        
        
def print_list_content(L):
    LL = ''
    for x in L:
        LL = LL + x
    #print LL
    
def begin_word(L):
    if L:
        if L[0]: 
            return not L[0][0] in punctuations+' \n'
            

englishStopWords = sets.Set(['a','able','about','across','after','all','almost','also','am','among','an','and','any','are','as','at','be','because','been','but','by','can','cannot','could','dear','did','do','does','either','else','ever','every','for','from','get','got','had','has','have','he','her','hers','him','his','how','however','i','if','in','into','is','it','its','just','least','let','likely','may','me','might','most','must','my','neither','no','nor','not','of','off','often','on','only','or','other','our','own','rather','said','say','says','she','should','since','so','some','than','that','the','their','them','then','there','these','they','this','to','too','us','wants','was','were','what','when','where','which','while','who','whom','why','will','with','would','yet','you','your'])

def impression_ngrams(NG, N, L):
    if NG[0] and NG[N]:
        print '\tRepetitions length ' + str(N) + ' - density ‱ ' + str(10000.*len(NG[N])/len(L)) + ' ('+str(len(NG[N])) + '/' + str(len(L)) +')' #+ ' - liste: ' + str(NG[N])
        if not NG[N] == [] and N < MAXIMUM_PHRASE_LENGTH:
            impression_ngrams(NG, N+1, L)
    
    
def impression_ext_ngrams(ngram, L, file, out):
    out.write(file)
    for i in range(1,MAXIMUM_PHRASE_LENGTH):
        if len(ngram) > i:
            out.write(';' + str(round(10000.*len(ngram[i])/len(L),3)))
        else:
            out.write(';' + str(0.))
    out.write('\n')
    
def repetition(L):
    return not (L[0] in englishStopWords) and (L[0] in L[1:])
    
def ajout_mots(D, L):
    for W in L:
        if W in D:
            D[W] =  D[W] + 1
        else:
            D[W] = 1
    return D
    
def ajout_mot(D, W):
    if W in D.keys():
        D[W] =  D[W] + 1
    else:
        D[W] = 1

    
def classement_repetitions(Di):
    E = dict()
    for W in iter(Di):
        i = Di[W]
        if i in E:
            E[i] = E[i] + [W]
        else:
            E[i] = [W]
    K = E.keys()
    K.sort(reverse=True)
    K = K[:20]
    for x in E.keys():
        if not x in K:
            del E[x]
    return E
    
def elim_point_virgules(M):
    #print L
    MM = ''
    for Char in M:
        if Char == ';':
            MM = MM +':'
        else: 
            MM = MM + Char
    return MM

    
def jieme(D, j):
    L = D.keys()
    L.sort(reverse=True)
    #print L
    if j > len(L):
        return []
    else:
        #print 'j = ' + str(j)
        return str(D[L[j-1]]) + '/' + str(L[j-1])

            
def impression_repetitions(D,file): 
    fn = os.getcwd() + '/out/rep_' + file[:-4] + '.csv'
    outfile = open(fn, 'w')
    #print 'Appel avec fichier ' + str(file) + ': '+ str(D)
    C = 'Longueur'
    for i in range(1, len(D)):
        C = C + '; L=' + str(i)
    outfile.write(C)
    for j in range(1,30):
        C = '\n'
        for i in range(1,len(D)):
            if i >= len(D) - 1:
                C = C + '; []'
            else:
                #print D[i-1]
                C = C + ';' + str(jieme(D[i-1], j))
        outfile.write(C)
    outfile.close()
            

def detection_repetition(tf, file, out, Global):   
    fn = os.getcwd() + '/' + file
    fic = open(fn, 'r')
    L = [] 
    D = [dict()]       
    for line in fic:
        W = words(line)
        L = L + W
        #D[0] = ajout_mots(D[0], W)
    #print L
    #D[0] = classement_repetitions(D[0])
    #print D    
    ngram = []
    ngram.insert(0,[])
    longueur = len(L) - tf
    for i in range(0, longueur):
        if begin_word(L[i:i+tf]) and repetition(L[i:i+tf]):
            #print i
            ngram[0].append(i)
            ajout_mot(D[0], L[i])
    #print 'Ngram[0]: ' + str(ngram[0])
    #print 'D[0]: ' + str(classement_repetitions(D[0]))
    N = 1
#    print str(classement_repetitions(D[0]))
    while not ngram[-1] == [] and N <= MAXIMUM_PHRASE_LENGTH:
        D.append(dict())
        calculate_ngram(N, L, ngram, tf, D, Global)
        N = N+1
    if ngram[0]:
        print '\nFile ' + file + ': '
        impression_ngrams(ngram, 1, L)
        impression_ext_ngrams(ngram, L, file, out)
    else:
        print 'Fichier ' + file + ': no repetition'
        out.write(file + ';' + str(0.) + ';' + str(0.) +';' + str(0.) +';' + str(0.) +';' + str(0.) +';' + str(0.) +';' + str(0.) +'\n')
    impression_repetitions(D, file)

    #print ngram
    
        
def repetition_(L1, L2): #return the number of repetition of L1 in L2
    return repetition_aux(L1, L2, 0)
    
def repetition_aux(L1, L2, N):
    if L2 == []:
        return N
    elif L1 == L2[0:len(L1)]:
        return repetition_aux(L1, L2[1:], N+1)
    else:
        return repetition_aux(L1, L2[1:], N)
        
def mot(L, C):
    for M in L:
        if begin_word(M) and not C == '':
            C = C + ' ' + M
        else:
            C = C + elim_point_virgules(M)
            #C = C + M
    return C
        
def calculate_ngram(N, L, NG, tf, Di, Global):
    if NG[-1] == []:
        Di[N-1] = []
        return NG
    else:
        LN = []
        for x in NG[-1]:
            Nb = repetition_(L[x:x+N], L[x:x+tf])
            if Nb > 1:
                LN.append(x)
                M = mot(L[x:x+N], '')
                ajout_mot(Di[N-1], M)
                ajout_mot(Global[N-1], M)
        NG.append(LN)
    Di[N-1] = classement_repetitions(Di[N-1])
    #print 'Di[' + str(N-1) + '] ' + str(Di[N-1])
    return NG
    
def is_a_text_file(file):
    return file[-4:] == '.txt'


if not os.path.isdir('out'):
    output_folder = os.mkdir('out')
    
outfile = open(dir + '/corpus_repetition_indices.csv', 'w')
outfile.write('Fichier')
G = [dict()]
for i in range(1, MAXIMUM_PHRASE_LENGTH):
    outfile.write(';Length '+str(i))
    G.append(dict())
outfile.write('\n')
for fic in os.listdir(dir):
    if is_a_text_file(fic):
        detection_repetition(taille_fenetre, fic, outfile, G)
    #os.close(fd)
for i in range(1, MAXIMUM_PHRASE_LENGTH):
    G[i-1] = classement_repetitions(G[i-1])

# TODO: This should live at the same level as repetition_index
impression_repetitions(G, 'corpus_phrase_reptitions.txt') 
outfile.close()
    

            
            
    
