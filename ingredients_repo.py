
ALCOHOL_INFO = {
    "bad": "Harsh Alcohols Detected: These alcohols will dry out your hair",
    "good": "Curly Girl Approved Alcohols: These alcohols won't dry our your hair",
    "not_alcohol": ""
}

ALCOHOL_DICT = {
    "bad" : {"alcohol", "alcohol 1", "alcohol1", "ethanol", "isopropanol", "propanol", "alcohol 40-b", "alcohol 40b", "alcohol denat", "alcohol-40b", "denatured alcohol", "ethyl alcohol", "isopropanol", "isopropyl alcohol", "propyl alcohol", "sd alcohol", "sd alcohol 40", "sugarcane derived alcohol"},
    "good" : {"behenyl alcohol", "cetearyl alcohol", "ceteryl alcohol", "cetyl alcohol", "isocetyl alcohol", "isostearyl alcohol", "lauryl alcohol", "myristyl alcohol", "stearyl alcohol", "c30-50 alcohols", "lanolin alcohol", "benzyl alcohol", "stearyl alcohol", "aminomethyl propanol", "oleyl alcohol", "brassica alcohol", "benzyl alcohol", "arachidyl alcohol", "phenethyl alcohol", "undecyl alcohol", "amyl cinnamyl alcohol", "amylcinnamyl alcohol", "amino-2-methyl-1-propanol", "aminomethyl propanol", "amino methyl propanol", "c14-22 alcohol", "c20-c22 alcohol", "phenylpropanol", "acetyl alcohol", "steareth alcohol", "phenyl ethyl alcohol", "phenylethyl alcohol", "acetylated lanolin alcohol", "cinnamyl alcohol", "phenethyl alcohol", "cinnamic alcohol", "behenyl alcohol", "pantothenyl alcohol", "coconut alcohol", "butylene alcohol", "steoryl alcohol"},
    "not_alcohol": {"triisopropanolamine"}
}

SULFATE_INFO = {
    "bad": "Harsh Sulfates Detected: Yikes! These are either sulfates or detergents that the curly girl community considers drying",
    "good": "Curly Girl Approved Cleansers: These are considered gentle by most of the curly girl community",
    "caution": "More Research Recommended: Some consider these CG-safe, others do not",
    "partial": "Unknown Cleansers: These may be misspelled non-CG sulfates or they may be fine"
}

