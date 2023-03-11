		var ws = new WebSocket("ws://" + location.host + "/game");
        var teamSelect = document.getElementById("team-select");
        var teamName = document.getElementById("team-name");
        var createTeam = document.getElementById("create-team");
        var teamList = document.getElementById("team-list");

        var game = document.getElementById("game");
        var creatureName = document.getElementById("creature-name");
        var submitCreature = document.getElementById("submit-creature");
        var teamScore = document.getElementById("team-score");
        var teamScores = document.getElementById("team-scores");

        var selectedTeam = null;

        // Autocomplete function for creature name input
        var creatures = ["a hydroid", "a keel worm", "a mysid shrimp", "a pill isopod", "a sea slater", "a sea squirt", "a spoon worm", "a stalked jellyfish", "a tube anemone", "a velutinid", "abietinaria abietina", "abra alba", "acanthocardia echinata", "acanthochitona crinitus", "achelia echinata", "acrosorium venulosum", "adamsia carciniopados", "aeolidia papillosa", "aequipecten opercularis", "aglaophenia pluma", "aglaothamnion hookeri", "aglaothamnion sepositum", "aglaozonia asexual cutleria", "ahnfeltia plicata", "alaria esculenta", "alcyonidioides mytili", "alcyonidium diaphanum", "alcyonidium gelatinosum", "alcyonidium hirsutum", "alcyonidium mytili", "alcyonium digitatum", "alcyonium glomeratum", "alentia gelatinosa", "alvania semistriata", "amathia lendigera", "american sting winkle", "ammodytes tobianus", "ampelisca brevicornis", "ampharete grubei", "ampharete lindstroemi", "amphilectus fucorum", "amphisbetia operculata", "ampithoe rubricata", "an isopod", "anaitides maculata", "anaitides mucosa", "anguinella palmata", "angular crab", "angulus tenuis", "anomia ephippium", "anoplodactylus angulatus", "antithamnion cruciatum", "antithamnionella spirographidis", "aonides oxycephala", "aora gracilis", "aphelochaeta marioni", "apherusa bispinosa", "apherusa jurinei", "apistonema carterae", "aplysilla sulfurea", "apoglossum ruscifolium", "aporrhais pespelecani", "arch-fronted swimming crab", "archidoris pseudoargus", "arctic cowrie", "arenicolides ecaudata", "aricidea minuta", "ascidia conchilega", "ascidia virginea", "ascidiella scabra", "asian shore crab", "aslia lefevrei", "aslia lefevrii", "asperococcus fistulosus", "asterias rubens", "asterocarpa humilis", "astropecten irregularis", "atlantic bobtail squid", "audouinella purpurea", "axinella dissimilis", "axinella infundibuliformis", "baked bean ascidian", "balanus balanus", "balanus crenatus", "ballan wrasse", "barleeia unifasciata", "barnea candida", "barnea parva", "bathyporeia elegans", "bathyporeia pelagica", "bathyporeia pilosa", "bathyporeia sarsi", "beach hopper", "beadlet anemone", "bicellariella ciliata", "bispira volutacornis", "bittium reticulatum", "black-footed limpet", "bladder wrack", "blidingia minima", "blue encrusting sponge", "blue jellyfish", "blue rayed limpet", "boergeseniella thuyoides", "bonnemaisonia asparagoides", "bonnemaisonia hamifera", "boot lace worm", "bostrychia scorpioides", "bowerbankia citrina", "bowerbankia gracilis", "bowerbankia imbricata", "bowerbankia pustulosa", "brachystomia scalaris", "breadcrumb sponge", "bristly mail-shell", "broad-clawed porcelain crab", "brongniartella byssoides", "brown forking weed", "brown shimp", "bryopsis hypnoides", "bryopsis plumosa", "buccinum undatum", "bugula flabellata", "bugula fulva", "bugula plumosa", "bugula turbinata", "bunny ears", "butterfish", "by-the-wind-sailor", "cadlina laevis", "calliblepharis ciliata", "calliopius laeviusculus", "callithamnion tetragonum", "callithamnion tetricum", "callophyllis laciniata", "callopora lineata", "calycella syringa", "calyptraea chinensis", "campecopea hirsuta", "candy striped flatworm", "capitella capitata", "caprella acanthifera", "caryophyllia smithii", "catenella caespitosa", "cellaria sinuosa", "cellepora pumicosa", "celleporella hyalina", "ceramium botryocarpum", "ceramium ciliatum", "ceramium deslongchampii", "ceramium deslongchampsii", "ceramium diaphanum", "ceramium echionotum", "ceramium gaditanum", "ceramium nodulosum", "ceramium pallidum", "ceramium secundatum", "ceramium shuttleworthianum", "ceramium strictum", "ceramium virgatum", "cerastoderma edule", "cerithiopsis tubercularis", "chaetomorpha capillaris", "chaetomorpha linum", "chaetomorpha mediterranea", "chaetomorpha melagonium", "chaetopterus variopedatus", "chamelea gallina", "chameleon prawn", "chameleon shrimp", "channel wrack", "chartella papyracea", "china limpet", "chlamys distorta", "chondracanthus acicularis", "chondria dasyphylla", "chorda filum", "chordaria flagelliformis", "chylocladia verticillata", "cingula cingillus", "ciocalypta penicillus", "cirratulus cirratus", "cirriformia tentaculata", "cladophora albida", "cladophora pellucida", "cladophora rupestris", "cladophora sericea", "cladostephus spongiosus", "clathria atrasanguinea", "clathrina coriacea", "clausinella fasciata", "clava multicornis", "cliona celata", "clitellio arenarius", "clock face anemone", "clockwise spiral worm", "clytia hemisphaerica", "codium tomentosum", "codium vermilara", "common brittle star", "common chiton", "common hermit crab", "common limpet", "common mussel", "common periwinkle", "common prawn", "common sole", "common spider crab", "common squat lobster", "common tortoiseshell limpet", "compass jellyfish", "compsothamnion thuyoides", "conger eel", "connemara clingfish", "conopeum reticulum", "coral weed", "corbula gibba", "cordylecladia erecta", "corella parallelogramma", "corkwing wrasse", "cormorant", "cornish sucker", "corophium sextonae", "corophium volutator", "corynactis viridis", "coryne muscoides", "crab hacker barnacle", "craterolophus convolvulus", "crepidula fornicata", "crimora papillata", "crisia denticulata", "crisia eburnea", "crisidia cornuta", "crossaster papposus", "cryptosula pallasiana", "ctenolabrus rupestris", "cuckoo wrasse", "curled octopus", "cushion star", "cuvie", "cyathura carinata", "cystoclonium purpureum", "cystoseira baccata", "dahlia anemone", "dainty crab", "daisy anemone", "deep hermit crab", "deep water dahlia", "delesseria sanguinea", "dendronotus frondosus", "dercitus bucklandi", "desmarestia aculeata", "desmarestia ligulata", "desmarestia viridis", "dexamine spinosa", "dexamine thea", "diaphorodoris luteocincta", "dictyopteris membranacea", "dictyota dichotoma", "didemnum maculosum", "diodora graeca", "diphasia rosacea", "diplosoma listerianum", "diplosoma spongiforme", "dipper", "dirty sea squirt", "disporella hispida", "distaplia rosea", "distomus variolosus", "dog whelk", "donax vittatus", "doto coronata", "doto fragilis", "drachiella heterocarpa", "drachiella spectabilis", "dragonet", "dulse", "dumontia contorta", "dusky doris", "dwarf brittlestar", "dynamena pumila", "dynamene bidentata", "dysidea fragilis", "eatonina fulgida", "echinocardium cordatum", "echinogammarus obtusatus", "echinus esculentus", "ectocarpus fasciculatus", "edible crab", "eelgrass", "egg wrack", "elachista fucicola", "electra pilosa", "elegant anemone", "ellisolandia elongata", "elminius modestus", "elysia viridis", "ensis ensis", "ensis siliqua", "enteromorpha compressa", "enteromorpha intestinalis", "enteromorpha linza", "enteromorpha prolifera", "erythrodermis traillii", "erythroglossum laciniatum", "erythrotrichia carnea", "escharella immersa", "escharoides coccinea", "esperiopsis fucorum", "eteone longa", "eudendrium capillare", "eudesme virescens", "eulimnogammarus obtusatus", "eumida sanguinea", "eunicella verrucosa", "eupolymnia nebulosa", "european bass", "european eel", "european flat oyster", "european lobster", "european spiny lobster", "european sting winkle", "eurydice pulchra", "exogone hebes", "exogone naidina", "fabricia sabella", "fabulina fabula", "facelina auriculata", "false eyelash weed", "false irish moss", "feather hydroid", "fifteen-spined stickleback", "filograna implexa", "fine-veined crinkle weed", "five bearded rockling", "flabellina pedata", "flat periwinkle", "fluffy white sea slug", "flustra foliacea", "flustrellidra hispida", "fucus ceranoides", "fucus distichus", "fucus vesiculosus var. linearis", "fulmar", "furbellow", "furcellaria lumbricalis", "furry purse sponge", "gammarellus homari", "gammarus zaddachi", "gastroclonium ovatum", "gelidium crinale", "gelidium latifolium", "gelidium pulchellum", "gelidium pusillum", "gelidium spinosum", "gem anemone", "giant goby", "gibbula pennanti", "gigartina pistillata", "ginger anemone", "glaucus pimplet", "glycera tridactyla", "gobiusculus flavescens", "goggle eyed prawn", "goniodoris nodosa", "gracilaria gracilis", "grateloupia filicina", "grateloupia turuturu", "great spider crab", "greater pipefish", "green blisters", "green leaf worm", "green paddleworm", "green sea urchin", "green sponge fingers", "grey seal", "grey top shell", "griffithsia corallinoides", "groovy crab", "guiryi's wrack", "gut weed", "gymnangium montagui", "gymnogongrus crenulatus", "hairy crab", "halarachnion ligulatum", "halecium halecinum", "halichondria bowerbanki", "haliclona cinerea", "haliclona oculata", "haliclona rosea", "haliclona simulans", "haliclona viscosa", "haliclystus auricula", "halidrys siliquosa", "haliotis tuberculata", "halisarca dujardini", "halisarca dujardinii", "halopteris catharina", "halopteris filicina", "halurus equisetifolius", "halurus flosculosus", "haraldiophyllum bonnemaisonii", "harbour crab", "harmothoe extenuata", "harmothoe imbricata", "harpoon weed", "helcion pellucidum", "hemimycale columella", "henricia oculata", "henricia sanguinolenta", "heteranomia squamula", "heterochaeta costata", "heterosiphonia plumosa", "hiatella arctica", "hildenbrandia rubra", "hincksia granulosa", "holothuria forskali", "honeycomb reef worm", "hooded prawn", "hyale prevostii", "hyale stebbingi", "hydractinia echinata", "hydrallmania falcata", "hydrobia ulvae", "hymeniacidon perleve", "hymeniacidon perlevis", "hymeniacidon sanguinea", "hypoglossum hypoglossoides", "irish moss", "jaera albifrons", "jania rubens", "janira maculosa", "janolus cristatus", "janua pagenstecheri", "jasmineira elegans", "jassa falcata", "jerky hopper", "kallymenia reniformis", "keel worm", "kefersteinia cirrata", "kellia suborbicularis", "kelp", "kelp fur", "kidney scale worm", "kirchenpaueria pinnata", "ladder ascidian", "laeospira corallinae", "lamellaria perspicua", "laminaria ochroleuca", "laminaria saccharina", "laomedea flexuosa", "lasaea adansoni", "leach's spider crab", "leathesia difformis", "leathesia marina", "lepidonotus clava", "lepidonotus squamatus", "leptasterias muelleri", "leptochiton asellus", "leptoplana tremellaris", "leuconia nivea", "leucosolenia botryoides", "leucosolenia complicata", "lichina pygmaea", "light bulb sea squirt", "ligia oceanica", "limacia clavigera", "limapontia capitata", "lineus ruber", "liocarcinus arcuatus", "lissoclinum perforatum", "lithophyllum incrustans", "lithothamnion glaciale", "little egret", "littorina fabalis", "littorina mariae", "littorina nigrolineata", "littorina obtusata", "littorina saxatilis var. rudis", "lomentaria clavellosa", "lomentaria orcadensis", "long-clawed porcelain crab", "long-legged spider crab", "lucernariopsis campanulata", "lucernariopsis cruxmelitensis", "luidia ciliaris", "lysianassa ceratina", "macoma balthica", "mactra stultorum", "malacoceros fuliginosus", "manayunkia aestuarina", "many ribbed jelly", "manzonia crassa", "marbled swimming crab", "margarites helicinus", "marine springtail", "mediomastus fragilis", "melinna palmata", "melita palmata", "membranoptera alata", "meredithia microphylla", "mesophyllum lichenoides", "metridium senile", "microciona atrasanguinea", "modiolarca tumida", "modiolus modiolus", "molgula manhattensis", "monostroma grevillei", "montagu's blenny", "montagu's crab", "montagu's sea snail", "montagu's stellate barnacle", "moon jelly", "morchellium argus", "mud sagartia", "musculus discors", "mya arenaria", "mya truncata", "mysella bidentata", "myxicola infundibulum", "myxilla incrustans", "nassarius incrassatus", "nassarius reticulatus", "nemalion helminthoides", "nemertesia antennina", "nemertesia ramosa", "neoamphitrite figulus", "neopentadactyla mixta", "neosiphonia harveyi", "nephasoma minutum", "nephtys cirrosa", "nephtys hombergii", "nereis pelagica", "netted dog whelk", "new zealand barnacle", "nitophyllum punctatum", "northern green sea urchin", "northern lacuna", "northern rock barnacle", "norway lobster", "notched isopod", "notomastus latericeus", "nucula nucleus", "nursehound", "nymphon gracile", "oarweed", "odonthalia dentata", "odontosyllis ctenostoma", "odontosyllis gibba", "odostomia plicata", "odostomia turrita", "okamura's pom-pom weed", "omalogyra atomus", "onchidella celtica", "onchidoris muricata", "onoba aculeus", "onoba semicostata", "ophiocomina nigra", "ophiopholis aculeata", "ophiura albida", "ophiura ophiura", "ophlitaspongia papilla", "ophlitaspongia seriata", "orange-striped green sea anemone", "orange anemone", "osmundea hybrida", "osmundea osmunda", "osmundea truncata", "owenia fusiformis", "oyster thief", "oystercatcher", "pachymatisma johnstonia", "pacific oyster", "painted top shell", "pale lacuna", "paracentrotus lividus", "parajassa pelagica", "paraonis fulgens", "parasmittina trispinosa", "partulida pellucida", "pecten maximus", "pentapora foliacea", "pepper dulse", "perophora listeri", "petalonia fascia", "phaeostachys spinifera", "pheasant shell", "pholas dactylus", "pholoe inornata", "pholoe synophthalmica", "phoronis hippocrepia", "phyllophora crispa", "phyllophora pseudoceranoides", "phyllophora sicula", "phymatolithon calcareum", "phymatolithon lenormandii", "phymatolithon purpureum", "pilayella littoralis", "pilinia rimosa", "pink mitten amphipod", "plaice", "platynereis dumerilii", "plocamium cartilagineum", "plumaria plumosa", "plumularia setacea", "pododesmus patelliformis", "poli's stellate barnacle", "pollachius pollachius", "pollicipes pollicipes", "polycarpa scuba", "polycera faeroensis", "polycera quadrilineata", "polyclinum aurantium", "polydora ciliata", "polyides rotunda", "polyides rotundus", "polymastia boletiformis", "polymastia mamillaris", "polymastia penicillus", "polyneura bonnemaisonii", "polysiphonia atlantica", "polysiphonia brodiei", "polysiphonia elongata", "polysiphonia fucoides", "polysiphonia lanosa", "polysiphonia nigra", "polysiphonia nigrescens", "polysiphonia stricta", "pomatoceros lamarcki", "pomatoschistus minutus", "pomatoschistus pictus", "pontocrates arenarius", "porania pulvillus", "porphyra linearis", "porphyra purpurea", "porphyra umbilicalis", "portuguese man-of-war", "prasiola stipitata", "protodorvillea kefersteini", "protula tubularia", "psamathe fusca", "pseudendoclonium submarinum", "pseudosuberites fallax", "pterocladia capillacea", "pterosiphonia complanata", "pterosiphonia parasitica", "pterothamnion plumula", "ptilota gunneri", "purple top shell", "purse sponge", "pycnogonum littorale", "pygospio elegans", "pyrenocollema halodytes", "ragged hydroid", "ragworm", "rainbow wrack", "ralfsia verrucosa", "raspailia hispida", "raspailia ramosa", "rayed artemis", "red doris", "red rags", "red ripple bryozoan", "red sea oak", "red speckled anemone", "retusa truncatula", "rhizoclonium riparium", "rhizoclonium tortuosum", "rhodochorton purpureum", "rhodomela confervoides", "rhodomela lycopodioides", "rhodophyllis divaricata", "rhodothamniella floridula", "rhodymenia delicatula", "rhodymenia holmesii", "rhodymenia pseudopalmata", "risso's crab", "rissoa interrupta", "rissoa parva", "rissoella diaphana", "rock cook", "rock goby", "rock pool shrimp", "root-arm medusa", "rosy feather-star", "rough periwinkle", "rough periwinkle", "rugose squat lobster", "runcina coronata", "rush-clawed shore crab", "sabella pavonina", "sabellaria spinulosa", "saccharina latissima", "salmacina dysteri", "sand hopper", "sand mason", "sand smelt", "sandalled anemone", "saw wrack", "scarlet and gold star coral", "schizomavella linearis", "schizymenia dubyi", "schottera nicaeensis", "scolelepis squamata", "scoloplos armiger", "scrobicularia plana", "scruparia chelata", "scrupocellaria reptans", "scrupocellaria scruposa", "scypha ciliata", "scytosiphon lomentaria", "sea gherkin", "sea hare", "sea lemon", "sea lettuce", "sea mat", "sea orange sponge", "sea scorpion", "securiflustra securifrons", "sepia officinalis", "sertularella gaudichaudi", "sertularella polyzonias", "sertularia argentea", "sertularia cupressina", "seven-spot ladybird", "shanny", "shore clingfish", "shore crab", "shore rockling", "sideways sea squirt", "sidnyum elegans", "sidnyum turbinatum", "single horn bryozoan", "skeneopsis planorbis", "small-headed clingfish", "small-spotted catshark", "small cushion star", "small periwinkle", "small snakelocks anemone", "snakelocks anemone", "snapping prawn", "solaster endeca", "soliers red string weed", "spermothamnion repens", "sphacelaria cirrosa", "sphaerococcus coronopifolius", "sphaeroma rugicauda", "sphenia binghami", "sphondylothamnion multifidum", "spiky lace sponge", "spiny squat lobster", "spiny starfish", "spio filicornis", "spio martinensis", "spiophanes bombyx", "spiral wrack", "spirobranchus triqueter", "spirorbis corallinae", "spirorbis rupestris", "spirorbis spirorbis", "spongomorpha aeruginosa", "spongomorpha arcta", "spongonema tomentosum", "spotted cowrie", "spotted kaleidoscope jellyfish", "st piran's hermit crab", "star ascidian", "starry sea lemon", "stelligera rigida", "stelligera stuposa", "stenothoe monoculoides", "sthenelais boa", "stolonica socialis", "strawberry anemone", "strawberry sea squirt", "streblospio shrubsolii", "styela clava", "stypocaulon scoparia", "suberites carnosus", "syllidia armata", "syllis gracilis", "taonia atomaria", "terebella lapidaria", "terpios fugax", "testudinalia testudinalis", "tethya aurantium", "tethya citrina", "tharyx killariensis", "thick-lipped dog whelk", "thick trough shell", "thong weed", "thorogobius ephippiatus", "tiny lacuna", "tompot blenny", "tonicella rubra", "toothed top shell", "topknot", "trailliella intricata", "trididemnum cereum", "trisopterus luscus", "tritonia lineata", "trumpet anemone", "tubificoides amplivasatus", "tubificoides benedii", "tubificoides pseudogaster", "tubularia indivisa", "tubularia larynx", "turban top shell", "turbonilla lactea", "turritella communis", "turtonia minuta", "ulothrix flacca", "ulva compressa", "ulva prolifera", "ulva pseudocurvata", "umbonula littoralis", "undaria pinnatifida", "variegated scallop", "variegated scallop", "velvet swimming crab", "venerupis corrugata", "venerupis senegalensis", "verrucaria maura", "verrucaria mucosa", "vertebrata lanosa", "virgularia mirabilis", "volcano barnacle", "walkeria uva", "wart barnacle", "warty sea slug", "websterinereis glauca", "werthers original sea squirt", "white tortoiseshell limpet", "whiting", "wireweed", "worm pipefish", "yellow-plumed sea slug", "yellow sea squirt"];
        var autocompleteCreature = function(input, array) {
            input.addEventListener("input", function() {
                var val = this.value;
                closeAllLists();
                if (!val) { return false; }
                var list = document.createElement("ul");
                list.setAttribute("id", this.id + "-autocomplete-list");
                list.setAttribute("class", "autocomplete-items");
                // Add a CSS style rule for the autocomplete-items class to increase the font size of the autocompleted creatured from the search bar
                list.style.fontSize = "1.4em";
                this.parentNode.appendChild(list);
                for (var i = 0; i < array.length; i++) {
                    if (array[i].toLowerCase().indexOf(val.toLowerCase()) > -1) {
                        var item = document.createElement("li");
                        item.innerHTML = "<strong>" + array[i].substr(0, val.length) + "</strong>";
                        item.innerHTML += array[i].substr(val.length);
                        item.addEventListener("click", function() {
                            input.value = this.innerText;
                            closeAllLists();
                        });
                        list.appendChild(item);
                    }
                }
            });

            function closeAllLists(elmnt) {
                var lists = document.getElementsByClassName("autocomplete-items");
                for (var i = 0; i < lists.length; i++) {
                    if (elmnt != lists[i] && elmnt != input) {
                        lists[i].parentNode.removeChild(lists[i]);
                    }
                }
            }

            document.addEventListener("click", function(e) {
                closeAllLists(e.target);
            });
        };

        // Initialize autocomplete for creature name input
        autocompleteCreature(creatureName, creatures);

        createTeam.addEventListener("click", function() {
            var name = teamName.value.trim();
            if (name.length > 0) {
                ws.send(JSON.stringify({
                    action: "create_team",
                    team_name: name
                }));
                ws.send(JSON.stringify({
                    action: "submit_creature",
                    team_name: name,
                    creature_name: name
                }));
                selectedTeam = name;
                document.getElementById("team-name-display").textContent = "(" + name + ")";
                // Hide team-select div and show game div
                teamSelect.style.display = "none";
                game.style.display = "block";
                submitCreature.style.display = "block";
                creatureName.style.display = "block";
            }
        });

        submitCreature.addEventListener("click", function() {
            var name = creatureName.value.trim().replace(/[^\w\s]|_/g, ''); // remove non-alphanumeric characters except for spaces
            name = encodeURIComponent(name); // encode special characters
            name = name.trim(); // remove any leading or trailing whitespace

            if (name.length > 0) {
                if (ws.readyState === WebSocket.OPEN) {
                    ws.send(JSON.stringify({
                        action: "submit_creature",
                        team_name: selectedTeam,
                        creature_name: name
                    }));
                    creatureName.value = "";
                } else {
                    console.log("WebSocket not open");
                }
            }
        });

        ws.onopen = function(event) {
            console.log("WebSocket opened");
        };

        ws.onmessage = function(event) {
            var data = JSON.parse(event.data);
            var action = data.action;

            if (action == "update_team_list") {
                var list = data.team_list;
                teamList.innerHTML = "";
                for (var i = 0; i < list.length; i++) {
                    var item = document.createElement("li");
                    item.innerText = list[i];
                    item.onclick = function() {
                        selectedTeam = this.innerText;
                        teamSelect.style.display = "none";
                        game.style.display = "block";
                        teamScore.innerText = "0";
                        submitCreature.style.display = "block";
                        creatureName.style.display = "block";
                        submitCreature.style.display = "block";
                    };
                    teamList.appendChild(item);
                }
            }

    if (action == "update_team_score") {
    var teamName = teamName.value.trim().replace(/[^\w\s]|_/g, ''); // remove non-alphanumeric characters except for spaces
    teamName = encodeURIComponent(teamName); // encode special characters
    teamName = teamName.trim(); // remove any leading or trailing whitespace
    teamName = teamName.slice(0, 1).toUpperCase() + teamName.slice(1).toLowerCase(); // capitalize first letter, lowercase the rest

    var score = data.score;
    var teamScoreElement = document.getElementById("team-score-" + teamName);
    if (teamScoreElement) {
        teamScoreElement.innerText = score;
    } else {
        var item = document.createElement("li");
        item.innerText = teamName + ": ";
        var scoreElement = document.createElement("span");
        scoreElement.id = "team-score-" + teamName;
        scoreElement.innerText = score;
        item.appendChild(scoreElement);
        teamScores.appendChild(item);
    }
}

     var teamCreaturesList = document.getElementById("team-creatures-list");
     if (action == "update_team_scores") {
         var teams = data.teams;
         for (var teamName in teams) {
             var score = teams[teamName].score;
             var teamScoreElement = document.getElementById("team-score-" + teamName);
             if (teamScoreElement) {
                 teamScoreElement.innerText = score;
             } else {
                 var item = document.createElement("li");
                 item.innerText = teamName + ": ";
                 var scoreElement = document.createElement("span");
                 scoreElement.id = "team-score-" + teamName;
                 scoreElement.innerText = score;
                 item.appendChild(scoreElement);
                 teamScores.appendChild(item);
             }
             
             // update the list of creatures for the team
             var teamCreatures = teams[teamName].creatures;
             var creaturesElement = document.getElementById("team-creatures-" + teamName);
             if (creaturesElement) {
                 creaturesElement.innerHTML = ""; // clear the existing list
                 for (var i = 0; i < teamCreatures.length; i++) {
                     var creatureName = teamCreatures[i];
                     if (creatures.includes(creatureName)) { // check if the creature is in var creatures
                         var creatureElement = document.createElement("li");
                         creatureElement.innerText = creatureName;
                         creaturesElement.appendChild(creatureElement);
                     }
                 }
             } else {
                 var item = document.createElement("li");
                 item.innerText = teamName + " creatures:";
                 var creaturesElement = document.createElement("ul");
                 creaturesElement.id = "team-creatures-" + teamName;
                 for (var i = 0; i < teamCreatures.length; i++) {
                     var creatureName = teamCreatures[i];
                     if (creatures.includes(creatureName)) { // check if the creature is in var creatures
                         var creatureElement = document.createElement("li");
                         creatureElement.innerText = creatureName;
                         creaturesElement.appendChild(creatureElement);
                     }
                 }
                 item.appendChild(creaturesElement);
                 teamCreaturesList.appendChild(item);
             }
         }
     }
        };
    
    window.onbeforeunload = function() {
      ws.close();
    };
    
    ws.onclose = function(event) {
      if (ws.readyState == WebSocket.CLOSED) {
            console.log("WebSocket closed");
      }
};

    ws.onerror = function(event) {
        console.log("WebSocket error", event);
    };