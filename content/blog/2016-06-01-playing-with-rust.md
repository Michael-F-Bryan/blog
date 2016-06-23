---
layout: post
title:  Playing Around With Rust
date:   2016-06-01 12:17 +0800
tags: rust, how-to
---

Recently I've started to play around with the [Rust][rust] programming
language and so far I'm liking it. Usually I tend to stay away from the more
"low level" programming languages... Memory leaks and segfaults have always
really pissed me off.

Rust is different though, from the ground up it's been designed with safety in
mind. It's impossible to get into a situation where you're trying to read from
a null pointer or access memory that doesn't belong to your program. Instead
the compiler just yells at you.

So for a bit of fun I thought I'd make a simple echo server. This is just a
program that'll sit on a particular port and then any messages that it recieves
are just sent back to the client.


## Imports

First we do a bunch of imports. Note that Rust uses the `use` key word here.

    #!rust
    // Get stuff from the std library
    use std::net::{TcpListener, TcpStream, Ipv4Addr};
    use std::thread;
    use std::str;

    // traits
    use std::io::Read;
    use std::io::Write;
    }

The first section should be fairly intuitive, I'm just importing the
TcpListener, TcpStream and Ipv4Addr structs from the std::net module. I'm also
directly importing the std::thread and std::str modules.

Next I'm importing two `traits`, `std::io::Read` and `std::io::Write`. Think of
these like interfaces in Java. Anything that uses these traits must implement
the methods specified by Write and Read. When you import these traits, anything
that has been specified to use them (in this case the `TcpStream`) struct, will
automagically be able to use the appropriate methods.

In this case we just want the `read()` and `write()` methods so we can read 
and write to the TCP socket stream that is created every time someone connects
to our server.


## Client Handler

Because I'm throwing each incoming connection into it's own thread, we need to
implement a function that will handle this connection. That's up next.

    #!rust
    /// Create a handler function that will take a TCP socket/stream,
    /// read from it, store the read message in a 512 byte buffer,
    /// then echo it back to the client.
    fn handle_client(mut stream: TcpStream) {
        // Get the peer's ip and port and print them to the 
        // screen
        let peer = stream.peer_addr().unwrap();
        println!("Connection received from {}:{}\n", peer.ip(), peer.port());

        let mut buf = [0; 512]; // Create a buffer for ourselves

        let m = stream.read(&mut buf).unwrap();

        // Turn the message from a byte array to a string and 
        // print it
        let msg = str::from_utf8(&buf[0..m]).unwrap().trim();
        println!("Received: {}", &msg);

        // Echo the message back to the client
        let bytes_sent = stream.write(&msg.as_bytes()).unwrap();
        println!("{} bytes sent to client", &bytes_sent);
        println!("");
    }

The first thing you see in that code snippet is a bunch of lines all starting
off with `///`. These are a special type of comment called `doc comments`. They
are similar to docstrings in python where the language gives you the ability to
annotate your code so that others (maybe you in 6 months time) are able to find
out how to use it at a glance, and possibly see some examples of it's use.
Rust's package manager, `cargo`, can then read through all of your source code
and turn your doc comments, function signatures, struct definitions and more
into automatically generated html documentation. Think of it like writing
documentation without the writing.

The handler is actually fairly simple, but for those who are unfamiliar or new
to Rust, it's probably pretty intimidating. First we're getting our client's
address and printing it to the screen, the `.unwrap()` on line 7 is because
there's the chance that the function might fail, so instead of returning the
raw result Rust will give us a special `Result`. This result can either be the
thing we asked for or an error code. In this case we're almost certain that
the peer exists (they sent us a request after all), so we're assuming we'll
never get an error and just assigning the result directly to `peer`. Next we
print our `peer`'s `ip()` and `port()` to the screen.

Next we create a buffer with space for 512 bytes, because almost all requests
are significantly smaller than 512 bytes this shouldn't be an issue. The
`stream.read(&mut buf)` call will pass the `stream.read()` function a mutable
reference to our buffer, then it'll fill the buffer with the first 512 bytes of
our client's request.

The reason we have to explicitly pass a mutable reference to the
`stream.read()` function is because of the way Rust ensures memory safety.
Basically, in order to prevent multiple functions/threads/processes/whatever
from editing a piece of data, only one caller at a time is given write access.
The `&mut` bit explicitly passes write access from the `handle_client()`
function to `stream.read()`. The `let m = stream.read()` bit is because the
`stream.read()` function will return the number of bytes read. So `m` is an
integer that tells us how many bytes in our buffer are actually relevant.

Line 16 looks pretty complicated, but really all we're doing is creating a
UTF-8 string from the first `m` bytes of our buffer, then trimming off any
whitespace from either end of the message.

Note that on the next line, we need to pass a read-only reference (the `&`) 
to the `println!()` macro. This is because normal passing of variables without
the `&` will actually pass ownership of a variable to the function. We still
want to be able to use our `msg`, so instead we give `println!()` a read-only
copy.

