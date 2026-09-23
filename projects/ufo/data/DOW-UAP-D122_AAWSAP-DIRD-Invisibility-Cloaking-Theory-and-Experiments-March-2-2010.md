# Historical Document: DOW-UAP-D122_AAWSAP-DIRD-Invisibility-Cloaking-Theory-and-Experiments-March-2-2010

## Source Metadata

- Original file: `DOW-UAP-D122_AAWSAP-DIRD-Invisibility-Cloaking-Theory-and-Experiments-March-2-2010.pdf`
- Pages: 29 (27 from text layer, 2 OCR, 0 illegible)
- OCR language: `eng`
- Processed at: `2026-09-23T18:00:05.405570+00:00`
- Processing pipeline: `pypdfium2 text layer + Tesseract OCR → Markdown → neo4j-graphrag SimpleKGPipeline`

## Text

[Page 1]
UNCLASSIFIED / /FOR-OFFEGEAL-USE-ORe
Pron Defense
ey: Intelligence
oss) Reference
— Document
BE Acquisition Threat Support
2 March 2010
ICOD: 1 December 2009
DIA-08-1003-001
Invisibility Cloaking: Theory
and Experiments
UNCLASSIFIED / (FO R-OFFEGEAL-USE-ORLY

[Page 2]
UNCLASSIFIED/j FOR OFFICIAL USE O14Lf
Invisibility Cloaking: Theory and Experiments
Prepared by:
Acquisition Support Division (DW0-3)
Defense Warning Office
Directorate for Analysis
Defense Intelligence Agency
Author:
AAP Person 68
Administrative Note
COPYRIGHT WARNING: Further dissemination of the photographs in this publication is not authorized.
This product is one in a series of advanced technology reports produced in FY 2009
under the Defense Intelligence Agency, Defense Warning Office's Advanced Aerospace
Weapon System Applications (AAWSA Pro ram. Comments or uestions pertaining to
this document should be addressed to AAP Person 1 AAWSA Program
Manager, Defense Intelligence Agency, ATTN: CLAR/DWO-3, Bldg 6000, Washington,
DC 20340-5100.
UNCLASSIFIED//FOR OFEICI0L Wlili 8ftt¥
ii

[Page 3]
UNCLASSIFIED/ /FOR OFFICIAL USE O14Lt
Contents
Introduction ............................................................................................................v
Camouflage ............................................................................................................ 1
Transparency ......................................................................................................... 3
Cloaking ................................................................................................................. 5
Metamaterials ........................................................................................................ 9
Optical Metamaterials .......................................................................................... 11
Fundamental Problem .......................................................................................... 15
Curved Space ....................................................................................................... 17
Broadband Invisibility .......................................................................................... 19
Implementation ................................................................................................... 20
Optical Cloaking ................................................................................................... 22
Summary.............................................................................................................. 23
References ........................................................................................................... 23
Figures
Figure 1. B2 Stealth Bomber .................................................................................. 1
Figure 2. Optical Camouflage ................................................................................. 2
Figure 3. The Secret Optical Camouflage ................................................................ 2
Figure 4. H. G. Wells's The Invisible Man: Invisibility by Transparency .................. 3
Figure 5. Complementary Media Invisibility Cloak .................................................. 4
Figure 6. Cloaking Shell .......................................................................................... 5
Figure 7. The Invisible Woman ............................................................................... 6
Figure 8. Fermat's Principle ................................................................................... 7
Figure 9. An Optical Material Deforms the Coordinates of Space ............................ 8
Figure 10. Light Waves at Cloaking Device ............................................................. 9
Figure 11. Cloaking Device for Microwaves .......................................................... 10
UNCLASSIFIED/,'POR: errl@IAL YSli 8PtLY
iii

[Page 4]
UNCLASSIFIED/ /FOR OFFl&I.t.k Uili QPIL¥
Figure 12. Lycurgus Cup (British Museum; AD Fourth Century)........................... 11
Figure 13. Idea for a Cloaking Device for Visible Light ......................................... 12
Figure 14. Advances in Metamaterials .................................................................. 13
Figure 15. Demonstration of Negative Refraction With "Bulk" Optical
Metamaterials Made of Nano-Fishnets ................................................. 14
Figure 16. Demonstration of Negative Refraction With "Bulk" Optical
Metamaterials Made of Nanowires ....................................................... 15
Figure 17. Fundamental Problem of Transformation-Based Cloaking Devices ...... 16
Figure 18. Wave Packets are Made by Combining Waves With Different
Frequencies......................................................................................... 17
Figure 19. Stereographic Projection ..................................................................... 18
Figure 20. Non-Euclidean Cloaking Device in Two Dimensions ............................. 19
Figure 21. Three-Dimensional Cloaking................................................................ 20
Figure 22. Coordinate Transformation Implemented by a Ground-Plate Cloak..... 21
Figure 23. Implementation of the Ground-Plate Cloak ......................................... 21
UNCLASSIFIED/ /fOll OPPl@IJIIL U:!I!! er~t"f
iv

[Page 5]
UNCLASSIFIED/ /POlt OfFI@Il.tk WIiii QJslL¥
Invisibility Cloaking: Theory and Experiments
Introduction
The idea of invisibility has fascinated people for millennia, inspiring many
myths, novels, and films. Invisibility cloaking has recently become a subject of
science and technology. This paper describes the important current theoretical
and experimental developments and tries to project into the future.
UNCLASSIFIED/ /fOR OFFI&l.t.k WIiii QI\IL¥
V

[Page 6]
UNCLASSIFIED/ /FOA OFFI&Il.tl l::181: 8HL'f
Camouflage
Invisibility may be achieved through three principal methods: camouflage,
transparency, and cloaking. Many animals and some plants use camouflage to disguise
themselves from predators-for example, by assuming the shapes and colors of objects
in their surroundings. The military has long used forms of camouflage; a recent military
application of camouflage is stealth technology.
Stealth planes have aerodynamically
unusual, edgy shapes and are coated
with a special material. Both features
serve the same purpose: to make the
plane "invisible" to radar. How does it
work? In radar, electromagnetic
microwaves are emitted by a source, and
their reflection by an object-an
airplane, for example-is detected. From
the direction and the t ime delay of the
reflected waves, the direction and
distance of the object are inferred. If the
object does not reflect the
electromagnetic microwaves back to the
source, it will not appear on the radar.
This is precisely what stealth technology
achieves. Owing to t he edgy shape of Figure 1. B2 Stealth Bomber
the stealth plane, most of the incident
electromagnetic waves are reflected in different directions; the coating of the plane
absorbs the rest. In this way, the stealth plane has become completely black in t he
spectral range of radar. As for radar waves, the sky is black, not blue, and the plane
has assumed the color of the background: the stealth plane is camouflaged.
UNCLASSIFIED/ /&iOA: OFFICl.t.k W&li 8,.lY
1

[Page 7]
UNCLASSIFIED/ /FOA OFFI&I.t.k Wfili 8,.LY
Another recent example of camouflage is
optical camouflage, developed by the
University of Tokyo's Tachi Laboratory.
Figure 2 shows an example of optical
camouflage. A camera captures the
background scene behind the person.
The image is processed and projected
onto the person via a semitransparent
mirror. The person wears an "invisibility
cloak" made of a retroreflective material
that reflects light back in t he direction
whence it came, like cats-eye-reflectors
do. As the cloak carries the projected
image of the background, the person
seems to disappear, but surely the
equipment standing around the person is
clearly visible. In addition, optical
camouflage works only in one direction;
seen from the side, the person is visible.
Nevertheless, optica l camouflage may
become a useful tool in some situations
where obstacles are in the way of sight- Figure 2. Optical Camouflage (Tachi Laboratory,
for example in surgery, where the Tokyo}
surgeon's hands and instruments may
obstruct the view. Figure 3 shows how optical camouflage works.
I JJ f"n>Jl'<to<
rt,.,,.. Ol"'J irlf' .-n•,r
,_.1111 thr,t.i.,.,.
The S~cret of Trollnsparent croalc 1
Figure 3. The Secret Optical Camouflage (Tachi Laboratory, Tokyo)
UNCLASSIFIED/ /FOP OFFICIO P I !iii ODIL¥
2

[Page 8]
UNCLASSIFIED/; POI\ OPPICIAL U.!I!! er•tY
Transparency
H. G. Wells's novel The Invisible Man
represents another strategy for
becoming invisible: transparency.
In Wells's novel, the invisible man, a
disgruntled college professor, invents a
substance that somehow changes the
refractive index1 of his body. Most
transparent substances, like glass, air,
or water, modify the speed of light,
because the atoms or molecules of these
substances absorb and re-emit light,
which takes time. The delay caused by
the atoms and molecules results in a
reduced speed of light and hence in a
refractive index larger than 1. It is,
however, also possible to achieve a
refractive index smaller than 1, although
only in narrow bands of the spectrum. In
these cases, the atoms or molecules
advance the wave fronts of light because
they are excited such that their electron
clouds oscillate ahead of the light. If the refractive index is uniform in a material, light
is reflected and refracted at the boundary but otherwise is traveling straight through.
On the other hand, if the refractive index varies, light is scattered at the index
inhomogeneities and gets lost. Most white substances appear white because of such
scattering . Milk, for example, consists of minuscule oily droplets-fat-in water. The
refractive index of the droplets differs from water, and hence light is scattered at them;
it does not penetrate the substance, and the diffused light appears as white. Now,
human bodies are visible, because they absorb light. Most of the absorption is due to
the scattering of light in biological tissue, in the cells of which the bodies are made. If
the refractive indices of a person's cells could somehow be changed to the refractive
index of air, the person would become transparent and disappear from view-like the
Invisible Man.
Some animals (for example, some jellyfish) are transparent, but the cells of higher
order animals are usually much too complex and diverse for transparency to become a
serious option for disguise. Exceptions are the transparent parts of the body, most
notably eye lenses, which consist of uniform cells kept in a state between life and
death. If this balance is upset, the lenses become opaque as a cataract develops.
Transparency is the idea behind some proposed forms of invisibility by technology. For
example, in plasmonic covering, 1 a particle should be surrounded by layers made of
metals and transparent substances, such as glass. The layers are designed such that
they cancel the scattering of light at the particle, hence making both the particle and
the layers transparent-that is, invisible. Another proposal 2 exploits the resonance of
the particle with a negative-refractive material that cancels out scattering. In a material
with negative refraction, the wave fronts of light appear to move in the opposite
1 The refractive index is the ratio between the speed of light in vacuum and the speed of light in a material.
UNCLASSIFIED//5O9 OEEICI0 .. Uili QPlkY
Figure 4. H. G. Wells's The Invisible
Man: Invisibility by Transparency
3

[Page 9]
-----
UNCLASSIFIED/ /FOR OFFl@IAL YSE OHL¥
direction from the propagation . The clearest and most advanced form of this concept is
the complementary media invisibility cloak. 3 Here, an optical antiobject is placed beside
the object one wishes to make disappear. The antiobject should be made of a
negatively refract ive material that exactly compensates the optica l appearance of t he
object. An image is contained in the deformations of light-wave fronts caused by the
imaged object. If these deformations are reversed, the image disappears, and t he
object becomes transparent- that is, invisible. The optical antiobject must be tailored to
the object and placed precisely at t he correct distance-that is, the distance where it is
made to ca ncel the image of t he object. The more complex t he object is, the more
complex t he antiobject must be for reversing all the scatterings of light. Such cloaking
at the distance ca nnot be instantaneous, as the light scattered by both object and
antiobject must settle to a stationary state where it becomes synchronized. A stationary
light field has only one color. So, in practice, these forms of transparency will work only
for small objects and for small parts of the spectrum and not for large objects in many
colors.
a) b)
ob' µ 1m
-L 0 L -L 0 L
c) d) ..,,
. ,, • I
, ,
I , , , I I I I I
I I ' I I ,
I
I
I ,
, I ' I
I ,
,
.
, 'µob ,
- ____ ,,,. -·· --·
Figure 5. Complementary Media Invisibility Cloak: (a) The slab of empty space x with O < x < Lis optically
canceled by a slab of negative-index material in -L < x < 0. (b) The same cancellation effect works with an object
in O < x < L if the negative-index slab contains an antiobject. (c) A spherical shell b < r < c is optically canceled by
a negative-index shell a < r < b. If the corer< a is optically equivalent to a sphere of radius c, then this device ls
invisible. (d) The same as (c), but with an object in the canceled shell b < r < c. The object is cloaked: both it and
the cloa king sphere are invisible.
UNCLASSIFIED/ /POlt orrlCIJ!!tt 05E: 014[ I
4

[Page 10]
UNCLASSIFIED// POI\ OPPICIJ!tt l!l!H! e ..tv
Cloaking
Cloaking4• 5 is a universal strategy for invisibility that works for objects of arbitrary
compositions and shapes within a given size. In cloaking, the hidden object is enclosed
by the cloaking device, a transparent shell that guides light around the object as if the
light would propagate through empty space. In this way, both the interior of the
cloaking device is hidden and the act of hiding is concealed.
Figure 6. Cloaking Shell6
How does one find the right design for such a cloaking device? As the Invisible Man
symbolizes transparency as a strategy for invisibility, inspiration for cloaking may come
from the Invisible Woman, a cartoon figure from the Fantastic Four. The Invisible
Woman is said to create a mysterious force field around her that bends space. Light
follows the curved space such that it smoothly flows around the Invisible Woman, like
water in a stream flowing around an obstacle. The key idea here is the concept of
curved space used for invisibil ity. The idea that turns the Invisible Woman with her
fabled force field from a fictitious character into something close to reality is the insight
that no force field is needed, that light-refracting materials like glass or water appear as
curved spaces by themselves.
UNCLASSIFIED/}FOA OFFICIO .. Uili 01"1 ..¥
5

