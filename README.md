# Tech Challenge

[Repository](https://github.com/yanivh/Polyglot-SpeechScore/tree/main) for the Tech Challenge

## **Coding Challenge description**
In **learner_input.json**, you are given an example input from one speaking exercise of a Lithuanian learning English. It contains the following information:

**text_to_record**: the phrase that the learner was asked to record.
**learner_recording**: file name of the corresponding learner recording in audios/ folder. 

You don't have to use these recordings in your implementation but you should listen to them.

**sr_transcript_of_learner_recording**: speech recognition transcript of what the learner said (we have already transribed the recordings for you to save time).

Your task is to, using Python and any other resources of your liking, implement a basic system that would **evaluate** this input and **give** the learner some **feedback**:

the goal of evaluation is to compare the expected result (**text_to_record**) with the learner input (**sr_transcript_of_learner_recording**) to assess whether the learner attempt was successful.

the goal of feedback is to **return** a **fair** and **helpful** message based on the results of the evaluation step. It is up to you to create this message. Some examples could be simply saying right or wrong, or returning phrases that should be repeated.


## **Solution description**

**Enhancing Learner Feedback Through Phonetic comparison**

Approaching this task I  found 2 valid options within the domain of linguistic analysis. <br><br>
**Phonetic** Comparison,  is useful when the focus is on pronunciation or when assessing similarity based on sound rather than spelling.<br><br>
**Graphemic** Comparison, is useful when the focus is on orthographic similarities or when assessing similarity based on spelling rather than pronunciation	<br><br>
Due to the limit of time I decided to focus on **Phonetic Comparison** , even though I am aware of the importance of Graphemic Comparison in providing vital data that can improve the overall user Feedback.



####     **Code Description - High level**

        Reads the learner inputs from a JSON file
        Gets the threshold from a config file
        Iterates over the learner inputs
        For each input
            Gets the expected text and the learner's transcript
            calculates the similarity ratio and feedback
            Performs a phonetic comparison
            Appends the results to a list
            Print informative message
        Finally, it writes the results to a JSON file and prints them.

#### Code Description - In details

The provided Python code is part of a larger project that aims to assess the pronunciation of a learner based on the similarity ratio between the expected text and the learner's transcript. The code uses several libraries such as `gruut`, `nltk`, and `difflib` to achieve this.

The function `assess_similarity(expected_text, learner_transcript, threshold=0.7)` is the main function that calculates the similarity ratio between the expected text and the learner's transcript. It uses the `difflib.SequenceMatcher` class to calculate this ratio. If the ratio is greater than or equal to the threshold (default is 0.7), it provides positive feedback, otherwise, it suggests improvement.
<br><br>
**difflib.SequenceMatcher** - provides a general indication of how similar the sequences are based on their characters or elements.

```python
similarity_ratio = difflib.SequenceMatcher(None, expected_text, learner_transcript).ratio()
if similarity_ratio >= threshold:
    feedback = f"Sounds good!"
else:
    feedback = f"Needs improvement!"
```

The function `grapheme_to_phoneme_gruut(grapheme, lang="en")` uses the `gruut` library to convert graphemes (written language) to phonemes (spoken language). It iterates over the sentences and words, printing the word and its phonemes.

The `word_segmentation(sentence, language='en')` function tokenizes the input sentence into words using the `nltk.word_tokenize` function, and removes punctuation marks.

The `phoneme_feedback(mismatch, matches)` function provides feedback based on the phoneme comparison output. If there are no mismatches, it provides positive feedback, otherwise, it suggests improvement.

The `phoneme_difference(elem1, elem2, threshold=0.7)` function calculates the difference between two phonemes. It uses the `phoneme_comparison` function to get the difference and matches between the phonemes of the expected text and the learner's transcript.

The `calculate(expected_text_phonemes, learner_transcript_phonemes, threshold=0.7)` function calculates the difference between the expected text phonemes and the learner transcript phonemes. It uses the `phoneme_difference` function to get the output for each pair of phonemes.

The `phonetic_comparison(expected_text_words, learner_transcript_words, threshold=0.7)` function performs a phonetic comparison based on the phonetic transcription of the words. It uses the `word_segmentation` function to segment the sentences into words, the `grapheme_to_phoneme_gruut` function to convert the words to phonemes, and the `calculate` function to get the comparison result.

The  `create_message` function generates a helpful message based on the results of the evaluation step. It calculates the total match score and identifies the words that need practice and the words that were successful. It then generates a message based on these results.


```python
if len(words_to_practice) > 0:
    message.append(f"Great effort! You're doing well with most of the words in the phrase. Let's focus on improving the pronunciation "
                   f"of words: \n {f' , '.join(words_to_practice)} \n to bring your accuracy even higher. Keep practicing, and youll master it in no time!")
else:
    message.append(f"Great job! You're doing well with all of the words in the phrase.")
```

In the `if __name__ == "__main__"` block, the code reads the learner inputs from a JSON file, gets the threshold from a config file, and iterates over the learner inputs. For each input, it gets the expected text and the learner's transcript, calculates the similarity ratio and feedback, performs a phonetic comparison, and appends the results to a list. Finally, it writes the results to a JSON file and prints them.

#### learner_output 

```json
[
    [
        {
            "expected_text": "I have two and a half euros.",
            "learner_transcript": "I have a, I have \u20ac8.5."
        },
        {
            "similarity_ratio": 0.52,
            "feedback": "Needs improvement!"
        },
        [
            [
                {
                    "word": "i",
                    "match_score": 1,
                    "feedback": "Sounds good!"
                }
            ],
            [
                {
                    "word": "have",
                    "match_score": 1,
                    "feedback": "Sounds good!"
                }
            ],
            [
                {
                    "word": "two",
                    "match_score": "-2",
                    "feedback": "Needs improvement!"
                }
            ],
            [
                {
                    "word": "and",
                    "match_score": "-3",
                    "feedback": "Needs improvement!"
                }
            ],
            [
                {
                    "word": "a",
                    "match_score": "-1",
                    "feedback": "Needs improvement!"
                }
            ],
            [
                {
                    "word": "half",
                    "match_score": "-3",
                    "feedback": "Needs improvement!"
                }
            ],
            [
                {
                    "word": "euros",
                    "match_score": "-6",
                    "feedback": "Needs improvement!"
                }
            ]
        ],
        [
            "Great effort! You're doing well with most of the words in the phrase. Let's focus on improving the pronunciation of words: \n two , and , a , half , euros \n to bring your accuracy even higher. Keep practicing, and youll master it in no time!"
        ]
    ],
    [
        {
            "expected_text": "interesting",
            "learner_transcript": "Interesting."
        },
        {
            "similarity_ratio": 0.8695652173913043,
            "feedback": "Sounds good!"
        },
        [
            [
                {
                    "word": "interesting",
                    "match_score": 0.7777777777777778,
                    "feedback": "Sounds good!"
                }
            ]
        ],
        [
            "Great job! You're doing well with all of the words in the phrase."
        ]
    ],
    [
        {
            "expected_text": "won",
            "learner_transcript": "One."
        },
        {
            "similarity_ratio": 0.2857142857142857,
            "feedback": "Needs improvement!"
        },
        [
            [
                {
                    "word": "won",
                    "match_score": 1,
                    "feedback": "Sounds good!"
                }
            ]
        ],
        [
            "Great job! You're doing well with all of the words in the phrase."
        ]
    ],
    [
        {
            "expected_text": "Today is the thirteenth of May, twenty twenty three.",
            "learner_transcript": "Today is the 13th of May, 2023."
        },
        {
            "similarity_ratio": 0.6024096385542169,
            "feedback": "Needs improvement!"
        },
        [
            [
                {
                    "word": "today",
                    "match_score": 1,
                    "feedback": "Sounds good!"
                }
            ],
            [
                {
                    "word": "is",
                    "match_score": 1,
                    "feedback": "Sounds good!"
                }
            ],
            [
                {
                    "word": "the",
                    "match_score": 1,
                    "feedback": "Sounds good!"
                }
            ],
            [
                {
                    "word": "thirteenth",
                    "match_score": 0.8333333333333334,
                    "feedback": "Sounds good!"
                }
            ],
            [
                {
                    "word": "of",
                    "match_score": 1,
                    "feedback": "Sounds good!"
                }
            ],
            [
                {
                    "word": "may",
                    "match_score": 1,
                    "feedback": "Sounds good!"
                }
            ],
            [
                {
                    "word": "twenty",
                    "match_score": "-5",
                    "feedback": "Needs improvement!"
                }
            ],
            [
                {
                    "word": "twenty",
                    "match_score": "-5",
                    "feedback": "Needs improvement!"
                }
            ],
            [
                {
                    "word": "three",
                    "match_score": "-3",
                    "feedback": "Needs improvement!"
                }
            ]
        ],
        [
            "Great effort! You're doing well with most of the words in the phrase. Let's focus on improving the pronunciation of words: \n twenty , twenty , three \n to bring your accuracy even higher. Keep practicing, and youll master it in no time!"
        ]
    ]
]
                    
```

#### Questions : 

#### Question 1
What limitations of using a speech-to-text engine for pronunciation training purposes have you observed?

#### Your answer

* **Limitation of Integer Representation**: Speech-to-text engines may encounter challenges in accurately transcribing numerical values, such as currency amounts (e.g., €8.5), years (e.g., 2023), or ordinal numbers (e.g., 13th), which require proper interpretation and representation.
* **Text Duplication:** Speech-to-text systems may struggle to correctly identify and handle instances of text duplication within a spoken utterance, leading to potential errors or redundancies in the transcription output. For instance, the phrase "I have a, I have" could be misinterpreted.
* **Lowercase Representation**: Speech-to-text engines may face difficulties in distinguishing between uppercase and lowercase letters, which can impact the accuracy of transcribed text, especially in cases where capitalization carries semantic significance. For example, transcribing "Interesting" as "interesting" may alter the intended meaning.
* **Identification of Similar Sounds**: Speech-to-text systems may have difficulty distinguishing between words that sound similar but have different meanings (homophones), leading to potential errors in transcription. For instance, "won" being transcribed as "one" could result in semantic inaccuracies.
* **Representation of Dates in Specific Formats**: Speech-to-text engines may struggle to accurately transcribe dates expressed in specific formats, such as "13th of May, 2023," requiring robust handling of date formats to ensure accurate interpretation and representation in the transcribed text. 

#### Question 2

You had very limited resources for this  implementation. Briefly describe what kind of approach you might have chosen if time and resources would not have been a problem.


#### Your answer
I will explore in few areas : <br>

* **Improved Speech-to-Text Engine**: Conduct thorough validation of various speech recognition models, including  [open source ](https://github.com/openai/whisper) solutions like Whisper by OpenAI. Explore the possibility of model retraining using Babbel user audio recordings to fine-tune in-house speech-to-text models.<br><br>
* **Enhanced Phoneme Recognition**: Investigate phoneme recognition libraries such as g2p and phonemizer to improve accuracy. Utilize Babbel user audio recordings and phoneme data for training the phoneme recognition model. Address potential issues identified in the previous question, such as similar sounds and text duplication.<br><br>
* **Support for Multiple Languages**: Expand the system's language support to cater to a diverse user base. This involves integrating language-specific models and datasets for accurate speech recognition and phoneme analysis across various languages.<br><br>
* **Implement Graphemic Comparison**: Develop a robust graphemic comparison mechanism to analyze differences and similarities in textual representations. This allows for more accurate assessment of pronunciation and feedback provision tailored to specific grapheme-phoneme mappings.<br><br>
* **Improved Feedback Mechanism**: Enhance the feedback mechanism to provide fair and helpful messages based on evaluation results. Consider implementing visual outputs for easier interpretation of feedback. Additionally, offer users the option to focus on practicing specific phonemes identified as challenging based on their performance.<br><br>
