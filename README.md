# Board Game Factory

### Contributors are welcome here! See the end of readme.

This is a vector-graphics framework intended for creating
and scaling up production of reusable assets with vector graphics.

It is a thick wrapper around cairo for vector graphics and pango for fully
featured text layout and rendering providing very user-friendly for composing
assets. 

I've developed it personally to satisfy my need for a solid prototyping
engine for board games, but inherently, it is in no way tied to making board games,
even though it contains a couple convenience classes for that (such as CardSheet for 
producing printable card sheets out of lists of components).

## Installation

Requires conda and having conda forge in channels (see https://conda-forge.org).

Unfortunately the cairo and pango binary libraries cannot be installed directly 
with pip. 

````
conda install cairo pango
pip install board-game-factory
````

## Features

 - High quality rendering - BGF is based fully in Vector Graphics, therefore allowing for renders of arbitrary resolution
 - Component Tree structure - similar to making GUIs in Java, you can embed a component inside a component inside a component...
 - Fully extensible components - the best way to use this framework is to
    create and compose your own components extending base components.
 - Fully dynamic and highly flexible sizing system:
   - Component width/height possible values:
     - INFER - the component decides on its own how large it should be
     - FILL - fill all available remaining space in the parent Container
     - '12.34%' - take up 12.34% of available space
     - 123 - take up 123 pixels
 - Many basic and advanced components are already implemented:
   - Container - base component with a layout manager, you add components into it. 
   - Shapes
     - Rectangle
     - RoundedRectangle
     - Circle
     - Line
   - TextUniform - a fully featured text rendering component (exposing most advanced features of pango) 
     for rendering text of a uniform style (all characters have same font, size, color, ...).
   - TextMarkup - advanced text component supporting markup for strings with multiple styles (boldface words, multiple colors, ...)
     - features smart inline laying of icons (any images) for embedding icons directly in text
   - Grid - a special component for creating table structures:
     - each cell can have unique parameters (e.g. layout manager)
     - incredibly flexible row and column definitions (INFER, FILL, %, px)
     - fully featured cell merging
   - just with those few components + LayoutManagers I've made all the samples you can see below in the link on imgur.
 - LayoutManagers
   - Absolute - define pixels
   - HorizontalFlow, VerticalFlow - align automatically to row or column
   - Fully extensible, you can write your own

## Usage

For examples of usage see tests.

## Things I made with BGF

Samples of prototypes I've made with this framework:

https://imgur.com/a/TS779gR

## Issues

Please report any issues and feel free to try and fix them on your own.


## Contributors Wanted!

I would love to welcome people on board who would like to extend the project
or improve it, if you're interested you can drop in a PR directly or we can first discuss,
you can reach me at adam.volny at gmail dot com.

For a hobby project, I think it has a surprisingly high quality of design and code. 
There are is quite a good test coverage, all tests are performed directly against
rendered references. This allowed for controlled development of many of the complex features
in this framework (dynamic sizing & positioning is really difficult with this
amount of supported features).

It could be extended to do many things (e.g. a gui board game asset builder, 
coupled with inputs from spreadsheets, ...), I would love to hear Your ideas!