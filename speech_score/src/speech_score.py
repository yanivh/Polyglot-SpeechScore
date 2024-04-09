
import difflib
import numpy as np
from gruut import sentences
import nltk
from nltk.corpus import cmudict
import panphon
import ipapy as ipa

import epitran
import stanza
import speech_score.src.utils as speech_score_utils


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


def levenshtein_distance(s1, s2):
    # Create a matrix to store distances
    rows = len(s1) + 1
    cols = len(s2) + 1
    matrix = [[0] * cols for _ in range(rows)]

    # Initialize the first row and column
    for i in range(rows):
        matrix[i][0] = i
    for j in range(cols):
        matrix[0][j] = j

    # Fill in the rest of the matrix
    for i in range(1, rows):
        for j in range(1, cols):
            if s1[i - 1] == s2[j - 1]:
                substitution_cost = 0
            else:
                substitution_cost = 1
            matrix[i][j] = min(matrix[i - 1][j] + 1,  # Deletion
                               matrix[i][j - 1] + 1,  # Insertion
                               matrix[i - 1][j - 1] + substitution_cost)  # Substitution

    # Return the bottom-right value of the matrix
    return matrix[rows - 1][cols - 1]


def fuzzy_match(s1, s2):
    # Calculate Levenshtein distance
    distance = levenshtein_distance(s1, s2)

    # Normalize the distance
    max_len = max(len(s1), len(s2))
    normalized_distance = distance / max_len

    return normalized_distance


def wer(string_a, string_b):
    # length of each string
    len_a = len(string_a)
    len_b = len(string_b)

    # dp table
    dp = [[0 for x in range(len_a + 1)] for y in range(len_b + 1)]

    # initialize first row and first column
    for i in range(len_a + 1):
        dp[0][i] = i

    for i in range(len_b + 1):
        dp[i][0] = i

    # dp update
    for i in range(1, len_b + 1):
        for j in range(1, len_a + 1):
            index_a = j - 1
            index_b = i - 1
            cost = 0.0 if string_a[index_a] == string_b[index_b] else 1.0
            # From Peter M: Please fix this type error or delete this file / function if its not needed. Removing the pyright below will make the error visible
            dp[i][j] = min(  # pyright: ignore
                dp[i - 1][j - 1] + cost, min(dp[i - 1][j] + 1, dp[i][j - 1] + 1)
            )

    return dp[len_b][len_a]


def grapheme_to_phoneme_gruut( grapheme, lang="en"):

    for sent in sentences(grapheme, lang=lang, espeak=True):
        for word in sent:
            if word.phonemes:
                word_phonemes = word.phonemes
                print(word.text, *word.phonemes)
                # text_to_record_array.append(*word.phonemes)

    return word.phonemes


def text_into_phonetic_representations_nltk(word):
    # Load the CMU Pronouncing Dictionary
    nltk.download('cmudict')
    pronouncing_dict = cmudict.dict()

    # Convert the word to lowercase
    word = word.lower()

    # Get phoneme representation from CMU Pronouncing Dictionary
    if word in pronouncing_dict:
        return pronouncing_dict[word]
    else:
        return None


def text_into_phonetic_representations_epitran(word):
    # Convert the word to lowercase
    word = word.lower()

    # Create an Epitran object for English
    ep = epitran.Epitran('eng-Latn')

    # Transcribe text into IPA
    ipa_transcription = ep.transliterate(word, normpunc=True, ligatures=False)

    print("Original text:", word)
    print("IPA transcription:", ipa_transcription)

    return ipa_transcription


def word_segmentation(sentence, language='en'):
    punctuation_marks = '.,?!;:()[]{}"\'-'


    stanza.download('en')  # This downloads the English models for the neural pipeline
    nlp = stanza.Pipeline(language)  # This sets up a default neural pipeline in English
    doc = nlp(sentence)
    doc.sentences[0].print_dependencies()


    # Identify the language of the sentence
    words = nltk.word_tokenize(sentence)

    #  remove punctuation_marks
    words = [word for word in words if word not in punctuation_marks]

    return words


def break_word_to_graphemes(word, grapheme_list=['ee', 'll', 'ay', 'eu', 'ou', 'ou']):
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


