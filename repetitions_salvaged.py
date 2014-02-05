# -*- coding: utf-8 -*-
import os
import sets

PUNCTUATIONS = ':;,?!-&§\'"”“‘.%$*-`—”“'
WHITE = ' \n\t\r'
SIZE_WINDOW = 21
MAXIMUM_PHRASE_LENGTH = 15
ENGLISH_STOP_WORDS = sets.Set(['a','able','about','across','after','all','almost','also','am','among','an','and','any','are','as','at','be','because','been','but','by','can','cannot','could','dear','did','do','does','either','else','ever','every','for','from','get','got','had','has','have','he','her','hers','him','his','how','however','i','if','in','into','is','it','its','just','least','let','likely','may','me','might','most','must','my','neither','no','nor','not','of','off','often','on','only','or','other','our','own','rather','said','say','says','she','should','since','so','some','than','that','the','their','them','then','there','these','they','this','to','too','us','wants','was','were','what','when','where','which','while','who','whom','why','will','with','would','yet','you','your'])

OUTPUT_ROOT = "output"
WORKS_DIRECTORY = "works"

class RepetitionAnalyzer:
    def words(self, string):
        LString = self.segmenter_nr(string)
        return self.wordsListe_iter(LString, [])

    def segmenter_nr(self, string):
        S = string
        N = 0
        A = ''
        R = []
        while not S == '':
            if N > 700 and S[0] in WHITE:
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

    def wordsListe(self, Lstring, R):
        if Lstring == []:
            return R
        else:
            NR = R + words_(Lstring[0], '', [])
            return self.wordsListe(Lstring[1:], NR)

    def wordsListe_iter(self, Lstring, R):
        while not Lstring == []:
            R = R + self.words_iteratif(Lstring[0], '', [])
            Lstring = Lstring[1:]
        return R


    def words_(self, string, A, R):
        if A == '':
            NR = R
        else:
            NR = R + [A]
        if string == '':
            return NR
        elif string[0] in WHITE:
           return words_(string[1:], '', NR)
        elif string[0] in PUNCTUATIONS:
            if A == '' or A[0] in PUNCTUATIONS:
                return words_(string[1:], A + string[0], R)
            else:
                return words_(string[1:], string[0], NR)
        else:
            if A == '' or A[0] in PUNCTUATIONS:
                return words_(string[1:], string[0], NR)
            else:
                return words_(string[1:], A + string[0], R)

    def add_chaine(self, LC, S):
        if S == '':
            return LC
        else:
            return LC + [S]

    def words_iteratif(self, string, A, R):
        #NR = add_chaine(R, A)
        while string <> '':
            if string[0] in WHITE:
                R = self.add_chaine(R, A)
                A = ''
            elif string[0] in PUNCTUATIONS:
                if A == '' or A[0] in PUNCTUATIONS:
                    A = A + string[0]
                else:
                    R = self.add_chaine(R, A)
                    A = string[0]
            else:
                if not A == '' and A[0] in PUNCTUATIONS:
                    R = self.add_chaine(R, A)
                    A = string[0]
                else:
                    A = A + string[0]
            string = string[1:]
            #R = add_chaine(R, A)
        return self.add_chaine(R, A)



    def print_list_content(self, L):
        LL = ''
        for x in L:
            LL = LL + x

    def begins_with_a_word(self, L):
        if L and L[0]:
            return not L[0][0] in PUNCTUATIONS+' \n'

    def impression_ngrams(self, NG, N, L):
        if NG[0] and NG[N]:
            print '\tRepetitions length ' + str(N) + ' - density ‱ ' + str(10000.*len(NG[N])/len(L)) + ' ('+str(len(NG[N])) + '/' + str(len(L)) +')' #+ ' - liste: ' + str(NG[N])
            if not NG[N] == [] and N < MAXIMUM_PHRASE_LENGTH:
                self.impression_ngrams(NG, N+1, L)


    def impression_ext_ngrams(self, ngram, L, input_file, output_file):
        output_file.write(input_file.name)
        for i in range(1,MAXIMUM_PHRASE_LENGTH):
            if len(ngram) > i:
                output_file.write(';' + str(round(10000.*len(ngram[i])/len(L),3)))
            else:
                output_file.write(';' + str(0.))
        output_file.write('\n')

    def is_repeated(self, L):
        return not (L[0] in ENGLISH_STOP_WORDS) and (L[0] in L[1:])

    def ajout_mot(self, D, W):
        if W in D.keys():
            D[W] += 1
        else:
            D[W] = 1

    def classement_repetitions(self, Di):
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

    def elim_point_virgules(self, M):
        #print L
        MM = ''
        for Char in M:
            if Char == ';':
                MM = MM +':'
            else:
                MM = MM + Char
        return MM


    def jieme(self, D, j):
        L = D.keys()
        L.sort(reverse=True)
        #print L
        if j > len(L):
            return []
        else:
            #print 'j = ' + str(j)
            return str(D[L[j-1]]) + '/' + str(L[j-1])


    def impression_repetitions(self, D, input_filename):
        output_filename = self.output_directory + os.sep + input_filename[:-4] + '.csv'
        output_file = open(output_filename, 'w')
        #print 'Appel avec fichier ' + str(file) + ': '+ str(D)
        C = 'Longueur'
        for i in range(1, len(D)):
            C = C + '; L=' + str(i)
        output_file.write(C)
        for j in range(1,30):
            C = '\n'
            for i in range(1,len(D)):
                if i >= len(D) - 1:
                    C = C + '; []'
                else:
                    #print D[i-1]
                    C = C + ';' + str(self.jieme(D[i-1], j))
            output_file.write(C)
        output_file.close()


    def detect_repetition(self, size_window, input_file, output_file, repetitions_dictionary):
        D = [dict()]

        words = []
        for line in input_file:
            words += self.words(line)

        ngram = []
        ngram.insert(0,[])

        # iterate over words in size_window sized chunks
        word_count = len(words) - size_window
        for count in range(0, word_count):
            words_chunk = words[count:count+size_window]
            if self.begins_with_a_word(words_chunk) and self.is_repeated(words_chunk):
                ngram[0].append(count)
                self.ajout_mot(D[0], words[count])

        N = 1

        while not ngram[-1] == [] and N <= MAXIMUM_PHRASE_LENGTH:
            D.append(dict())
            self.calculate_ngram(N, words, ngram, size_window, D, repetitions_dictionary)
            N += 1

        if ngram[0]:
            print '\nFile ' + input_file.name + ': '
            self.impression_ngrams(ngram, 1, words)
            self.impression_ext_ngrams(ngram, words, input_file, output_file)
        else:
            print input_file.name
            print 'Fichier ' + input_file.name + ': no repetition'
            output_file.write(input_file.name + ';' + str(0.) + ';' + str(0.) +';' + str(0.) +';' + str(0.) +';' + str(0.) +';' + str(0.) +';' + str(0.) +'\n')

        works_filename = WORKS_DIRECTORY + os.sep + input_file.name.split(os.sep)[-1]
        self.impression_repetitions(D, works_filename)

    # Return the number of repetition of L1 in L2
    def repetition_count(self, L1, L2, N=0):
        if L2 == []:
            return N
        elif L1 == L2[0:len(L1)]:
            return self.repetition_count(L1, L2[1:], N+1)
        else:
            return self.repetition_count(L1, L2[1:], N)

    def mot(self, L, C):
        for M in L:
            if self.begins_with_a_word(M) and not C == '':
                C = C + ' ' + M
            else:
                C = C + self.elim_point_virgules(M)
        return C

    def calculate_ngram(self, N, L, NG, tf, Di, Global):
        if NG[-1] == []:
            Di[N-1] = []
            return NG
        else:
            LN = []
            for x in NG[-1]:
                Nb = self.repetition_count(L[x:x+N], L[x:x+tf])
                if Nb > 1:
                    LN.append(x)
                    M = self.mot(L[x:x+N], '')
                    self.ajout_mot(Di[N-1], M)
                    self.ajout_mot(Global[N-1], M)
            NG.append(LN)
        Di[N-1] = self.classement_repetitions(Di[N-1])
        #print 'Di[' + str(N-1) + '] ' + str(Di[N-1])
        return NG

    # Initialize the output directory which looks like: <OUTPUT_ROOT>/<input_directory>
    # e.g. if input_directory is Corpus it would be: output/Corpus
    #
    # This allows you to run the analysis over different datasets without overwriting
    # exists results.
    def create_output_directory(self):
        self.output_directory = OUTPUT_ROOT + os.sep + self.input_directory

        # output root is where output from all runs gets placed
        if not os.path.isdir(OUTPUT_ROOT):
            os.mkdir(OUTPUT_ROOT)

        # output directory specific to the set of input
        if not os.path.isdir(self.output_directory):
            os.mkdir(self.output_directory)

        # output directory for resulting analysis of each work
        if not os.path.isdir(self.output_directory + os.sep + WORKS_DIRECTORY):
            os.mkdir(self.output_directory + os.sep + WORKS_DIRECTORY)

    # Initializes the file containing the repetition indices across the corpus.
    # Also initializes the Dictionary.
    def open_repetition_index_file(self, name="corpus_repetition_indices"):
        output_file = open(self.output_directory + os.sep + name + '.csv', 'w')
        output_file.write('Fichier')

        for i in range(1, MAXIMUM_PHRASE_LENGTH):
            output_file.write(';Length '+str(i))
        output_file.write('\n')
        return output_file

    # Initialize a dictionary used to store the repetition indices
    def create_repetition_dictionary(self):
        return [dict() for i in range(0, MAXIMUM_PHRASE_LENGTH)]

    def is_text_filename(self, filename):
        return filename[-4:] == '.txt'

    def populate_repetition_index(self, input_directory, repetition_index_file, repetition_dictionary):
        for input_filename in os.listdir(input_directory):
            if self.is_text_filename(input_filename):
                input_file = open(input_directory + os.sep + input_filename)
                self.detect_repetition(SIZE_WINDOW, input_file, repetition_index_file, repetition_dictionary)

    def analyze(self):
        print "Analyzing " + os.getcwd()

        repetition_index_file = self.open_repetition_index_file()
        repetition_dictionary = self.create_repetition_dictionary()

        self.populate_repetition_index(self.input_directory, repetition_index_file, repetition_dictionary)

        for i in range(1, MAXIMUM_PHRASE_LENGTH):
            repetition_dictionary[i-1] = self.classement_repetitions(repetition_dictionary[i-1])

        self.impression_repetitions(repetition_dictionary, 'corpus_phrase_reptitions.txt')

        repetition_index_file.close()

    def __init__(self, input_directory="Corpus"):
        self.input_directory = input_directory
        self.create_output_directory()

if __name__ == '__main__':
    RepetitionAnalyzer().analyze()