If you've made it this far then chances are that the rest of this function will
be fairly easy to understand. We're just writing back the recieved message
(note that we turn it back into bytes with the `msg.as_bytes()`) and then
printing to the screen the number of bytes sent.


## Main

Similar to in C, each Rust program will start from the `main()` function. Here
I am setting up a socket server, then for each client that connects, I'm
checking whether the connection was successful `Ok(stream)`, or an error,
`Err(e)`. If there was an error then we simply log it and then continue,
however if everything is fine then we spawn a new thread and running the
handler.

    #!rust
    fn main() {
        let host = Ipv4Addr::new(127, 0, 0, 1);
        let port = 8080;

        let  listener =  TcpListener::bind((host, port)).unwrap();

        println!("Echo server listening on {}:{}", &host, &port);

        for stream in listener.incoming() {
            match stream {
                Err(e) => { 
                    println!("Error connecting: {}", &e);
                },
                Ok(stream) => {
                    thread::spawn(move || handle_client(stream));
                },
            };
        };
    }

Something to note is the curious `move || handle_client(stream)` bit. What
we're actually doing is creating a closure (sometimes called an anonymous or, 
lambda function in other languages) with the double pipes (`||`) and passing 
that to the spawned thread. The `move` statement will effectively make a copy 
of the closure's stack frame so that even if the parent function (in this 
case `main()`) were to return, the closure wouldn't be trying to access 
pointers to things that don't exist any more.  

It's a fairly intricate topic and requires understanding how the stack works
under the hood, as well as how stack frames work in general and what happens to
them when a function exits. But you can just think of the `move` as "detaching"
the thread from the function that called it. Allowing our lambda function to
stay valid.


## A Note On `.unwrap()`

Instead of using Exceptions and try/catch blocks like Java and Python do,
success or failure of a function is usually reported through what is returned.
The return value of your function is normally wrapped by an `Option` or a
`Result`. For example, when you try to open a file, you recieve a result
that'll either give you a file handler (`Ok(file_handler)`), or give you an
error message (`Err(e)`).

    #!rust
    let f = File::new("blah.txt");

    match f {
        Ok(file_handle) => let f = file_handle,
        Err(e) => println!("Got an error: {}", e),
    }

This is usually merged into one expression with a `let match`:


    #!rust
    let f = match File::new("blah.txt") {
        Ok(file_handle) => file_handler,
        Err(e) => println!("Got an error: {}", e),
    }

Note that the bit between the arrow (`=>`) and the comma is an expression and
that in Rust, the return value of a series of expressions is the value of the
last expression.

i.e.

    #!rust
    let x = {
        foo();
        bar();
        baz()
    }

    // x == baz()

As useful as this explicit checking to see if a function did what you expected
it to may be, it gets pretty repetitive after a while. Therefore a couple
helper methods were created, one of which is called `.unwrap()`. The unwrap
will interpret the `Result` or `Option` and either give you the thing you
requested or `panic!()` (i.e. Blow up and give you an error message).

There is also a `.unwrap_or(default)` method that'll give you the thing you
wanted or a default value if there is an error. Using this you have a chance to
either exit gracefully or recover from the error, compared to crashing the
program like `.unwrap()` does.

For more information on how error handling works in Rust, I recommend that you
consult the [official documentation][docs].


## Source Code

And of course, here's the source code for the entire thing.

    #!rust
    // Imports
    use std::net::{TcpListener, TcpStream, Ipv4Addr};
    use std::thread;
    use std::str;

    // traits
    use std::io::Read;
    use std::io::Write;


    /// Create a handler function that will take a TCP socket/stream,
    /// read from it, store the read message in a 512 byte buffer,
    /// then echo it back to the client.
    fn handle_client(mut stream: TcpStream) {
        // Get the peer's ip and port and print them to the 
        // screen
        let peer = stream.peer_addr().unwrap();
        println!("Connection received from {}:{}\n", peer.ip(), peer.port());

        let mut buf = [0; 512]; // Create a buffer for ourselves

        let m = stream.read(&mut buf).unwrap();

        // Turn the message from a byte array to a string and 
        // print it
        let msg = str::from_utf8(&buf[0..m]).unwrap().trim();
        println!("Received: {}", &msg);

        // Echo the message back to the client
        let bytes_sent = stream.write(&msg.as_bytes()).unwrap();
        println!("{} bytes sent to client", &bytes_sent);
        println!("");
    }

    fn main() {
        let host = Ipv4Addr::new(127, 0, 0, 1);
        let port = 8080;

        let  listener =  TcpListener::bind((host, port)).unwrap();

        println!("Echo server listening on {}:{}", &host, &port);

        for stream in listener.incoming() {
            match stream {
                Err(e) => { 
                    println!("Error connecting: {}", &e);
                },
                Ok(stream) => {
                    thread::spawn(move || handle_client(stream));
                },
            };
        };
    }


[rust]: https://www.rust-lang.org/
[docs]: https://doc.rust-lang.org/book/error-handling.html#the-basics
