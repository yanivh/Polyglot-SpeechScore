import difflib
import numpy as np
from gruut import sentences
import nltk
from utils import read_json_file
from itertools import zip_longest


def evaluate_pronunciation(text_to_record, sr_transcript_of_learner_recording):
    # Clean up the transcripts and remove punctuation
    # clean_text_to_record = ''.join(ch for ch in text_to_record if ch.isalnum()).lower()
    # clean_sr_transcript = ''.join(ch for ch in sr_transcript_of_learner_recording if ch.isalnum()).lower()

    # Calculate the similarity ratio between the expected text and the learner's transcript
    similarity_ratio = difflib.SequenceMatcher(None, text_to_record, sr_transcript_of_learner_recording).ratio()

    print(similarity_ratio)

    # Define a threshold for similarity ratio
    threshold = 0.8

    # Provide feedback based on the similarity ratio
    if similarity_ratio >= threshold:
        print("Your pronunciation sounds good!")
    else:
        print("Your pronunciation needs improvement. Try repeating the phrase again.")

    return similarity_ratio


def grapheme_to_phoneme_gruut(grapheme, lang="en"):
    '''

    :param grapheme:
    :param lang:
    :return:
    '''
    for sent in sentences(grapheme, lang=lang, espeak=True):
        for word in sent:
            if word.phonemes:
                print(word.text, *word.phonemes)
    return word.phonemes


def word_segmentation(sentence, language='en'):
    '''
        Description:
        Convert to lowercase
        tokaniz e the sentence
        Removing extra symbols,
        todo: Remove not alphabetic characters.
        todo : Remove duplicates.
        :param
            sentence:
            language: default 'en'
        :return:
        '''

    punctuation_marks = '.,?!;:()[]{}"\'-'

    sentence = sentence.lower()

    # Identify the language of the sentence
    words = nltk.word_tokenize(sentence, language=language)

    #  remove punctuation_marks
    words = [word for word in words if word not in punctuation_marks]

    return words


def break_word_to_graphemes(word, grapheme_list=['ee', 'll', 'ay', 'eu', 'ou', 'ou']):
    '''
    Break a word into graphemes based on a list of graphemes
    :param word:
    :param grapheme_list:
    :return:
    '''
    # Convert  word to lowercase for case-insensitive comparison
    word = word.lower()

    graphemes = []
    i = 0
    while i < len(word):
        if i < len(word) - 1 and word[i:i + 2] in grapheme_list:
            index = grapheme_list.index(word[i:i + 2])
            graphemes.append(grapheme_list[index])
            i += 2
        elif word[i] in grapheme_list:
            graphemes.append(word[i])
            i += 1
        else:
            graphemes.append(word[i])
            i += 1
    return graphemes


def calculate(text_to_record_phonemes, text_learner_recording_phonemes):
    '''

    :param text_to_record_phonemes:
    :param text_learner_recording_phonemes:
    :return:
    '''

    output = []

    try:

        for i, (elem1, elem2) in enumerate(
                zip_longest(text_to_record_phonemes, text_learner_recording_phonemes, fillvalue=None)):

            #  check if elem1 and elem2 are not None
            if elem2 != None and elem1 != None:
                text_to_record_phonemes_ = elem1
                text_learner_recording_phonemes_ = elem2
            elif elem1 == None:
                text_to_record_phonemes_ = {'word': [], 'phonemes': []}
            elif elem2 == None:
                text_learner_recording_phonemes_ = {'word': [], 'phonemes': []}

            difference, matches = phoneme_comparison(text_to_record_phonemes_['phonemes'],
                                                     text_learner_recording_phonemes_['phonemes'])

            if len(matches) == 0 and len(difference) == 0:
                output.append({'word': '', 'match_score': 0})
            elif difference:
                output.append({'word': text_to_record_phonemes_['word'], 'match_score': f'-{len(difference)}'})
            else:
                output.append({'word': text_to_record_phonemes_['word'],
                               'match_score': len(matches) / len(text_to_record_phonemes_['phonemes'])})

    except Exception as e:
        print(f"Error: {e}")

    return output


