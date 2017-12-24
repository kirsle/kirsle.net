# Future Project Ideas

## Hybrid WebSocket/TCP Socket Library (Go)

*2017-12-19*

This would be a Go library for writing custom TCP services, like Go [net](https://golang.org/pkg/net/), but which also transparently handles WebSocket HTTP requests. This way your custom protocol can be used easily by custom clients as well as by WebSocket clients.

It would only require that your protocol waits for the client to speak first after connecting. This way, if the first line by the client is an HTTP request, the TCP server can parse the rest of the headers and send back an HTTP response, either to upgrade the connection to a WebSocket or to give a static HTML response (like an error page).

Out-of-box the HTTP support would send *all* WebSocket requests (regardless of URI) to the TCP server and all other HTTP requests to a static error page. Customization options would include replacing the static error page with a custom one, inserting a standard HTTP multiplexer (router) for more custom routes, or requiring the WebSocket request be at a specific URI.

## Stream Slicer (Go)

*2017-12-20*

This would be a Go library that can accept a stream object (for example, a file handle) that implements `io.ReadSeeker` and returns a "slice" of that stream, with a limited range.

An example use case could be implementing a file archiving algorithm, where the data for an individual file is at a certain offset of the archive and has a certain length. You could get a "slice" of the archive for _just_ that file, and `.Read()` it until EOF, without worrying about the implementation details.

API example:

```go
// Get a filehandle stream
fh, _ := os.Open("/path/to/file.bin")

// Slice out a part of it from 512 bytes in and
// a length of 1024 bytes.
slice := streamslice.New(fh, 512, 1024)

result := make([]byte, 1024)
slice.Read(result)
```

Implementation notes:

```go
// The struct + method surface could be like...
type StreamSlice struct {
    source io.ReadSeeker  // the larger / original filehandle
    start int // offset from `source` to be treated as position zero
    index int // current position in the 'slice' starting from zero
    stop int // the `start` + the offset to limit the slice

    // StreamSlice also implements io.ReadSeeker
    Read(p []byte) (n int, err error)
    Seek(offset int64, whence int) (int64, error)
}

func New(fh io.ReadSeeker, offset int64, length int64) *StreamSlice {
    return &StreamSlice{
        source: fh,
        start: offset,
        index: 0,
        stop: offset + length,
    }
}

func (s *StreamSlice) Read(p []byte) (n int, err error) {
    // something along the lines of... seek to the current index,
    // read until we reach `stop` or run out of space in `p`,
    // whichever comes first. TBD.
    s.source.Seek(s.offset + s.index, io.SeekStart)
    // ...
    return
}
```

The struct would keep private references to the original stream, the absolute position of said stream where your slice begins, the _relative_ position of the slice itself, and the length. When calling `Read()`, it would `index++` until it reaches the `stop` and then return EOF.

When the user calls `Seek(0, io.SeekStart)` to rewind the slice, calling `Read()` would again return bytes starting from the beginning of the slice.

This could be a fun demonstration of working with Go's type system to create a useful interface for *any* kind of `io.ReadSeeker`, not just file-like objects.