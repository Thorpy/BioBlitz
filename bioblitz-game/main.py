import os
import asyncio
import json
import uvicorn
import fcntl
from typing import Callable
from fastapi import FastAPI, Request
from fastapi.websockets import WebSocket, WebSocketState, WebSocketDisconnect
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from urllib.parse import unquote
from threading import Lock


app = FastAPI()
home_dir = os.environ['HOME']
data_path = f"{home_dir}/BioBlitz/bioblitz-game/"
data_file_path = os.path.join(data_path, "static", "data.json")
past_games_path = os.path.join(data_path, "Past Games")
app.mount("/static", StaticFiles(directory=f"{home_dir}/BioBlitz/bioblitz-game/static"), name="static")

class Game:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "creature_scores"):
            # Game instance already initialized
            return
        # Define initial scores for creatures
        self.creature_scores = {
            "a hydroid (candelabrum cocksii)":3,
            "a keel worm (spirobranchus lamarcki)":3,
            "a mysid shrimp (siriella armata)":10,
            "a pill isopod (sphaeroma serratum)":5,
            "a sea slater (stenosoma lancifer)":5,
            "a sea squirt (aplidium nordmanni)":10,
            "a sea squirt (aplidium pallidum)":10,
            "a sea squirt (aplidium punctum)":3,
            "a sea squirt (aplidium turbinatum)":10,
            "a spoon worm (thalassema thalassemum)":10,
            "a stalked jellyfish (calvadosia campanulata)":6,
            "a tube anemone (cerianthus lloydii)":20,
            "a velutinid (lamellaria latens)":10,
            "abietinaria abietina (abietinaria abietina)":20,
            "abra alba (abra alba)":20,
            "acanthocardia echinata (acanthocardia echinata)":20,
            "acanthochitona crinitus (acanthochitona crinitus)":6,
            "achelia echinata (achelia echinata)":20,
            "acrosorium venulosum (acrosorium venulosum)":20,
            "adamsia carciniopados (adamsia carciniopados)":20,
            "aeolidia papillosa (aeolidia papillosa)":3,
            "aequipecten opercularis (aequipecten opercularis)":8,
            "aglaophenia pluma (aglaophenia pluma)":20,
            "aglaothamnion hookeri (aglaothamnion hookeri)":20,
            "aglaothamnion sepositum (aglaothamnion sepositum)":20,
            "aglaozonia (asexual cutleria) aglaozonia (asexual cutleria)":20,
            "ahnfeltia plicata (ahnfeltia plicata)":20,
            "alaria esculenta (alaria esculenta)":20,
            "alcyonidioides mytili (alcyonidioides mytili)":20,
            "alcyonidium diaphanum (alcyonidium diaphanum)":20,
            "alcyonidium gelatinosum (alcyonidium gelatinosum)":20,
            "alcyonidium hirsutum (alcyonidium hirsutum)":10,
            "alcyonidium mytili (alcyonidium mytili)":20,
            "alcyonium digitatum (alcyonium digitatum)":20,
            "alcyonium glomeratum (alcyonium glomeratum)":20,
            "alentia gelatinosa (alentia gelatinosa)":3,
            "alvania semistriata (alvania semistriata)":20,
            "amathia lendigera (amathia lendigera)":20,
            "american sting winkle (urosalpinx cinerea)":8,
            "ammodytes tobianus (ammodytes tobianus)":20,
            "ampelisca brevicornis (ampelisca brevicornis)":20,
            "ampharete grubei (ampharete grubei)":20,
            "ampharete lindstroemi (ampharete lindstroemi)":20,
            "amphilectus fucorum (amphilectus fucorum)":20,
            "amphisbetia operculata (amphisbetia operculata)":20,
            "ampithoe rubricata (ampithoe rubricata)":20,
            "an isopod (idotea balthica)":5,
            "an isopod (idotea granulosa)":6,
            "an isopod (idotea pelagica)":6,
            "anaitides maculata (anaitides maculata)":20,
            "anaitides mucosa (anaitides mucosa)":20,
            "anguinella palmata (anguinella palmata)":20,
            "angular crab (goneplax rhomboides)":10,
            "angulus tenuis (angulus tenuis)":10,
            "anomia ephippium (anomia ephippium)":10,
            "anoplodactylus angulatus (anoplodactylus angulatus)":20,
            "antithamnion cruciatum (antithamnion cruciatum)":20,
            "antithamnionella spirographidis (antithamnionella spirographidis)":20,
            "aonides oxycephala (aonides oxycephala)":20,
            "aora gracilis (aora gracilis)":20,
            "aphelochaeta marioni (aphelochaeta marioni)":20,
            "apherusa bispinosa (apherusa bispinosa)":20,
            "apherusa jurinei (apherusa jurinei)":20,
            "apistonema carterae (apistonema carterae)":20,
            "aplysilla sulfurea (aplysilla sulfurea)":20,
            "apoglossum ruscifolium (apoglossum ruscifolium)":10,
            "aporrhais pespelecani (aporrhais pespelecani)":20,
            "arch fronted swimming crab (liocarcinus navigator)":8,
            "archidoris pseudoargus (archidoris pseudoargus)":20,
            "arctic cowrie (trivia arctica)":4,
            "arenicolides ecaudata (arenicolides ecaudata)":10,
            "aricidea minuta (aricidea minuta)":20,
            "ascidia conchilega (ascidia conchilega)":10,
            "ascidia virginea (ascidia virginea)":20,
            "ascidiella scabra (ascidiella scabra)":20,
            "asian shore crab (hemigrapsus sanguineus)":10,
            "aslia lefevrei (aslia lefevrei)":8,
            "aslia lefevrii (aslia lefevrii)":20,
            "asperococcus fistulosus (asperococcus fistulosus)":20,
            "asterias rubens (asterias rubens)":7,
            "asterocarpa humilis (asterocarpa humilis)":20,
            "astropecten irregularis (astropecten irregularis)":20,
            "atlantic bobtail squid (sepiola atlantica)":6,
            "audouinella purpurea (audouinella purpurea)":20,
            "axinella dissimilis (axinella dissimilis)":20,
            "axinella infundibuliformis (axinella infundibuliformis)":20,
            "baked bean ascidian (dendrodoa grossularia)":4,
            "balanus balanus (balanus balanus)":10,
            "balanus crenatus (balanus crenatus)":5,
            "ballan wrasse (labrus bergylta)":10,
            "barleeia unifasciata (barleeia unifasciata)":20,
            "barnea candida (barnea candida)":20,
            "barnea parva (barnea parva)":20,
            "bathyporeia elegans (bathyporeia elegans)":20,
            "bathyporeia pelagica (bathyporeia pelagica)":20,
            "bathyporeia pilosa (bathyporeia pilosa)":20,
            "bathyporeia sarsi (bathyporeia sarsi)":20,
            "beach hopper (orchestia gammarellus)":10,
            "beadlet anemone (actinia equina)":1,
            "bicellariella ciliata (bicellariella ciliata)":20,
            "bispira volutacornis (bispira volutacornis)":10,
            "bittium reticulatum (bittium reticulatum)":8,
            "black footed limpet (patella depressa)":2,
            "bladder wrack (fucus vesiculosus)":1,
            "blidingia minima (blidingia minima)":10,
            "blue encrusting sponge (terpios gelatinosus)":5,
            "blue jellyfish (cyanea lamarckii)":5,
            "blue rayed limpet (patella pellucida)":2,
            "boergeseniella thuyoides (boergeseniella thuyoides)":20,
            "bonnemaisonia asparagoides (bonnemaisonia asparagoides)":20,
            "bonnemaisonia hamifera (bonnemaisonia hamifera)":20,
            "boot lace worm (lineus longissimus)":3,
            "bostrychia scorpioides (bostrychia scorpioides)":20,
            "bowerbankia citrina (bowerbankia citrina)":20,
            "bowerbankia gracilis (bowerbankia gracilis)":20,
            "bowerbankia imbricata (bowerbankia imbricata)":20,
            "bowerbankia pustulosa (bowerbankia pustulosa)":20,
            "brachystomia scalaris (brachystomia scalaris)":20,
            "breadcrumb sponge (halichondria panicea)":2,
            "bristly mail shell (acanthochitona crinita)":3,
            "broad clawed porcelain crab (porcellana platycheles)":1,
            "brongniartella byssoides (brongniartella byssoides)":20,
            "brown forking weed (bifurcaria bifurcata)":5,
            "brown shimp (crangon crangon)":8,
            "bryopsis hypnoides (bryopsis hypnoides)":20,
            "bryopsis plumosa (bryopsis plumosa)":20,
            "buccinum undatum (buccinum undatum)":7,
            "bugula flabellata (bugula flabellata)":20,
            "bugula fulva (bugula fulva)":20,
            "bugula plumosa (bugula plumosa)":20,
            "bugula turbinata (bugula turbinata)":20,
            "bunny ears (lomentaria articulata)":3,
            "butterfish (pholis gunnellus)":10,
            "by the wind sailor (velella velella)":10,
            "cadlina laevis (cadlina laevis)":10,
            "calliblepharis ciliata (calliblepharis ciliata)":10,
            "calliopius laeviusculus (calliopius laeviusculus)":20,
            "callithamnion tetragonum (callithamnion tetragonum)":20,
            "callithamnion tetricum (callithamnion tetricum)":20,
            "callophyllis laciniata (callophyllis laciniata)":8,
            "callopora lineata (callopora lineata)":20,
            "calycella syringa (calycella syringa)":20,
            "calyptraea chinensis (calyptraea chinensis)":20,
            "campecopea hirsuta (campecopea hirsuta)":10,
            "candy striped flatworm (prostheceraeus vittatus)":8,
            "capitella capitata (capitella capitata)":7,
            "caprella acanthifera (caprella acanthifera)":20,
            "caryophyllia smithii (caryophyllia smithii)":7,
            "catenella caespitosa (catenella caespitosa)":10,
            "cellaria sinuosa (cellaria sinuosa)":20,
            "cellepora pumicosa (cellepora pumicosa)":10,
            "celleporella hyalina (celleporella hyalina)":20,
            "ceramium botryocarpum (ceramium botryocarpum)":20,
            "ceramium ciliatum (ceramium ciliatum)":20,
            "ceramium deslongchampii (ceramium deslongchampii)":20,
            "ceramium deslongchampsii (ceramium deslongchampsii)":20,
            "ceramium diaphanum (ceramium diaphanum)":20,
            "ceramium echionotum (ceramium echionotum)":20,
            "ceramium gaditanum (ceramium gaditanum)":20,
            "ceramium nodulosum (ceramium nodulosum)":20,
            "ceramium pallidum (ceramium pallidum)":20,
            "ceramium secundatum (ceramium secundatum)":20,
            "ceramium shuttleworthianum (ceramium shuttleworthianum)":20,
            "ceramium strictum (ceramium strictum)":20,
            "ceramium virgatum (ceramium virgatum)":20,
            "cerastoderma edule (cerastoderma edule)":20,
            "cerithiopsis tubercularis (cerithiopsis tubercularis)":20,
            "chaetomorpha capillaris (chaetomorpha capillaris)":20,
            "chaetomorpha linum (chaetomorpha linum)":20,
            "chaetomorpha mediterranea (chaetomorpha mediterranea)":20,
            "chaetomorpha melagonium (chaetomorpha melagonium)":10,
            "chaetopterus variopedatus (chaetopterus variopedatus)":20,
            "chamelea gallina (chamelea gallina)":8,
            "chameleon prawn (hippolyte varians)":4,
            "chameleon shrimp (praunus flexuosus)":10,
            "channel wrack (pelvetia canaliculata)":3,
            "chartella papyracea (chartella papyracea)":20,
            "china limpet (patella ulyssiponensis)":4,
            "chlamys distorta (chlamys distorta)":20,
            "chondracanthus acicularis (chondracanthus acicularis)":10,
            "chondria dasyphylla (chondria dasyphylla)":20,
            "chorda filum (chorda filum)":10,
            "chordaria flagelliformis (chordaria flagelliformis)":20,
            "chylocladia verticillata (chylocladia verticillata)":20,
            "cingula cingillus (cingula cingillus)":10,
            "ciocalypta penicillus (ciocalypta penicillus)":20,
            "cirratulus cirratus (cirratulus cirratus)":5,
            "cirriformia tentaculata (cirriformia tentaculata)":7,
            "cladophora albida (cladophora albida)":20,
            "cladophora pellucida (cladophora pellucida)":10,
            "cladophora rupestris (cladophora rupestris)":8,
            "cladophora sericea (cladophora sericea)":20,
            "cladostephus spongiosus (cladostephus spongiosus)":10,
            "clathria atrasanguinea (clathria atrasanguinea)":20,
            "clathrina coriacea (clathrina coriacea)":20,
            "clausinella fasciata (clausinella fasciata)":10,
            "clava multicornis (clava multicornis)":20,
            "cliona celata (cliona celata)":20,
            "clitellio arenarius (clitellio arenarius)":20,
            "clock face anemone (peachia cylindrica)":20,
            "clockwise spiral worm (spirorbis tridentatus)":2,
            "clytia hemisphaerica (clytia hemisphaerica)":20,
            "codium tomentosum (codium tomentosum)":20,
            "codium vermilara (codium vermilara)":20,
            "common brittle star (ophiothrix fragilis)":1,
            "common chiton (lepidochitona cinerea)":2,
            "common hermit crab (pagurus bernhardus)":1,
            "common limpet (patella vulgata)":1,
            "common mussel (mytilus edulis)":1,
            "common periwinkle (littorina littorea)":1,
            "common prawn (palaemon serratus)":1,
            "common sole (solea solea)":10,
            "common spider crab (maja brachydactyla)":3,
            "common squat lobster (galathea squamifera)":3,
            "common tortoiseshell limpet (tectura testudinalis)":8,
            "compass jellyfish (chrysaora hysoscella)":3,
            "compsothamnion thuyoides (compsothamnion thuyoides)":20,
            "conger eel (conger conger)":10,
            "connemara clingfish (lepadogaster candolii)":7,
            "conopeum reticulum (conopeum reticulum)":8,
            "coral weed (corallina officinalis)":2,
            "corbula gibba (corbula gibba)":20,
            "cordylecladia erecta (cordylecladia erecta)":20,
            "corella parallelogramma (corella parallelogramma)":20,
            "corkwing wrasse (symphodus melops)":6,
            "cormorant (phalacrocorax carbo)":10,
            "cornish sucker (lepadogaster purpurea)":3,
            "corophium sextonae (corophium sextonae)":20,
            "corophium volutator (corophium volutator)":20,
            "corynactis viridis (corynactis viridis)":20,
            "coryne muscoides (coryne muscoides)":20,
            "crab hacker barnacle (sacculina carcini)":3,
            "craterolophus convolvulus (craterolophus convolvulus)":20,
            "crepidula fornicata (crepidula fornicata)":5,
            "crimora papillata (crimora papillata)":20,
            "crisia denticulata (crisia denticulata)":20,
            "crisia eburnea (crisia eburnea)":20,
            "crisidia cornuta (crisidia cornuta)":20,
            "crossaster papposus (crossaster papposus)":20,
            "cryptosula pallasiana (cryptosula pallasiana)":10,
            "ctenolabrus rupestris (ctenolabrus rupestris)":20,
            "cuckoo wrasse (labrus mixtus)":20,
            "curled octopus (eledone cirrhosa)":20,
            "cushion star (asterina gibbosa)":1,
            "cuvie (laminaria hyperborea)":6,
            "cyathura carinata (cyathura carinata)":20,
            "cystoclonium purpureum (cystoclonium purpureum)":10,
            "cystoseira baccata (cystoseira baccata)":20,
            "dahlia anemone (urticina felina)":2,
            "dainty crab (pirimela denticulata)":10,
            "daisy anemone (cereus pedunculatus)":2,
            "deep hermit crab (pagurus prideaux)":20,
            "deep water dahlia (urticina eques)":20,
            "delesseria sanguinea (delesseria sanguinea)":10,
            "dendronotus frondosus (dendronotus frondosus)":20,
            "dercitus bucklandi (dercitus bucklandi)":10,
            "desmarestia aculeata (desmarestia aculeata)":8,
            "desmarestia ligulata (desmarestia ligulata)":10,
            "desmarestia viridis (desmarestia viridis)":20,
            "dexamine spinosa (dexamine spinosa)":20,
            "dexamine thea (dexamine thea)":20,
            "diaphorodoris luteocincta (diaphorodoris luteocincta)":20,
            "dictyopteris membranacea (dictyopteris membranacea)":20,
            "dictyota dichotoma (dictyota dichotoma)":20,
            "didemnum maculosum (didemnum maculosum)":8,
            "diodora graeca (diodora graeca)":10,
            "diphasia rosacea (diphasia rosacea)":20,
            "diplosoma listerianum (diplosoma listerianum)":20,
            "diplosoma spongiforme (diplosoma spongiforme)":6,
            "dipper (cinclus cinclus)":20,
            "dirty sea squirt (ascidiella aspersa)":3,
            "disporella hispida (disporella hispida)":20,
            "distaplia rosea (distaplia rosea)":20,
            "distomus variolosus (distomus variolosus)":20,
            "dog whelk (nucella lapillus)":1,
            "donax vittatus (donax vittatus)":20,
            "doto coronata (doto coronata)":20,
            "doto fragilis (doto fragilis)":20,
            "drachiella heterocarpa (drachiella heterocarpa)":20,
            "drachiella spectabilis (drachiella spectabilis)":20,
            "dragonet (callionymus lyra)":7,
            "dulse (palmaria palmata)":2,
            "dumontia contorta (dumontia contorta)":5,
            "dusky doris (onchidoris bilamellata)":7,
            "dwarf brittlestar (amphipholis squamata)":1,
            "dynamena pumila (dynamena pumila)":4,
            "dynamene bidentata (dynamene bidentata)":6,
            "dysidea fragilis (dysidea fragilis)":8,
            "eatonina fulgida (eatonina fulgida)":20,
            "echinocardium cordatum (echinocardium cordatum)":7,
            "echinogammarus obtusatus (echinogammarus obtusatus)":20,
            "echinus esculentus (echinus esculentus)":20,
            "ectocarpus fasciculatus (ectocarpus fasciculatus)":20,
            "edible crab (cancer pagurus)":1,
            "eelgrass (zostera marina)":6,
            "egg wrack (ascophyllum nodosum)":2,
            "elachista fucicola (elachista fucicola)":20,
            "electra pilosa (electra pilosa)":3,
            "elegant anemone (sagartia elegans)":7,
            "ellisolandia elongata (ellisolandia elongata)":20,
            "elminius modestus (elminius modestus)":10,
            "elysia viridis (elysia viridis)":8,
            "ensis ensis (ensis ensis)":20,
            "ensis siliqua (ensis siliqua)":10,
            "enteromorpha compressa (enteromorpha compressa)":20,
            "enteromorpha intestinalis (enteromorpha intestinalis)":10,
            "enteromorpha linza (enteromorpha linza)":20,
            "enteromorpha prolifera (enteromorpha prolifera)":20,
            "erythrodermis traillii (erythrodermis traillii)":20,
            "erythroglossum laciniatum (erythroglossum laciniatum)":20,
            "erythrotrichia carnea (erythrotrichia carnea)":20,
            "escharella immersa (escharella immersa)":20,
            "escharoides coccinea (escharoides coccinea)":20,
            "esperiopsis fucorum (esperiopsis fucorum)":20,
            "eteone longa (eteone longa)":20,
            "eudendrium capillare (eudendrium capillare)":20,
            "eudesme virescens (eudesme virescens)":20,
            "eulimnogammarus obtusatus (eulimnogammarus obtusatus)":20,
            "eumida sanguinea (eumida sanguinea)":20,
            "eunicella verrucosa (eunicella verrucosa)":20,
            "eupolymnia nebulosa (eupolymnia nebulosa)":10,
            "european bass (dicentrarchus labrax)":20,
            "european eel (anguilla anguilla)":7,
            "european flat oyster (ostrea edulis)":4,
            "european lobster (homarus gammarus)":7,
            "european spiny lobster (palinurus elephas)":20,
            "european sting winkle (ocenebra erinacea)":2,
            "eurydice pulchra (eurydice pulchra)":20,
            "exogone hebes (exogone hebes)":20,
            "exogone naidina (exogone naidina)":20,
            "fabricia sabella (fabricia sabella)":20,
            "fabulina fabula (fabulina fabula)":20,
            "facelina auriculata (facelina auriculata)":6,
            "false eyelash weed (calliblepharis jubata)":5,
            "false irish moss (mastocarpus stellatus)":3,
            "feather hydroid (kirchenpaueria halecioides)":10,
            "fifteen spined stickleback (spinachia spinachia)":10,
            "filograna implexa (filograna implexa)":20,
            "fine veined crinkle weed (cryptopleura ramosa)":8,
            "five bearded rockling (ciliata mustela)":2,
            "flabellina pedata (flabellina pedata)":20,
            "flat periwinkle (littorina obtusata_or_fabalis)":1,
            "fluffy white sea slug (acanthodoris pilosa)":20,
            "flustra foliacea (flustra foliacea)":20,
            "flustrellidra hispida (flustrellidra hispida)":6,
            "fucus ceranoides (fucus ceranoides)":6,
            "fucus distichus (fucus distichus)":20,
            "fucus vesiculosus var. linearis (fucus vesiculosus var. linearis)":10,
            "fulmar (fulmarus glacialis)":20,
            "furbellow (saccorhiza polyschides)":3,
            "furcellaria lumbricalis (furcellaria lumbricalis)":8,
            "furry purse sponge (sycon ciliatum)":7,
            "gammarellus homari (gammarellus homari)":20,
            "gammarus zaddachi (gammarus zaddachi)":20,
            "gastroclonium ovatum (gastroclonium ovatum)":10,
            "gelidium crinale (gelidium crinale)":20,
            "gelidium latifolium (gelidium latifolium)":20,
            "gelidium pulchellum (gelidium pulchellum)":20,
            "gelidium pusillum (gelidium pusillum)":20,
            "gelidium spinosum (gelidium spinosum)":8,
            "gem anemone (aulactinia verrucosa)":2,
            "giant goby (gobius cobitis)":7,
            "gibbula pennanti (gibbula pennanti)":10,
            "gigartina pistillata (gigartina pistillata)":10,
            "ginger anemone (isozoanthus sulcatus)":20,
            "glaucus pimplet (anthopleura thallia)":7,
            "glycera tridactyla (glycera tridactyla)":20,
            "gobiusculus flavescens (gobiusculus flavescens)":10,
            "goggle eyed prawn (eualus cranchii)":10,
            "goniodoris nodosa (goniodoris nodosa)":10,
            "gracilaria gracilis (gracilaria gracilis)":10,
            "grateloupia filicina (grateloupia filicina)":20,
            "grateloupia turuturu (grateloupia turuturu)":20,
            "great spider crab (hyas araneus)":20,
            "greater pipefish (syngnathus acus)":6,
            "green blisters (rivularia bullata)":4,
            "green leaf worm (eulalia viridis)":2,
            "green paddleworm (phyllodoce groenlandica)":8,
            "green sea urchin (psammechinus miliaris)":2,
            "green sponge fingers (codium fragile)":5,
            "grey seal (halichoerus grypus)":10,
            "grey top shell (gibbula cineraria)":1,
            "griffithsia corallinoides (griffithsia corallinoides)":20,
            "groovy crab (xaiva biguttata)":20,
            "guiryi's wrack (fucus guiryi)":10,
            "gut weed (ulva intestinalis)":2,
            "gymnangium montagui (gymnangium montagui)":20,
            "gymnogongrus crenulatus (gymnogongrus crenulatus)":20,
            "hairy crab (pilumnus hirtellus)":5,
            "halarachnion ligulatum (halarachnion ligulatum)":20,
            "halecium halecinum (halecium halecinum)":20,
            "halichondria bowerbanki (halichondria bowerbanki)":20,
            "haliclona cinerea (haliclona cinerea)":20,
            "haliclona oculata (haliclona oculata)":20,
            "haliclona rosea (haliclona rosea)":20,
            "haliclona simulans (haliclona simulans)":20,
            "haliclona viscosa (haliclona viscosa)":20,
            "haliclystus auricula (haliclystus auricula)":20,
            "halidrys siliquosa (halidrys siliquosa)":8,
            "haliotis tuberculata (haliotis tuberculata)":20,
            "halisarca dujardini (halisarca dujardini)":10,
            "halisarca dujardinii (halisarca dujardinii)":8,
            "halopteris catharina (halopteris catharina)":20,
            "halopteris filicina (halopteris filicina)":20,
            "halurus equisetifolius (halurus equisetifolius)":20,
            "halurus flosculosus (halurus flosculosus)":20,
            "haraldiophyllum bonnemaisonii (haraldiophyllum bonnemaisonii)":20,
            "harbour crab (liocarcinus depurator)":6,
            "harmothoe extenuata (harmothoe extenuata)":20,
            "harmothoe imbricata (harmothoe imbricata)":20,
            "harpoon weed (asparagopsis armata)":4,
            "helcion pellucidum (helcion pellucidum)":20,
            "hemimycale columella (hemimycale columella)":20,
            "henricia oculata (henricia oculata)":20,
            "henricia sanguinolenta (henricia sanguinolenta)":20,
            "heteranomia squamula (heteranomia squamula)":20,
            "heterochaeta costata (heterochaeta costata)":20,
            "heterosiphonia plumosa (heterosiphonia plumosa)":20,
            "hiatella arctica (hiatella arctica)":20,
            "hildenbrandia rubra (hildenbrandia rubra)":8,
            "hincksia granulosa (hincksia granulosa)":20,
            "holothuria forskali (holothuria forskali)":20,
            "honeycomb reef worm (sabellaria alveolata)":2,
            "hooded prawn (athanas nitescens)":5,
            "hyale prevostii (hyale prevostii)":20,
            "hyale stebbingi (hyale stebbingi)":20,
            "hydractinia echinata (hydractinia echinata)":20,
            "hydrallmania falcata (hydrallmania falcata)":20,
            "hydrobia ulvae (hydrobia ulvae)":20,
            "hymeniacidon perleve (hymeniacidon perleve)":7,
            "hymeniacidon perlevis (hymeniacidon perlevis)":4,
            "hymeniacidon sanguinea (hymeniacidon sanguinea)":20,
            "hypoglossum hypoglossoides (hypoglossum hypoglossoides)":20,
            "irish moss (chondrus crispus)":2,
            "jaera albifrons (jaera albifrons)":20,
            "jania rubens (jania rubens)":5,
            "janira maculosa (janira maculosa)":7,
            "janolus cristatus (janolus cristatus)":20,
            "janua pagenstecheri (janua pagenstecheri)":10,
            "jasmineira elegans (jasmineira elegans)":20,
            "jassa falcata (jassa falcata)":8,
            "jerky hopper (echinogammarus marinus)":6,
            "kallymenia reniformis (kallymenia reniformis)":20,
            "keel worm (pomatoceros triqueter)":1,
            "kefersteinia cirrata (kefersteinia cirrata)":20,
            "kellia suborbicularis (kellia suborbicularis)":20,
            "kelp (laminariales)":3,
            "kelp fur (obelia geniculata)":10,
            "kidney scale worm (harmothoe impar)":4,
            "kirchenpaueria pinnata (kirchenpaueria pinnata)":20,
            "ladder ascidian (botrylloides leachii)":3,
            "laeospira corallinae (laeospira corallinae)":20,
            "lamellaria perspicua (lamellaria perspicua)":8,
            "laminaria ochroleuca (laminaria ochroleuca)":20,
            "laminaria saccharina (laminaria saccharina)":10,
            "laomedea flexuosa (laomedea flexuosa)":20,
            "lasaea adansoni (lasaea adansoni)":20,
            "leach's spider crab (inachus phalangium)":20,
            "leathesia difformis (leathesia difformis)":10,
            "leathesia marina (leathesia marina)":6,
            "lepidonotus clava (lepidonotus clava)":5,
            "lepidonotus squamatus (lepidonotus squamatus)":20,
            "leptasterias muelleri (leptasterias muelleri)":20,
            "leptochiton asellus (leptochiton asellus)":20,
            "leptoplana tremellaris (leptoplana tremellaris)":4,
            "leuconia nivea (leuconia nivea)":20,
            "leucosolenia botryoides (leucosolenia botryoides)":20,
            "leucosolenia complicata (leucosolenia complicata)":20,
            "lichina pygmaea (lichina pygmaea)":7,
            "light bulb sea squirt (clavelina lepadiformis)":4,
            "ligia oceanica (ligia oceanica)":10,
            "limacia clavigera (limacia clavigera)":5,
            "limapontia capitata (limapontia capitata)":20,
            "lineus ruber (lineus ruber)":20,
            "liocarcinus arcuatus (liocarcinus arcuatus)":20,
            "lissoclinum perforatum (lissoclinum perforatum)":6,
            "lithophyllum incrustans (lithophyllum incrustans)":3,
            "lithothamnion glaciale (lithothamnion glaciale)":8,
            "little egret (egretta garzetta)":20,
            "littorina fabalis (littorina fabalis)":20,
            "littorina mariae (littorina mariae)":8,
            "littorina nigrolineata (littorina nigrolineata)":20,
            "littorina obtusata (littorina obtusata)":5,
            "littorina saxatilis var. rudis (littorina saxatilis var. rudis)":20,
            "lomentaria clavellosa (lomentaria clavellosa)":10,
            "lomentaria orcadensis (lomentaria orcadensis)":20,
            "long clawed porcelain crab (pisidia longicornis)":2,
            "long legged spider crab (macropodia rostrata)":4,
            "lucernariopsis campanulata (lucernariopsis campanulata)":20,
            "lucernariopsis cruxmelitensis (lucernariopsis cruxmelitensis)":10,
            "luidia ciliaris (luidia ciliaris)":20,
            "lysianassa ceratina (lysianassa ceratina)":20,
            "macoma balthica (macoma balthica)":10,
            "mactra stultorum (mactra stultorum)":20,
            "malacoceros fuliginosus (malacoceros fuliginosus)":20,
            "manayunkia aestuarina (manayunkia aestuarina)":20,
            "many ribbed jelly (aequorea forskalea)":4,
            "manzonia crassa (manzonia crassa)":20,
            "marbled swimming crab (liocarcinus marmoreus)":10,
            "margarites helicinus (margarites helicinus)":20,
            "marine springtail (anurida maritima)":5,
            "mediomastus fragilis (mediomastus fragilis)":20,
            "melinna palmata (melinna palmata)":20,
            "melita palmata (melita palmata)":10,
            "membranoptera alata (membranoptera alata)":20,
            "meredithia microphylla (meredithia microphylla)":20,
            "mesophyllum lichenoides (mesophyllum lichenoides)":5,
            "metridium senile (metridium senile)":20,
            "microciona atrasanguinea (microciona atrasanguinea)":20,
            "modiolarca tumida (modiolarca tumida)":20,
            "modiolus modiolus (modiolus modiolus)":20,
            "molgula manhattensis (molgula manhattensis)":20,
            "monostroma grevillei (monostroma grevillei)":20,
            "montagu's blenny (coryphoblennius galerita)":2,
            "montagu's crab (xantho hydrophilus)":1,
            "montagu's sea snail (liparis montagui)":7,
            "montagu's stellate barnacle (chthamalus montagui)":1,
            "moon jelly (aurelia aurita)":5,
            "morchellium argus (morchellium argus)":4,
            "mud sagartia (sagartia troglodytes)":20,
            "musculus discors (musculus discors)":20,
            "mya arenaria (mya arenaria)":20,
            "mya truncata (mya truncata)":20,
            "mysella bidentata (mysella bidentata)":20,
            "myxicola infundibulum (myxicola infundibulum)":20,
            "myxilla incrustans (myxilla incrustans)":20,
            "nassarius incrassatus (nassarius incrassatus)":20,
            "nassarius reticulatus (nassarius reticulatus)":20,
            "nemalion helminthoides (nemalion helminthoides)":20,
            "nemertesia antennina (nemertesia antennina)":20,
            "nemertesia ramosa (nemertesia ramosa)":20,
            "neoamphitrite figulus (neoamphitrite figulus)":20,
            "neopentadactyla mixta (neopentadactyla mixta)":20,
            "neosiphonia harveyi (neosiphonia harveyi)":20,
            "nephasoma minutum (nephasoma minutum)":20,
            "nephtys cirrosa (nephtys cirrosa)":20,
            "nephtys hombergii (nephtys hombergii)":20,
            "nereis pelagica (nereis pelagica)":20,
            "netted dog whelk (tritia reticulata)":2,
            "new zealand barnacle (austrominius modestus)":3,
            "nitophyllum punctatum (nitophyllum punctatum)":10,
            "northern green sea urchin (strongylocentrotus droebachiensis)":20,
            "northern lacuna (lacuna vincta)":10,
            "northern rock barnacle (semibalanus balanoides)":3,
            "norway lobster (nephrops norvegicus)":20,
            "notched isopod (idotea emarginata)":8,
            "notomastus latericeus (notomastus latericeus)":20,
            "nucula nucleus (nucula nucleus)":20,
            "nursehound (scyliorhinus stellaris)":5,
            "nymphon gracile (nymphon gracile)":5,
            "oarweed (laminaria digitata)":2,
            "odonthalia dentata (odonthalia dentata)":20,
            "odontosyllis ctenostoma (odontosyllis ctenostoma)":20,
            "odontosyllis gibba (odontosyllis gibba)":20,
            "odostomia plicata (odostomia plicata)":20,
            "odostomia turrita (odostomia turrita)":20,
            "okamura's pom pom weed (caulacanthus okamurae)":5,
            "omalogyra atomus (omalogyra atomus)":20,
            "onchidella celtica (onchidella celtica)":10,
            "onchidoris muricata (onchidoris muricata)":20,
            "onoba aculeus (onoba aculeus)":20,
            "onoba semicostata (onoba semicostata)":20,
            "ophiocomina nigra (ophiocomina nigra)":8,
            "ophiopholis aculeata (ophiopholis aculeata)":10,
            "ophiura albida (ophiura albida)":20,
            "ophiura ophiura (ophiura ophiura)":20,
            "ophlitaspongia papilla (ophlitaspongia papilla)":20,
            "ophlitaspongia seriata (ophlitaspongia seriata)":20,
            "orange striped green sea anemone (diadumene lineata)":20,
            "orange anemone (diadumene cincta)":20,
            "osmundea hybrida (osmundea hybrida)":10,
            "osmundea osmunda (osmundea osmunda)":20,
            "osmundea truncata (osmundea truncata)":20,
            "owenia fusiformis (owenia fusiformis)":20,
            "oyster thief (colpomenia peregrina)":2,
            "oystercatcher (haematopus ostralegus)":20,
            "pachymatisma johnstonia (pachymatisma johnstonia)":20,
            "pacific oyster (magallana gigas)":2,
            "painted top shell (calliostoma zizyphinum)":1,
            "pale lacuna (lacuna pallidula)":20,
            "paracentrotus lividus (paracentrotus lividus)":20,
            "parajassa pelagica (parajassa pelagica)":20,
            "paraonis fulgens (paraonis fulgens)":20,
            "parasmittina trispinosa (parasmittina trispinosa)":20,
            "partulida pellucida (partulida pellucida)":20,
            "pecten maximus (pecten maximus)":8,
            "pentapora foliacea (pentapora foliacea)":20,
            "pepper dulse (osmundea pinnatifida)":2,
            "perophora listeri (perophora listeri)":20,
            "petalonia fascia (petalonia fascia)":20,
            "phaeostachys spinifera (phaeostachys spinifera)":20,
            "pheasant shell (tricolia pullus)":8,
            "pholas dactylus (pholas dactylus)":8,
            "pholoe inornata (pholoe inornata)":20,
            "pholoe synophthalmica (pholoe synophthalmica)":20,
            "phoronis hippocrepia (phoronis hippocrepia)":20,
            "phyllophora crispa (phyllophora crispa)":20,
            "phyllophora pseudoceranoides (phyllophora pseudoceranoides)":20,
            "phyllophora sicula (phyllophora sicula)":20,
            "phymatolithon calcareum (phymatolithon calcareum)":8,
            "phymatolithon lenormandii (phymatolithon lenormandii)":7,
            "phymatolithon purpureum (phymatolithon purpureum)":20,
            "pilayella littoralis (pilayella littoralis)":20,
            "pilinia rimosa (pilinia rimosa)":20,
            "pink mitten amphipod (maera grossimana)":5,
            "plaice (pleuronectes platessa)":20,
            "platynereis dumerilii (platynereis dumerilii)":20,
            "plocamium cartilagineum (plocamium cartilagineum)":20,
            "plumaria plumosa (plumaria plumosa)":20,
            "plumularia setacea (plumularia setacea)":10,
            "pododesmus patelliformis (pododesmus patelliformis)":20,
            "poli's stellate barnacle (chthamalus stellatus)":2,
            "pollachius pollachius (pollachius pollachius)":20,
            "pollicipes pollicipes (pollicipes pollicipes)":20,
            "polycarpa scuba (polycarpa scuba)":20,
            "polycera faeroensis (polycera faeroensis)":20,
            "polycera quadrilineata (polycera quadrilineata)":20,
            "polyclinum aurantium (polyclinum aurantium)":20,
            "polydora ciliata (polydora ciliata)":20,
            "polyides rotunda (polyides rotunda)":7,
            "polyides rotundus (polyides rotundus)":10,
            "polymastia boletiformis (polymastia boletiformis)":20,
            "polymastia mamillaris (polymastia mamillaris)":20,
            "polymastia penicillus (polymastia penicillus)":20,
            "polyneura bonnemaisonii (polyneura bonnemaisonii)":20,
            "polysiphonia atlantica (polysiphonia atlantica)":20,
            "polysiphonia brodiei (polysiphonia brodiei)":20,
            "polysiphonia elongata (polysiphonia elongata)":20,
            "polysiphonia fucoides (polysiphonia fucoides)":20,
            "polysiphonia lanosa (polysiphonia lanosa)":8,
            "polysiphonia nigra (polysiphonia nigra)":20,
            "polysiphonia nigrescens (polysiphonia nigrescens)":20,
            "polysiphonia stricta (polysiphonia stricta)":20,
            "pomatoceros lamarcki (pomatoceros lamarcki)":20,
            "pomatoschistus minutus (pomatoschistus minutus)":20,
            "pomatoschistus pictus (pomatoschistus pictus)":20,
            "pontocrates arenarius (pontocrates arenarius)":20,
            "porania pulvillus (porania pulvillus)":20,
            "porphyra linearis (porphyra linearis)":20,
            "porphyra purpurea (porphyra purpurea)":20,
            "porphyra umbilicalis (porphyra umbilicalis)":10,
            "portuguese man of war physalia physalis)":10,
            "prasiola stipitata (prasiola stipitata)":20,
            "protodorvillea kefersteini (protodorvillea kefersteini)":20,
            "protula tubularia (protula tubularia)":20,
            "psamathe fusca (psamathe fusca)":20,
            "pseudendoclonium submarinum (pseudendoclonium submarinum)":20,
            "pseudosuberites fallax (pseudosuberites fallax)":20,
            "pterocladia capillacea (pterocladia capillacea)":20,
            "pterosiphonia complanata (pterosiphonia complanata)":20,
            "pterosiphonia parasitica (pterosiphonia parasitica)":20,
            "pterothamnion plumula (pterothamnion plumula)":10,
            "ptilota gunneri (ptilota gunneri)":20,
            "purple top shell (gibbula umbilicalis)":1,
            "purse sponge (grantia compressa)":6,
            "pycnogonum littorale (pycnogonum littorale)":20,
            "pygospio elegans (pygospio elegans)":20,
            "pyrenocollema halodytes (pyrenocollema halodytes)":20,
            "ragged hydroid (coryne pusilla)":10,
            "ragworm (perinereis cultrifera)":4,
            "rainbow wrack (cystoseira tamariscifolia)":2,
            "ralfsia verrucosa (ralfsia verrucosa)":20,
            "raspailia hispida (raspailia hispida)":20,
            "raspailia ramosa (raspailia ramosa)":20,
            "rayed artemis (dosinia exoleta)":5,
            "red doris (rostanga rubra)":7,
            "red rags (dilsea carnosa)":3,
            "red ripple bryozoan (watersipora subatra)":2,
            "red sea oak (phycodrys rubens)":10,
            "red speckled anemone (anthopleura ballii)":5,
            "retusa truncatula (retusa truncatula)":20,
            "rhizoclonium riparium (rhizoclonium riparium)":20,
            "rhizoclonium tortuosum (rhizoclonium tortuosum)":20,
            "rhodochorton purpureum (rhodochorton purpureum)":20,
            "rhodomela confervoides (rhodomela confervoides)":20,
            "rhodomela lycopodioides (rhodomela lycopodioides)":20,
            "rhodophyllis divaricata (rhodophyllis divaricata)":20,
            "rhodothamniella floridula (rhodothamniella floridula)":4,
            "rhodymenia delicatula (rhodymenia delicatula)":20,
            "rhodymenia holmesii (rhodymenia holmesii)":20,
            "rhodymenia pseudopalmata (rhodymenia pseudopalmata)":20,
            "risso's crab (xantho pilipes)":1,
            "rissoa interrupta (rissoa interrupta)":20,
            "rissoa parva (rissoa parva)":6,
            "rissoella diaphana (rissoella diaphana)":20,
            "rock cook (centrolabrus exoletus)":20,
            "rock goby (gobius paganellus)":2,
            "rock pool shrimp (palaemon elegans)":1,
            "root arm medusa (cladonema radiatum)":10,
            "rosy feather star (antedon bifida)":6,
            "rough periwinkle (littorina neglecta)":5,
            "rough periwinkle (littorina saxatilis)":2,
            "rugose squat lobster (munida rugosa)":20,
            "runcina coronata (runcina coronata)":20,
            "rush clawed shore crab (hemigrapsus takanoi)":20,
            "sabella pavonina (sabella pavonina)":6,
            "sabellaria spinulosa (sabellaria spinulosa)":8,
            "saccharina latissima (saccharina latissima)":4,
            "salmacina dysteri (salmacina dysteri)":20,
            "sand hopper (gammarus locusta)":4,
            "sand mason (lanice conchilega)":3,
            "sand smelt (atherina presbyter)":7,
            "sandalled anemone (actinothoe sphyrodeta)":10,
            "saw wrack (fucus serratus)":1,
            "scarlet and gold star coral (balanophyllia regia)":10,
            "schizomavella linearis (schizomavella linearis)":20,
            "schizymenia dubyi (schizymenia dubyi)":20,
            "schottera nicaeensis (schottera nicaeensis)":20,
            "scolelepis squamata (scolelepis squamata)":20,
            "scoloplos armiger (scoloplos armiger)":20,
            "scrobicularia plana (scrobicularia plana)":20,
            "scruparia chelata (scruparia chelata)":20,
            "scrupocellaria reptans (scrupocellaria reptans)":20,
            "scrupocellaria scruposa (scrupocellaria scruposa)":20,
            "scypha ciliata (scypha ciliata)":20,
            "scytosiphon lomentaria (scytosiphon lomentaria)":8,
            "sea gherkin (pawsonia saxicola)":4,
            "sea hare (aplysia punctata)":4,
            "sea lemon (doris pseudoargus)":3,
            "sea lettuce (ulva lactuca)":1,
            "sea mat (membranipora membranacea)":2,
            "sea orange sponge (suberites ficus)":5,
            "sea scorpion (taurulus bubalis)":3,
            "securiflustra securifrons (securiflustra securifrons)":20,
            "sepia officinalis (sepia officinalis)":10,
            "sertularella gaudichaudi (sertularella gaudichaudi)":20,
            "sertularella polyzonias (sertularella polyzonias)":20,
            "sertularia argentea (sertularia argentea)":20,
            "sertularia cupressina (sertularia cupressina)":20,
            "seven spot ladybird (coccinella septempunctata)":8,
            "shanny (lipophrys pholis)":1,
            "shore clingfish (lepadogaster lepadogaster)":3,
            "shore crab (carcinus maenas)":1,
            "shore rockling (gaidropsarus mediterraneus)":3,
            "sideways sea squirt (ascidia mentula)":6,
            "sidnyum elegans (sidnyum elegans)":20,
            "sidnyum turbinatum (sidnyum turbinatum)":20,
            "single horn bryozoan (schizoporella unicornis)":3,
            "skeneopsis planorbis (skeneopsis planorbis)":20,
            "small headed clingfish (apletodon dentatus)":8,
            "small spotted catshark (scyliorhinus canicula)":7,
            "small cushion star (asterina phylactica)":4,
            "small periwinkle (melarhaphe neritoides)":4,
            "small snakelocks anemone (sagartiogeton undatus)":8,
            "snakelocks anemone (anemonia viridis)":1,
            "snapping prawn (alpheus macrocheles)":10,
            "solaster endeca (solaster endeca)":20,
            "soliers red string weed (solieria chordalis)":10,
            "spermothamnion repens (spermothamnion repens)":20,
            "sphacelaria cirrosa (sphacelaria cirrosa)":20,
            "sphaerococcus coronopifolius (sphaerococcus coronopifolius)":20,
            "sphaeroma rugicauda (sphaeroma rugicauda)":20,
            "sphenia binghami (sphenia binghami)":20,
            "sphondylothamnion multifidum (sphondylothamnion multifidum)":20,
            "spiky lace sponge (leucosolenia spp.)":20,
            "spiny squat lobster (galathea strigosa)":20,
            "spiny starfish (marthasterias glacialis)":4,
            "spio filicornis (spio filicornis)":20,
            "spio martinensis (spio martinensis)":20,
            "spiophanes bombyx (spiophanes bombyx)":20,
            "spiral wrack (fucus spiralis)":3,
            "spirobranchus triqueter (spirobranchus triqueter)":10,
            "spirorbis corallinae (spirorbis corallinae)":20,
            "spirorbis rupestris (spirorbis rupestris)":20,
            "spirorbis spirorbis (spirorbis spirorbis)":5,
            "spongomorpha aeruginosa (spongomorpha aeruginosa)":20,
            "spongomorpha arcta (spongomorpha arcta)":20,
            "spongonema tomentosum (spongonema tomentosum)":20,
            "spotted cowrie (trivia monacha)":5,
            "spotted kaleidoscope jellyfish (haliclystus octoradiatus)":10,
            "st piran's hermit crab (clibanarius erythropus)":2,
            "star ascidian (botryllus schlosseri)":1,
            "starry sea lemon (geitodoris planata)":7,
            "stelligera rigida (stelligera rigida)":20,
            "stelligera stuposa (stelligera stuposa)":20,
            "stenothoe monoculoides (stenothoe monoculoides)":20,
            "sthenelais boa (sthenelais boa)":10,
            "stolonica socialis (stolonica socialis)":20,
            "strawberry anemone (actinia fragacea)":1,
            "strawberry sea squirt (aplidium elegans)":8,
            "streblospio shrubsolii (streblospio shrubsolii)":20,
            "styela clava (styela clava)":10,
            "stypocaulon scoparia (stypocaulon scoparia)":10,
            "suberites carnosus (suberites carnosus)":20,
            "syllidia armata (syllidia armata)":20,
            "syllis gracilis (syllis gracilis)":20,
            "taonia atomaria (taonia atomaria)":20,
            "terebella lapidaria (terebella lapidaria)":10,
            "terpios fugax (terpios fugax)":20,
            "testudinalia testudinalis (testudinalia testudinalis)":20,
            "tethya aurantium (tethya aurantium)":20,
            "tethya citrina (tethya citrina)":20,
            "tharyx killariensis (tharyx killariensis)":20,
            "thick lipped dog whelk (hinia incrassata)":3,
            "thick trough shell (spisula solida)":10,
            "thong weed (himanthalia elongata)":2,
            "thorogobius ephippiatus (thorogobius ephippiatus)":20,
            "tiny lacuna (lacuna parva)":20,
            "tompot blenny (parablennius gattorugine)":5,
            "tonicella rubra (tonicella rubra)":10,
            "toothed top shell (phorcus lineatus)":1,
            "topknot (zeugopterus punctatus)":8,
            "trailliella intricata (trailliella intricata)":20,
            "trididemnum cereum (trididemnum cereum)":20,
            "trisopterus luscus (trisopterus luscus)":20,
            "tritonia lineata (tritonia lineata)":20,
            "trumpet anemone (aiptasia mutabilis)":20,
            "tubificoides amplivasatus (tubificoides amplivasatus)":20,
            "tubificoides benedii (tubificoides benedii)":20,
            "tubificoides pseudogaster (tubificoides pseudogaster)":20,
            "tubularia indivisa (tubularia indivisa)":20,
            "tubularia larynx (tubularia larynx)":20,
            "turban top shell (gibbula magus)":3,
            "turbonilla lactea (turbonilla lactea)":20,
            "turritella communis (turritella communis)":20,
            "turtonia minuta (turtonia minuta)":20,
            "ulothrix flacca (ulothrix flacca)":20,
            "ulva compressa (ulva compressa)":20,
            "ulva prolifera (ulva prolifera)":10,
            "ulva pseudocurvata (ulva pseudocurvata)":20,
            "umbonula littoralis (umbonula littoralis)":20,
            "undaria pinnatifida (undaria pinnatifida)":20,
            "variegated scallop (chlamys varia)":3,
            "variegated scallop (mimachlamys varia)":4,
            "velvet swimming crab (necora puber)":1,
            "venerupis corrugata (venerupis corrugata)":6,
            "venerupis senegalensis (venerupis senegalensis)":10,
            "verrucaria maura (verrucaria maura)":6,
            "verrucaria mucosa (verrucaria mucosa)":20,
            "vertebrata lanosa (vertebrata lanosa)":6,
            "virgularia mirabilis (virgularia mirabilis)":20,
            "volcano barnacle (perforatus perforatus)":1,
            "walkeria uva (walkeria uva)":20,
            "wart barnacle (verruca stroemia)":4,
            "warty sea slug (palio nothus)":10,
            "websterinereis glauca (websterinereis glauca)":20,
            "werthers original sea squirt (corella eumyota)":4,
            "white tortoiseshell limpet (tectura virginea)":5,
            "whiting (merlangius merlangus)":20,
            "wireweed (sargassum muticum)":2,
            "worm pipefish (nerophis lumbriciformis)":1,
            "yellow plumed sea slug (berthella plumula)":2,
            "yellow sea squirt (ciona intestinalis)":8,
        }
        # Define initial teams dictionary
        self.teams = {}
        self.lock = Lock()
        self.load_data()

    def load_data(self):
        data_file_path = os.path.join(data_path, "static", "data.json")
        if os.path.exists(data_file_path):
            with open(data_file_path, "r") as f:
                fcntl.flock(f, fcntl.LOCK_EX)
                self.teams = json.load(f)
                fcntl.flock(f, fcntl.LOCK_UN)

    def save_data(self):
        data_file_path = os.path.join(data_path, "static", "data.json")
        with open(data_file_path, "w") as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            json.dump(self.teams, f)
            fcntl.flock(f, fcntl.LOCK_UN)


    def get_creature_score(self, creature_name):
        # Return the score for a given creature
        return self.creature_scores.get(creature_name.lower(), 0)

    def add_team(self, team_name):
        # Check if the team name is JSON-friendly
        try:
            json.dumps({"team_name": team_name})
        except:
            raise ValueError("Team name is not JSON-friendly")

        # Add a new team to the game
        team_name_lower = team_name.lower()
        if team_name_lower not in self.teams:
            # if the team doesn't already exist
            self.teams[team_name_lower] = {"score": 0, "creatures": []}

        # Prepare a message to send to clients with updated team scores and creatures found
        creatures = self.teams[team_name_lower]["creatures"]
        data = {"action": "update_team_scores", "teams": self.teams, "creatures": creatures}
        message = json.dumps(data)
        return message

    def submit_creature(self, team_name, creature_name):
        self.load_data()
        # Add a creature to a team and update the team's score
        creature_name = unquote(creature_name.lower())
        print(team_name + ":" + creature_name)
        creature_score = self.get_creature_score(creature_name)
        with self.lock:
            if team_name.lower() in self.teams:
                if creature_name.lower() not in self.teams[team_name.lower()]["creatures"]:
                    self.teams[team_name.lower()]["score"] = int(self.teams[team_name.lower()]["score"]) + creature_score
                    self.teams[team_name.lower()]["creatures"].append(creature_name.lower())
            else:
                self.add_team(team_name.lower())
                self.teams[team_name.lower()]["score"] += creature_score
                self.teams[team_name.lower()]["creatures"].append(creature_name.lower())

            # Prepare a message to send to clients with updated team scores
            self.save_data()
            creatures = self.teams[team_name.lower()]["creatures"]
            data = {"action": "update_team_scores", "teams": self.teams, "creatures": creatures}
            message = json.dumps(data)
        return message

    def get_team_scores(self):
        # Prepare a message to send to clients with updated team scores
        capitalized_teams = {team_name.capitalize(): data for team_name, data in self.teams.items()}
        data = {"action": "update_team_scores", "teams": capitalized_teams}
        message = json.dumps(data)
        return message

