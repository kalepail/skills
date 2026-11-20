---
name: audio-convert
description: "Convert audio files into standard formats (m4a, mp3, wav, flac) on macOS with ffmpeg and afconvert. Use for unfamiliar or Apple-only audio files (.qta, .caf, .aifc, audio-only .mov), iPhone spatial audio recordings (APAC, ambisonics), extracting audio from video, or changing codec, bitrate, sample rate, or channels. Do not use for video transcoding, audio editing or mastering, transcription, or speech synthesis."
---

# Audio convert

Two macOS tools: `ffmpeg`/`ffprobe` (for example via Homebrew) and Apple's built-in `afconvert`/`afinfo` (`/usr/bin`). `ffmpeg` covers almost every format. `afconvert` is the fallback for Apple-only codecs that `ffmpeg` cannot decode.

## 1. Probe first

Run both probes. Each one sees tracks the other misreports.

```sh
afinfo "$f"                          # every audio track, codec, channel layout, duration
ffprobe -hide_banner "$f" 2>&1 | tail -20   # stream index map; "Unsupported codec" lines
```

Pick the track to convert from this output. Done when you know each audio track's codec, channel count, and whether `ffmpeg` can decode it.

## 2. Convert

Write the output beside the source with the same base name and a new extension. Leave the source file in place.

**Prefer a stream copy.** When the track is already AAC, MP3, ALAC, or FLAC, change only the container. This is lossless and instant:

```sh
ffmpeg -i "$f" -map 0:a:0 -c:a copy "${f%.*}.m4a"     # AAC/ALAC -> .m4a
```

`-map 0:a:0` selects the first audio stream. Without it, `ffmpeg` may try to carry data or undecodable streams and fail.

**Re-encode** only when the user wants a format the codec does not fit:

```sh
ffmpeg -i "$f" -map 0:a:0 -c:a libmp3lame -q:a 2 "${f%.*}.mp3"   # MP3, ~190 kbps VBR
ffmpeg -i "$f" -map 0:a:0 "${f%.*}.wav"                          # 16-bit PCM WAV
ffmpeg -i "$f" -map 0:a:0 -c:a flac "${f%.*}.flac"               # lossless, smaller than WAV
ffmpeg -i "$f" -map 0:a:0 -c:a aac -b:a 256k "${f%.*}.m4a"       # AAC re-encode
```

**`ffmpeg` cannot decode the track** ("Unsupported codec"): use `afconvert`. It reads track 0 by default; `--read-track N` picks another (0-based, the `Track ID` order in `afinfo`).

```sh
afconvert --read-track 1 -f WAVE -d LEI24 "$f" "${f%.*}-track1.wav"
```

## 3. Verify

Run `afinfo` on the output. Done when the codec and channel count are what you intended and the duration matches the source within a fraction of a second.

## iPhone spatial audio (.qta)

An iPhone spatial audio recording saves a QuickTime audio file (`.qta`) with:

- **Track 0**: stereo AAC, 48 kHz. `ffmpeg` stream-copies it to `.m4a`. This is the version most people want.
- **Track 1**: 4-channel APAC (Apple Positional Audio Codec), first-order ambisonics ACN/SN3D. `ffmpeg` cannot decode APAC. `afconvert --read-track 1 -f WAVE -d LEI24` decodes it to a 4-channel WAV (~0.5 GB per 15 minutes), but the WAV carries no channel-layout tag. Tell the user the channels are ACN/SN3D ambisonics so their tool (Reaper, an ambisonic decoder plugin) reads them correctly.
- Two `mebx` metadata streams. Skip them.

`afconvert` refuses to downmix the APAC track straight to stereo (`'cclo' failed (-66564)`). The stereo AAC track already is that downmix.