[Page 11]
UNCLASSIFIED/, FOR OFFICIAL USE Oilti
This idea comes from Fermat's principle
of the shortest optical path. 7 Suppose
that light travels from A to B. According
to Fermat's principle, light follows the
path that takes the shortest time. In
refractive materials, the speed of light is
modified-in most cases reduced-by the
refractive index. The time it takes for
light to pass through an infinitesimal
element of space is proportional to the
refractive index. So, if the index varies
in an optical material or in the
boundaries between materials, the
optical measure of path length varies,
which is the defining feature of a curved
geometry. To provide a simple example,
a lens focuses parallel light rays into a
point; the parallels meet there, which is
the hallmark of a non-Euclidian
geometry. So something as familiar as a
lens creates something as fantastic as a
curved geometry.
Figure 7. The Invisible Woman. Invisibility by bending
light, an inspiration for cloaking.
UNCLASSIFIED/}FOR. 8FFIEiIAL YSE 8HL1/
6

[Page 12]
UNCLASSIFIED/ /FOlt 8PPl@IAL YSI: 8,.LY
Figure 8. Fermat's Principle. The grey level indicates the refractive index. In traveling from A to B, light follows
the path that takes the shortest time, traveling, if possible, through regions of low index .
The bending of light in materials or, equivalently, the change of the spatial geometry by
optical materials is the cause of most optical illusions. For instance, the figure used to
illustrate Fermat's Principle shows the path of light in a mirage. The air above a hot
surface, hot tarmac, or desert sand is hotter than the air farther above. As hot air is
thinner than cooler air, the refractive index is lower above the hot surface. Light rays
are bent upwards, conjuring up images of water in the distance that, in reality, are
images of the sky. Such optical geometries may also be employed for creating the
ultimate illusion: invisibility. Imagine an optical material changing the geometry of
space, as shown in Figure 9 below.
UNCLASSIFIED/;CFOA OFFitl.t.k W&lii 0PUslf
7

