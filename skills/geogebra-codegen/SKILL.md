---
name: geogebra-codegen
description: Generate runnable GeoGebra code from natural-language math and construction requests. Use when a user asks for GeoGebra commands, wants a worksheet or applet construction described in plain language, needs direct GeoGebraScript for points, lines, circles, polygons, functions, transformations, lists, matrices, text, coordinate settings, or 2D and 3D math objects, or explicitly wants JavaScript with the GeoGebra Apps API such as ggbApplet.evalCommand, listeners, setValue, getValue, visibility, color, or embedded applet interactivity. Output must be exactly one fenced code block with a language identifier, containing either GeoGebraScript or JavaScript depending on the requested execution mode.
---

# Geogebra Codegen

## Overview

Translate user intent into the correct GeoGebra execution mode and emit runnable code only. Support both direct GeoGebraScript and JavaScript through the GeoGebra Apps API. Favor conservative syntax, explicit creation order, and defaults that keep the result runnable without follow-up clarification.

## Workflow

1. Infer the mathematical or interaction intent from the user's language.
2. Decide the execution mode.
3. Reduce the request to either GeoGebraScript statements or JavaScript API calls.
4. Output only code inside one fenced code block, one statement per line, in dependency order.

## Mode Selection

- Use `GeoGebraScript` by default when the user asks for GeoGebra code, constructions, functions, geometry, algebra, lists, matrices, text, or styling without mentioning JavaScript.
- Use `JavaScript / GeoGebra Apps API` when the user explicitly asks for JavaScript, `ggbApplet`, listeners, button actions, click handlers, update handlers, browser embedding, applet control, or dynamic webpage integration.
- If the user mentions both, follow the more explicit request. If they say `JavaScript`, do not silently downgrade to GeoGebraScript.
- If the user does not specify a mode but the task clearly depends on listeners or browser-driven interactivity, choose `JavaScript / GeoGebra Apps API`.

## Output Contract

- Return exactly one fenced code block.
- Use `geogebra` for GeoGebraScript output.
- Use `javascript` for GeoGebra Apps API output.
- Inside the code block, output code only.
- Do not add explanations, headings, comments, or prose before or after the code block.
- In GeoGebraScript mode, prefer direct definitions such as `A = (0, 0)` or `f(x) = x^2`.
- In JavaScript mode, use `ggbApplet` APIs consistently and keep the snippet runnable in an embedded-app context.
- Keep names short and conventional: `A`, `B`, `C`, `f`, `g`, `c`, `L1`, `P1`.
- Create prerequisite objects before dependent objects.
- If the user omits dimensions or coordinates, choose simple defaults rather than asking.

## Scope Rules

- Support two output families only: direct GeoGebraScript and JavaScript via the GeoGebra Apps API.
- Do not emit HTML, CSS, page scaffolding, or unrelated browser code unless the user explicitly asks for it.
- For browser-only topics that do not belong to the GeoGebra Apps API, translate to the nearest supported result when possible.
- Prefer mathematical constructions over UI widgets when syntax is uncertain in GeoGebraScript mode.
- Prefer `ggbApplet.evalCommand(...)` for creating GeoGebra objects from JavaScript mode unless a dedicated API call is clearly better.

## Syntax Preferences

- Prefer one command per line.
- Prefer explicit points over anonymous coordinates when later reused.
- Prefer standard commands and object definitions over clever compressed syntax.
- Use numeric defaults that are easy to inspect, such as small integers and symmetric coordinates.
- Keep optional styling sparse unless the user explicitly asks for it.
- In JavaScript mode, prefer small self-contained snippets that assume `ggbApplet` is already available.

## Reference Files

- Read [references/knowledge-base-topics.md](references/knowledge-base-topics.md) for the bundled topic scope.
- Read [references/output-rules.md](references/output-rules.md) before generating final output.
- Read [references/patterns.md](references/patterns.md) when the request maps to a common geometry, algebra, list, matrix, text, styling, or `ggbApplet` interaction pattern.

## Examples

User request: `Draw a square of side length 4 and show both diagonals`

Expected output style:

```geogebra
A = (0, 0)
B = (4, 0)
C = (4, 4)
D = (0, 4)
p = Polygon[A, B, C, D]
d1 = Segment[A, C]
d2 = Segment[B, D]
```

User request: `Define y = x^3 - 3x and give its derivative`

Expected output style:

```geogebra
f(x) = x^3 - 3x
g(x) = Derivative[f]
```

User request: `Use JavaScript to create two points and compute their distance`

Expected output style:

```javascript
function createDistanceDemo() {
  ggbApplet.evalCommand("A = (0, 0)");
  ggbApplet.evalCommand("B = (3, 4)");
  ggbApplet.evalCommand("d = Distance[A, B]");
}
```

User request: `Use ggbApplet to listen for updates on A and store its x-coordinate in a`

Expected output style:

```javascript
function onUpdate(objName) {
  if (objName === "A") {
    ggbApplet.setValue("a", ggbApplet.getXcoord("A"));
  }
}

ggbApplet.registerUpdateListener(onUpdate);
```
