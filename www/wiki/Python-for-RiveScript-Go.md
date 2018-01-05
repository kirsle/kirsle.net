# Python for RiveScript Go

It'd be nice if rivescript-go were able to parse and run Python object macros for RiveScript bots, by using the [Python C API](https://docs.python.org/3/c-api/index.html).

There are two projects I found so far: [sbinet/go-python](https://github.com/sbinet/go-python) and [qur/gopy](https://github.com/qur/gopy). They both only support Python 2 so far, but that will work for now.

I did some experimenting and came up with the following Go code that demonstrates the key pieces of functionality needed: dynamically parse a Python function, call the function giving it an array of string arguments, and retrieve the result of the function as a Go string.

```go
package main

import (
	"fmt"
	"github.com/sbinet/go-python"
)

func init() {
	err := python.Initialize()
	if err != nil {
		panic(err.Error())
	}
}

func main() {
	// The source code of the python function we wanna be able to call.
	pycode := `
def test(rs, args):
    print "Test works"
    return "Forwards: {}\nBackwards: {}".format(
        " ".join(args),
        " ".join(args[::-1]),
    )
`

	// The []string to use as the 'args' param to `def test()`
	args := StringList_ToPython("Hello", "world")
	defer args.DecRef() // Always do this so Python can count references well.

	// To load the function you can simply eval the code in the global scope:
	python.PyRun_SimpleString(pycode)

	// Get the main module's dictionary so we can get a reference to our
	// function back out of it.
	main_module   := python.PyImport_AddModule("__main__")
	main_dict     := python.PyModule_GetDict(main_module)
	test_function := python.PyDict_GetItemString(main_dict, "test")

	// The tuple of (rs, args) arguments to pass to the function.
	// This tuple is the *args in Python lingo.
	test_args := python.PyTuple_New(2)
	python.PyTuple_SetItem(test_args, 0, python.Py_None)
	python.PyTuple_SetItem(test_args, 1, StringList_ToPython("Hello", "world"))

	// Call the actual Python function now. Functions return a *PyObject, and
	// we can cast it back to a string.
	returned := test_function.CallObject(test_args)
	result := python.PyString_AsString(returned)

	// Print the result of the function.
	fmt.Println("Result:", result)
}

// StringList_ToPython is a helper function that simply converts a Go []string
// into a Python List of the same length with the same contents.
func StringList_ToPython(items... string) *python.PyObject {
	list := python.PyList_New(len(items))

	for i, item := range items {
		python.PyList_SetItem(list, i, python.PyString_FromString(item))
	}

	return list
}
```