[Page 13]
UNCLASSIFIED/fFOR: 8FFI@IAL Y!H! 9HL'f
B
I I I I I I
I I I i
_,__ I I I ,... :-... I
,,. ...... I I I ., , I i I 1'\
I I I I \ _""""T, ...._ ~---' _..____._ . .. '-"- ·•-~
I I I ' I I
I .1 I I I I I
- I I I I
I
\ +-·-'- - I ·- -1- -r·-·- --.- -i- _ ,_
-~i- _ ,___ I 1./ - ·-t- I
_,_,_
' ~
- ~roe: _ .... .!.,, ,.,.
I I
I I I ' I I
I I I I
Figure 9. An Optical Material Deforms the Coordinates of Space. A: virtual space, B: real space.
The material acts like a transformation of space. In the device, each point in real space
is put to a new location in a virtual space (outside of the device, space remains the
same). The device creates the illusion that light propagates along straight lines through
the virtual space, whereas in reality it is bent. Suppose the device encloses a hollow
region that is not part of t he virtual space or, to be more precise, a region with a
surface that, in virtual space, has become a single point. The red circle in Figure 9B is
reduced to the red dot in Figure 9A. As the hollow region is not part of the virtual space
where light propagates, everything inside it has become invisible. As the coordinates of
virtual space smoothly go over into the coordinates of real space at the outer surface of
the device, light rays are not distorted. Any object inside the cloaking device is hidden,
and so is the act of hiding itself. Moreover, the cloaking device not only would bend
light rays but would modify the entire structure of light waves in such a way that
detecting the hidden object is impossible. Light waves would advance around the
hidden core of the device, engulfing it, as Figure 10 shows.8
UNCLASSIFIED//EOA: OEEICI0 .. Uili OPU:¥
8

[Page 14]
UNCLASSIFIED/,'FOR: OFFl@IAL l!ISI!!! 9HLY
Figure 10. Light Waves at Cloaking Device. Wave propagation in (a) virtual space and (b) real space.
This idea of cloaking by coordinate transformations was put forward by two
independent groups. Their theories appeared in Science Express on 25 May 2006 and
were published back to back in Science magazine later on. The first paper9 only
considered isotropic materials, optical materials where the speed of light at each point
is the same in each direction but may vary from point to point. Most natural optical
materials, except for some crystals and all liquid crystals, are isotropic. In isotropic
materials, invisibility is perfect only for light rays, but the cloaking device may cause
dislocations of light waves. In addition to the optical implementation of coordinate
transformations, some other tricks are required. The second paper10 considered
anisotropic materials for cloaking or other manipulations of electromagnetic waves.
Here, perfect invisibility is possible in principle (but not in practice, as is discussed
later). I n October 2006, the first cloaking device was demonstrated, 11 for microwaves.
Science magazine regarded cloaking as one of the top 10 science breakthroughs of the
year (it was top in physics and engineering) . Scientific American listed the inventors of
cloaking devices-Sir John Pendry, David Smith, David Schurig, and Ulf Leonhardt￾among the top 50 policy, business, and research leaders of the year. The first paper12
on cloaking had initially been rejected by most major science and physics journals
before it finally appeared in Science, but since 2006, cloaking has become a
mainstream subject on which about a thousand papers have been published so far.
Metamaterials
The first prototype13 of a cloaking device was designed to operate in the microwave
region of the electromagnetic spectrum, for a wavelength of about 3 cm. The device
consists of 10 rings of flexible circuit board. The copper of the circuit board has been
etched away, apart from characteristic structures of about 3-mm size, so-called split￾ring resonators.
UNCLASSIFIED//509 OFFICIOP 1!55 ODtf PX
9

