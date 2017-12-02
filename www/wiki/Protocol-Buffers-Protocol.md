# Protocol Buffers Protocol

Notes on how one could use Google's [Protocol Buffers](https://developers.google.com/protocol-buffers/) to create an arbitrary TCP stream-based network protocol. For sake of example, use a simple chat-based messaging protocol.

Like many protocols your messages would have a "type" (or action) and associated data.

## Protobuf Messages

```protobuf
// Login packet, to authenticate with the server
message Login {
    required string username = 1;
    required string password = 2;
}

// Register packet, to sign up
message Register {
    required string username = 1;
    required string password = 2;
    required string email = 3;
}

// Packet for holding a chat message, this is symmetrical
// meaning the client sends this to the server for an outbound
// message and the server sends it to the client for inbound
message Chat {
    required string from = 1;
    required string to = 2;
    required string body = 3;
}
```

## Handshake Flow

It's good practice to version your network protocols, so the first thing the client should do is send a relatively boring message saying the version number. This part of the protocol would **never** change. Maybe something like (`>>>` is the client to the server and `<<<` is the server's response):

```
>>> VER 1
<<< VER 1
```

The server responds with the same version number to acknowledge its support. You should also plan other possible responses (such as communicating to the client that its version number is obsolete and that it should update its software, in case you need to make a massive overhaul of the protocol in the future).

## Packet Format

After the initial version handshake the client and server switch to protocol buffers for all messages. Each type of message has its own protobuf message schema, so it needs some way to know which type of message it's sending and how long it is (so it knows when one message ends and the next packet begins).

So each packet would consist of a format like:

1. [At least*] one byte to indicate the Message Type
2. A fixed size packed integer to indicate the length of the protobuf message (i.e. a 32-bit integer, or 4 binary bytes... or you could probably get away with 16-bit and have a max size of 65K for each protobuf message)
3. The binary-encoded protobuf message.

\* The Message Type byte should reserve one bit for extensibility: for example, reserve the highest bit. This means that initially you can only have up to 128 types of messages in your protocol (using Message Type IDs from 0 to 127 (`01111111`), and if you run out of space you can set the highest bit to `1` (so, `128` for `100000000`) and that could instruct your protocol to read the *next* byte to continue finding the Message Type. [UTF-8 encoding](https://www.youtube.com/watch?v=MijmeoH9LT4) works on a similar principal. The highest bit of every byte would be reserved for extending the length, so you don't run out of space as the protocol grows.

If you found you need to extend the length limit (part #2 of the packet format), you could handle this by incrementing the Protocol Version Number from the handshake. Client and server could both switch to larger integers when using the new protocol.

The mapping between Message Type values and your protobuf messages would be done on your own. For example you could arbitrarily say that Message Type 1 is Login, 2 is Register, 3 is Logout, etc.