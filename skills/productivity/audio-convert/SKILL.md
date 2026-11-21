---
name: audio-convert
description: "Convert audio files into standard formats (m4a, mp3, wav, flac) on macOS with ffmpeg and afconvert. Use for unfamiliar or Apple-only audio files (.qta, .caf, .aifc, audio-only .mov), iPhone spatial audio recordings (APAC, ambisonics), audio extraction from video, or a change of codec, bitrate, sample rate, or channel count. Do not use for video transcoding, audio editing or mastering, transcription, or speech synthesis."
---

# Audio convert

Use two macOS tool pairs:

- `ffmpeg` and `ffprobe` (for example, from Homebrew) decode almost every format.
- Apple's built-in `afconvert` and `afinfo` (`/usr/bin`) decode Apple-only codecs that `ffmpeg` cannot.

## 1. Probe first

Run both probes. Each one shows tracks that the other misreports.

```sh
afinfo "$f"                                                   # each audio track: codec, channels, layout, duration
ffprobe -hide_banner "$f" 2>&1 | grep -E 'Duration|Stream #|Unsupported'   # stream map and undecodable streams
```

Pick the source track from this output. Done when you know the codec and channel count of each audio track, and whether `ffmpeg` can decode it.

## 2. Convert

Write the output next to the source, with the same base name and a new extension. Keep the source file. If the target extension matches the source extension, choose a distinct output path (for example, `${f%.*}-converted.m4a`) so `ffmpeg` does not collide with the input.

**Prefer a stream copy.** When the track already uses the target codec and needs no bitrate, sample-rate, or channel change, change only the container. A stream copy is lossless and fast:

```sh
ffmpeg -i "$f" -map 0:a:0 -c:a copy "${f%.*}.m4a"    # AAC or ALAC -> .m4a (use .mp3 for MP3, .flac for FLAC)
```

`-map 0:a:0` selects only the first audio stream; `0:a:1` selects the second. Without `-map`, `ffmpeg` can also select video or subtitle streams allowed by the output container, or fail on undecodable audio tracks.

**Re-encode** when the requested format, codec, bitrate, sample rate, or channel count differs from the source:

```sh
ffmpeg -i "$f" -map 0:a:0 -c:a libmp3lame -q:a 2 "${f%.*}.mp3"   # MP3, ~190 kbps VBR
ffmpeg -i "$f" -map 0:a:0 "${f%.*}.wav"                          # 16-bit PCM WAV
ffmpeg -i "$f" -map 0:a:0 -c:a flac "${f%.*}.flac"               # lossless, smaller than WAV
ffmpeg -i "$f" -map 0:a:0 -c:a aac -b:a 256k "${f%.*}.m4a"       # AAC re-encode (rename output if input is .m4a)
```

**When `ffmpeg` cannot decode the track** (`Unsupported codec`), use `afconvert`. It reads the first track by default. `--read-track N` selects another track. `N` counts from 0 in the order that `afinfo` lists the tracks, so `Track ID: 1` is index 0.

```sh
afconvert --read-track 1 -f WAVE -d LEI24 "$f" "${f%.*}-track1.wav"   # second track -> 24-bit WAV
```

## 3. Verify

Run `afinfo` on the output. Done when the output exists at a distinct path, its codec, bitrate, sample rate, and channel count match your intent, and its duration matches the source within a fraction of a second.

## iPhone spatial audio (.qta)

A typical iPhone spatial audio recording is a QuickTime audio file (`.qta`) with these streams:

- **Track 0**: stereo AAC, 48 kHz. `ffmpeg` stream-copies it to `.m4a`. Most users want this version.
- **Track 1**: 4-channel APAC (Apple Positional Audio Codec), first-order ambisonics in ACN/SN3D. `ffmpeg` cannot decode APAC. `afconvert --read-track 1 -f WAVE -d LEI24` decodes it to a 4-channel WAV (about 0.5 GB per 15 minutes). The WAV has no channel-layout tag. Tell the user that the channels are ACN/SN3D ambisonics, so that their tool (Reaper, an ambisonic decoder plugin) reads them correctly.
- One or more `mebx` playback metadata streams (typically two). Skip them.

For stereo, use Track 0: it is already the stereo downmix. `afconvert` cannot downmix the APAC track to stereo AAC (`'cclo' failed (-66564)`), and `-c 2` drops channels without a downmix.
