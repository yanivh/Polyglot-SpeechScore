import nltk
from utils import read_json_file, write_json_file, get_threshold, read_json_file
from utils_audio import play_audio, create_audio_from_phonemes, transcribe_audio, diarization_audio_pyannote
from utils_speech_recognition import word_segmentation, grapheme_to_phoneme
from itertools import zip_longest
import difflib
import pyannote


def assess_similarity(expected_text, learner_transcript, threshold=0.7):
    """
    Assess the pronunciation of a learner based on the similarity ratio between the expected text and the learner's transcript.
    :param expected_text: The expected text to be pronounced by the learner.
    :param learner_transcript: The transcript of the learner's pronunciation.
    :param threshold: Define a threshold for similarity ratio.
    :return: Similarity ratio between the expected text and learner's transcript.
    """
    # Calculate the similarity ratio between the expected text and the learner's transcript
    similarity_ratio = difflib.SequenceMatcher(None, expected_text, learner_transcript).ratio()
    feedback = f""
    # Provide feedback based on the similarity ratio
    if similarity_ratio >= threshold:
        feedback = f"Sounds good!"
    else:
        feedback = f"Needs improvement!"

    return similarity_ratio, feedback


def phoneme_feedback(mismatch, matches):
    '''
    Provide feedback based on the phoneme comparison output
    :param output:
    :return:
    '''

    # Check if all values are equal to 1
    if len(mismatch) == 0:
        feedback = f"Sounds good!"
    else:
        feedback = f"Needs improvement!"

    return feedback


def phoneme_difference(elem1, elem2, threshold=0.7):
    '''
    Calculate the difference between two phonemes
    :param elem1:
    :param elem2:
    :param threshold:
    :return:
    '''

    try:
        output = []
        if elem2 is not None and elem1 is not None:
            expected_text_phonemes_ = elem1
            learner_transcript__phonemes_ = elem2
        elif elem2 is None and elem1 is not None:
            expected_text_phonemes_ = elem1
            learner_transcript__phonemes_ = {'word': [], 'phonemes': []}

        difference, matches = phoneme_comparison(expected_text_phonemes_['phonemes'],
                                                 learner_transcript__phonemes_['phonemes'])

        feedback = phoneme_feedback(difference, matches)

        if len(matches) == 0 and len(difference) == 0:
            output.append({'word': '', 'match_score': 0, 'feedback': feedback})
        elif difference:
            output.append(
                {'word': expected_text_phonemes_['word'], 'match_score': f'-{len(difference)}', 'feedback': feedback})

        else:
            output.append({'word': expected_text_phonemes_['word'],
                           'match_score': len(matches) / len(expected_text_phonemes_['phonemes']),
                           'feedback': feedback})

    except Exception as e:
        print(f"Error: {e}")

    return output


def calculate(expected_text_phonemes, learner_transcript_phonemes, threshold=0.7):
    '''
    Calculate the difference between the expected text phonemes and the learner transcript phonemes
    :param expected_text_phonemes:
    :param learner_transcript_phonemes:
    :return:
    '''

    output = []

    try:
        for i, (elem1, elem2) in enumerate(
                zip_longest(expected_text_phonemes, learner_transcript_phonemes, fillvalue=None)):
            output.append(phoneme_difference(elem1, elem2, threshold=threshold))

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


def phonetic_comparison(expected_text_words, learner_transcript_words, threshold=0.7):
    '''
    phanetic comparison based on the phonetic transcription of the words
    :param expected_text_words:
    :param learner_transcript_words:
    :return:
    '''

    feedback = ""
    comparison = []

    expected_text_words = word_segmentation(sentence=expected_text, language='english')
    learner_transcript_words = word_segmentation(sentence=learner_transcript, language='english')

    expected_text_phonemes = []
    for word in expected_text_words:
        expected_text_phonemes.append({'word': word, 'phonemes': grapheme_to_phoneme(word)})

    learner_transcript_phonemes = []
    for word in learner_transcript_words:
        learner_transcript_phonemes.append({'word': word, 'phonemes': grapheme_to_phoneme(word)})

    comparison = calculate(expected_text_phonemes, learner_transcript_phonemes, threshold=threshold)

    return comparison


def create_message(sentence_result):
    '''
    return a fair and helpful message based on the results of the evaluation step.
    :return:
    '''

    message = []

    total_match_score = 0
    words_to_practice = []
    words_successful = []
    for word_result in sentence_result[2]:
        if int(word_result[0]['match_score']) < 0 or word_result[0] is None:
            words_to_practice.append(word_result[0]['word'])
        else:
            words_successful.append(word_result[0]['word'])

    if len(words_to_practice) > 0:
        message.append(
            f"Great effort! You're doing well with most of the words in the phrase. Let's focus on improving the pronunciation "
            f"of words: \n {f' , '.join(words_to_practice)} \n to bring your accuracy even higher. Keep practicing, and youll master it in no time!")
    else:
        message.append(f"Great job! You're doing well with all of the words in the phrase.")

    return message


if __name__ == "__main__":

    # model trained to work well for multiple languages
    nltk.download('punkt')

    learner_inputs = read_json_file("speech_score/data/metadata/learner_input.json")

    threshold = get_threshold("speech_score/data/config/config.json")

    result = []

    #  Iterate on learner input sentences
    for learner_input in learner_inputs:
        #  initialize variables for each sentence
        sentence_result = []
        expected_text = ""
        learner_transcript = ""
        similarity_ratio = 0
        feedback = ""
        assess_pronunciation_result = {}

        expected_text = learner_input['text_to_record']
        learner_transcript = learner_input['sr_transcript_of_learner_recording']

        #  Give some general feedback on the overall sentence
        similarity_ratio, feedback = assess_similarity(expected_text, learner_transcript, threshold=threshold)

        #  Give feedback on each word in the sentence
        phonetics_comparison = phonetic_comparison(expected_text, learner_transcript, threshold=threshold)

        # Add all analysis results to the result list
        sentence_result.append({'expected_text': expected_text, 'learner_transcript': learner_transcript})
        sentence_result.append({'similarity_ratio': similarity_ratio, 'feedback': feedback})
        sentence_result.append(phonetics_comparison)

        helpful_message = create_message(sentence_result)

        sentence_result.append(helpful_message)
        result.append(sentence_result)

        print(helpful_message)

    # Save the result to a JSON file
    write_json_file(result, "speech_score/data/metadata/learner_output.json")
    print(result)

    # continue to ɛkˈspɛrɪm(ə)nt/ with Audio-to-text

    # file_name = "youtube.wav"  # Replace with the path to your audio file
    file_name = "euros.wav"
    play_audio("speech_score/data/audios", file_name)
    diarization = diarization_audio_pyannote(file_name)
    transcribe = transcribe_audio(file_name, model_size="small.en")
    print (transcribe)
