# GeoGebra Knowledge Base Topics

This file is the bundled topic snapshot used by the skill.

It was derived from a GeoGebra Scripts book crawl. The source crawl did not preserve each applet's full internal GeoGebra construction, but it did preserve a reliable chapter-and-material index. Use that index as a topic boundary, not as executable source code.

## High-value topics to preserve

These titles are strong signals for what the skill should support in GeoGebraScript and, when appropriate, in JavaScript through the GeoGebra Apps API:

- Sticky point to line
- Buttons / Scripting test
- Change 3D view
- Coloring lists and classes of objects
- Tool for Exploring Color Palettes
- Gradient vector field Custom tool
- DynamicCoordinates[] demo (snap to list)
- SetPerspective Demo (switch between Graphics and Spreadsheet)
- Demo: count number of times A is in same position as B
- Scripting: Writing polynomials with text
- Scripting: Select first false element from list
- Check box in 3D view
- Demo: resizable matrix
- Sliders great trick
- Introduction to GeoGebraScript
- Combine shapes
- Canvas sizes
- Periodic function defined on [a,b]
- SetAxesRatio 1-1 and Set dimensions
- Pulsing point
- Select n elements randomly form list
- Sticky point to list of points
- Re-color check box and resize
- Adding points to list by clicking
- Remove objects of the same kind
- Euler's totient function

## JavaScript-heavy topics to support conditionally

These materials are relevant when the user explicitly wants `ggbApplet` or browser-embedded applet behavior. They should not be used as the default output mode for ordinary construction requests:

- Demo: make Input Box disappear using JavaScript
- Interaction with two 3D views using JavaScript
- Copy of Demo: plot graph in new tab
- Setting HSV colors with JavaScript
- Quick Start: Advanced Integration
- VersionDetector
- Link on image
- Demo: 2 applets communicating
- Demo: save slider value in localStorage
- Save image script

Support the GeoGebra Apps API portion when the user explicitly asks for JavaScript. Still avoid unrelated browser scaffolding, storage logic, or full web page markup unless the user requests it.

## Capability buckets extracted from the crawl

### Geometry and constructions

- Points, segments, lines, rays, circles, polygons
- Snapping ideas and constrained positions
- Shape composition and object relationships
- 2D and 3D object setup

### Algebra and functions

- Polynomial definitions
- Periodic functions
- Number theory examples such as Euler's totient function
- Derivatives, integrals, intersections, and related derived objects

### Lists, matrices, and discrete structures

- Lists of points
- Object classes and grouped styling
- Resizable matrices
- Selecting elements from lists
- Random sampling from lists

### Presentation, styling, and scripting

- Color changes
- Visibility and label intent
- Axes ratio and view setup
- Text objects for displaying formulas or values
- Buttons, click handling, update handling, and dynamic object control

## Practical interpretation for this skill

- Keep the skill centered on constructions, functions, lists, matrices, text, styling commands, and `ggbApplet` control flows that map cleanly to GeoGebra execution.
- Use the chapter titles as evidence that both direct GeoGebraScript and JavaScript-driven interaction belong in scope.
- Treat full browser application logic as out of scope unless the user explicitly asks for it.
