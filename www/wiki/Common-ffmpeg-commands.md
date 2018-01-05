# Common ffmpeg commands

For personal reference, some common things I've had to look up for ffmpeg.

# Chromecast-ability

## Convert to h264+aac

To make a video file Chromecast-able, the video codec needs to be h.264 and the audio codec needs to be AAC.

If a video is Chromecastable, you're able to drag and drop the video into a Google Chrome browser window and it should play the video inside the browser. You can then cast your tab to the Chromecast and watch it on your TV. Videos that *aren't* encoded correctly will instead attempt to "download" when dragged into the window and they need to be reencoded so they work.

The base command that should be able to convert any video is this:

```bash
ffmpeg -i $input -c:v libx264 -preset slow -crf 22 -c:a aac $output
```

## Extract Subtitles from MKV Videos

Some `.mkv` videos have subtitles embedded inside the video file itself, where players like VLC can get them. When you convert these to h.264 you lose the subtitle information. If you want to keep subtitles for VLC, you have to extract them from the original `.mkv` file into a stand-alone `.srt` subtitle file.

You can `dnf install mkvtoolnix` on Fedora to get the tools to manipulate mkv files.

First, you need to find the track number that has the subtitles in it. You can do this within VLC by going to Tools->Media Information, Codec tab, and look for the stream number for the subtitles. An example video had Stream 0 (video), Stream 1 (audio) and Stream 2 (subtitle). You can also install `mkvtoolnix-gui` and use the `mkvinfo` command.

Then to extract the subtitles:

```bash
mkvextract tracks $input $tracknum:$output

# example
mkvextract tracks Video.mkv 2:Video.srt
```

As long as VLC sees a matching SRT file name that corresponds to the video you're watching, it can use the subtitles.

# Rotation and Metadata

Videos recorded on a smartphone are oftentimes encoded "sideways" and have an Orientation metadata tag that tells smart video players how to rotate the video for playback. Video players like VLC know how to deal with the Orientation tag so the video typically looks right in VLC, but other tools (and sometimes Facebook etc.) don't and the video ends up being rotated 90 degrees in either direction.

There's probably a way to strip the metadata at the same time as rotating the video, but I found I had to use two separate commands:

```bash
# reset the rotation metadata
ffmpeg -i $input -metadata:s:v:0 rotate=0 $output

# rotate the video 90 degrees clockwise
ffmpeg -i $input -vf "transpose=1" $output
```

The transpose option takes the following values:

* `0`: 90CounterCLockwise and Vertical Flip  (default) 
* `1`: 90Clockwise
* `2`: 90CounterClockwise
* `3`: 90Clockwise and Vertical Flip