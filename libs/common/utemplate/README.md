utemplate
=========

`utemplate` is a lightweight and memory-efficient template engine for
Python, primarily designed for use with Pycopy, a lightweight Python
implementation (https://github.com/pfalcon/pycopy). It is also fully
compatible with CPython and other compliant Python implementations.

`utemplate` syntax is roughly based on Django/Jinja2 syntax (e.g.
`{% if %}`, `{{var}}`), but only the most needed features are offered
(for example, "filters" (`{{var|filter}}`) are syntactic sugar for
function calls, and so far are not planned to be implemented, function
calls can be used directly instead: `{{filter(var)}}`).

`utemplate` compiles templates to Python source code, specifically to
a generator function which, being iterated over, produces consecutive
parts (substrings) of the rendered template. This allows for minimal
memory usage during template substitution (with Pycopy, it starts
from mere hundreds of bytes). Generated Python code can be imported as
a module directly, or a simple loader class (`utemplate.compiled.Loader`)
is provided for convenience.

There is also a loader class which will compile templates on the fly,
if not already compiled - `utemplate.source.Loader`.

Finally, there's a loader which will automatically recompile a template
module if source template is changed - `utemplate.recompile.Loader`.
This loader class is the most convenient to use during development, but
on the other hand, it performs extra processing not required for a
finished/deployed application.

To test/manage templates, `utemplate_util.py` tool is provided. For
example, to quickly try a template (assuming you are already in
`examples/` dir):

    pycopy ../utemplate_util.py run squares.tpl

or

    python3 ../utemplate_util.py run squares.tpl

Templates can take parameters (that's how dynamic content is generated).
Template parameters are passed as arguments to a generator function
produced from a template. They also can be passed on the `utemplate_util.py`
command line (arguments will be treated as strings in this case, but
can be of any types if called from your code):

    pycopy ../utemplate_util.py run test1.tpl foo bar

Quick Syntax Reference
----------------------

Evaluating Python expression, converting it to a string and outputting to
rendered content:

* `{{<expr>}}`

Where `expr` is an arbitrary Python expression - from a bare variable name,
to function calls, `yield from`/`await` expressions, etc.

Supported statements:

* `{% args <var1>, <var2>, ... %}` - specify arguments to a template
  (optional, should be at the beginning of a template if you want to
  pass any arguments). All argument types as supported by Python can
  be used: positional and keyword, with default values, `*args` and
  `**kwargs` forms, etc.
* `{% if <expr> %}`, `{% elif <expr> %}`, `{% else %}`, `{% endif %}` -
  similar to Python's `if` statement
* `{% for <var> in <expr> %}`, `{% endfor %}` - similar to Python's
  `for` statement
* `{% while <expr> %}`, `{% endwhile %}` - similar to Python's `while`
  statement
* `{% set <var> = <expr> %}` - assignment statement
* `{% include "name.tpl" %}` - statically include another template
* `{% include {{name}} %}` - dynamically include template whose name is
  stored in variable `name`.

File Naming Conventions
-----------------------

* The recommended extension for templates is `.tpl`, e.g. `example.tpl`.
* When template is compiled, dot (`.`) in its name is replaced
  with underscore (`_`) and `.py` appended, e.g. `example_tpl.py`. It
  thus can be imported with `import example_tpl`.
* The name passed to `{% include %}` statement should be full name of
  a template with extension, e.g. `{% include "example.tpl" %}`.
* For dynamic form of the `include`, a variable should similarly contain
  a full name of the template, e.g. `{% set name = "example.tpl" %}` /
  `{% include {{name}} %}`.

Examples
--------

`examples/squares.tpl` as mentioned in the usage examples above has the
following content:

```
{% args n=5 %}
{% for i in range(n) %}
| {{i}} | {{"%2d" % i ** 2}} |
{% endfor %}
```

More examples are available in the [examples/](examples/) directory.

If you want to see a complete example web application which uses `utemplate`,
refer to https://github.com/pfalcon/notes-pico .

License
-------

`utemplate` is written and maintained by Paul Sokolovsky. It's available
under the MIT license.
