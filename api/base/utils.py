from pydub import AudioSegment
import uuid
import io


def generate_uuid_key(length=6):
    """Generate a unique key by shortening a UUID."""
    uuid_str = str(uuid.uuid4().hex)
    return uuid_str[:length]


def convert_blob_to_mp3(blob):
    # Read the blob data
    audio_data = io.BytesIO(blob)

    # Load the audio data as PCM
    audio_segment = AudioSegment.from_file(audio_data, format="wav")

    # Export the audio segment as MP3
    output_buffer = io.BytesIO()
    audio_segment.export(output_buffer, format="mp3")

    # Get the MP3 data
    mp3_data = output_buffer.getvalue()

    return mp3_data