class GameWebSocket(WebSocket):
    websockets = [] # list to store all WebSocket connections

    def __init__(self, websocket: WebSocket, receive: Callable, send: Callable):
        super().__init__(websocket, receive=receive, send=send)
        self.teams = {} # dictionary to store teams and their creatures
        self.game = Game() # initialize the game
        self.application_state = WebSocketState.CONNECTED

        # Open the connection immediately
        asyncio.ensure_future(self.on_connect())

    async def on_connect(self):
        # Add the current instance to the list of websockets.
        self.websockets.append(self)

        # Broadcast the team list and scores to the new client.
        await self.broadcast_team_list()
        await self.broadcast_team_scores()

    async def on_receive(self, message: str):
        # Handle a message from the client.
        data = json.loads(message)
        action = data.get("action")

        if action == "create_team":
            team_name = data.get("team_name")
            if team_name is not None:
                self.game.add_team(team_name)
                await self.broadcast_team_list()

        elif action == "submit_creature":
            team_name = data.get("team_name")
            creature_name = data.get("creature_name")
            if team_name is not None and creature_name is not None:
                self.game.submit_creature(team_name, creature_name)
                await self.broadcast_team_scores()

    async def broadcast_team_list(self):
        # Send the team list to all clients.
        team_list = [team_name for team_name in self.game.teams]
        data = {"action": "update_team_list", "team_list": team_list}
        message = json.dumps(data)
        tasks = []
        for websocket in self.websockets:
            if websocket.application_state == WebSocketState.CONNECTED:
                try:
                    tasks.append(websocket.send_text(message))
                except:
                    self.websockets.remove(websocket)
        try:
            await asyncio.gather(*tasks)
        except:
            pass

    async def broadcast_team_scores(self):
        # Send the team scores to all clients.
        message = self.game.get_team_scores()
        tasks = []
        for websocket in self.websockets:
            if websocket.application_state == WebSocketState.CONNECTED:
                try:
                    await websocket.send_text(message)
                except:
                    self.websockets.remove(websocket)
        await asyncio.gather(*tasks)

    async def on_disconnect(self, close_code: int):
        if self in self.websockets:
            self.websockets.remove(self)


