

#*file con codice in più utilizzato per fare prove varie
#colori sito 
#006769
#40A578
#9DDE8B
#FFFFFF

import colorspace 
pal = colorspace.hcl_palettes().get_palette("ag_GrnYl")  

colorspace.specplot(pal(60))
pal(4)
colorspace.specplot(colorspace.deutan(pal(60)))
colorspace.contrast_ratio(pal(4), bg="black", plot=True)
colorspace.contrast_ratio(["#006769", "#40A578", "#9DDE8B", "#E6FF94"], plot = True, bg = "#006769")
#bene con "#9DDE8B", "#E6FF94"
colorspace.contrast_ratio(["#006769", "#40A578", "#9DDE8B", "#E6FF94"], plot = True, bg = "#40A578") #meh, non lo userei come sfondo
colorspace.contrast_ratio(["#006769", "#40A578", "#9DDE8B", "#E6FF94"], plot = True, bg = "#9DDE8B") #questo solo con #006769
colorspace.contrast_ratio(["#006769", "#40A578", "#9DDE8B", "#E6FF94"], plot = True, bg = "#E6FF94") #nemmeno questo 
colorspace.contrast_ratio(["#006769", "#40A578", "#9DDE8B", "#FFFFFF"], plot = True, bg = "#006769")
#con bianco ancora meglio, più leggibile 