[Page 15]
UNCLASSIFIED/fFOlil OFFI&Ilil l:ISE 8Hl¥
The split-ring resonators are
electromagnetic circu its; they respond to
the electromagnetic field of microwave
rad iation. Their response depends on
their shapes. For example, in the
cloaking device shown in Figure 11, the
double stripes in the middle of the split￾ring resonators vary from ring to ring. As
these stripes form an electric capacitor,
the capacitance of the resonators also
varies. The colored curves show how the
electromagnetic functions change over
the distance from the center of the
cloaking device as a result of the varied
capacitance. As they are always positive,
negative refraction is not required for
cloaking. At the inner ring, the red curve
reaches zero, defining the boundary of
the cloaking device. The rings with their
split-ring structures are designed to Figure 11. Cloaking Device for Microwaves14
perform an approximation of the
coordinate transformation shown and explained in the previous section. How is this
possible? The split-ring resonators act like the atoms or molecules of a normal optical
or electromagnetic material : they absorb electromagnetic waves and re-emit them with
a phase delay or advance that depends on their electromagnetic response. Like atoms
or molecules, they are much smaller than the electromagnetic wavelength-3-mm cell
size versus 3-cm wavelength in the case of the microwave cloaking device15- such that
the waves cannot resolve them individually but, rather, react to them as if they were a
bulk material with electromagnetic properties that may differ from point to point. Unlike
atoms or molecules, the electromagnetic response of each split-ring resonator is tailor￾made because it depends on the shape of the resonator that can be easily modified.
For example, in the case of the microwave-cloaking device, 16 the electromagnetic
response depends on the capacitance that is varied by changing the length of the
double stripes in the resonators. An unstructured circuit board reacts completely
differently to the microwave radiation: it would simply reflect it like the mesh in the
window of a microwave oven. A material with electromagnetic or optical properties that
depends on structures much smaller than the wavelength is called a metamaterial.
Metamaterials per se are nothing new; the ancient Romans invented the first optical
metamaterial: ruby glass. The Romans probably did not know it, but their recipe for
ruby glass contained one crucial ingredient:17 tiny gold droplets, typically 5-60
nanometers (nm) in size. These gold particles color the glass in an extraordinary way,
as demonstrated by the exquisite Lycurgus Cup shown in Figure 12. In daylight, the cup
appears a greenish color, but illuminate it from the inside, and it glows ruby. The gold
particles act like the split-ring resonators of the microwave-cloaking device, 18 but here
on light, not on microwave radiation . Light consists of electromagnetic waves as well,
but with significantly smaller wavelengths of around 500 nm. The gold particles are
thus much smaller than the wavelength of light, and they turn out to be resonators as
well: in them, electric currents flow in a way that is dictated by their shapes and sizes.
When the light wave hits the resonance of the gold particle, most of its energy is
UNCLASSIFIED//EOA: OEEICI C .. Uili OPU1¥
10

[Page 16]
UNCLASSIFIED/ /FOR: OFFl@IAL l!ISI!!! 9HL'f
converted into the electromagnetic oscillation of the gold particle in much the same way
a tuning fork responds to sound of the right frequency .
However, the electromagnetic oscillation
is damped out by the electric resistance
in the metal, and its energy is absorbed
and ultimately turned into heat. The
color of light corresponds to the
frequency or wavelength . If one of the
frequencies is absorbed, the
corresponding color is missing in the
spectrum. For the gold particles in the
Lycurgus Cup, this color is green; a
spectrum with green missing appears
red, which produces the cup's exquisite
color. (Light is also scattered in the
material, and this scattering is enhanced
near the green of the resonance; hence
the greenish color of the cup seen in
daylight.)
What is new about metamaterials is the
degree of control on their structures
achieved by applying modern technology
and the level of theoretical
Figure 12. Lycurgus Cup (British Museum; fourth
century AD). This Roman cup is made of ruby glass.
When viewed in reflected light- for example, in daylight￾it appears green. However, when a light is shone into the
cup and transmitted through the glass, it appears red .
The cup illustrates the myth of King Lycurgus. He is seen
being dragged into the underworld by the Greek nymph
Ambrosia, who is disguised as a vine.
understanding of their workings. The Romans most probably never understood why
ruby glass is neither golden like gold nor transparent like glass, its ingredients, but
ruby . They did not know that light is an electromagnetic wave, nor did they know the
basic laws of electromagnetism . And they would not have had the technological tools to
use this knowledge in the design of novel optical metamaterials.
Optical Metamaterials
As light is simply an electromagnetic wave with shorter wavelengths than microwave
radiation, one could imagine an optical cloaking device as the microwave cloak but with
much smaller cells, fitted to the smaller wavelength. However, this simple idea is too
simple, for two different reasons. One is that metals like the copper of the circuit board
or the gold of ruby glass are more electrically resistant to currents oscillating with the
frequency of visible light than to currents in the microwave range of the spectrum.
Second, and more important, the cells of a metamaterial also emit electromagnetic
rad iation in an incoherent way, not just as a coherent response to the incoming
electromagnetic wave, similar to the spontaneous emission of light by atoms and
molecules. The spontaneous emission is significantly stronger in the optical range of the
spectrum. In short, metamaterials do not scale; they must be designed differently for
visible light, and the loss of light by absorption and incoherent scattering usually is
greater for visible light than for microwaves. Figure 13 below illustrates the idea19 for
an optical cloaking metamaterial. Instead of split-ring resonators, nano-scale metal
wires are embedded in a transparent host material, for example glass. The wires
replace the split-ring resonators on the circuit board of the microwave-cloaking device.
They act similarly to the gold particles embedded in ruby glass; their optical properties
UNCLASSIFIED/ /EAR OFFICIO! I 155 ODIL¥
11

[Page 17]
UNCLASSIFIED/ /POR: errl@IAL YSI: 8HLY
depend on t heir lengt hs and on their arrangement, which, in principle, can be tailor￾made and controlled using the tools of modern nanotechnology. The thin wires will have
lower electric losses than split-ring resonators, and their radiation losses by the
equivalent of spontaneous emission are reduced as well. Such optical cloaking devices
do not yet exist, but one can gauge the progress in the required technology by
considering the progress in negatively refracti ng optical materials.
Figure 13. Idea for a Cloaking Device for Visible Light. Metal nanowires replace the split-ring resonators of
the microwave cloaking device. Coordinate transformation and structure of the optical cloak. a: The coordinate
transformation that compresses a cylindrical region r < b into a concentric cylindrical shel l a < r < b. There is no
variation along the vertical direction. The radii rl and r2 define the internal and external radius of a fraction of the
cylindrical cloak . b: A small fraction of the cylindrical cloak. The wires are all perpendicular to the cylinder's inner
and outer interfaces, but their spatial positions do not have to be periodic and can be random.20
Figure 14 below21 illustrates the route toward achieving negative refraction in t he
visible range of the spectrum. Losses typically are a greater problem for negatively
UNCLASSIFIEDJ;<fOA OFFitI.t.k Wlili QPUsY
12

