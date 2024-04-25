# from pocketsphinx import Segmenter
# import subprocess

# seg = Segmenter()
# incmd = f"sox -q -r {seg.sample_rate} -c 1 -b 16 -e signed-integer -d -t raw -".split()
# outcmd = f"sox -q -t raw -r {seg.sample_rate} -c 1 -b 16 -e signed-integer -".split()
# with subprocess.Popen(incmd, stdout=subprocess.PIPE) as sox:
#     try:
#         for idx, speech in enumerate(seg.segment(sox.stdout)):
#             outfile = "%03d_%.2f-%.2f.wav" % (
#                 idx,
#                 speech.start_time,
#                 speech.end_time,
#             )
#             with subprocess.Popen(outcmd + [outfile], stdin=subprocess.PIPE) as soxout:
#                 soxout.stdin.write(speech.pcm)
#             print("Wrote %s" % outfile)
#     except KeyboardInterrupt:
#         pass
from pocketsphinx import Endpointer, Decoder, set_loglevel
import subprocess
import sys
import os
import warnings
warnings.filterwarnings("ignore")


def main():
    set_loglevel("INFO")
    ep = Endpointer()
    decoder = Decoder(
        samprate=ep.sample_rate,
    )
    soxcmd = f"sox -q -r {ep.sample_rate} -c 1 -b 16 -e signed-integer -d -t raw -"
    sox = subprocess.Popen(soxcmd.split(), stdout=subprocess.PIPE)
    while True:
        frame = sox.stdout.read(ep.frame_bytes)
        prev_in_speech = ep.in_speech
        speech = ep.process(frame)
        if speech is not None:
            if not prev_in_speech:
                print("Speech start at %.2f" % (ep.speech_start), file=sys.stderr)
                decoder.start_utt()
            decoder.process_raw(speech)
            hyp = decoder.hyp()
            if hyp is not None:
                print("PARTIAL RESULT:", hyp.hypstr, file=sys.stderr)
            if not ep.in_speech:
                print("Speech end at %.2f" % (ep.speech_end), file=sys.stderr)
                decoder.end_utt()
                print(decoder.hyp().hypstr)


try:
    main()
except KeyboardInterrupt:
    pass