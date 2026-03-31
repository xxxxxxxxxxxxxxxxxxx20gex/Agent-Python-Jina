# GeoGebra Output Rules

Always satisfy these rules in the final answer:

1. Output exactly one fenced code block.
2. Use `geogebra` for direct GeoGebraScript.
3. Use `javascript` for GeoGebra Apps API snippets.
4. Inside the block, output only runnable code for the selected mode.
5. Do not add any explanation before or after the code block.
6. Do not emit comments unless the user explicitly asks for them.
7. Keep statements in dependency order.
8. Prefer direct object definitions and common commands over uncommon or UI-specific features.

## Mode selection

- Default to `geogebra` when the user asks for GeoGebra code without mentioning JavaScript.
- Switch to `javascript` when the user explicitly asks for JavaScript, `ggbApplet`, listeners, or embedded applet control.
- If the request depends on listeners, callbacks, or `ggbApplet.register...`, use `javascript`.
- If the request is only about mathematical objects and constructions, use `geogebra`.

## Safe defaults

- If coordinates are missing, use small integers.
- If a size is missing, choose a simple value such as `2`, `3`, or `4`.
- If the user asks for a named object, honor that name when practical.
- If the user asks for a color or thickness, use `SetColor`, `SetLineThickness`, or `SetPointSize` after the object exists.
- In JavaScript mode, assume `ggbApplet` already exists and is ready unless the user explicitly asks for initialization code.

## Avoid when possible

- HTML scaffolding
- CSS
- DOM interaction unrelated to GeoGebra
- `localStorage`
- Cross-applet communication
- New-tab or external-link behavior
- Overly compressed one-line constructions that are hard to debug

## Fallback policy

If a request includes unsupported browser behavior, preserve the closest supported GeoGebra or `ggbApplet` behavior and omit the unrelated browser details.
