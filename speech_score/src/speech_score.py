from gruut import sentences
import nltk
from utils import read_json_file
from itertools import zip_longest
import difflib


def assess_pronunciation(expected_text, learner_transcript, threshold = 0.8):
    """
    Assess the pronunciation of a learner based on the similarity ratio between the expected text and the learner's transcript.
    :param expected_text: The expected text to be pronounced by the learner.
    :param learner_transcript: The transcript of the learner's pronunciation.
    :param threshold: Define a threshold for similarity ratio.
    :return: Similarity ratio between the expected text and learner's transcript.
    """
    # Calculate the similarity ratio between the expected text and the learner's transcript
    similarity_ratio = difflib.SequenceMatcher(None, expected_text, learner_transcript).ratio()

    # Provide feedback based on the similarity ratio
    if similarity_ratio >= threshold:
        print(" Sounds good!")
    else:
        print(" Needs improvement!")

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
        tokanize
        Removing extra symbols,
        todo: Remove not alphabetic characters.
        todo : Remove duplicates text.
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


def calculate(expected_text_phonemes, learner_transcript_phonemes):
    '''

    :param expected_text_phonemes:
    :param learner_transcript_phonemes:
    :return:
    '''

    output = []

    try:

        for i, (elem1, elem2) in enumerate(
                zip_longest(expected_text_phonemes, learner_transcript_phonemes, fillvalue=None)):

            #  check if elem1 and elem2 are not None
            if elem2 != None and elem1 != None:
                expected_text_phonemes_ = elem1
                learner_transcript__phonemes_ = elem2
            elif elem1 == None:
                expected_text_phonemes_ = {'word': [], 'phonemes': []}
            elif elem2 == None:
                learner_transcript__phonemes_ = {'word': [], 'phonemes': []}

            difference, matches = phoneme_comparison(expected_text_phonemes_['phonemes'],
                                                     learner_transcript__phonemes_['phonemes'])

            if len(matches) == 0 and len(difference) == 0:
                output.append({'word': '', 'match_score': 0})
            elif difference:
                output.append({'word': expected_text_phonemes_['word'], 'match_score': f'-{len(difference)}'})
            else:
                output.append({'word': expected_text_phonemes_['word'],
                               'match_score': len(matches) / len(expected_text_phonemes_['phonemes'])})

    except Exception as e:
        print(f"Error: {e}")

    return output


def phoneme_comparison(text_to_record_phonetic, text_learner_recording_phonetic):
    '''

    :param text_to_record_phonetic:
    :param text_learner_recording_phonetic:
    :return:
    '''

    difference = list(set(text_to_record_phonetic).difference(text_learner_recording_phonetic))
    matches = list(set(text_to_record_phonetic).intersection(text_learner_recording_phonetic))

    return difference, matches

def phonetic_comparison (expected_text_words, learner_transcript_words):
    '''
    phanetic comparison based on the phonetic transcription of the words
    :param expected_text_words:
    :param learner_transcript_words:
    :return:
    '''

    expected_text_words = word_segmentation(sentence=expected_text, language='english')
    learner_transcript_words = word_segmentation(sentence=learner_transcript, language='english')

    expected_text_phonemes = []
    for word in expected_text_words:
        expected_text_phonemes.append({'word': word, 'phonemes': grapheme_to_phoneme_gruut(word)})

    learner_transcript_phonemes = []
    for word in learner_transcript_words:
        learner_transcript_phonemes.append({'word': word, 'phonemes': grapheme_to_phoneme_gruut(word)})

    comparison = calculate(expected_text_phonemes, learner_transcript_phonemes)

    return comparison


if __name__ == "__main__":

    nltk.download('punkt')
    learner_inputs = read_json_file("speech_score/data/metadata/learner_input.json")

    result = []
    expected_text = ""
    learner_transcript = ""

    #  iterate on learner input sentences
    for learner_input in learner_inputs:
        expected_text = learner_input['text_to_record']
        learner_transcript = learner_input['sr_transcript_of_learner_recording']

        #  Give some general feedback on the overall sentence
        assess_pronunciation(expected_text, learner_transcript)

        #  Give feedback on each word in the sentence
        comparison = phonetic_comparison(expected_text, learner_transcript)

        result.append(comparison)

    print(result)