SULFATE_DICT = {
    "bad" : {"ammonium lauryl sulfate", "ammonium lauryl sulphate", "ammonium laureth sulfate", "ammonium laureth sulphate", "sodium lauryl sulfate", "sodium lauryl sulphate", "sodium laureth sulfate", "sodium laureth sulphate", "tea lauryl sulfate", "tea lauryl sulphate", "tea-dodecylbenzenesulfonate", "triethanolamine lauryl sulfate", "triethanolamine lauryl sulphate", "sodium cetearyl sulfate", "sodium cetearyl sulphate", "sodium coco sulfate", "sodium coco sulphate", "sodium cocosulfate", "sodium cocosulphate", "sodium coco-sulfate", "sodium coco-sulphate", "sodium coceth sulfate", "sodium coceth sulphate", "ammonium laureth sulfate", "ammonium laureth sulphate", "ammonium lauryl sulfate", "ammonium lauryl sulphate", "sodium myreth sulfate", "sodium myreth sulphate", "sodium polystyrene sulfate", "sodium polystyrene sulphate", "ammonium cocoyl sulfate", "ammonium cocoyl sulphate", "sodium c12-18 alkyl sulfate", "sodium c12-18 alkyl sulphate", "sodium alkyl sulfate", "sodium alkyl sulphate", "sodium laureth-40 sulfate", "sodium laureth-40 sulphate", "alkylbenzene sulfonate", "alkyl benzene sulfonate", "ammonium xylenesulfonate", "ammonium xylene-sulfonate", "ethyl peg-15 cocamine sulfate", "sodium xylenesulfonate", "sodium xylene-sulfonate", "tea-dodecylbenzenesulfonate", "tea dodecylbenzenesulfonate"},
    "caution" : {"olefin sulfonate", "oliefin sulfonate", "sodium c14-16 olefin sulfonate", "sodium c14-15 olefin sulfonate", "sodium c12-14 olefin sulfonate", "sodium c14-26 olefin sulfonate", "sodium c 14-18 olefin sulfonate", "sodium c 16-18 olefin sulfonate", "sodium cocoyl sarcosinate", "sodium lauroyl sarcosinate", "sodium lauryl sarcosinate", "sodium lauroyl sarcosine", "sodium lauryl sulfoacetate", "sodium cocoyl glutamate", "sodium lauroyl methyl isethionate", "sodium lauryl methyl isothionate", "sodium lauroyl methyl lsethionate", "sodium lauroylmethyl isethionate", "dioctyl sodium sulfosuccinate", "disodium cocoyl glutamate", "sodium myristoyl sarcosinate"},
    "good" : {"disodium laureth sulfosuccinate", "disodium laureth succinate", "sodium lauryl glucose carboxylate", "sodium methyl cocoyl taurate", "sodium lauroyl glutamate", "ammonium cocoyl isethionate", "sodium cocoyl isethionate", "coco betaine", "coco betaine", "cocamidopropyl betaine", "disodium cocoamphodiacetate", "cocamidopropyl hydroxysultaine", "lauryl hydroxysultaine", "sodium cocoamphoacetate", "sodium lauroamphoacetate", "coco glucoside", "capryl glucoside", "caprylyl glucoside", "decyl glucoside", "lauryl glucoside", "decyl polyglucose", "disodium cocoamphodipropionate", "babassuamidopropyl betaine", "sodium laurylglucosides hydroxypropylsulfonate", "sodium lauroyl lactylate", "sodium lauroyl hydrolyzed silk", "sodium methyl 2-sulfolaurate", "disodium 2-sulfolaurate", "sodium lauroyl oat amino acids", "disodium lauryl sulfosuccinate"},
    "partial" : {"ammonium lauryl", "lauryl sulfate", "lauryl sulphate", "cetearyl sulfate", "cetearyl sulphate", "cocosulfate", "coco-sulfate", "coco sulfate", "cocoyl sulfate", "cocosulphate", "coco-sulphate", "coco sulphate", "cocoyl sulphate", "coceth sulfate", "coceth sulphate", "laureth sulfate", "laureth sulphate", "ammonium laureth", "sarcosinate", "sodium lauryl", "sodium myreth", "myreth sulfate", "myreth sulphate", "sodium lauroyl", "sodium laureth", "laureth sulfate", "laureth sulphate", "ammonium lauryl", "ammonium xylenesulfonate", "ammonium xylene-sulfonate", "cocoyl glutamate", "polystyrene sulfate", "polystyrene sulphate", "alkyl sulfate", "alkyl sulphate"}
}

PSW_INFO = {
    "paraben" : "Controversial, More Research Recommended: May be linked to cancer",
    "soap": "More Research Recommended: Could contain soap which as harsh as sulfates",
    "witchhazel" : "More research recommended: May contain alcohol, prone to cause dryness"
} 

PSW_DICT = {
    "paraben" : {"paraben"},
    "soap" : {"sodium palm", "saponified", "saponification", "soap", "sodium carboxylate", "saponifying", "potassium hydroxide"},
    "witchhazel" : {"witch", "hamamelis", "hamamellis", "hazel"}
}

SILICON_INFO = {
    "good" : "Curly Girl Approved",
    "bad": "Bad Silicones Detected: Most likely non-CG silicones so not water soluble and cause buildup"
}

SILICON = {
    "bad" : {"cone", "dimethicon", "silane", "siloxane", "dimethcione", "botanisil", "silicon", "silylate", "silsesquioxane", "siloxysilicate", "microsil"},
    "good" : {"peg", "ppg", "pg-" , "saccharomycessilicon ferment", "silicon ferment"}
}

WAX_INFO = {
    "bad" : "Bad Waxes/Oils Detected: Can Cause Buildup and prevent moisture absorbtion",
    "good": "Ok Waxes & Oils: modified to make them water soluble",
    "not": "Curly Girl Approved"
}

WAX_DICT = {
    "bad" : {"wax", "cire", "cera", "paraffin", "lanolin", "mineral oil", "petrolatum", "isohexadecane", "isohexanedecane", "isododecane", "dodecene", "dodecane", "isohexad", "shellac", "bees wax", "beeswax", "candelia wax", "cire dabeille", "cera alba", "microcrystalline wax", "myrica pubescens fruit wax", "synthetic beeswax", "euphorbia cerifera (candelilla) wax", "stearoxytrimethyl silane and stearyl alcohol (silky wax)", "cera alba (beeswax)", "microcrystalline wax (cera microcristallina)"},
    "good" : {"peg-8 beeswax", "emulsifying wax", "emulsifying wax nf", "peg 8 beeswax", "peg-75 lanolin"},
    "not" : {"lonincera", "lonicera", "acetylated lanolin alcohol", "lanolin alcohol", "ceramide ng", "ceramides", "ceramide"}
}
    