def phoneme_comparison(text_to_record_phonetic, text_learner_recording_phonetic):
    '''

    :param text_to_record_phonetic:
    :param text_learner_recording_phonetic:
    :return:
    '''
    output = []

    difference = list(set(text_to_record_phonetic).difference(text_learner_recording_phonetic))
    matches = list(set(text_to_record_phonetic).intersection(text_learner_recording_phonetic))

    return difference, matches


def graphemic_comparison(text_to_record_phonetic, text_learner_recording_phonetic):
    '''

    :param text_to_record_phonetic:
    :param text_learner_recording_phonetic:
    :return:
    '''
    output = []
    for i in range(len(text_to_record_phonetic)):
        text_to_record_word = str(text_to_record_phonetic[i])
        if text_learner_recording_phonetic[i]:
            text_learner_recording_word = str(text_learner_recording_phonetic[i])
        else:
            text_learner_recording_word = ""

        difference = list(set(text_to_record_phonetic[i]).difference(text_learner_recording_phonetic[i]))
        matches = list(set(text_to_record_phonetic[i]).intersection(text_learner_recording_phonetic[i]))

        return difference, matches


def get_feature_table():
    feature_table = {}

    lines = open(
        "phoible-segments-features.tsv",
        "r",
        encoding="utf-8",
    ).readlines()
    for line in lines[1:]:
        fields = line.strip().split("\t")
        phone = fields[0]

        feats = []
        for field in fields[1:]:
            if field == "0":
                feats.append(0)
            elif field == "-":
                feats.append(-1)
            elif field == "+":
                feats.append(1)
            else:
                feats.append(0)

        feature_table[phone] = np.array(feats)

    return feature_table


def extract_panphon_feature(phone, phoible_segments_features_table, language='en'):
    if phone not in phoible_segments_features_table:
        return np.zeros(37)
    else:
        return phoible_segments_features_table[phone]


if __name__ == "__main__":

    nltk.download('punkt')
    learner_inputs = read_json_file("speech_score/data/metadata/learner_input.json")
    # phoible_segments_features_table = get_feature_table()

    result = []
    text_to_record = ""
    text_learner_recording = ""

    #  iterate on learner input sentences
    for learner_input in learner_inputs:
        text_to_record = learner_input['text_to_record']
        text_learner_recording = learner_input['sr_transcript_of_learner_recording']

        # Phonetic comparison section - Start
        text_to_record_words = word_segmentation(sentence=text_to_record, language='english')
        text_learner_recording_words = word_segmentation(sentence=text_learner_recording, language='english')

        text_to_record_phonemes = []
        for word in text_to_record_words:
            text_to_record_phonemes.append({'word': word, 'phonemes': grapheme_to_phoneme_gruut(word)})

        text_learner_recording_phonemes = []
        for word in text_learner_recording_words:
            text_learner_recording_phonemes.append({'word': word, 'phonemes': grapheme_to_phoneme_gruut(word)})

        result.append(calculate(text_to_record_phonemes, text_learner_recording_phonemes))
    print(result)

    #  phonetic comparison section - end

    #  graphemic comparison section - start
    # text_to_record_words = word_segmentation(sentence=text_to_record, language='english')
    # text_learner_recording_words = word_segmentation(sentence=text_learner_recording, language='english')
    #
    # text_to_record_graphemes = []
    # for word in text_to_record_words:
    #     text_to_record_graphemes.append(break_word_to_graphemes(word))
    #
    #
    # text_learner_recording_graphemes = []
    # for word in text_learner_recording_words:
    #     text_learner_recording.append(break_word_to_graphemes(word))
    #
    # result = graphemic_comparison(text_to_record_graphemes, text_learner_recording_graphemes)

#  graphemic comparison section - end