[Page 18]
UNCLASSIFIED/ /POlt 8FFl@IAL lel§li 8PUs:lf
refractive materials than for the metamaterials of cloaking devices. So the graph
indicates the possible progress toward optical cloaking.
1000
100
10
0.01 •
2000 001 00 001
Figure 14. Advances in Metamaterials. The sol id symbols denote materials with negative refraction; the open
symbols denote optical materials with negative magnetic response . Orange : data from structures based on the
double split-ring resonator (SRR) ; green : data from U-shaped SRRs; blue : data from pairs of metallic nanorods;
red : data from the "fishnet" structure. The four insets give pictures of fabricated structures in different frequency
regions. 22
On the other hand, cloaking devices require bulk metamaterials with varying cell
structures. The first moderately bulk negatively refracting materials23 , 24 were made
only recently.
The most severe practical problem of the currently discussed cloaking devices is not the
technology for manufacturing and structuring the required metamaterials but a problem
at the core of their principal design .25
UNCLASSIFIED/ f FOA OFFI&I.t.k Uili Ql"lk¥
13

[Page 19]
UNCLASSIFIED (FOR OFFTCIALUSE-ONE
‘ b 2
J 7 , “Fa :
’ ry bd ‘
DO ve ean n=1 FY n<0
tui! a Iaes f,
WS Tae
J
0 yy a Y A : ¥ . ’ *
JON : ry ’ a ¥ q fas -——
* gd “a fy ft fe 4 + ee I cen
Ss MJ
aa
c Lens 1 Sample Lens 2 Camera
. Sa ee r= 1.5
*") ae
\ - e n=-1
<$-—_______-» q—_____»
f f
Figure 15. Demonstration of Negative Refraction With “Bulk” Optical Metamaterials Made of Nano-
Fishnets?®
14
UNCLASSIFIED / / EOR.OSPLGEH-USE-ONTT

[Page 20]
UNCLASSIFIED/ /POI\ OPPICIJ!tt U.!E! Oflt (
I
~
I2 , I I
I I
I I
r.,_ - -- I
Figure 16. Demonstration of Negative Refraction With "Bulk" Optical Metamaterials Made of
Nanowires27
Fundamental Problem
The demonstrated microwave-cloaking device only works correctly for microwave
radiation of a specific frequency (wavelength), and the proposed optical cloaking device
would also work for just one frequency; that is, for only one color. Light of different
colors would be severely distorted. So, to see things disappear in a cloaking device, one
should wear tinted glasses of the required color, which of course completely defeats the
purpose. This design flaw is inevitable, 28 no matter how much progress is made in the
technology of metamaterials, for the following reason: the device is designed such that
light waves traveling around the object enclosed by the cloaking device are completely
indistinguishable from light waves propagating through empty space. This is achieved
by implementing the coordinate transformation shown below in Figure 17.29
UNCLASSIFIED/ /fOll OPPIEIJtt U.!E! Oflt I
15

[Page 21]
UNCLASSIFIED/ /FOR OFFICIAL USE ONLY
B
I I I I I I I I I
I I I
! I I I I
~.,.. ' I -.-_ , I
V j I I I' I
~ I I I
,
"' I I ' j I
I I '
I
I I
' - ·- - ... .' I - I j I
--- ---...- -\ I
I
I '
I\. - 1-- ,----i-- _,_,_ I ,_ ... I .,, i,... I I .. >-- I I ~· ... • I I I I I I I
I I I I I I I
I I I I I I
I I I I I I I
Figure 17. Fundamental Problem of Transformation-Based Cloaking Devices30
The device creates the illusion of the empty virtual space A where light travels along
straight lines, whereas in reality light rays are curved by the coordinate transformation
from virtual space to real space B. If the light waves are indistinguishable from light
propagating through empty space, the speed of light in the cloaking device must be
larger than the speed of light in the surrounding material-air, for instance-to make up
for the longer path on the detour through the cloak. To make matters worse, the speed
of light must be infinitely large at the inner lining of the invisibility cloak. To understand
this, consider a light ray that just straddles the red point in the virtual space shown in
A. In real space, B, this point is enlarged to a finite volume that contains the hidden
core of the cloaking device. Now, if for light propagation virtual space and real space
are indistinguishable, the light ray should pass the extended path along the inner lining
in precisely the time it takes to pass a single point, zero time. Consequently, the speed
of light must approach infinity near the core of the cloaking device. The following
argument shows that this is possible in principle, but also that such devices would be
completely useless as a cloaking device in practice.
In wave propagation, one distinguishes between the phase velocity and the group
velocity. The phase velocity is the velocity at which the phase fronts of waves appear to
move. For light, the wave fronts are the features of oscillations across space and time;
by themselves they do not transport energy or information. On the other hand, the
phase fronts are orthogonal to the paths of light rays; if they are ti lted, rays are
refracted. Therefore, the refraction of light, the bending of light rays, is controlled by
the phase velocity. The refractive index that enters Fermat's principle of the shortest
optical path is the phase index, the ratio between the speed of light in vacuum and the
phase velocity in the material. The group velocity is the speed at which wave packets,
pulses, and most information travels; it is the velocity of a wave group. Such a group
consists of a range of single-frequency waves that, by their interference, establish the
group, t he wave packet, as Figure 18 below shows.
UNCLASSIFIED/ /FOR. OFFI@IAL l:t!H!! 9HL'I"
16

[Page 22]
UNCLASSIFIED/,'FOR: OFFl@IAL l!ISl!!! 9HLY
A B C
Figure 18. Wave Packets are Made by Combining Waves With Different Frequencies. The picture shows
the simplest example: two waves (A and B) that add up to the wave packet (C).
Suppose that the phase velocity varies for different frequencies, what is called
dispersion. In this case, the wave group made by the constructive interference of the
single-frequency waves moves at a different speed than the phase velocity: group and
phase velocities differ. So, in dispersive materials, the phase velocity may approach
infinity without violating the principles of relativity, but only for a single frequency,
because otherwise the group velocity would tend to infinity as well. The cloaking of
electromagnetic waves of fixed frequency is possible, as the successful demonstration
of the microwave-cloaking device has confirmed, but the cloaking of wave packets
carrying information is impossible. It turns out31 that the group velocity actually tends
to zero at the inner lining of such cloaking devices; wave packets would get stuck there
instead of traveling around. Turning invisibility from a tantalizing idea into a practical
device requires a new paradigm.32
Curved Space
Light rays are curved in materials with varying refractive index. In conventional
cloaking devices, the rays are curved because the material performs a transformation
to curved coordinates. However, the curvature of a space does not depend on
coordinates; curved coordinates create the illusion of curvature, but the space they
describe is still flat. A flat space obeys the axioms of Euclidean geometry, in particular
the parallel axiom: through each point outside out of straight line goes exactly one
parallel line; parallels never meet. The light rays focused by a lens clearly violate the
parallel axiom, because parallel light rays meet at the focus of the lens. Optical
materials establish non-Euclidean geometries in general; the Euclidian geometries of
cloaking devices are rather the exceptions. The advantage of Euclidean spaces is that
one can easily visualize them; curved space is difficult to comprehend, in particular
three-dimensional curved space. However, two-dimensional curved spaces can be
visualized as surfaces of three-dimensional curved objects. These surfaces are the
virtual spaces that are implemented, by the optical material, in physical space.
The simplest example is the sphere. On the surface of the sphere, the equivalent of
straight lines, the geodesic lines, are the great circles. The great circles originating from
one point meet again at the antipodal points, which shows that the surface of the
sphere establishes a non -Euclidean geometry. To implement this geometry in the two￾UNCLASSIFIED/ /EAR OFFICIO! I 155 ONL¥
17

[Page 23]
UNCLASSIFIED/ /POK OFFICIAL USE Oilti
dimensional plane, one can use the stereographic projection, the central ingredient of
the Mercator projection in cartography that is used to map the surface of a round
object, the Earth, onto a flat sheet of paper.
A line drawn from the North Pole of the sphere through a point on the surface intersects
the equatorial plane at one point. This point is the stereographic projection of the point
on the sphere. Figure 19 shows that the stereographic projection of a circle on the
sphere is a circle on the plane with a different radius. The stereographic projection
distorts the measure of space, but the distortion around any given point is the same in
all directions, because otherwise circles would be deformed. Therefore, an optical
material that implements the geometry of the sphere via the stereographic projection
must be isotropic. One can read off the required refractive index from the drawing as
follows: in virtual space, on the sphere, light propagates at the speed of light in vacuum
from a point to its infinitesimally close neighbor; in physical space the distance between
the two infinitesimal neighbors is modified-the speed of light is changed by the
refractive index that is given by the ratio between infinitesimal distances in virtual
space and the corresponding distances in physical space. For the stereographic
projection, the refractive index is smaller than 1 for points on the northern hemisphere
and larger than 1 on the southern hemisphere. This device is known as Maxwell's fish￾eye lens. 33 In this lens, light follows the great circles, light goes around in circles, and
light rays meet at antipodal points; the fish-eye makes a perfect lens (although a fairly
near-sighted one). It is possible to extend these ideas to three-dimensional curved
spaces. For example, the surface of the four-dimensional sphere is a three-dimensional
curved space, and the device implementing this hyperspace object is just a three￾dimensional fish-eye. Hyperspace is not out of this world; it can be built, and it turns
out to be practically useful for invisibility. 34
Figure 19. Stereographic Projection
UNCLASSIFIED/ /FOR 8ffl@IAI:: 1:JSi 8PtLY
18

[Page 24]
C
UNCLASSIFIED/fFOA OFFI&iIAk Ulilii ONkY
Broadband Invisibility
To understand why non-Euclidean geometry comes to the rescue of invisibility, consider
the following two-dimensional example. 35 Imagine a virtual space made of a flat space,
a sheet of paper, and a curved space, the surface of a sphere. The two spaces touch at
one line. Consider the fate of light rays in this two-dimensional virtual world. Light rays
would either pass the sphere or enter, through the connecting line, the surface of the
sphere, whereupon, after one loop, they would continue in the same direction as they
entered, as if the tour on the sphere had never happened. The sphere is invisible; it
shows only as a time delay of the light ray. Although the sphere is invisible, it does not
make something else invisible yet. However, this is easily arranged. Imagine a mirror
around the equator of the sphere. The ray bounces off at the mirror, but, after another
bounce, is back on track. A mirror in this curved space reflects light back to itself! The
mirror creates the illusion that the light performs a full great circle, whereas in reality it
stays on one hemisphere. The other hemisphere is hidden. Alternatively, some lines on
the sphere are never crossed by light rays. Such lines can be opened like an eye; the
space they enclose is hidden from sight.
Figure 20. Non-Euclidean Cloaking Device in Two Dimensions. The device creates the illusion shown in A:
light propagates through a virtual space that consists of a plane and the surface of a sphere, a curved space, which
touch along a line. Some incident light rays venture from the plane to the sphere; they return after one loop and
continue in the same direction. Note that the rays never cross the red zigzag line on the sphere. Plane and sphere
carry a coordinate grid that is mapped onto physical space B. The magenta circle defines the boundary of the
device. Its interior has been expanded to make space for the grid of the sphere. In particular, the line where plane
and sphere touch has been opened like an eye (thick black lines) to include the sphere. This is not a cloaking
device yet, but one could place a mirror around the equator of the virtual sphere C, making the northern
UNCLASSIFIED/ /FOR OFFI&iIAk l::18E 8HLY
19

[Page 25]
UNCLASSIFIED/ /FOR: errl@IAL YSI: e ..tv
hemisphere invisible and creating the same illusion as shown in A. Alternatively (D), one could expand the red line
that light never crosses to create a hidden space.
Why are such curved optical spaces of any practical advantage? They seem more
complicated, but the distortion of space in such spaces is always finite, never infinite as
in the conventional Euclidean cloaking devices. As the spatial distortions directly
correspond to the required refractive indices, the required optical properties are never
infinite, and hence such devices can, in principle, operate in a broad band of the
spectrum. Curved space is more practical than flat space, although the theory is more
complicated. These ideas can be extended from the two-dimensional toy model to the
three-dimensional world, but they can no longer be visualized. Figure 21 below shows
some ray trajectories in three-dimensional non-Euclidean cloaking devices.
Figure 21. Three-Dimensional Cloaking. One can extrapolate the ideas illustrated in the previous figure to
three-dimensional space, replacing the plane by flat space and the sphere by a hypersphere. The lentil-shaped
object indicates the hidden interior of the device; the partly shaded grid, the boundary of the invisibility device. For
better contrast, light rays are shown in red. A: Rays are bent around the invisible region . B: In three dimensions,
some rays turn out to perform two loops in hyperspace that appear in physical space as light wrapped around the
invisible interior.
Such non-Euclidean cloaking devices are imperfect because they delay the light
traveling through the cloak. With sensitive timing or wave-front sensing one could, in
principle, detect the presence of the cloaking device. Perfect cloaking is impossible, but
as long as time delays and wave-front dislocations are of no concern, invisibility could
become reality.
Implementation
Non-Euclidean cloaking devices do not have an obvious symmetry like the Euclidean
microwave-cloaking device. 36 They require materials with an electromagnetic response
that varies from cell to cell and is anisotropic. Most probably, such cloaking structures
can be made for microwaves. A precursor of the necessary technology is the recently
demonstrated ground-plate cloak. 37 This device implements the coordinate
transformation shown below (that already appeared in the first paper on cloaking by
UNCLASSIFIED/ /&OR OFFICI.t.k WS& 8,.LY
20

[Page 26]
UNCLASSIFIED/ /FOR: errl@IAL YSIE 8HLY
coordinate transformations). This is not a cloaking device: it compresses an extended
region of space to a reflecting plate; the interior is hidden behind the plate, but the
plate is clearly visible. Such a device conceals the extension and shape of the hidden
region but not the fact of hiding itself.
B
Figure 22. Coordinate Transformation Implemented by a Ground-Plate Cloak
In order to implement the ground-plate cloak, thousands of cells with split-ring
resonators with individual, tailor-made electromagnetic properties were designed, as
Figure 23 shows.
0. 0.8 12 6
mm)
Figure 23. Implementation of the Ground-Plate Cloak38
UNCLASSIFIED//EOR QFFIEIAk WS& 8HLY
21

[Page 27]
UNCLASSIFIED/ /FOA OFfilCIOls. 11 5'5 ON! X
Optical Cloaking
Cloaking in the optical range of the spectrum poses several challenges. The present
design of non-Euclidean cloaking devices still requires materials where, in some parts of
the device, the speed of light is larger than in the environment of the device, which, in
practice, means larger than the speed of light in vacuum. Most probably, this problem
can be circumvented by inventing new designs and new geometrical forms of suitable
curved spaces, because there is no mathematical reason why non-Euclidean cloaking
should be limited in this way. However, solving this problem takes imagination and
mathematical creativity; it cannot be planned by a clear roadmap, but it can be
encouraged and stimulated. It could take 1 or 2 years or a much longer time until such
designs are invented; truly imaginative research is unpredictable. This research takes a
specific mindset, clear mathematical thinking combined with playfulness and physical
intuition, a stimulating environment, and freedom. The greatest challenge for turning
invisibility from an idea into a workable device is not technology but imagination. The
only way to solve this problem is to follow the Solomonic advice to invest in the right
people.
The technology for cloaking will depend on the design of such advanced cloaking
devices. Probably they will require highly anisotropic materials, but perhaps liquid
crystals could be sufficient. Maybe metamaterials are not needed after all. In this case,
invisibility could become a feasible technology within a generation. If optical
metamaterials are needed, they will rely on structuring on extremely short scales,
possibly on sub-nanometer distances. The technology for making such structures will be
developed because the silicon-electronics industry will need them; but whether large￾scale devices with sub-nanometer structures can be made remains to be seen.
Another practical challenge is impedance managing. Ideal cloaking devices require
materials with equal electric and magnetic response because they implement
geometries and geometries are universal-they act on both the electric and the
magnetic fields of electromagnetic waves like light. In practice, broadband optical
materials mostly respond to the electric field but not to the magnetic one. Optical
magnetism has been demonstrated with metamaterials, 39 but only in narrow regions of
the spectrum. If the electric response differs from the magnetic response, the
electromagnetic impedance is mismatched, which results in reflections. One could
reduce such reflections by using smooth refractive-index profiles as appropriate
antireflection coatings.
Most probably, cloaking devices will be rigid shells; to make them flexible like wearable
invisibility cloaks poses a significant challenge. The reason is that their optical
properties must be adjusted to their geometrical shapes, as the refractive-index profile
of a cloaking device depends on its shape. If the shape changes, the index-profile must
follow suit. The required optical properties should be calculated in real time, and the
material should change accordingly. Liquid crystals could adjust their optical properties,
but controlling a large, complicated array of liquid crystals with possibly several layers
appears to be difficult, despite the progress made in liquid-crystal displays.
UNCLASSIFIED/ /FOA OFFI&I.t.k W&li &P•kY
22

[Page 28]
UNCLASSIFIED/ /FOR OFFI@IAL l::ISE OHL¥
Summary
A cloaking device is a passive device made of a transparent material that guides light
around any object in its interior as if the light has passed through empty space. The
cloaking device conceals the object and hides the act of hiding itself. Perfect cloaking
devices are impossible because they require materials where t he speed of light
approaches infinity. Imperfect cloaking devices could be made. Such devices implement
suitable curved-space geometries. For electromagnetic microwaves, cloaking devices
are definitely within reach of the present technology. Whether invisibility in the visible
range of t he spectrum will become a reality is not entirely clear yet. Most probably, this
will depend more on the new theoretical research than on advances in new materials,
and on the application of mathematical intelligence, intuition, and imagination.
1 A. Alu and N. Engheta, Achieving transparency with plasmonic and metamaterial coatings, Physical Review E 72,
016623 (2005).
2 G. W. Milton and N.-A. P. Nicorovici, On the cloaking effects associated with anomalous localized resonance,
Proceed ings of the Royal Society London A 462, 3027 (2006).
3 Y. Lai, H. Chen, Z-Q. Zhang, and C. T. Cha n, Complementary Media Invisibility Cloak that Cloaks Objects at a
Distance Outside the Cloaking Shell, Physical Review Letters 102, 093901 (2009).
4 U. Leonhardt, Optical Conformal Mapping, Science 312, 1777 (2006). 5 J. B. Pendry, D. Schurig, and D. R. Smith, Controlling Electromagnetic Fields, Science 312, 1780 (2006). 6 J. B. Pendry, D. Schurig, and D. R. Smith, Controlling Electromagnetic Fields, Science 312, 1780 (2006). 7 U. Leonhardt and T. G. Phi lbin, Transformation Optics and the Geometry of Light, preprint arXiv:0805.4778, to
appear in Progress in Optics.
8 U. Leonhardt and T. G. Philbin, Transformation Optics and the Geometry of Light, preprint arXiv :0805.4778, to
appear in Progress in Optics.
9 U. Leonhardt, Optical Conformal Mapping, Science 312, 1777 (2006). 10 J. B. Pendry, D. Schurig, and D. R. Smith, Controlling Electromagnetic Fields, Science 312, 1780 (2006) . 11 D. Schurig, J. J. Mock, B. J. Justice, S. A. Cummer, J. B. Pendry, A. F. Starr, and D. R. Smith, Metamaterial
Electromagnetic Cloak at Microwave Frequencies, Science 314, 977 (2006). 12 U. Leonhardt, Optical Conformal Mapping, Science 312, 1777 (2006). 13 D. Schurig, J. J. Mock, B. J. Justice, S. A. Cummer, J. B. Pendry, A. F. Starr, and D. R. Smith, Metamaterial
Electromagnetic Cloak at Microwave Frequencies, Science 314, 977 (2006). 14 D. Schurig, J. J. Mock, B. J. Justice, S. A. Cummer, J. B. Pendry, A. F. Starr, and D. R. Smith, Metamaterial
Electromagnetic Cloak at Microwave Frequencies, Science 314, 977 (2006).
15 D. Schurig, J. J. Mock, B. J. Justice, S. A. Cummer, J. B. Pendry, A. F. Starr, and D. R. Smith, Metamaterial
Electromagnetic Cloak at Microwave Frequencies, Science 314, 977 (2006).
16 D. Schurig, J. J. Mock, B. J. Justice, S. A. Cummer, J.B. Pendry, A. F. Starr, and D. R. Smith, Metamaterial
Electromagnetic Cloak at Microwave Frequencies, Science 314, 977 (2006). 17 F. E. Wagner, S. Haslbeck, L. Stievano, S. Ca logero, Q. A. Pan khurst, and P. Martinek, Before striking gold in
gold-ruby glass, Nature 407, 691 (2000).
18 D. Schurig, J. J. Mock, B. J. Justice, S. A. Cummer, J.B. Pendry, A. F. Starr, and D.R. Smith, Metamaterial
Electromagnetic Cloak at Microwave Frequencies, Science 314, 977 (2006).
19 W. Cai, U. K. Chettiar, A. V. Kildishev, and V. M. Shalaev, Optical cloaking with metamaterials, Nature Photonics
1, 224 (2007).
20 W. Cai, U. K. Chettiar, A. V. Kildishev, and V. M. Shalaev, Optical cloaking with metamaterials, Nature Photonics
1, 224 (2007). 21 C. M. Soukoulis, S. Linden, and M. Wegener, Costas M. Soukoulis, Stefan Linden, and Martin Wegener, Negative
Refractive Index at Optical Wavelengths, Science 315, 47 (2007).
22 C. M. Soukoulis, S. Linden, and M. Wegener, Costas M. Soukoulis, Stefan Linden, and Martin Wegener, Negative
Refractive Index at Optical Wavelengths, Science 315, 47 (2007). 23 J. Yao, Z. Liu, Y. Liu, Y. Wang, C. Sun, G. Barta!, A. M. Stacy, and X. Zhang, Optical Negative Refraction in Bulk
Metamaterials of Nanowires, Science 321 , 930 (2008).
24 J. Valentine, S. Zhang, T. Zentgraf, E. Ulin-Avila, D. A. Genov, G. Barta!, and X. Zhang, Three-dimensional
optica l metamaterial with a negative refractive index, Nature 455, 376 (2008). 25 U. Leonhardt and T. G. Philbin, General relativity in electrical engineering, New Journal of Physics 8, 247 (2006). 26 (11 ) J. Yao, Z. Liu, Y. Liu, Y. Wang, C. Sun, G. Barta!, A. M. Stacy, and X. Zhang, Optical Negative Refraction in
Bulk Metamaterials of Nanowires, Science 321, 930 (2008).
23
UNCLASSIFIED/,CFOA OFFI&I.t.L l::ISE OHL¥

[Page 29]
UNCLASSIFIED// FOR OFFICIAL USE ONLY
27 J. Valentine, S. Zhang, T. Zentgraf, E. Ulin-Avila, D. A. Genov, G. Bartal, and X. Zhang, Three-dimensional
optical metamaterial with a negative refractive index, Nature 455, 376 (2008).
28 U. Leonhardt and T. G. Philbin, General relativity in electrical engineering, New Journal of Physics 8, 247 (2006). 29 U. Leonhardt and T. Tye, Broadband Invisibility by Non-Euclidean Cloaking, Science 323, 110 (2009). 30 U. Leonhardt and T. Tye, Broadband Invisibi lity by Non-Euclidean Cloaking, Science 323, 110 (2009).
31 H. Chen and C. T. Chan, Time delays and energy transport velocities in three dimensional idea l cloaking devices,
Journal of Applied Physics 104, 033113 (2008).
32 U. Leonhardt and T. Tye, Broadband Invisibility by Non-Eucl idean Cloaking, Science 323, 110 (2009).
33 M. Born and E. Wolf, Principles of Optics (Cambridge University Press, Cambridge, 1999). 34 U. Leonhardt and T. Tye, Broadband Invisibility by Non-Euclidean Cloaking, Science 323, 110 (2009).
35 U. Leonhardt and T. Tye, Broadband Invisibility by Non-Euclidean Cloaking, Science 323, 110 (2009).
36 D. Schurig, J. J. Mock, B. J. Justice, S. A. Cummer, J. B. Pendry, A. F. Starr, and D. R. Smith, Metamaterial
Electromagnetic Cloak at Microwave Frequencies, Science 314, 977 (2006). 37 R. Liu, C. Ji, J. J. Mock, J. Y. Chin, T. J. Cui, and D. R. Smith, Broadband Ground-Plane Cloak, Science 323, 366
(2009).
38 R. Liu, C. Ji, J. J. Mock, J. Y. Chin, T. J. Cui, and D. R. Smith, Broadband Ground-Plane Cloak, Science 323, 366
(2009). 39 C. M. Soukoulis, S. Linden, and M. Wegener, Costas M. Soukoulis, Stefan Linden, and Martin Wegener, Negative
Refractive Index at Optical Wavelengths, Science 315, 47 (2007).
UNCLASSIFIED//509 OEEICI0 .. Uili QPUEY
24
