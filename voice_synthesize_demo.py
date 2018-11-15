"""
Text to speech service demo script, with command line interface.
(This script assumes that the proper version of vlc is installed, and aws account/credentials are configured).
"""
try:
    import vlc
except (ImportError, OSError):
    print('Vlc and|or it\' bindings not installed correctly')
    exit(-1)
import boto3
import time
import os
import click
from contextlib import closing

'''
Possible Voice Ids, and language codes copied from AWS docs
https://docs.aws.amazon.com/polly/latest/dg/voicelist.html
VoiceId='Geraint'|'Gwyneth'|'Mads'|'Naja'|'Hans'|'Marlene'|'Nicole'|'Russell'|'Amy'|'Brian'|'Emma'|'Raveena'|'Ivy'|'Joanna'|'Joey'|'Justin'|'Kendra'|'Kimberly'|'Matthew'|'Salli'|'Conchita'|'Enrique'|'Miguel'|'Penelope'|'Chantal'|'Celine'|'Lea'|'Mathieu'|'Dora'|'Karl'|'Carla'|'Giorgio'|'Mizuki'|'Liv'|'Lotte'|'Ruben'|'Ewa'|'Jacek'|'Jan'|'Maja'|'Ricardo'|'Vitoria'|'Cristiano'|'Ines'|'Carmen'|'Maxim'|'Tatyana'|'Astrid'|'Filiz'|'Vicki'|'Takumi'|'Seoyeon'|'Aditi'|'Zhiyu'|'Bianca'|'Lucia'|'Mia',
LanguageCode='cmn-CN'|'cy-GB'|'da-DK'|'de-DE'|'en-AU'|'en-GB'|'en-GB-WLS'|'en-IN'|'en-US'|'es-ES'|'es-MX'|'es-US'|'fr-CA'|'fr-FR'|'is-IS'|'it-IT'|'ja-JP'|'hi-IN'|'ko-KR'|'nb-NO'|'nl-NL'|'pl-PL'|'pt-BR'|'pt-PT'|'ro-RO'|'ru-RU'|'sv-SE'|'tr-TR'
'''


def play_whole_audio(src):
    """
    :param src: file path on disc or url
    """
    p = vlc.MediaPlayer(src)
    p.play()
    while True:
        state = p.get_state()
        if state == vlc.State.Ended:
            break
        if state == vlc.State.Error:
            raise RuntimeError('Error during playing file')
        time.sleep(0.1)


def text_to_speech(text: str):
    """
    :param text: text to synthesize
    :return: audio file in mp3 format (bytes)
    """
    client = boto3.client('polly')
    response = client.synthesize_speech(
        OutputFormat='mp3',
        Text=text,
        TextType='text',
        VoiceId='Jacek'#'Salli'
    )
    if not 'AudioStream':
        raise IOError('Failed to download synthesized speech')
    with closing(response["AudioStream"]) as stream:
        return stream.read()


@click.command()
@click.option('--text', help='Text to synthesize')
def cli(text):
    tmp_outfile = "polly-boto.mp3"

    stream = text_to_speech(text)
    try:
        with open(tmp_outfile, 'wb') as f:
            f.write(stream)
        play_whole_audio(tmp_outfile)
        os.remove(tmp_outfile)
    except (IOError, RuntimeError) as e:  # tmp file read/write problem, or vlc error while playing
        print(e)
        exit(-1)


if __name__ == '__main__':
    cli()
