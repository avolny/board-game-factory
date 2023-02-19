from bgfactory import ff

component = ff.RoundedRectangle(0, 0, 300, 200, radius=60, stroke_width=15, stroke_src=(0.2, 0.3, 0.7), fill_src=ff.COLOR_WHITE)

component.image().show()

# component.image().save('image.png')

component.image().save('assets/readme/example01.png')