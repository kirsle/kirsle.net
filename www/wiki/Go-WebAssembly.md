# WebAssembly and Go(lang)

Some notes, links and tips for working with WebAssembly programs written in Go.

## Example

(from [github.com/mattn/golang-wasm-example](https://github.com/mattn/golang-wasm-example))

Quick synopsis of an example WASM app in Go that fetches a PNG image over HTTP
and draws it into a canvas.

```go
// +build js,wasm

package main

import (
	"encoding/base64"
	"io/ioutil"
	"log"
	"net/http"
	"net/url"
	"syscall/js"
)

func main() {
	href := js.Global().Get("location").Get("href")
	u, err := url.Parse(href.String())
	if err != nil {
		log.Fatal(err)
	}
	u.Path = "/logo.png"

	log.Println("loading image file: " + u.String())
	resp, err := http.Get(u.String())
	if err != nil {
		log.Fatal(err)
	}
	defer resp.Body.Close()
	b, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		log.Fatal(err)
	}
	enc := base64.StdEncoding.EncodeToString(b)

	canvas := js.Global().Get("document").Call("getElementById", "canvas")
	ctx := canvas.Call("getContext", "2d")
	image := js.Global().Call("eval", "new Image()")
	image.Call("addEventListener", "load", js.FuncOf(func(this js.Value, args []js.Value) interface{} {
		ctx.Call("drawImage", image, 0, 0)
		return nil
	}))
	image.Set("src", "data:image/png;base64,"+enc)

	canvas.Call("addEventListener", "click", js.FuncOf(func(this js.Value, args []js.Value) interface{} {
		js.Global().Get("window").Call("alert", "Don't click me!")
		return nil
	}))

	select {}
}
```

## Links

### Documentation

* [WebAssembly (Go Wiki)](https://github.com/golang/go/wiki/WebAssembly)
* [MDN - CanvasRenderingContext2D](https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D) -
  HTML5 Canvas API documentation (general front-end knowledge).

### Examples

* [Cat-o-licious](https://github.com/fiorix/cat-o-licious) is a simple game using
  SDL2 and originally targeted toward desktop applications. The author ported the
  engine over to WASM using the HTML5 Canvas API in place of SDL2 functions.
* [golang-wasm-example](https://github.com/mattn/golang-wasm-example) at time of
  writing shows a simple WASM app in Go that fetches a PNG image and renders it
  into an HTML5 Canvas. The Go portion was also copied above.
* [sdl-canvas-wasm](https://github.com/timhutton/sdl-canvas-wasm) is a **C++**
  example that natively uses SDL2 and compiles to WebAssembly.
  [Live demo here.](https://timhutton.github.io/sdl-canvas-wasm/)
