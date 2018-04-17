Steps to denoise audio file:
1- Install sox, sox mp3 codecs and ffmpeg
2- Open the audio file and choose an interval where only noise exists;
3- Extract this interval to a file:
{{{ffmpeg -ss 00:00:00 -t 00:00:00.8 -i audiofile.mp3 -acodec copy noisesample.mp3}}}
4- Create a profile for this noise:
{{{sox noisesample.mp3 -n noiseprof noise_profile}}}
5- Use the following to batch perform noise removing:
{{{python
import remove_noise as rm
rm.remove_noise('folder', 'noise_profile')}}}
where folder is the path of the folder containing the audio files, and noise_profile is the path of
the noise profile file created before.