def graphemic_comparison(list1, list2):
    for i in range(len(list1)):
        word1 = str(list1[i])
        if list2[i]:
            word2 = str(list2[i])
        else:
            word2 = ""

        # Convert the words to lowercase for case-insensitive comparison
        word1 = word1.lower()
        word2 = word2.lower()

        # Check if the words are identical
        if word1 == word2:
            print(f" {word1} : {word2} , words are identical")
            continue

        # Check if the words have the same length
        if len(word1) != len(word2):
            print(f" {word1} : {word2} , have different lengths.")
            # continue
            # return "The words have different lengths."

        # Initialize a counter for the number of differing characters
        differing_characters = 0

        # Iterate over each character in the words and count differences
        for char1, char2 in zip(word1, word2):
            if char1 != char2:
                differing_characters += 1

        # Generate a message based on the number of differing characters
        if differing_characters == 0:
            print(f" {word1} : {word2} ,The words have the same letters in different order.")
        elif differing_characters == 1:
            print(f" {word1} : {word2} ,The words differ by only one letter.")
        else:
            print(f" {word1} : {word2} ,The words differ by more than one letter.")


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

    learner_input = speech_score_utils.read_json_file("speech_score/data/metadata/learner_input.json")

    #  phonetic comparison section - start

    text_to_record = "I like to watch Youtube."
    sr_transcript_of_learner_recording = "I like to watch You too"

    phoible_segments_features_table = get_feature_table()

    text_to_record_words = word_segmentation(sentence=text_to_record, language='en')
    sr_transcript_of_learner_recording_words = word_segmentation(sentence=sr_transcript_of_learner_recording,
                                                                    language='en')

    text_to_record_phonetic = []
    for word in text_to_record_words:
        text_to_record_phonetic.append(grapheme_to_phoneme_gruut(word))


    sr_transcript_of_learner_recording_phonetic = []
    for word in sr_transcript_of_learner_recording_words:
        sr_transcript_of_learner_recording_phonetic.append(grapheme_to_phoneme_gruut(word))


    result = graphemic_comparison(text_to_record_phonetic, sr_transcript_of_learner_recording_phonetic)


    # for phone in gruut_text_to_record:
    #     print(phone)
    #     gruut_text_to_record_feature = extract_panphon_feature(phone, phoible_segments_features_table)
    #     print (gruut_text_to_record_feature)
    #
    # for phone in gruut_sr_transcript_of_learner_recording:
    #     print(phone)
    #     gruut_sr_transcript_of_learner_recording_feature = extract_panphon_feature(phone, phoible_segments_features_table)
    #     print (gruut_sr_transcript_of_learner_recording_feature)
    #
    #     text_to_record_feature_lst = np.array(text_to_record_feature[0], dtype=np.float32)
    # sr_transcript_of_learner_recording_feature_lst = np.array(sr_transcript_of_learner_recording_feature[0],
    #                                                           dtype=np.float32)
    #
    # print(np.inner(text_to_record_feature_lst, sr_transcript_of_learner_recording_feature_lst))

    print(1)

    #  phonetic comparison section - end

    #  graphemic comparison section - start
    nltk.download('punkt')

    text_to_record = "one"
    sr_transcript_of_learner_recording = "won"

    text_to_record_words = break_sentence_words(sentence=text_to_record, language='en')
    sr_transcript_of_learner_recording_words = break_sentence_words(sentence=sr_transcript_of_learner_recording,
                                                                    language='en')

    text_to_record_graphemes = []
    for word in text_to_record_words:
        text_to_record_graphemes.append(break_word_to_graphemes(word))
        print(text_to_record_graphemes)

    sr_transcript_of_learner_recording_graphemes = []
    for word in sr_transcript_of_learner_recording_words:
        sr_transcript_of_learner_recording_graphemes.append(break_word_to_graphemes(word))
        print(sr_transcript_of_learner_recording_graphemes)

    result = graphemic_comparison(text_to_record_graphemes, sr_transcript_of_learner_recording_graphemes)

#  graphemic comparison section - end


#  not relevant section


# similarity_ratio = dist = np.linalg.norm(np.array(text_to_record_graphemes)-np.array(sr_transcript_of_learner_recording_graphemes))
# similarity_ratio    = evaluate_pronunciation(sr_transcript_of_learner_recording_graphemes, text_to_record_graphemes)

# print(similarity_ratio)

# text_to_record = "watch yo "
# sr_transcript_of_learner_recording = "watch you"

# ipapy
# ipapy_word1_1 = text_into_phonetic_representations_epitran(text_to_record)
# ipapy_word1_2 = text_into_phonetic_representations_epitran(sr_transcript_of_learner_recording)

# gruut
# gruut_word1 = text_into_phonetic_representations_gruut(text_to_record.split(' ')[0])
# gruut_word2 = text_into_phonetic_representations_gruut(sr_transcript_of_learner_recording.split(' ')[0])

# nltk
# nltk_word1_1 = text_into_phonetic_representations_nltk(text_to_record.split(' ')[0])
# nltk_word1_2 = text_into_phonetic_representations_nltk(sr_transcript_of_learner_recording.split(' ')[0])


# feature_table= feature_table()


# word1 = "euro"


# a=feature_table[phonemes_word1[0][0]]

# Print the phonemes for each word
# print(f"Phonemes for '{word1}': {phonemes_word1}")


# distance = fuzzy_match(text_to_record, sr_transcript_of_learner_recording)
# print("Normalized Levenshtein distance between '{}' and '{}' is: {}".format(text_to_record, sr_transcript_of_learner_recording, distance))

# a1 = wer(text_to_record, sr_transcript_of_learner_recording)


# result_embedding = embedding_(text_to_record, sr_transcript_of_learner_recording)

# print(f'similarity_ratio: {similarity_ratio}, result_embedding{result_embedding}')


# price_str = "€2.5"
# converted_price = convert_to_words(price_str)
# print(converted_price)  # Output: "two and a half euros"
