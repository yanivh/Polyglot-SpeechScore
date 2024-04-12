# Tech Challenge

## **objective**

The primary objective of this exercise is to help you gain a better understanding of the types of problems you would be solving in your daily work, rather than testing the coding skills. Additionally, this challenge allows us to observe your problem-solving approach and thought process within the language learning domain.


## **Coding description**
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
        Gets the threshold from a config file, 
        Iterates over the learner inputs.
        For each input
            Gets the expected text and the learner's transcript, 
            calculates the similarity ratio and feedback, 
            Performs a phonetic comparison
            Appends the results to a list. 
        Finally, it writes the results to a JSON file and prints them

#### Code Description - In details

The provided Python code is part of a larger project that aims to assess the pronunciation of a learner based on the similarity ratio between the expected text and the learner's transcript. The code uses several libraries such as `gruut`, `nltk`, and `difflib` to achieve this.

The function `assess_similarity(expected_text, learner_transcript, threshold=0.7)` is the main function that calculates the similarity ratio between the expected text and the learner's transcript. It uses the `difflib.SequenceMatcher` class to calculate this ratio. If the ratio is greater than or equal to the threshold (default is 0.7), it provides positive feedback, otherwise, it suggests improvement.

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
        ]
    ]
]
                    
```

#### Questions : 

#### Question 1
What limitations of using a speech-to-text engine for pronunciation training purposes have you observed?

#### Your answer

 - Integer representation, for example: €8.5 , 2023 , 13th<br>
 - Text duplication, for example : I have a, I have<br>
 - Lower case, for example : Interesting<br>
 - Identify similar Sounds, for example : One instead   won<br>
 - Represent date per specific format, for example : 13th of May, 2023<br>

#### Question 2

You had very limited resources for this  implementation. Briefly describe what kind of approach you might have chosen if time and resources would not have been a problem.


#### Your answer
I will invest time in few areas: <br>
<br>
**Improved speech-to-text engine**
* Validate different speech recognition models like the [open source version ](https://github.com/openai/whisper)of **Whisper** by OpenAi.
* Model Retraining - Using Babbel user audio recordings, to retrain in house speech-to-text models.  

**Improve phonemes recognition**
* Enhance the system's accuracy.
* addressing any potential issues (describe in in the previous question)
* Support multiple languages


**Implement Graphemic Comparison**
<br><br>
**Improve feedback**
* Give a fair and helpful message based on the results of the evaluation step.
**Visual output** 
* Option to practice the specific phoneme, identified as difficult for users to practice.
