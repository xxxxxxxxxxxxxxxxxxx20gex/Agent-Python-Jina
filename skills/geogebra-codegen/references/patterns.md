# GeoGebra Patterns

Use these patterns as conservative templates. Adapt names and values to the user's request.

## Mode guide

- Use the `GeoGebraScript` patterns when the user wants direct GeoGebra code.
- Use the `JavaScript / ggbApplet API` patterns when the user asks for JavaScript, listeners, or embedded-applet control.

## GeoGebraScript: Basic geometry

```text
A = (0, 0)
B = (4, 0)
C = (2, 3)
tri = Polygon[A, B, C]
```

```text
A = (0, 0)
B = (4, 0)
s = Segment[A, B]
g = Line[A, B]
```

```text
O = (0, 0)
c = Circle[O, 3]
P = (3, 0)
t = Tangent[P, c]
```

## GeoGebraScript: Intersections and measurements

```text
f: x + y = 4
g: y = x + 1
P = Intersect[f, g]
```

```text
A = (0, 0)
B = (3, 4)
d = Distance[A, B]
```

## GeoGebraScript: Functions and calculus

```text
f(x) = x^2 - 4x + 3
g(x) = Derivative[f]
```

```text
f(x) = sin(x)
a = Integral[f, 0, pi]
```

```text
f(x) = x^2
g(x) = Translate[f, (2, 0)]
```

## GeoGebraScript: Lists and matrices

```text
L = Sequence[(k, k^2), k, 1, 5]
```

```text
M = {{1, 2}, {3, 4}}
```

```text
L = {2, 5, 7, 11, 13}
n = Length[L]
```

## GeoGebraScript: Text and labels

```text
A = (2, 1)
txt = Text("Point A", (3, 2))
```

```text
f(x) = x^2
txt = Text("f(x) = x^2", (-4, 6))
```

## GeoGebraScript: Styling

```text
A = (1, 2)
SetColor[A, 255, 0, 0]
SetPointSize[A, 6]
```

```text
c = Circle[(0, 0), 3]
SetColor[c, 0, 102, 204]
SetLineThickness[c, 5]
```

## GeoGebraScript: View setup

```text
SetAxesRatio[1, 1]
```

```text
ZoomIn[-5, -5, 5, 5]
```

## JavaScript / ggbApplet API: Object creation

```javascript
ggbApplet.evalCommand("A = (0, 0)");
ggbApplet.evalCommand("B = (4, 0)");
ggbApplet.evalCommand("s = Segment[A, B]");
```

```javascript
function buildTriangle() {
  ggbApplet.evalCommand("A = (0, 0)");
  ggbApplet.evalCommand("B = (4, 0)");
  ggbApplet.evalCommand("C = (2, 3)");
  ggbApplet.evalCommand("tri = Polygon[A, B, C]");
}
```

## JavaScript / ggbApplet API: Values and styling

```javascript
ggbApplet.setValue("a", 5);
var current = ggbApplet.getValue("a");
```

```javascript
ggbApplet.setColor("A", 255, 0, 0);
ggbApplet.setPointSize("A", 6);
ggbApplet.setVisible("A", true);
```

## JavaScript / ggbApplet API: Coordinates

```javascript
var x = ggbApplet.getXcoord("A");
var y = ggbApplet.getYcoord("A");
```

```javascript
ggbApplet.setCoords("A", 2, 5);
```

## JavaScript / ggbApplet API: Listeners

```javascript
function onClick(objName) {
  if (objName === "btn1") {
    ggbApplet.evalCommand("P = (1, 1)");
  }
}

ggbApplet.registerClickListener(onClick);
```

```javascript
function onUpdate(objName) {
  if (objName === "A") {
    ggbApplet.setValue("a", ggbApplet.getXcoord("A"));
  }
}

ggbApplet.registerUpdateListener(onUpdate);
```

## Notes

- Prefer `ZoomIn` or explicit coordinates over browser-specific canvas instructions.
- Prefer mathematical variables over UI widgets unless the user explicitly requires a widget and the syntax is certain.
- When a construction needs repeated reuse, define base points or parameters first.
- In JavaScript mode, prefer `ggbApplet.evalCommand(...)` for creating objects and dedicated `ggbApplet` methods for reading or mutating them.