@app.websocket("/game")
async def game(websocket: WebSocket):
    await websocket.accept() # accept the WebSocket connection
    game_websocket = GameWebSocket(
        websocket, receive=websocket.receive, send=websocket.send
    )
    await game_websocket.on_connect()

    try:
        while True:
            data = await websocket.receive_text() # wait for data to receive from the WebSocket client
            await game_websocket.on_receive(data) # handle the data received
    except WebSocketDisconnect:
        await game_websocket.on_disconnect(1000) # handle the WebSocket disconnection


@app.get("/")
async def read_index():
    file_path = f"{home_dir}/BioBlitz/bioblitz-game/static/index.html"
    return FileResponse(file_path)

@app.get("/admin")
async def read_admin():
    file_path = f"{home_dir}/BioBlitz/bioblitz-game/static/admin.html"
    return FileResponse(file_path)

@app.put("/data.json")
async def update_data(data: dict):
    data_file_path = f"{home_dir}/BioBlitz/bioblitz-game/static/data.json"
    with open(data_file_path, "w") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        json.dump(data, f, indent=2)
        fcntl.flock(f, fcntl.LOCK_UN)
    return {"message": "Data updated successfully"}

@app.post('/move_file')
async def move_file(request: Request):
    data = await request.json()
    # Create the destination folder if it doesn't exist
    os.makedirs(past_games_path, exist_ok=True)

    # Generate a new name for the file if it already exists in the destination folder
    count = 1
    new_name = None
    if len(os.listdir(past_games_path)) == 0:
        new_name = '1.json'
    elif os.path.exists(os.path.join(past_games_path, '1.json')):
        count += 1
        new_name = f'{count}.json'
    else:
        while True:
            new_path = os.path.join(past_games_path, os.path.basename(data_file_path))
            if new_name:
                new_path = os.path.join(past_games_path, new_name)
            if not os.path.exists(new_path):
                break
            count += 1
            new_name = f'{count}.json'

    # Move the file to the destination folder
    os.rename(data_file_path, os.path.join(past_games_path, new_name))
    Game._instance = None
    Game.teams = {}
    return {'new_name': new_name}

if __name__ == "__main__":
    uvicorn.run(app, host="192.168.4.1", port=8000) # run the app on 192.168.4.1:8000 using uvicorn server (opens with splines captive portal)
