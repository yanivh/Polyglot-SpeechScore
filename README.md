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

**Enhancing Learner Feedback Through Phonetic and Graphemic comparison**

The overarching objective is to assess how closely the learner's recorded speech matches the expected text. To achieve this, I examined two valid approaches within linguistic analysis: phonetic and graphemic representations. Each method offers unique insights depending on the context and criteria of comparison, detailed further in the attached appendix.

By incorporating both phonetic and graphemic representations, we aim to offer comprehensive feedback to learners. A high similarity score between the learner's input and the expected text will warrant positive feedback, while discrepancies may prompt suggestions for improvement. This approach ensures a thorough evaluation and helpful guidance for learners striving to improve their spoken language skills.

## **Solution walk-through**

**Create** a virtual environment and install the required packages:
`python3 -m venv .venv
source .venv/bin/activate` 



## **questions**