import os
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import torch
from waveglow.glow import WaveGlow
import whisper
from utils_speech_recognition import words_per_segment
from utils import get_config_key
from pyannote.audio import Pipeline
import pyannote


def transcribe_audio(file_name, model_size='base.en', folder_path="speech_score/data/audios"):
    '''

    # Size         Parameters  English-only model  Multilingual model  Required VRAM  Relative speed
    # tiny         39 M        tiny.en             tiny                ~1 GB          ~32x
    # base         74 M        base.en             base                ~1 GB          ~16x
    # small        244 M       small.en            small               ~2 GB          ~6x
    # medium       769 M       medium.en           medium              ~5 GB          ~2x
    # large        1550 M      N/A                 large               ~10 GB         1x

    :param size:
    :param file_name:
    :param folder_path:
    :return:
    '''
    audio_file_path = os.path.join(folder_path, file_name)
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_file_path)
    return result["text"]


# Function to play audio
def play_audio(folder_path, file_name):
    audio_file_path = os.path.join(folder_path, file_name)
    audio = AudioSegment.from_wav(audio_file_path)
    play(audio)


def synthesize_speech():
    # Initialize Tacotron 2 model
    # hparams_=hparams_tacotron2.create_hparams()
    # tacotron2_model = Tacotron2(hparams_)
    #
    # tacotron2_model.eval()

    # Load the WaveGlow model
    waveglow = WaveGlow(
        n_mel_channels=80,
        n_flows=12,
        n_group=8,
        n_early_every=4,
        n_early_size=2,
        WN_config={'n_layers': 8, 'n_channels': 256, 'kernel_size': 3}
    )
    # waveglow.load_state_dict(torch.load('waveglow_256channels.pt')['model'])
    #
    # waveglow = torch.hub.load('nvidia/DeepLearningExamples:torchhub', 'nvidia_waveglow')
    # waveglow = waveglow.remove_weightnorm(waveglow)
    # waveglow = waveglow.to('cuda')
    waveglow.eval()

    text = "Hello, how are you today?"

    # Synthesize speech waveform
    with torch.no_grad():
        print(1)
        # Encode text into mel spectrogram using Tacotron or any other text-to-mel model
        # mel_spectrogram = encode_text_to_mel(text)
        #
        # # Convert mel spectrogram into waveform using WaveGlow
        # audio_waveform = waveglow.infer(mel_spectrogram)

    # Save synthesized audio to file
    # output_file = "synthesized_audio.wav"
    # torch.save(audio_waveform, output_file)

    # waveglow.load_state_dict(torch.load('waveglow_256channels.pt')['model'])
    waveglow.eval()

    # Text input
    text = "Hello, how are you today?"


# Function to create audio from phonemes
def create_audio_from_phonemes(phonemes, folder_path, file_name):
    '''

    :param phonemes:
    :param folder_path:
    :param file_name:
    :return:
    '''
    # Join phonemes into a string separated by spaces
    phoneme_string = " ".join(phonemes)

    # Initialize gTTS with phonetic input and the IPA language code
    tts = gTTS(text=phoneme_string, lang='en-us')

    # Save the audio to the specified output file
    tts.save(os.path.join(folder_path, file_name))


def diarization_audio_pyannote(file_name, folder_path="speech_score/data/audios"):
    audio_file_path = os.path.join(folder_path, file_name)

    huggingface_token = get_config_key(key_name="huggingfaceTOKEN")

    try:
        # load the diarization pipeline from huggingface
        pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1",
            use_auth_token=huggingface_token)

        # run the pipeline on an audio file
        diarization = pipeline(audio_file_path)

        # dump the diarization output to disk using RTTM format
        with open("audio.rttm", "w") as rttm:
            diarization.write_rttm(rttm)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    model = whisper.load_model("small")
    diarization_result = pipeline(audio_file_path)
    transcription_result = model.transcribe(audio_file_path, word_timestamps=True)

    final_result = words_per_segment(transcription_result, diarization_result)

    for _, segment in final_result.items():
        print(f'{segment["start"]:.3f}\t{segment["end"]:.3f}\t {segment["speaker"]}\t{segment["text"]}')
