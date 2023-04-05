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
            "a hydroid":3,
            "a keel worm":3,
            "a mysid shrimp":10,
            "a pill isopod":5,
            "a sea slater":5,
            "a sea squirt":10,
            "a spoon worm":10,
            "a stalked jellyfish":6,
            "a tube anemone":20,
            "a velutinid":10,
            "abietinaria abietina":20,
            "abra alba":20,
            "acanthocardia echinata":20,
            "acanthochitona crinitus":6,
            "achelia echinata":20,
            "acrosorium venulosum":20,
            "adamsia carciniopados":20,
            "aeolidia papillosa":3,
            "aequipecten opercularis":8,
            "aglaophenia pluma":20,
            "aglaothamnion hookeri":20,
            "aglaothamnion sepositum":20,
            "aglaozonia asexual cutleria":20,
            "ahnfeltia plicata":20,
            "alaria esculenta":20,
            "alcyonidioides mytili":20,
            "alcyonidium diaphanum":20,
            "alcyonidium gelatinosum":20,
            "alcyonidium hirsutum":10,
            "alcyonidium mytili":20,
            "alcyonium digitatum":20,
            "alcyonium glomeratum":20,
            "alentia gelatinosa":3,
            "alvania semistriata":20,
            "amathia lendigera":20,
            "american sting winkle":8,
            "ammodytes tobianus":20,
            "ampelisca brevicornis":20,
            "ampharete grubei":20,
            "ampharete lindstroemi":20,
            "amphilectus fucorum":20,
            "amphisbetia operculata":20,
            "ampithoe rubricata":20,
            "an isopod":6,
            "anaitides maculata":20,
            "anaitides mucosa":20,
            "anguinella palmata":20,
            "angular crab":10,
            "angulus tenuis":10,
            "anomia ephippium":10,
            "anoplodactylus angulatus":20,
            "antithamnion cruciatum":20,
            "antithamnionella spirographidis":20,
            "aonides oxycephala":20,
            "aora gracilis":20,
            "aphelochaeta marioni":20,
            "apherusa bispinosa":20,
            "apherusa jurinei":20,
            "apistonema carterae":20,
            "aplysilla sulfurea":20,
            "apoglossum ruscifolium":10,
            "aporrhais pespelecani":20,
            "arch-fronted swimming crab":8,
            "archidoris pseudoargus":20,
            "arctic cowrie":4,
            "arenicolides ecaudata":10,
            "aricidea minuta":20,
            "ascidia conchilega":10,
            "ascidia virginea":20,
            "ascidiella scabra":20,
            "asian shore crab":10,
            "aslia lefevrei":8,
            "aslia lefevrii":20,
            "asperococcus fistulosus":20,
            "asterias rubens":7,
            "asterocarpa humilis":20,
            "astropecten irregularis":20,
            "atlantic bobtail squid":6,
            "audouinella purpurea":20,
            "axinella dissimilis":20,
            "axinella infundibuliformis":20,
            "baked bean ascidian":4,
            "balanus balanus":10,
            "balanus crenatus":5,
            "ballan wrasse":10,
            "barleeia unifasciata":20,
            "barnea candida":20,
            "barnea parva":20,
            "bathyporeia elegans":20,
            "bathyporeia pelagica":20,
            "bathyporeia pilosa":20,
            "bathyporeia sarsi":20,
            "beach hopper":10,
            "beadlet anemone":1,
            "bicellariella ciliata":20,
            "bispira volutacornis":10,
            "bittium reticulatum":8,
            "black-footed limpet":2,
            "bladder wrack":1,
            "blidingia minima":10,
            "blue encrusting sponge":5,
            "blue jellyfish":5,
            "blue rayed limpet":2,
            "boergeseniella thuyoides":20,
            "bonnemaisonia asparagoides":20,
            "bonnemaisonia hamifera":20,
            "boot lace worm":3,
            "bostrychia scorpioides":20,
            "bowerbankia citrina":20,
            "bowerbankia gracilis":20,
            "bowerbankia imbricata":20,
            "bowerbankia pustulosa":20,
            "brachystomia scalaris":20,
            "breadcrumb sponge":2,
            "bristly mail-shell":3,
            "broad-clawed porcelain crab":1,
            "brongniartella byssoides":20,
            "brown forking weed":5,
            "brown shimp":8,
            "bryopsis hypnoides":20,
            "bryopsis plumosa":20,
            "buccinum undatum":7,
            "bugula flabellata":20,
            "bugula fulva":20,
            "bugula plumosa":20,
            "bugula turbinata":20,
            "bunny ears":3,
            "butterfish":10,
            "by-the-wind-sailor":10,
            "cadlina laevis":10,
            "calliblepharis ciliata":10,
            "calliopius laeviusculus":20,
            "callithamnion tetragonum":20,
            "callithamnion tetricum":20,
            "callophyllis laciniata":8,
            "callopora lineata":20,
            "calycella syringa":20,
            "calyptraea chinensis":20,
            "campecopea hirsuta":10,
            "candy striped flatworm":8,
            "capitella capitata":7,
            "caprella acanthifera":20,
            "caryophyllia smithii":7,
            "catenella caespitosa":10,
            "cellaria sinuosa":20,
            "cellepora pumicosa":10,
            "celleporella hyalina":20,
            "ceramium botryocarpum":20,
            "ceramium ciliatum":20,
            "ceramium deslongchampii":20,
            "ceramium deslongchampsii":20,
            "ceramium diaphanum":20,
            "ceramium echionotum":20,
            "ceramium gaditanum":20,
            "ceramium nodulosum":20,
            "ceramium pallidum":20,
            "ceramium secundatum":20,
            "ceramium shuttleworthianum":20,
            "ceramium strictum":20,
            "ceramium virgatum":20,
            "cerastoderma edule":20,
            "cerithiopsis tubercularis":20,
            "chaetomorpha capillaris":20,
            "chaetomorpha linum":20,
            "chaetomorpha mediterranea":20,
            "chaetomorpha melagonium":10,
            "chaetopterus variopedatus":20,
            "chamelea gallina":8,
            "chameleon prawn":4,
            "chameleon shrimp":10,
            "channel wrack":3,
            "chartella papyracea":20,
            "china limpet":4,
            "chlamys distorta":20,
            "chondracanthus acicularis":10,
            "chondria dasyphylla":20,
            "chorda filum":10,
            "chordaria flagelliformis":20,
            "chylocladia verticillata":20,
            "cingula cingillus":10,
            "ciocalypta penicillus":20,
            "cirratulus cirratus":5,
            "cirriformia tentaculata":7,
            "cladophora albida":20,
            "cladophora pellucida":10,
            "cladophora rupestris":8,
            "cladophora sericea":20,
            "cladostephus spongiosus":10,
            "clathria atrasanguinea":20,
            "clathrina coriacea":20,
            "clausinella fasciata":10,
            "clava multicornis":20,
            "cliona celata":20,
            "clitellio arenarius":20,
            "clock face anemone":20,
            "clockwise spiral worm":2,
            "clytia hemisphaerica":20,
            "codium tomentosum":20,
            "codium vermilara":20,
            "common brittle star":1,
            "common chiton":2,
            "common hermit crab":1,
            "common limpet":1,
            "common mussel":1,
            "common periwinkle":1,
            "common prawn":1,
            "common sole":10,
            "common spider crab":3,
            "common squat lobster":3,
            "common tortoiseshell limpet":8,
            "compass jellyfish":3,
            "compsothamnion thuyoides":20,
            "conger eel":10,
            "connemara clingfish":7,
            "conopeum reticulum":8,
            "coral weed":2,
            "corbula gibba":20,
            "cordylecladia erecta":20,
            "corella parallelogramma":20,
            "corkwing wrasse":6,
            "cormorant":10,
            "cornish sucker":3,
            "corophium sextonae":20,
            "corophium volutator":20,
            "corynactis viridis":20,
            "coryne muscoides":20,
            "crab hacker barnacle":3,
            "craterolophus convolvulus":20,
            "crepidula fornicata":5,
            "crimora papillata":20,
            "crisia denticulata":20,
            "crisia eburnea":20,
            "crisidia cornuta":20,
            "crossaster papposus":20,
            "cryptosula pallasiana":10,
            "ctenolabrus rupestris":20,
            "cuckoo wrasse":20,
            "curled octopus":20,
            "cushion star":1,
            "cuvie":6,
            "cyathura carinata":20,
            "cystoclonium purpureum":10,
            "cystoseira baccata":20,
            "dahlia anemone":2,
            "dainty crab":10,
            "daisy anemone":2,
            "deep hermit crab":20,
            "deep water dahlia":20,
            "delesseria sanguinea":10,
            "dendronotus frondosus":20,
            "dercitus bucklandi":10,
            "desmarestia aculeata":8,
            "desmarestia ligulata":10,
            "desmarestia viridis":20,
            "dexamine spinosa":20,
            "dexamine thea":20,
            "diaphorodoris luteocincta":20,
            "dictyopteris membranacea":20,
            "dictyota dichotoma":20,
            "didemnum maculosum":8,
            "diodora graeca":10,
            "diphasia rosacea":20,
            "diplosoma listerianum":20,
            "diplosoma spongiforme":6,
            "dipper":20,
            "dirty sea squirt":3,
            "disporella hispida":20,
            "distaplia rosea":20,
            "distomus variolosus":20,
            "dog whelk":1,
            "donax vittatus":20,
            "doto coronata":20,
            "doto fragilis":20,
            "drachiella heterocarpa":20,
            "drachiella spectabilis":20,
            "dragonet":7,
            "dulse":2,
            "dumontia contorta":5,
            "dusky doris":7,
            "dwarf brittlestar":1,
            "dynamena pumila":4,
            "dynamene bidentata":6,
            "dysidea fragilis":8,
            "eatonina fulgida":20,
            "echinocardium cordatum":7,
            "echinogammarus obtusatus":20,
            "echinus esculentus":20,
            "ectocarpus fasciculatus":20,
            "edible crab":1,
            "eelgrass":6,
            "egg wrack":2,
            "elachista fucicola":20,
            "electra pilosa":3,
            "elegant anemone":7,
            "ellisolandia elongata":20,
            "elminius modestus":10,
            "elysia viridis":8,
            "ensis ensis":20,
            "ensis siliqua":10,
            "enteromorpha compressa":20,
            "enteromorpha intestinalis":10,
            "enteromorpha linza":20,
            "enteromorpha prolifera":20,
            "erythrodermis traillii":20,
            "erythroglossum laciniatum":20,
            "erythrotrichia carnea":20,
            "escharella immersa":20,
            "escharoides coccinea":20,
            "esperiopsis fucorum":20,
            "eteone longa":20,
            "eudendrium capillare":20,
            "eudesme virescens":20,
            "eulimnogammarus obtusatus":20,
            "eumida sanguinea":20,
            "eunicella verrucosa":20,
            "eupolymnia nebulosa":10,
            "european bass":20,
            "european eel":7,
            "european flat oyster":4,
            "european lobster":7,
            "european spiny lobster":20,
            "european sting winkle":2,
            "eurydice pulchra":20,
            "exogone hebes":20,
            "exogone naidina":20,
            "fabricia sabella":20,
            "fabulina fabula":20,
            "facelina auriculata":6,
            "false eyelash weed":5,
            "false irish moss":3,
            "feather hydroid":10,
            "fifteen-spined stickleback":10,
            "filograna implexa":20,
            "fine-veined crinkle weed":8,
            "five bearded rockling":2,
            "flabellina pedata":20,
            "flat periwinkle":1,
            "fluffy white sea slug":20,
            "flustra foliacea":20,
            "flustrellidra hispida":6,
            "fucus ceranoides":6,
            "fucus distichus":20,
            "fucus vesiculosus var. linearis":10,
            "fulmar":20,
            "furbellow":3,
            "furcellaria lumbricalis":8,
            "furry purse sponge":7,
            "gammarellus homari":20,
            "gammarus zaddachi":20,
            "gastroclonium ovatum":10,
            "gelidium crinale":20,
            "gelidium latifolium":20,
            "gelidium pulchellum":20,
            "gelidium pusillum":20,
            "gelidium spinosum":8,
            "gem anemone":2,
            "giant goby":7,
            "gibbula pennanti":10,
            "gigartina pistillata":10,
            "ginger anemone":20,
            "glaucus pimplet":7,
            "glycera tridactyla":20,
            "gobiusculus flavescens":10,
            "goggle eyed prawn":10,
            "goniodoris nodosa":10,
            "gracilaria gracilis":10,
            "grateloupia filicina":20,
            "grateloupia turuturu":20,
            "great spider crab":20,
            "greater pipefish":6,
            "green blisters":4,
            "green leaf worm":2,
            "green paddleworm":8,
            "green sea urchin":2,
            "green sponge fingers":5,
            "grey seal":10,
            "grey top shell":1,
            "griffithsia corallinoides":20,
            "groovy crab":20,
            "guiryi's wrack":10,
            "gut weed":2,
            "gymnangium montagui":20,
            "gymnogongrus crenulatus":20,
            "hairy crab":5,
            "halarachnion ligulatum":20,
            "halecium halecinum":20,
            "halichondria bowerbanki":20,
            "haliclona cinerea":20,
            "haliclona oculata":20,
            "haliclona rosea":20,
            "haliclona simulans":20,
            "haliclona viscosa":20,
            "haliclystus auricula":20,
            "halidrys siliquosa":8,
            "haliotis tuberculata":20,
            "halisarca dujardini":10,
            "halisarca dujardinii":8,
            "halopteris catharina":20,
            "halopteris filicina":20,
            "halurus equisetifolius":20,
            "halurus flosculosus":20,
            "haraldiophyllum bonnemaisonii":20,
            "harbour crab":6,
            "harmothoe extenuata":20,
            "harmothoe imbricata":20,
            "harpoon weed":4,
            "helcion pellucidum":20,
            "hemimycale columella":20,
            "henricia oculata":20,
            "henricia sanguinolenta":20,
            "heteranomia squamula":20,
            "heterochaeta costata":20,
            "heterosiphonia plumosa":20,
            "hiatella arctica":20,
            "hildenbrandia rubra":8,
            "hincksia granulosa":20,
            "holothuria forskali":20,
            "honeycomb reef worm":2,
            "hooded prawn":5,
            "hyale prevostii":20,
            "hyale stebbingi":20,
            "hydractinia echinata":20,
            "hydrallmania falcata":20,
            "hydrobia ulvae":20,
            "hymeniacidon perleve":7,
            "hymeniacidon perlevis":4,
            "hymeniacidon sanguinea":20,
            "hypoglossum hypoglossoides":20,
            "irish moss":2,
            "jaera albifrons":20,
            "jania rubens":5,
            "janira maculosa":7,
            "janolus cristatus":20,
            "janua pagenstecheri":10,
            "jasmineira elegans":20,
            "jassa falcata":8,
            "jerky hopper":6,
            "kallymenia reniformis":20,
            "keel worm":1,
            "kefersteinia cirrata":20,
            "kellia suborbicularis":20,
            "kelp":3,
            "kelp fur":10,
            "kidney scale worm":4,
            "kirchenpaueria pinnata":20,
            "ladder ascidian":3,
            "laeospira corallinae":20,
            "lamellaria perspicua":8,
            "laminaria ochroleuca":20,
            "laminaria saccharina":10,
            "laomedea flexuosa":20,
            "lasaea adansoni":20,
            "leach's spider crab":20,
            "leathesia difformis":10,
            "leathesia marina":6,
            "lepidonotus clava":5,
            "lepidonotus squamatus":20,
            "leptasterias muelleri":20,
            "leptochiton asellus":20,
            "leptoplana tremellaris":4,
            "leuconia nivea":20,
            "leucosolenia botryoides":20,
            "leucosolenia complicata":20,
            "lichina pygmaea":7,
            "light bulb sea squirt":4,
            "ligia oceanica":10,
            "limacia clavigera":5,
            "limapontia capitata":20,
            "lineus ruber":20,
            "liocarcinus arcuatus":20,
            "lissoclinum perforatum":6,
            "lithophyllum incrustans":3,
            "lithothamnion glaciale":8,
            "little egret":20,
            "littorina fabalis":20,
            "littorina mariae":8,
            "littorina nigrolineata":20,
            "littorina obtusata":5,
            "littorina saxatilis var. rudis":20,
            "lomentaria clavellosa":10,
            "lomentaria orcadensis":20,
            "long-clawed porcelain crab":2,
            "long-legged spider crab":4,
            "lucernariopsis campanulata":20,
            "lucernariopsis cruxmelitensis":10,
            "luidia ciliaris":20,
            "lysianassa ceratina":20,
            "macoma balthica":10,
            "mactra stultorum":20,
            "malacoceros fuliginosus":20,
            "manayunkia aestuarina":20,
            "many ribbed jelly":4,
            "manzonia crassa":20,
            "marbled swimming crab":10,
            "margarites helicinus":20,
            "marine springtail":5,
            "mediomastus fragilis":20,
            "melinna palmata":20,
            "melita palmata":10,
            "membranoptera alata":20,
            "meredithia microphylla":20,
            "mesophyllum lichenoides":5,
            "metridium senile":20,
            "microciona atrasanguinea":20,
            "modiolarca tumida":20,
            "modiolus modiolus":20,
            "molgula manhattensis":20,
            "monostroma grevillei":20,
            "montagu's blenny":2,
            "montagu's crab":1,
            "montagu's sea snail":7,
            "montagu's stellate barnacle":1,
            "moon jelly":5,
            "morchellium argus":4,
            "mud sagartia":20,
            "musculus discors":20,
            "mya arenaria":20,
            "mya truncata":20,
            "mysella bidentata":20,
            "myxicola infundibulum":20,
            "myxilla incrustans":20,
            "nassarius incrassatus":20,
            "nassarius reticulatus":20,
            "nemalion helminthoides":20,
            "nemertesia antennina":20,
            "nemertesia ramosa":20,
            "neoamphitrite figulus":20,
            "neopentadactyla mixta":20,
            "neosiphonia harveyi":20,
            "nephasoma minutum":20,
            "nephtys cirrosa":20,
            "nephtys hombergii":20,
            "nereis pelagica":20,
            "netted dog whelk":2,
            "new zealand barnacle":3,
            "nitophyllum punctatum":10,
            "northern green sea urchin":20,
            "northern lacuna":10,
            "northern rock barnacle":3,
            "norway lobster":20,
            "notched isopod":8,
            "notomastus latericeus":20,
            "nucula nucleus":20,
            "nursehound":5,
            "nymphon gracile":5,
            "oarweed":2,
            "odonthalia dentata":20,
            "odontosyllis ctenostoma":20,
            "odontosyllis gibba":20,
            "odostomia plicata":20,
            "odostomia turrita":20,
            "okamura's pom-pom weed":5,
            "omalogyra atomus":20,
            "onchidella celtica":10,
            "onchidoris muricata":20,
            "onoba aculeus":20,
            "onoba semicostata":20,
            "ophiocomina nigra":8,
            "ophiopholis aculeata":10,
            "ophiura albida":20,
            "ophiura ophiura":20,
            "ophlitaspongia papilla":20,
            "ophlitaspongia seriata":20,
            "orange-striped green sea anemone":20,
            "orange anemone":20,
            "osmundea hybrida":10,
            "osmundea osmunda":20,
            "osmundea truncata":20,
            "owenia fusiformis":20,
            "oyster thief":2,
            "oystercatcher":20,
            "pachymatisma johnstonia":20,
            "pacific oyster":2,
            "painted top shell":1,
            "pale lacuna":20,
            "paracentrotus lividus":20,
            "parajassa pelagica":20,
            "paraonis fulgens":20,
            "parasmittina trispinosa":20,
            "partulida pellucida":20,
            "pecten maximus":8,
            "pentapora foliacea":20,
            "pepper dulse":2,
            "perophora listeri":20,
            "petalonia fascia":20,
            "phaeostachys spinifera":20,
            "pheasant shell":8,
            "pholas dactylus":8,
            "pholoe inornata":20,
            "pholoe synophthalmica":20,
            "phoronis hippocrepia":20,
            "phyllophora crispa":20,
            "phyllophora pseudoceranoides":20,
            "phyllophora sicula":20,
            "phymatolithon calcareum":8,
            "phymatolithon lenormandii":7,
            "phymatolithon purpureum":20,
            "pilayella littoralis":20,
            "pilinia rimosa":20,
            "pink mitten amphipod":5,
            "plaice":20,
            "platynereis dumerilii":20,
            "plocamium cartilagineum":20,
            "plumaria plumosa":20,
            "plumularia setacea":10,
            "pododesmus patelliformis":20,
            "poli's stellate barnacle":2,
            "pollachius pollachius":20,
            "pollicipes pollicipes":20,
            "polycarpa scuba":20,
            "polycera faeroensis":20,
            "polycera quadrilineata":20,
            "polyclinum aurantium":20,
            "polydora ciliata":20,
            "polyides rotunda":7,
            "polyides rotundus":10,
            "polymastia boletiformis":20,
            "polymastia mamillaris":20,
            "polymastia penicillus":20,
            "polyneura bonnemaisonii":20,
            "polysiphonia atlantica":20,
            "polysiphonia brodiei":20,
            "polysiphonia elongata":20,
            "polysiphonia fucoides":20,
            "polysiphonia lanosa":8,
            "polysiphonia nigra":20,
            "polysiphonia nigrescens":20,
            "polysiphonia stricta":20,
            "pomatoceros lamarcki":20,
            "pomatoschistus minutus":20,
            "pomatoschistus pictus":20,
            "pontocrates arenarius":20,
            "porania pulvillus":20,
            "porphyra linearis":20,
            "porphyra purpurea":20,
            "porphyra umbilicalis":10,
            "portuguese man-of-war":10,
            "prasiola stipitata":20,
            "protodorvillea kefersteini":20,
            "protula tubularia":20,
            "psamathe fusca":20,
            "pseudendoclonium submarinum":20,
            "pseudosuberites fallax":20,
            "pterocladia capillacea":20,
            "pterosiphonia complanata":20,
            "pterosiphonia parasitica":20,
            "pterothamnion plumula":10,
            "ptilota gunneri":20,
            "purple top shell":1,
            "purse sponge":6,
            "pycnogonum littorale":20,
            "pygospio elegans":20,
            "pyrenocollema halodytes":20,
            "ragged hydroid":10,
            "ragworm":4,
            "rainbow wrack":2,
            "ralfsia verrucosa":20,
            "raspailia hispida":20,
            "raspailia ramosa":20,
            "rayed artemis":5,
            "red doris":7,
            "red rags":3,
            "red ripple bryozoan":2,
            "red sea oak":10,
            "red speckled anemone":5,
            "retusa truncatula":20,
            "rhizoclonium riparium":20,
            "rhizoclonium tortuosum":20,
            "rhodochorton purpureum":20,
            "rhodomela confervoides":20,
            "rhodomela lycopodioides":20,
            "rhodophyllis divaricata":20,
            "rhodothamniella floridula":4,
            "rhodymenia delicatula":20,
            "rhodymenia holmesii":20,
            "rhodymenia pseudopalmata":20,
            "risso's crab":1,
            "rissoa interrupta":20,
            "rissoa parva":6,
            "rissoella diaphana":20,
            "rock cook":20,
            "rock goby":2,
            "rock pool shrimp":1,
            "root-arm medusa":10,
            "rosy feather-star":6,
            "rough periwinkle":5,
            "rough periwinkle":2,
            "rugose squat lobster":20,
            "runcina coronata":20,
            "rush-clawed shore crab":20,
            "sabella pavonina":6,
            "sabellaria spinulosa":8,
            "saccharina latissima":4,
            "salmacina dysteri":20,
            "sand hopper":4,
            "sand mason":3,
            "sand smelt":7,
            "sandalled anemone":10,
            "saw wrack":1,
            "scarlet and gold star coral":10,
            "schizomavella linearis":20,
            "schizymenia dubyi":20,
            "schottera nicaeensis":20,
            "scolelepis squamata":20,
            "scoloplos armiger":20,
            "scrobicularia plana":20,
            "scruparia chelata":20,
            "scrupocellaria reptans":20,
            "scrupocellaria scruposa":20,
            "scypha ciliata":20,
            "scytosiphon lomentaria":8,
            "sea gherkin":4,
            "sea hare":4,
            "sea lemon":3,
            "sea lettuce":1,
            "sea mat":2,
            "sea orange sponge":5,
            "sea scorpion":3,
            "securiflustra securifrons":20,
            "sepia officinalis":10,
            "sertularella gaudichaudi":20,
            "sertularella polyzonias":20,
            "sertularia argentea":20,
            "sertularia cupressina":20,
            "seven-spot ladybird":8,
            "shanny":1,
            "shore clingfish":3,
            "shore crab":1,
            "shore rockling":3,
            "sideways sea squirt":6,
            "sidnyum elegans":20,
            "sidnyum turbinatum":20,
            "single horn bryozoan":3,
            "skeneopsis planorbis":20,
            "small-headed clingfish":8,
            "small-spotted catshark":7,
            "small cushion star":4,
            "small periwinkle":4,
            "small snakelocks anemone":8,
            "snakelocks anemone":1,
            "snapping prawn":10,
            "solaster endeca":20,
            "soliers red string weed":10,
            "spermothamnion repens":20,
            "sphacelaria cirrosa":20,
            "sphaerococcus coronopifolius":20,
            "sphaeroma rugicauda":20,
            "sphenia binghami":20,
            "sphondylothamnion multifidum":20,
            "spiky lace sponge":20,
            "spiny squat lobster":20,
            "spiny starfish":4,
            "spio filicornis":20,
            "spio martinensis":20,
            "spiophanes bombyx":20,
            "spiral wrack":3,
            "spirobranchus triqueter":10,
            "spirorbis corallinae":20,
            "spirorbis rupestris":20,
            "spirorbis spirorbis":5,
            "spongomorpha aeruginosa":20,
            "spongomorpha arcta":20,
            "spongonema tomentosum":20,
            "spotted cowrie":5,
            "spotted kaleidoscope jellyfish":10,
            "st piran's hermit crab":2,
            "star ascidian":1,
            "starry sea lemon":7,
            "stelligera rigida":20,
            "stelligera stuposa":20,
            "stenothoe monoculoides":20,
            "sthenelais boa":10,
            "stolonica socialis":20,
            "strawberry anemone":1,
            "strawberry sea squirt":8,
            "streblospio shrubsolii":20,
            "styela clava":10,
            "stypocaulon scoparia":10,
            "suberites carnosus":20,
            "syllidia armata":20,
            "syllis gracilis":20,
            "taonia atomaria":20,
            "terebella lapidaria":10,
            "terpios fugax":20,
            "testudinalia testudinalis":20,
            "tethya aurantium":20,
            "tethya citrina":20,
            "tharyx killariensis":20,
            "thick-lipped dog whelk":3,
            "thick trough shell":10,
            "thong weed":2,
            "thorogobius ephippiatus":20,
            "tiny lacuna":20,
            "tompot blenny":5,
            "tonicella rubra":10,
            "toothed top shell":1,
            "topknot":8,
            "trailliella intricata":20,
            "trididemnum cereum":20,
            "trisopterus luscus":20,
            "tritonia lineata":20,
            "trumpet anemone":20,
            "tubificoides amplivasatus":20,
            "tubificoides benedii":20,
            "tubificoides pseudogaster":20,
            "tubularia indivisa":20,
            "tubularia larynx":20,
            "turban top shell":3,
            "turbonilla lactea":20,
            "turritella communis":20,
            "turtonia minuta":20,
            "ulothrix flacca":20,
            "ulva compressa":20,
            "ulva prolifera":10,
            "ulva pseudocurvata":20,
            "umbonula littoralis":20,
            "undaria pinnatifida":20,
            "variegated scallop":3,
            "variegated scallop":4,
            "velvet swimming crab":1,
            "venerupis corrugata":6,
            "venerupis senegalensis":10,
            "verrucaria maura":6,
            "verrucaria mucosa":20,
            "vertebrata lanosa":6,
            "virgularia mirabilis":20,
            "volcano barnacle":1,
            "walkeria uva":20,
            "wart barnacle":4,
            "warty sea slug":10,
            "websterinereis glauca":20,
            "werthers original sea squirt":4,
            "white tortoiseshell limpet":5,
            "whiting":20,
            "wireweed":2,
            "worm pipefish":1,
            "yellow-plumed sea slug":2,
            "yellow sea squirt":8,
        }
        # Define initial teams dictionary
        self.teams = {}
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
        # Add a creature to a team and update the team's score
        creature_name = unquote(creature_name.lower())
        creature_score = self.get_creature_score(creature_name)
        if team_name.lower() in self.teams:
            if creature_name.lower() not in self.teams[team_name.lower()]["creatures"]:
                self.teams[team_name.lower()]["score"] += creature_score
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

    return {'new_name': new_name}

@app.post('/rename_file')
async def rename_file(request: Request):
    data = await request.json()

    # Rename the file
    os.rename(data_file_path, os.path.join(past_games_path, data['new_name']))

    return {}

@app.post('/end_game')
async def end_game(request: Request):
    # Move the data.json file to the "Past Games" folder
    move_file_data = {'source': data_file_path, 'destination': past_games_path}
    response = await move_file(request=Request(json=move_file_data))

    # Get the new name for the data.json file
    new_name = response['new_name']

    # Rename the data.json file if necessary
    if new_name:
        game_count = len(os.listdir(past_games_path))
        new_path = os.path.join(past_games_path, f'{game_count + 1}.json')
        data_file_path = os.path.join(data_path, "static", "data.json")
        os.rename(data_file_path, new_path)

    return {}

if __name__ == "__main__":
    uvicorn.run(app, host="192.168.4.1", port=8000) # run the app on 192.168.4.1:8000 using uvicorn server (opens with splines captive portal)
