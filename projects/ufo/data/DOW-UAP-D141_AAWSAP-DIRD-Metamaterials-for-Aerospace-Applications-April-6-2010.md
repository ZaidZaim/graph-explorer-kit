# Historical Document: DOW-UAP-D141_AAWSAP-DIRD-Metamaterials-for-Aerospace-Applications-April-6-2010

## Source Metadata

- Original file: `DOW-UAP-D141_AAWSAP-DIRD-Metamaterials-for-Aerospace-Applications-April-6-2010.pdf`
- Pages: 38 (35 from text layer, 0 OCR, 3 illegible)
- OCR language: `eng`
- Processed at: `2026-09-23T18:08:43.498216+00:00`
- Processing pipeline: `pypdfium2 text layer + Tesseract OCR → Markdown → neo4j-graphrag SimpleKGPipeline`

## Text

[Page 1]
UNCLASSIFIED / /FOR-OFFECHHE-USE-ONE—
KERR Defense
Ay Intelligence
OAs) Reference
_ Document
yr ti‘(‘éCS' Acquisition Threat Support
6 April 2010
ICOD: 1 December 2009
DIA-08-1004-006
Metamaterials for Aerospace
Applications
UNCLASSIFIED/ /POR-OPFTCEAE-USE-ONE—

[Page 2]
UNCLASSIFIED/ {FOR OEFICIP.L YSE 8Ntt
Metamaterials for Aerospace Applications
Prepared by:
Acquisition Support Division (DW0-3)
Defense Warning Office
Directorate for Analysis
Defense Intelligence Agency
Author:
AAP Person 78
Administrative Note
COPYRIGHT WARNING: Further dissemination of the photographs in this publication is not authorized.
This product is one in a series of advanced technology reports produced in FY 2009
under the Defense Intelligence Agency, Defense Warning Office's Advanced Aerospace
weapon System Applications (AAWSA) Program. Comments or questions pertaining to
this document should be addressed to JAAP Person 1 J AAWSA Program
Manager, Defense Intelligence Agency, ATTN: CLAR/DWO-3, Bldg 6000, Washington,
DC 20340-5100.
UNCLASSIFIED/ /EOR OEFICI,t.L W8!! e»Ntt
ii

[Page 3]
UNCLASSIFIED/ (fQR OFFIClt.k YSE 8HLI
Contents
Definition of Metamaterials .................................................................................... 1
Applications to Sub-Diffraction Imaging: Super-Lens and Hyper-Lens .................. 6
Applications to Circuits and Waveguide Miniaturization: Slowing Down and
Manipulating Electromagnetic Pulses (EMP) Using Advanced Metamaterials ....... 16
Metamaterials for Energy Harvesting ................................................................... 20
Nonlinear Non-Reciprocal Chiral Metamaterials: For Developing Novel Optical
Isolators and "One-Way" Microwave Mirrors ....................................................... 27
Tunable Switchable Metamaterials ....................................................................... 30
Summary and Conclusions ................................................................................... 31
References ........................................................................................................... 31
Figures
Figure 1. Example of a Metamaterial Component: The Magnetic Split Ring
Resonator (SRR) Design .......................................................................... 2
Figure 2. Example of Another Metamaterial Component: Electric Ring Resonator
Figure 3. Geometry of Original Planar Metamaterial Unit Cells (OE1-OE6) and Their
Figure 4. Recent Optical Metamaterials for Telecommunication Wavelength and
Figure 6. Schematic of the SiC-based Super-lens Which is Imaging Sub-wavelength
(ERR)......................................................................................................... 2
Complements (CE1-CE6) ......................................................................... 3
Mid-Infrared Indefinite Permittivity Material .......................................... 5
Figures. Schematic of The Super-lens With n=-1 Refractive Index Corresponding
to ( Surrounded by Vacuum ..................................................................... 7
Holes Buried Under the SiO2 Layer.......................................................... 8
Figure 7. Theoretical Concepts (left panel) and Experimental Implementation
(right panel) of an Optical Hyperlens Capable of Magnifying Sub￾Diffraction Objects to Observable (larger than Size................................. 9
Figure 8. Hyperlens Based on a Converging Array of Metal Wires ........................ 10
Figure 9. Far-Field Super-lens (FSL) Based on an Indefinite Permittivity
Metamaterial Placed Between the Object and the Image-Releasing
Grating .................................................................................................. 12
Figure 10. Tomographic Multi-Beam Multi-Detector Holography of Sub-Wavelength
Objects Using Indefinite Permittivity Medium (IPM) ........................... 12
Figure 11. First Experimental Demonstration of Propagating Sub-Diffraction Waves
Figure 12. Schematic for 2-Beams/2-Detectors Interferometric Measurement
Figure 13. Experimental Setup for 2-Beams/2-Detectors Interferometric
in the Indefinite Permittivity Medium (IPM) ....................................... 13
and Numerical Simulation................................................................... 14
Measurement in the Lab and Preliminary Experimental Results .......... 15
UNCLASSIFIED/ {fQR OFEICl.t.ls: W81!! 8flti
iii

[Page 4]
UNCLASSIFIED//POR: OPPlelAL liSE 8PtLY
Figure 14. Schematic of Pulse Compression in Magnetized Plasma ...................... 16
Figure 15. Trapped Rainbow: A Waveguide With Negative Index Core Can Stop
Light.................................................................................................... 17
Figure 16. "Plasmonic Molecule" Exhibiting EIT ................................................... 18
Figure 17. True Multi-Layer Metamaterial With a Unit Cell Shown in Figure16:
Radiative Antenna (Single Metal Strip) Coupled to a Dark Antenna
(Two Perpendicular Metal Bars) .......................................................... 19
Figure 18. "Perfect" Narrow-Band Microwave Absorber....................................... 20
Figure 19. Wide-Angle Plasmonic Absorber Based on Negative Index
Metamaterial ....................................................................................... 21
Figure 20. Specific Design of a Wide-Angle Plasmonic Absorber Based on Negative
Index Metamaterial Operating at A= 1550 nm ..................................... 22
Figure 21. Experimental Reflectivity vs. Wavelength and Theoretical Plot of
Reflectivity Contours ........................................................................... 23
Figure 22. Preliminary Attempts to Design a Better Absorber Using Complementary
MetaMaterials (U-shaped C-MM) ......................................................... 25
Figure 23. Engineering the Complex Reflectivity Coefficient Using the Concept of a
MetaMirror.......................................................................................... 26
Figure 24. Example of a Generic Chiral Metamaterial ........................................... 28
Figure 25. Example of Time-Irreversibility of Light Propagation Inside the Twisted
Fiber Core............................................................................................ 29
Figure 26. THz Properties of an Electric Split Ring Resonator .............................. 31
UNCLASSIFIED/ {EAR OFEICll.k WSI!! eNti
iv

[Page 5]
UNCLASSIFIED/ (FOR OFFIClt.k YSE 8Htt
Definition of Metamaterials
A metamaterial is defined as an artificial medium whose properties (mechanical, optical,
magnetic, or other) cannot be found in naturally-occurring materials. The emphasis of
this study will be on electromagnetic and optical metamaterials. Such metamaterials
can exhibit rather extreme properties, such as negative refractive index, which implies
that both electric permittivity and magnetic permeability must be negative
( £ < 0 µ < 0) (Reference 1). Such meta materials used to be called "left-handed" I
because of the unusual phase relationship between the electric and magnetic fields.
Specifically, in most (positive index, including vacuum) media one uses the right-hand
rule to define the relationsh[p between electric field ( E) magnetic field ( H), and the
propagation wavenumber ( f ). The physical basis of the right-hand rule is that the
direction of energy propagation defined by the Poynting vector S=cEx HI 47Z' and the
direction of the phase velocity (defined by the wavenumber k) must coincide. That
does not hold true for negative index metamaterials where the two directions are
opposite, therefore, t he left-handed relationship must hold for the three vectors.
Nevertheless, the "left-handed" designation did not withstand the test of time because
it was causing confusion and creating irrelevant allusions to helica l (a.k.a. chiral)
structures. Although chiral structures can indeed exhibit negative index behavior
(Reference 2), chirality is not necessary.
A typical metamaterial consists of resonant elements such as Split Ring Resonators
(SRR). An example of an SRR is shown in Figure 1. The main function of the SRR is to
enable strong magnetic response of the structure. A simple empirical formula exists for
the magnetic permeability of a metamaterial comprised of the SRRs:
(1)
where {J)M is the resonant frequency of the SRR, and F is proportional to t he volume
filling factor of SRRs. It is noteworthy that SRRs are designed in such a way that it has
a large capacitance. As the result, the resonant frequency of an SRR is small, (that is,
the SRR-containing cell is very sub-wavelength). In the example shown in Figure 1
(taken from Reference 6), the unit cell operated at {J)j27Z" = 10 GHz is A/10. I n fact, the
sub-wavelength size of the meta material is what distinguishes them from their close
cousins: photonic crystals. By properly designing magnetic SRRs, it is possible to
achieve any value of µ for any given frequency. Special challenges exist for optical
structures, though, as will be explained below.
UNCLASSIFIED/ {fQR OFEICl.t.ls: W81!! 8flti
1

[Page 6]
UNCLASSIFIED/ (EOR OFFICit.k W&E 8Htt
C I. r I.Lr
I 0.260 1.654 0.003
2 0.254 1.677 .023
3 0.-45 1.7 1 .052
4 0. 0 1.771 .0
0.20 I. 25 .1..0
6 0.190 I. 6 .1
7 0.17 1.9 I . I
0.148 2.027 .220
9 0.129 2.110 .2 0
10 0.116 2. 0.279 -,-........,. _____.,___, ,---··, _ _ _ ,,.... .. ,~
in-plane lattice parameters are av= a,= 10/3 mm, The ring is square, with edge length I =3 mm and tracewidth w
= 0. 2 mm. The substrate is 381 µm-thick Duroi d 5870 (E = 2.33, td = 0.0012 at 10 GHz, where td is the loss
ta ngent). The Cu fi lm, from which t he SRRs are patterned, is 17 µm thick. The parameters rand s are given in the
ta ble together with the associated value of µ,. (Reference 6)
Electric properties of metamaterials can be similarly controlled. An example of a planar
electrically-active metamaterial is shown in Figure 2.
r1yun: .L , cxc1mp1t: u, i:I r111::cc1 mc1 c11::nc11 1.,umpun 11::nc; 1 n - ,.,_,..,_., _
-
- Figure 2. Example of Another Metamaterial Component: Electric
Ring Resonator (ERR). This component provides tunable resonant
electric response to the incident electromagnetic field, and can be
util ized for engineering the frequency -dependent dielectric
permittivity &(w) . Possi ble application : THz and microwave absorbers,
(Reference 7)
UNCLASSIFIED/ {EAR OFFICIAk W81!!! Bflti
2

[Page 7]
UNCLASSIFIED//POR. Offl@IAL YS! OP~LV
The electric response of such (or similar) metamaterial is given by
(2)
where w R is the resonant frequency and r is the loss coefficient.
Negative index metamaterials are by no means the only potentially useful metamedia.
Several new concepts such as Indefinite Permittivity Metamaterials (1PM) (References
3, 4) and Epsilon-Near-Zero (ENZ) metamaterials (Reference 5) have recently emerged
and found some exciting applications t hat will be reviewed below. IPMs ca n be used as
ultra-compact spatial filters (both high-pass and low-pass) whereas ENR metamaterials
can be used for making sub-wavelength waveguides capable of coupling close to 100
percent of the incident radiation (Reference 8), as well as directing it around tight
bends with negligible bending losses. Yet another class of planar metamaterials,
complementary metamaterials (CMMs), has recently emerged (Reference 7). Instead of
using metallic structures deposited on a substrate (left panel of Figure 3), CMMs consist
of slits in the continuous metal screen (right panel of Figure 3). The shape of the slits
coincides with that of the materials themselves. Such complementary metamaterials
have been recently used for making epsilon-near zero waveguides (Reference 8).
CE1 CE4
CE2 CE5
CE3 CE6
Figure 3. Geometry of Original Planar Metamaterial Unit Cells (OE1-0E6) and Their Complements
(CE1-CE6}. The polarization of normally incident electromagnetic rad iation is configured as shown in OEl
and CEl for the original and complementary metamaterials, respectively. (Reference 9)
UNCLASSIFIED/ {EAR OFFICI.IJ.k WSI!!! tJflti
3

[Page 8]
UNCLASSIFIED/ (EAR OFEICJ0k W&E 8Htt
In general, metamaterials offer a new way of designing electromagnetic structures with
arbitrary values of permittivity/permeability tensors, as well as other parameters (such
as bi-anisotropy coefficient). In many instances, metamaterials enable us to
considerably minimize sizes of resonators, transmission lines, and so forth. Such
miniaturization is possible due to the resonant nature of the individual unit cells.
Specifically, the structures shown in Figure 3 have high capacitance; therefore, their
individual sizes are very sub-wavelength. That enables arrangement within sub￾wavelength units that can be densely packed and result in strongly miniaturized
components. It is this miniaturization that makes metamaterials interesting for
aerospace application where small weight and size are essential.
While the most spectacular progress in the field of electromagnetic metamaterials has
so far occurred in the microwave range, it is the optical (visible, infrared, mid-infrared)
spectral regions that hold most promise for revolutionary applications. Electromagnetic
metamaterials have a tremendous potential for revolutionizing propagation, storage,
and conversion of electromagnetic waves across the entire Electromagnetic Spectrum.
In our opinion, the most exciting applications that are relevant for aerospace
applications include energy harvesting, developing novel optical devices with unusual
yet practically important capabilities (for example, non-reciprocal devices), enhancing
the efficiency of nonlinear optical devices, developing novel imaging modalities capable
of breaking the diffraction limit (for example, super-lenses, hyper-lenses, far field
super-lenses), and developing novel lithographic techniques.
Optical metamaterials are still a very new area. Just a handful of experimental
demonstrations of multi-layer (truly bulk) optical metamaterials exist at the moment.
Among the most recent ones are (a) demonstration of the negative index optical
metamaterial at the telecommunications wavelength (Reference 10) that used the so￾called fishnet structure shaped as a prism for demonstrating Snell's Law, and (b)
demonstration of the Indefinite Permittivity Material (IPM) and negative refraction
(which, in the context of anisotropic metamaterials, is not the same as negative
refractive index) in the mid-infrared part of the spectrum (Reference 11). These
structures have the distinction of being multi-layer (or bulk). Most previous examples of
optical metamaterials have dealt with single or double-layer substances which cannot
be, strictly speaking, characterized as metamaterials. The difficulty in obtaining strong
magnetic activity in optical metamaterials has been explained in several recent reviews
(References 12, 13). In a nutshell, the issue is that the magnetic moment of most
structures (including atomic systems) is very small, much smaller than the electric
moment. Therefore, it is difficult to observe any optical effects that can be clearly
assigned to magnetic activity. This is especially true for the structures that are much
smaller than one wavelength. Exceptions, such as artificially constructed split rings, are
possible. However, such structures cannot be operated at very high frequency because
of the excitation of electrostatic resonances (Reference 12). In other words, when the
resonant frequency is too high (or the dielectric permittivity of a metal is not sufficiently
large), electrostatic resonances disrupt magnetic activity. More specifically, the energy
inside and in the vicinity of a metamaterial element (for example, Split Ring Resonator)
becomes predominantly electrostatic, (that is, in the form of the kinetic energy of
oscillating electrons). The recently described multi-layer fishnet (Reference 10) is not
an exception: its unit cell (that is, the lateral period) is only one-half of the operating
wavelength.
UNCLASSIFIED/ {EAR OFEICll.k W8I!! eNti
4

[Page 9]
UNCLASSIFIED/ ( FOR OFFIClt.k YSE 8Htt
10 12 14
WmOfllllll{)lml
Figure 4 . Recent Optical Metamaterials for Telecommunication Wavelength A = 1.5 1,1m (Left and
Middle) and Mid-Infrared IPM. The multi-layer fishnet is made of si lver films separated by a dielectric spacer. A
focused ion beam was used to produce the prism-shaped fishnet. The 1PM was obtained by depositing interleaved
80 nm layers of Ino.s3Gao.41As and Alo.. slno.s2As. The layers, approximately 8.1 µm thick, grown by molecular beam
epitaxy on lattice-matched InP substrates. The InGaAs layers were uniformly doped to create different values of
permittivity in alternating layers. (Reference 10 and 11)
That is not to say that there is not ongoing theoretical and experimental work on
designing optical metamaterials for practical applications. The author's research group
at UT- Austin, has designed the first Plasmonic Negative Index Metamaterials (P-NIM)
super-lens (Reference 14 ), developed novel techniques for analyzing optical properties
of plasmonic nanostructures, (including band-structure calculations of periodic
nanostructures) (Reference 15) and quasi-static calculations of plasmonic resonances
(Reference 16). The UT-Austin group has also designed a number of unique sub￾wavelength P-NIMs in the optical part of the spectrum (References 14, 17, 18), and has
recently published a review of optical P-NIMs (Reference 12). The group has also
contributed to developing and experimentally implementing the concept of the "perfect
lens" (Reference 19) based on plasmonic/polaritonic materials. A perfect lens enables
imaging of sub-wavelength objects in the infrared part of the spectrum, including
objects buried under the surface. Also developed is a Wide-Angle "Perfect" Absorber of
Mid-Infrared Radiation {WAPAMIR) (Reference 20) based on the negative index
metamaterial whose impedance is perfectly matched to vacuum.
Below is a concise summary of various topics/applications that are especially suitable
for the aerospace industry. This study concentrates on the facility of meta materials to
miniaturize various optical and microwave components. Metamaterials can also be used
for imaging very small (sub-wavelength) objects without resorting to costly and space￾consuming near-field scanning optical microscopy. Also described are the ongoing
efforts in the field to make extremely compact metamaterials-based lasers. Smaller
lasers mean smaller weight and more room for other diagnostic devices and useful
payload within the confines of a space vehicle. Applications of metamaterials to photon
harvesting is especially fitting for advanced aerospace platforms because of the
necessity to collect electromagnetic energy for battery recharging, diagnostic
spectroscopy, and other vital functions of a space vehicle.
• Complementary Metamaterials for Energy Harvesting. Development of ultra￾thin photovoltaic and thermo-photovoltaic cells is hampered by weak photon
absorption in semiconductors. Metamaterials can modify absorption making it
wavelength-selective (tunable), highly efficient, and, if desired, wide-angle. Recently
a way has been found for creating quarter-wavelength resonators backed by leaky
mirrors made out of CMMs.
5
UNCLASSIFIED/ {fQR OFEICl.t.ls: W81!! 8flti

[Page 10]
UNCLASSIFIEr,//POR: OPPIEll<L tt.!I!! 9HL3f
• Far Field Super-Lens Based on the Interferometry of Sub-Diffraction Waves.
Sub-diffraction imaging has long been considered to be possible only using near￾field microscopes. Those are fairly complex, slow-scanning, and large devices that
are not appropriate for advanced aerospace platforms. Metamaterials enable new
imaging modalities: super-lenses, hyper-lenses, and far-field super-lenses. In
addition to a survey of the existing scientific literature, novel ideas on developing a
new interferometric Far-field Super-Lens (FSL) based on the multi-beam multi￾detector technique utilizing materials with Indefinite Permitivity Tensor are
presented. Fabrication of such Indefinite Permittivity Materials (IPMs) for the mid￾infrared part of the spectrum is achieved and demonstrates the capabilities of
transmitting electromagnetic waves with the spatial period much smaller than the
vacuum wavelength of light. Interference between sub-diffraction waves enables
disentangling multiple diffractive orders and extracting their amplitudes.
• Nonlinear Non-Reciprocal Chiral Metamaterials: Developing Novel Optical
Isolators and "One-Way" Microwave Mirrors. These developments are
motivated by the need to construct one-way "light diodes" for compact optical
isolators. Presently there are two approaches to optical isolation: the most common
using magnetic fields, and the less developed based on using nonlinearities. A
different approach relies on the phenomenon of adiabatic mode conversion in
nonlinear chiral metamaterials. Preliminary theoretical results for a simple chiral
fiber with a variable twist period (pitch) that enables full transmission of a tightly
confined core mode in the forward direction and full mode-conversion of the core
mode into a cladding mode for the backwards propagation is obtained.
• Slowing Down Light and Miniaturizing Optical Components Using the
Phenomenon of Electromagnetically Induced Transparency in
Metamaterials. The speed of light places a natural limit on the size of
optical/microwave components. Metamaterials offer an exciting opportunity to slow
down light. This has two major implications: (a) light can be stored/manipulated in
smaller volumes, and (b) nonlinear effects are strongly enhanced by the resulting
energy compression.
Applications to Sub-Diffraction Imaging: Super-Lens and
Hyper-Lens
The super-lens is one of the earliest applications of metamaterials (Reference 21), and
its principle is shown is Figure 5. Without the super-lens, all information about sub￾diffraction (or sub-wavelengths, which is equivalent) features of the periodic object
would have been lost. The reason for the information loss is evanescent decay of the
large spatial wavenumbers. The only method of accessing/measuring these features
would be to scan the object using a near field scanning optical microscope. By inserting
a super-lens between the object and the imaging plane, evanescent waves may be
amplified and the image transferred forward. Unfortunately, this approach by itself does
not remove the need for a near-field scanning device; the image that is recreated in the
imaging plane is still sub-wavelength, and needs to be read out.
UNCLASSIFIED/ {EAR OFEICl.t.ls: Y81!! 9flti
6

[Page 11]
UNCLASSIFIED/ (fQR OFFIClt.k YSE 8HLI
A>d
..
Figures. Schematic of the Super-Lens with n=-1 Refractive Index Corresponding to(£= -1, µ =-1)
Surrounded By Vacuum. Super-lens' presence enables imaging sub-diffraction objects such as the periodic
grating shown here.
There are, however, interesting circumstances when it is very important to transport
the image towards the scanning device. One such special circumstance is spatially￾resolved spectroscopy of small (for example, cellular) structures. One can envision
space expeditions to other planets that could, potentially, result in finding some
evidence of primitive cellular-level life. It would then be highly desirable to examine the
structure of the living cell in its natural environment. In all likelihood, that environment
would be liquid. Therefore, it would be very desirable to examine the cell without
actually touching it with a tip of a near-field optical microscope. Thus, the sub-surface
imaging of a small object which is buried underneath a liquid layer would be necessary.
No such experiments have so far been conducted. However, several years ago there
was an experiment demonstrating imaging of sub-diffraction objects buried under the
layer of silicon dioxide.
The schematic and experimental results from the experiment (Reference 19) are shown
in Figure 6. In this experiment the sub-wavelength objects were simple holes that were
milled in the metal using an FIB. They were buried underneath the super-lens
consisting of SiC (negative epsilon material for mid-infrared frequencies) and silicon
dioxide (positive epsilon material). Note that this configuration (materials with 6 1 > 0
and 62 ~ - 61< 0 joined together: sandwiched or positioned next to each other) is typical
for a near-field super-lens. The difference between the near-field super-lens shown in
Figure 6 and the "ideal" super-lens shown in Figure 5 is that the ideal also requires a
material with a negative value of magnetic permeability.
UNCLASSIFIED/ {fQR OFEICl.t.ls: W81!! 8flti
7

[Page 12]
UNCLASSIFIED/ (fQR OFFIClt.k YSE 8HLI
a
Figure 6. Schematic of the SiC-Based Super-Lens Which is Imaging Sub-Wavelength Holes Buried Under
the Si02 Layer. The imaged objects are >../20 holes milled in gold using FIB. The scattered signal is picked up by
the tip of an NSOM and directed towards the IR detector. Depending on the imaging wavelength, either amplitude
(e) or the phase (f,g) of the signal are prominent.
As the laser beam scatters off the sub-wavelength holes, its electric field is picked up
by the tip of a Near-Field Scattering Optical Microscope (NSOM) and re-scattered into
the far-field. There it is interfered with the reference pulse and picked up by an infrared
detector. Note that this interferometric technique enables one to extract both the phase
and amplitude of the field, as shown in Figure 6. This significantly broadens the spectral
range over which the super-lens yields meaningful information . For example, the
amplitude contrast is highest at A = 10.85 µm shown in panel ( e) while the phase
contrasts are the highest at A =11.03 µm and A =10.65 µm.
UNCLASSIFIED/ {fQR OFEICl.t.ls: W81!! 8flti
8

[Page 13]
UNCLASSIFIEr,,} POR: OPPIEll<L tt.!I!! 8HL'f
Despite the convenience of the near-field super-lens, (that is, its ability to transport the
image) it still requires an NSOM to read out the image. Within the confines of an
advanced aerospace platform such device (with its necessary auxiliaries) may not fit.
Therefore, one has to consider alternative metamaterials-based ideas for sub-diffraction
imaging. One such idea, the hyper-lens, has been proposed recently by two groups
(References 22-24), and already experimentally tested by another group (Reference
25). The principle of the hyper-lens is very simple: to use an indefinite permittivity
medium (sometimes referred to as the hyperbolic medium because the relationship
between the propagation wavenumbers and the frequency, also known as the constant
frequency contour, has a hyperbolic nature) in a tapered format. Several conceptual
implementations such as the spoke-like structure and the cylindrical multi-layer
structure (see Figure 7, left panel) have been suggested. The hyper-lens works on two
principles: (a) indefinite permittivity materials (of which t he super-lens is one example)
are capable of propagating sub-diffraction waves, and (b) the expanding nature of the
hyper-lens can magnify images to the 'A./2 size, at which point they become observable
in a conventional microscope. One recent experimental implementation of the hyper￾lens in UV is shown in the right panel of Figure 7. The hyper-lens is made of 16 layers
of Ag/ AbOJ. This specific hyper-lens was used for imaging a line pair object with line
width of 35 nm and spacing of 150 nm and was operated at>,., =400 nm . The magnified
image (350 nm spacing) can be clearly resolved with an optical microscope [numerical
aperture (NA) = 1.4], t hus demonstrating magnification and proj ection of a sub￾diffraction-limited image into the far field.
Jacob, Alekseyev, Narimanov, Opt.Exp.'06
1To the fir-field opllCI 1
Salandrino & Engheta, PRB'06 Govyadinov & Podolsky, Liuet.al, Science'07
PRB'06
Figure 7. Theoretical Concepts (left panel) and Experimental Implementation (right panel) of an Optical
Hyper-lens Capable of Magnifying Sub-Diffraction Objects to Observable (larger than A,/2) Size
UNCLASSIFIED/ {EAR OFFICI.IJ.k W81!! tJfltf
9

[Page 14]
UNCLASSIFIED/ (FOR OFEICI0k YSE 8Htt
Note that the hyper-lens concept does not require employing a bulky near-field
scanning optical microscope. However, the practical implementation of the hyper-lens is
by no means simple. The original implementation required depositing the sample on the
curved surface of the hyper-lens. A more practical implementation of the super-lens has
been theoretically proposed by another group (Reference 26). The concept is shown in
Figure 8. The hyper-lens involves an array of thin metallic wires converging towards the
tip. As is demonstrated, a dense array of metal wires separated by much less than the
wavelength constitutes a metamaterial with the indefinite permittivity tensor.
Specifically, the tensor component along the wires is given by:
(3)
where the z component is along the wires and perpendicular direction is normal to the
wires. Because the only propagating waves are the TEM waves satisfying the
o/ =k; c2 dispersion relation, this meta-medium is strongly anisotropic and supports
sub-wavelength waves which perform imaging. The spatial resolution is given by the
spacing between wires. Figure 8 (right panel) shows the magnified image of a small
('A/25) object placed at the tip of the hyper-lens. The magnification factor is Sx.
5
30-
20. 2
15-
5-.
0
-4 :·
-5------------------- -1 o __. 0 X!L0 -5 5
5
-5 -5
Figures. Hyper-Lens Based on a Converging Array of Metal Wires. A small object can be placed at the tip,
illuminated from the top, and magnified by the expanding array of wires. Left panel : schematic. Right panel: A./25
object magnified by a factor Sx by the expanding hyper-lens. This hyper-lens can operate at mid-IR frequencies.
(Reference 26)
Another concept for sub-wavelength imaging employing metamaterials is the so-called
Far-Field Super-Lens (FSL). The concept is pioneered in Reference 27. The idea is
10
UNCLASSIFIED/ {EAR OFFICI.IJ.k W81!!! Britt

[Page 15]
UNCLASSIFIED/ (EAR OFEICJ0k W&E 8Htt
described in Figure 9. A sub-wavelength object (for example, two slits) is located at the
bottom of a multi-layer super-lens. Another sub-wavelength grating is deposited on top
of the super-lens. Because the super-lens (and for that matter, any indefinite
permittivity material) is capable of propagating sub-diffraction waves, the
electromagnetic perturbations created by the object are propagated through the super￾lens upwards, until they encounter the sub-wavelength grating. At that point these sub￾wavelength perturbations are diffracted on the image-releasing grating and converted
into the far-field electromagnetic waves. Those far-field waves are collected by the
objective of a microscope and observed through the eyepiece. The schematic is shown
in Figure 9(a). Note that, again, there is no need for NSOM . The actual implementation
of the FSL used the following object: a nanowire pair with 50 nm wide slit and 70 nm
gap inscribed by focused ion beam on a 40 nm thick Cr film on the quartz substrate.
Diffraction-limited image from a conventional optical microscope cannot resolve the two
nanowires (NA = 1.4, Ao= 377 nm) as can be seen in Figure 9(c), but the FSL-equipped
microscope can as shown in Figure 9(d).
Despite the success of this demonstration, there are serious issues involved in imaging
sub-wavelength objects. Specifically it is pointed out in Reference 27 that multiple
diffractive orders can become entangled, (that is, launched in the same direction into
the far field). Disentangling these diffraction orders is very important. The payoff would
be imaging of fully 2-D (flat) objects with a resolution smaller than the period of the
image-releasing grating. More precisely, this ambiguity is illustrated by the right panel
in Figure 10. If the sub-wavelength object is represented by the continuous spectrum
(blue line), then the spectrum can be sampled within the discrete set of "zones" which
are defined by the diffractive orders of the image-releasing grating. The width of each
zone is 2w/ c, and they are labeled as 1st order, 2nd order, and so forth. Wave numbers
belonging to the different zones can be diffracted onto the same far-field detector as
explained in Figure 10. In order to disentangle the 1st and the 2nd zones, a single
detector cannot provide sufficient information. It turns out that using two detectors (A
and B) and two laser beams (Beam A and Beam B) provides additional information that
is sufficient to disentangle the two zones. This additional information is obtained by
comparing the intensity on the two detectors A and B. Another advantage of this
imaging technique is that it is interferometric in nature. Therefore, even if the
contribution of some of these spectral zones' orders is very weak, it can still be
detected because of the high sensitivity of the interferometric techniques. What makes
this interference special is that it involves sub-diffractive waves propagating through
the indefinite permittivity metamaterial. Below some of the experiments conducted in
the laboratory that demonstrate such interference are discussed.
UNCLASSIFIED/ {EAR OFEICll.k W8I!! eNti
11

[Page 16]
UNCLASSIFIED/}FOlil OliliiliCililL. W&li QPIL.¥
Far-fiold .......
m m
D
m ___....
figure 9. fSL Based on an Indefinite Permittivity Metamaterial Placed Between the Object and the
Image-Releasing Grating. The grating releases into the far field sub-diffraction waves produced by light
scattering off the object. The role of the meta material is to propagate sub-diffraction waves from object to grating.
(Reference 27)
Ever since Merlin's invention (Reference 28) of the sub-diffraction near-field plate, it
has become clear that the interference between sub-diffraction electromagnetic fields
can result in the formation of a deeply sub-wavelength image. The near-field plate,
however, is not an imaging device; its purpose is to create a well-defined image using
an elaborate pre-fabricated sub-wavelength structure on the plate's surface. The goal
for this study is to observe an a priori unknown sub-wavelength image using a near￾field structure. In the past, successes (Reference 19) in retrieving images of sub￾wavelength objects (such as A/20 holes) using an NSOM for radiation detection are
achieved. An NSOM is a near-field instrument, therefore, a much more desirable
detection method would involve far-field detection. To advance this goal, and to
develop a tool sometimes referred to as the FSL, we've initiated research on multi￾beam multi-detector sub-wavelength holography illustrated in Figure 10.
2-nd
k
BeamA /// ~~eamB
figure 10. Tomographic Multi-Beam Multi-Detector Holography of Sub-Wavelength Objects Using
Indefinite Permittivity Medium (IPM). Incident beam(s) scatter off the sub-A object, propagate through the
1PM, and then get re-scattered into the far field by the grating with the period D. The purpose of the multi-detector
arrangement is to disentangle the k1 and kz spatial wave numbers in t he object's spectrum (shown in the left
panel). Beams A and B are phase-shifted with respect to each other.
UNCLASSIFIED/ {EAR OFFICIAk 1!181!!! Bflti
+-+ 41t/D
2ro/c
12

[Page 17]
. ·,
'
:
:
~ ·~t~=~- :~
' •··-·
UNCLASSIFIED/ (FOR OFEICI0k YSE 8Htt
Our implementation of the FSL utilizes an 1PM whose dielectric permittivity tensor is
anisotropic and contains positive and negative components: c1_ > 0,c11 < 0, where parallel
refers to the !PM/object interface. We have already fabricated such IPMs using SiO2-
SiC-SiO2 multi-layer, and are investigating other approaches involving selectively-doped
semiconductor multi-layers similar to the ones used by Gmachl's group at Princeton.
SiO2-SiC-SiO2 multi-layers are produced in-house (with SiC films shipped by Professor
Ferro from University of Lyons, France). The main function of the 1PM is to propagate
sub-diffraction waves ( "ii > wl c) with as little decay as possible. That happens because
these sub-diffraction waves are no longer evanescent: k1 ~ -kI
~&11 I &1- > 0. It is
demonstrated experimentally that there exists a frequency range for which sub￾diffraction waves propagate through the 1PM with less attenuation than the radiation￾zone waves ( "ii < w/ c ), see Figure 11.
MCT detector on optical rail
~
0.
,.,,.: ~r~~
«)
100nmAll
,-L -oc~·k--in-, 220nm Si02
2.94 µml-J
i ~
IO r;:t ~r~~ros~::, amplifier 440 nm SiC £ ; II 1!
220 nm 00, «) 100 nm All "
-~ 01= iii !tt··= 500nm § - 2' • -r--· 0 - ' C .
~ --+---- •
Optical :j 10 t--~- .j~ chopp.:i- ~ ,-<.U. i= .5 :
1010.6 10.7 10.8 10.9 11.0 11.1 11.2 11.3 11.4
Wavelength (µm)
Figure 11. First Experimental Demonstration of Propagating Sub-Diffraction Waves in the 1PM. (Left):
Experimental setup demonstrating how sub-diffraction waves are launched into the 1PM using FIB-fabricated sub￾wavelength grating. Because the periods of the bottom ("launching") and top ("transforming") gratings are
different, far-field observation of different harmonics of the bottom grating is enabled. (Right): Experimental
results: the first sub-diffraction harmonic of the grating (green line) becomes stronger than the zeroth radiation￾zone harmonic of the grating (blue line) in the region where£1- > 0, &11 < 0 .
Once sub-diffraction waves propagate through the 1PM, they can diffract on the image￾releasing grating (see Figure 10) and be radiated out into the far field. A detector array
can be used to collect the signal and reconstruct the image. Unfortunately, different
wave numbers k 11 of the object are directed into the same detector and produce an
ambiguity in extracting their respective amplitudes A(k11 ). This ambiguity is illustrated
by Figure 10: wave numbers k1 = tik + 21r ID and k2 = M + 41r ID are directed to the
same far-field detector. Simply put, a single number (intensity of light with the wave
number tik < w I c incident on the detector) is insufficient for determining two scattering
13
UNCLASSIFIED/ {fQR OFEICl.t.ls: Y81!! 8flti
- --t;aa-'------,----------,----
-···-··-:-·· ...-~--,
-2 :i===:==~·~St~

[Page 18]
UNCLASSIFIED/ (fQR OFFIClt.k YSE 8HLI
amplitudes ( A(k1) and A(k2 ) ). Therefore, a new concept has to be developed, and the
multi-detector technique is such a concept.
The concept requires two detectors and two coherent laser beams. The two beams are
formed using a beam-splitter and a variable delay line imparting a phase shift to the
two beams (see the actual experimental photograph in Figure 13 where the beam￾splitter BS and the Delay Line are shown). We have theoretically demonstrated that the
intensity dependences of the two detector intensities / 1(1/1) and / 2 (1/f) as a function of
the phase delay 1/f provides enough information to recover both A(k1) and A(k2) .
Unequal grating phase interference: dh, t ld orders
D1 =2.74 µm
H
100 nm Au
220 nm Si02
440 nm SiC
220 nm SiO2
100 nm Au
- . · -
0o 20 40 60 BO 100 120 140 160 180 200 220 240
Example "micrometer position" not correlated lo phase
Figure 12. (Left): Schematic for 2-Beams/2-Detectors Interferometric Measurement. (Right):
Numerical Simulation: intensity on the two detectors as a function of the phase delay between beams A and B
produced by the interference between the zeroth and first diffractive orders of the bottom diffractive grating
(numerical simulation). The second detector provides the necessary second data point which is necessary for
separating the contributions of different diffractive orders.
Two sets of experiments demonstrating the feasibility of the concept are conducted.
None of these experiments constitutes imaging per se. However, without demonstrating
the two key milestones described below, proper imaging experiments cannot be
attempted.
The first milestone involves demonstrating that 1PM indeed supports propagating (non￾evanescent) sub-diffraction waves. Figure 11 shows the experimental schematic (left
panel) and experimental results. The bottom grating "imprints" its Fourier components
(zeroth, first, second, third, and so forth) onto the incident laser pulse t hereby
generating electromagnetic waves that are launched into the SiC-based 1PM. The zeroth
harmonic is inside the radiation zone (that is, it is not sub-diffraction), while the first,
second, and so forth sub-diffraction. These EM waves scatter off the top grating having
a slightly different period and are released into the far field. Because the direction in
which waves are released depend on the Fourier harmonic's number, we can
experimentally separate and measure them. Clearly, the relative magnitudes of these
diffractive orders dramatically vary as a function of the laser wavelength. For example,
the zeroth diffraction order clearly dominates in the &J_ < 0,&11 > Ofrequency range.
However, in the sj_ > 0, s11 < Ofrequency range the first diffractive order becomes larger
UNCLASSIFIED/ {fQR OFEICl.t.ls: W81!! 8flti
14

[Page 19]
UNCLASSIFIED/;'FOA OlililCI0~ 1155 ON! X
than the zeroth one. This confirms the recently predicted effect that for IPMs one can
indeed observe a very counterintuitive effect: sub-diffraction waves can indeed
propagate with less loss than the diffraction-limited ones.
The second milestone involves demonstrating the possibility of observing the
interference of sub-diffraction electromagnetic waves inside the IPM using the two￾beam/two-detector technique. Figure 10 demonstrates this interference pattern which
reveals the phase advance of the sub-diffraction waves inside the IPM. While we have
so far demonstrated the interference between the first Fourier component of the grating
(sub-diffraction) and the zeroth Fourier component, we see the possibility of interfering
even more sub-diffraction waves (2nd and 3rd).
Interference scan, 10.800 micro11s
• • 10 12
ln1er11!r~!'.oe ~~~•-! 1.31 ~ -~ons
I°' +-t---+--- ----1-1,__,__ _ +f-_,___ l-f--t-i
lnst-t-l---l-+--l-l--,f+--1- -1--t- l--l-i
I DA ,__,,_,__ .,._1--,.-1--1-,
Figure 13. (Left): Experimental Setup for 2-Beams/2-Detectors Interferometric Measurement in Our
Lab. (Right): Preliminary Experimental Results : infrared intensity on two detectors (red and black lines) are
(i) different from each other; (ii) have a sinusoidal dependence on the delay line position (in microns), which is
equivalent to the phase delay between the two beams; (iii) are shifted in phase by the amount equal to twice the
phase difference between the pt order (sub-diffraction) and 0th order (radiation zone) Fourier components of the
bottom grating. Measurements taken at J..= 10.8 µm and J..= 11.3 µm.
With these two milestones established, it is now possible to conduct true sub￾wavelength imaging experiments using two (or more) far-field detectors and jointly
processing their inputs.
UNCLASSIFIED/ {EAR OFFICIAk 1!18!!!! Bflti
15

[Page 20]
UNCLASSIFIED/ (FOR OFFIClt.k YSE 8Htt
Applications to Circuits and Waveguide Miniaturization:
Slowing Down and Manipulating Electromagnetic Pulses
(EMP) Using Advanced Metamaterials
Given the space constraints of an advanced aerospace platform and the amount of the
useful payload that has to be carried, it is very important that every optical and
microwave component be as small as possible. Because of the very large speed of light,
there is a natural limit to how small such components can be made. Any structure
capable of processing EMPs (be those optical, THz, or microwave) of temporal duration
r must be at least L =er long. For example, a 1 ns microwave pulse can be
manipulated inside a device that is at least 1 ft long. Pulse manipulation can be
understood very broadly by pulse compression, frequency shifting, harmonics
generation, or other. For aerospace communications systems, it may be very desirable
to have the ability to manipulate the format of EMPs, (that is, to change their
frequency, duration, and repetition rate). Slowing down or even stopping the EMP can
circumvent the length requirement if the group velocity is reduced to vg << c , and thus
the required length is L = vgr.
~c
_L ___ C __
CT
Figure 14. Schematic of Pulse Compression in Magnetized Plasma. A radiation pulse with initial frequency
w0 and duration T slows down in the plasma to a group velocity v80 << C. Adiabatic spatially uniform variation
of the magnetic field changes the radiation frequency to W1 and increases the group velocity to v g, >> Vgo. The
emerging pulse is compressed to I; =Tv80 I v8 1 . (Reference 29)
An example of the pulse slowing down and subsequent manipulation is first discussed in
Reference 29 in the somewhat esoteric context of magnetized plasma. Pulse duration,
frequency, and (for multiple pulses) repetition rate can be controlled by storing (or
slowing down) electromagnetic waves and subsequently changing the system's
parameters. The essence of the compact pulse manipulator is shown in Figure 14. The
pulse is slowed down inside the compact plasma device and manipulated by changing
the magnitude of the magnetic field. The advantage of slowing the pulses down is
three-fold. First, the device can be made smaller, resulting in size savings. Second, the
temporal scale on which the system has to be manipulated is lengthened because the
pulse is moving slowly. Finally, the potentially large ratio between v81 >> vgo results in
the more dramatic dynamic range of possible pulse compression ratios. Plasma-based
UNCLASSIFIED/ {fQR OFEICl.t.ls: W81!! 8flti
16

[Page 21]
UNCLASSIFIED/ (FOR OFEICI0k YSE 8Htt
devices may not be appropriate in the aerospace context because of their large size,
power requirements, large magnetic coils, and so forth.
Fortunately, metamaterials offer some exciting opportunities for slowing down
electromagnetic waves as has been recently recognized (Reference 30). Specifically,
the authors have theoretically demonstrated that an axially varying heterostructure
with a metamaterial core of negative refractive index can be used to efficiently and
coherently bring light to a complete standstill. One of the most remarkable aspects of
the approach is that it works for relatively broadband pulses. The broadband capability
is achieved through "tapering" (or axial variation) of a metamaterial's parameters such
as the effective e andµ. Due to tapering, each frequency component of the wave
packet is stopped at a different guide thickness, leading to the spatial separation of its
spectrum and the formation of a 'trapped rainbow'. In Reference 30, the authors have
actually opted for a physical tapering of the waveguide (that is, reducing the thickness
of the NIM waveguide along the length of the waveguide), although other approaches
such as varying e and p will also work.
Guided electromagnetic wave
a
ERHH > 0 uRHH > 0 r3 , , r3 f LHH > 0 ,1LHH > 0
r3 t r3
------!
)___ __
f'RHH >0 uRHH > 0 r2 , , r2 l HH > o llLHH > O
r2 ' ' r2
--+ /3 r
Ordinary waveguide Negative refractive index tapered waveguide
-+- [3
Figure 15. Trapped Rainbow: A Waveguide with Negative Index Core Can Stop Light. A guided wave
packet is efficiently injected from the ordinary waveguide to the left-handed heterostructure LHH (see also Figure
4 ), inside which it propagates smoothly owing to the slow (adiabatic) reduction in the thickness of the core. The
smallest (red) frequency components of the wave are stopped at the smallest core thicknesses of the LHH, while
the largest (blue) components stop at correspondingly larger core thicknesses. (Reference 30)
The schematic of the light-stopping structure based on the waveguide with a negative
index core (dubbed left-handed heterostructure, or LHH, in Reference 30 is shown in
Figure 14. Although light stopping is possible in other guided configurations that do not
necessarily requireµ to be negative (for example, a metal-dielectric-metal waveguide
would suffice), the key here is that perfect impedance matching can be achieved for the
metamaterials-based waveguides with the negative index core. That is very important
for maximizing the coupling efficiency from the regular waveguide to the LHH. Although
Reference 30 does not present any specific ideas as to what could be done with the
UNCLASSIFIED/ {EAR OFFICI.IJ.k Y81!!! tJflti
17

[Page 22]
UNCLASSIFIED/fFOA OFFI€1.t.k W&i ONkY
slowed down and/or stopped light, the schematic shown in Figure 13 provides some key
ideas. Moreover, the prospect of producing a low-loss negative index material in the
optical domain still remains somewhat distant. Therefore, it may be worthwhile to
examine other approaches to slowing down light that have emerged in the past few
years.
Stopping and/or slowing down light is an old idea originating from the atomic concept of
Electromagnetically Induced Transparency (EIT). The phenomenon has been considered
to be purely quantum mechanical until several groups have demonstrated that it has
some classical analogies (Reference 31). Remarkably, at least one group has
demonstrated in the past year that EIT can be achieved using plasmonic meta materials
(Reference 32). The idea is to create a plasmonic "molecule" consisting of a radiative
element coupled with a subradiant (dark) element. The plasmonic molecule showed
electromagnetic response that closely resembles the electromagnetically induced
transparency in an atomic system. Because of its subwavelength dimension, this
electromagnetically induced transparency-like molecule was shown to be suitable as a
building block to construct a "slow light" plasmonic metamaterial. The specific design of
the plasmonic molecule is shown in Figure 15.
10.0
36.5
33.3
30°0
26.7
23.5
20.2
16-9
13-7
10.1
7. 11
3.88
0
Figure 16. "Plasmonic Molecule" Exhibiting EIT. Lelt: Radiative element (metal strip) by itself gets strongly
polarized by the incident EM wave, resulting in weak transmission/strong reflection. Right: Radiative element
coupled to the "dark" element (two strips). Dark element possesses a non-radiative quadrupole resonance which is
excited by the radiative element and de-polarizes the radiative element. The result: vanishing reflection, high
transmission. Color bar: IEInormalized to the incident laser field at>. = 700 nm. (Reference 32)
This specific plasmonic molecule consists of the "dark state" (two parallel plasmonic
antennas oriented perpendicular to the incident vertical electric field) and the "radiative
state" (single plasmonic antenna oriented parallel to the electric field). The quality
factor of the "dark antenna" state is an order of magnitude higher than that of the
"radiative" antenna. When the "radiative" antenna is spatially separated from the "dark"
antenna (or when the dark antennas are not present at all), all or most of the incident
radiation is reflected from an array of "radiative" antennas whenever the resonance
frequency of the antenna coincides with that of the laser. In this example, the long
antenna is 128 nm long, and the resonance wavelength is at>-. = 700 nm. The key
effect here is that the resonance of the "dark" antenna should be at the same
wavelength.
UNCLASSIFIED/ {EAR OFEICl.t.ls: Y81!! 8flti
18

[Page 23]
UNCLASSIFIED/ (EAR OFEICJ0k W&E 8Htt
Because the exploited resonance has a quadrupole nature, it is slightly red-shifted. For
that reason, the length of the "dark" antenna is 100 nm. When the two antennas are
brought together, the radiative antenna polarizes the dark antenna, which, in turn,
depolarizes the radiative antenna. As a result, the dipole moment of the coupled system
is drastically reduced, the reflection drops and transmission increases to almost 100
percent (limited only by losses). Most of the energy is now stored inside the non￾radiative (dark) antenna.
If multiple layers of dark/bright antennas are employed as shown in Figure 16, then
one can achieve one of the most important manifestations of EIT; "slow" light. Slow
light can have many interesting technological applications because (a) slow light is easy
to manipulate by changing the structure's parameters (as described in the section on
tunable metamaterials), and (b) slow light has a high field intensity (enhanced by the
ratio of the free-space propagation speed to the slow propagation speed), therefore, all
nonlinear processes are enhanced for slow light. Such nonlinear processes may include
harmonics generation, optical diode action (see the section on non-reciprocal optical
elements), and many others.
(a)
Figure 17. True Multi-Layer Metamaterial With a Unit Cell Shown in Figure 15: radiative antenna (single
metal strip) coupled to a dark antenna (two perpend icu lar metal bars). Such metamaterial exhibits "slow" light
propagation along the incidence direction (slowed down by a factor 30 or more). (Reference 32)
It is important to realize that the geometry suggested in Reference 32 is not unique.
For example, the dark and radiative antennas need not reside in the same plane. Nor is
the effect of EIT (and the related phenomenon of slow light) limited to the optical
domain. Both infrared and microwave-range designs have started emerging. These
frequency domains are likely to be of greater use for advanced aerospace platforms
than the visible range targeted by most studies.
UNCLASSIFIED/ {EAR OFEICll.k W8I!! eNti
19

[Page 24]
UNCLASSIFIED/ (FOR OFFIClt.k YSE 8Htt
Metamaterials for Energy Harvesting
One of the most important applications of meta materials is related to developing
"perfect absorbers" of infrared electromagnetic radiation, be it in the mid-to-long
infrared part of the spectrum (making it relevant for night vision, harvesting of the
Earth glow mid-infrared radiation, and so forth) or in the near-to-mid-IR spectrum
(making it relevant for day-time infrared photography of the earth terrain). For
example, day-time infrared photography relies on the different sunlight reflectivities of
surfaces (for example, snow, brick walls, concrete walls, grass, and so forth), and can
easily distinguish between those surfaces. This reflectivity differential tends to be the
greatest between 2-3 microns, and rapidly decays toward longer wavelengths. Open
sky contains very little infrared radiation which explains why infrared
imaging/photography is very important for aerial and satellite surveys. Because light
scattering in the atmosphere scales as >,.-4 , imaging through the atmosphere in the
visible range is impossible, and infrared imaging becomes important. This is especially
true for the 1 < A < 4 µm range. For longer wavelengths {A> 10 µm) this brightness
differential is largely gone because the emission spectrum is dominated by thermal
emission. In fact, the Earth glow maximum is around A> 10 µm, with most of the
energy contained in the 3 µm < A < 14 µm range. This longer wavelength (mid-to-far
IR) spectral range is also very important. It can be used for night-time energy
scavenging by high-altitude satellites and other aerospace platforms.
There has been a surge of activity in this area, first in the microwave/THz part of the
electromagnetic spectrum (References 33, 34), and subsequently in mid-to-far infrared
(Reference 20). The concept of narrow-band metamaterials-based absorbers introduced
in Reference 33 has the potential for developing highly efficient bolometer arrays. When
applied to the infrared part of the spectrum, it can be used for space navigation,
especially when weak infrared signals from specific stellar objects need to be picked up
and discriminated from other radiation sources. For such applications, the narrow-band
"perfect" absorption is highly suitable. An array of such bolometers would reject
(reflect) all undesirable frequencies and focus on the single wavelength characteristic of
the source of interest. Moreover, if an array of different (for example, tuned to different
frequencies) narrow band detectors can be deployed, then the hyper-spectral imaging
capability could bring additional benefits. For example, absolute temperatures of a
radiation source (that is, stellar bodies) could be accurately determined, and could
improve the accuracy of space navigation further.
(a) (b) (c)
-l
~ (J)
3
iii" (J)
6"
:::,
H
0.04
0.03
0.02
0.01
Figure 18. "Perfect" Narrow-Band Microwave Absorber. (a-c): Unit cell design. Right panel: simulated
absorption/transmission/reflection. (Reference 33)
UNCLASSIFIED/ /EAR QFFICl.t.ls W8I! Bfltf
20

[Page 25]
UNCLASSIFIED/ /POil Offl@IAI:: YS& 8Nl::\f
One possible design for the microwave frequency band is shown in Figure 17. High
absorption is accomplished by reducing reflections to zero. This is accomplished by
choosing metamaterials parameters such that &eri@,.) =µ.1i@,. ) at the resonant
frequency co,. . Note that both the real and imaginary parts of the permittivity and
permeability must be equal to each other, and that the imaginary parts don't
necessarily need to be small for absorber applications. In fact, it is desirable that they
are not too small, thereby enabling 100 percent absorption within a single layer of
metamaterial. The above design can be scaled down to the THz range, as was later
demonstrated in Reference 34. It is difficult to find strongly absorbing materials at THz
frequencies that are compatible with standard photolithography. Thus, a potential
application of these metamaterial structures is as absorbing elements in thermal
detectors. A strong absorption coefficient is also necessary to have a small thermal
mass. This is important for optimizing the temporal response of thermal detectors. The
metamaterial presented here has a 6 micron thick film (that is, )\/50 thickness for THz
radiation) and 70 percent absorptivity, which yields an absorption coefficient of 2000
cm- 1 .
One drawback of the original design was the narrow angular range of the absorber. The
absorption dropped dramatically when the incidence angle was as small as 20 degrees.
The reason for that is a relatively large unit cell of the metamaterial. In fact, when the
unit cell size is larger or comparable to )IJ2n, where n is the refractive index of the
substrate, it is inappropriate to call such structure a "metamaterial". A true impedance￾matched metamaterial would, in fact, always have a very broad angular response.
' . ' ' . . H --- - --- - --- -- - •-- - --- - -------- •------ X
. ' ' !
0.8 --------------- 1---------------1---------------:
. '
~-6---------------i -------------+--------------
-0.4 ----------- ----[ ---------------; ____ _________ __
0.2 PIMNIM Lx
L x= c,J .E=J.L=-1 +i
L=200nm,i::=1-L=-1 +i
10 20 30 40
Figure 19. Wide-Angle Plasmonic Absorber Based on Negative Index Metamaterial. Right panel:
schematic of an absorption-measuring experiment. A generic metamaterial with 8 YY = f.l zz = - 1+i, f.lx., = l is
assumed . Left panel : angular dependence of the absorption for a generic and specific (shown in the inset)
metamaterial. Both exhibit wide-angle absorptivity. (Reference 20)
This fact can be expressed by a simple formula for the absorption coefficient
A (Reference 20):
UNCLASSIFIED/fFOA OFFICilial.L. W&li OlhlL.¥
21

[Page 26]
UNCLASSIFIED/ (FOR OFEICI0k YSE 8Htt
,----------2
A=l - cos0-.Jt:YY I A, -sin. 20/(µxxA z> (4)
cos0 + J£ YY Iµ,, - sin 2 0 l(µx.<µ,,)
where we've assumed that, for normal incidence, this metamaterial is impedance￾matched: £ YY = 1-'zz = - 1+ i. Equation 4 can be simplified under the assumption
oflcS')'.)' I >> l,µ"" = 1: A :=:d - tan4 (0/2), implying that A~ 0.97 even for 0 = n /6. The
challenge, if course, is to design a true impedance-matched optical metamaterial.
Success has been achieved in designing such a metamaterial (Reference 20).
The recently published design is shown in Figure 19. The unit cell consists of two layers
of plasmonic antennas; the cut-wire antenna that imparts magnetic (as well as some
electric) response to this metamaterial, and the continuous-wire antennas that impart a
purely electric response. It is found that the wide-angle capability could be very
important for several applications. Wide-angle power absorption efficiency is desirable
for miniaturizing photodetectors or microbolometers down to the wavelength size.
Continuous Silver
20nm
80
nm
I
I wires
control
µ eff
1450 1500 1550 1600 1650 1700
Wavelength [nm]
Figure 20. Specific Design of a Wide-Angle Plasmonic Absorber Based on Negative Index Metamaterial
Operating at A= 1550 nm. Left panel: Schematic of the silver-based plamonic structure. Right panel: Extracted
permittivity and permeability for the normal incidence demonstrate impedance matching: £ YY =µ,, =-1 +i.
(Reference 20)
For example, to focus light on a wavelength-sized photodetector or micro-bolometer
requires high-NA optics (a NA=0.5 or higher). Therefore, a photodetector should be
able to absorb light incident at 30 degree angle. For advanced aerospace platforms it is
easy to envision a scenario where an airborne platform is powered by a high-power
infrared laser source located on Earth. If the wavelength falls inside the transparency
window of the atmosphere (between 3 and 4 µm, and also around 10 µm), then such a
22
UNCLASSIFIED/ /FOR QFFI@IAL tt.!I! Oi4Lf
3
2
_1
-2
-3
Impedance
- Matching , .. , . ,' -. lit - ..
I ,. ,.. • -
- Re e
""'" Im E
•• Reµ
Im.ti
-4~----~-~ --~-~

[Page 27]
UNCLASSIFIED/ (FOR OFEICI0k YSE 8Htt
prospect is not too farfetched because scattering in mid-infrared by atmospheric gases
is essentially zero. For such a remote powering scenario to be feasible, one would need
a highly efficient absorber at the specific wavelength corresponding to that of the
source. Moreover, as the space platform is moving, it is desirable that the absorption
remain high even for non-normal incidence angles.
The second application is for thermophotovoltaics (TPV) (Reference 35). Some type of
thermophotovoltaic converter will almost undoubted ly be installed on the advanced
aerospace platforms of the future. Presently even advanced ( experimental) electric cars
are using TPV cells to convert the heat from their engines into electricity. Such
converters have already been shown to be capable of increasing the range of electric
vehicles by a factor of 3. We believe that metamaterials could play an important role in
developing highly efficient TPV cells. By virtue of Kirchhoff's law, emissivity of a thermal
emitter approaches the blackbody limit only if the absorptivity approaches unity.
Moreover, wavelength-selective radiators can dramatically improve the efficiency of
current generation in a TPV cell if their emission spectrum is matched to the bandgap of
the TPV converter. For example, a typical TPV converter, GaSb, has the bandgap of EG
= 0. 7 eV that would be ideally suited to a wavelength-selective radiator operating in
near infrared around A= 1.7 µm.
ReHecllcn from SiC on Au Absorption vs. n, and ni for 1'.=13µm (ro=760cm-')
2.5~--~--~--~--~--~
2 SIC
07
_i!;'0.6 - 1.5 C _;,, 'oii ii 0.5
'ii .§" a: 0.4 1
03
0.2 0.5
0.1 · · ••·Toeory
- Experimental data
oL------------=========l 6 6.5 7 7.5 600 700 600 900 1000 I 100 1200 Real(n) k(cm"'l
Figure 21. (Left) Experimental Result, Reflectivity Versus Wavelength, that Inspired the Proposed
Effort: A Modestly Absorbing Material (SIC) Turns Into a "Perfect Mid-IR Absorber" When a A/4 -Thick
SiC Film Is Backed by a Metal Mirror. (Right): Theoretical Plot - Constant Reflectivity Contours Plotted
in the (Real(n), Imag(n)) Space. High material absorptivity Imag(n) is required to achieve perfect absorption
(R=O). Posed question : can a metamaterials-based semi-transparent mirror enhance absorption and result in an
almost-perfect ultra-thin absorber?
The perfect absorbers shown in Figures 17-19 may be too complex for practical
applications. Metamaterials tend to be lossy because of the large field concentration in
the metal. Therefore, work has recently started working on a new type of metamaterial
(so-called CMMs mentioned in the Introduction), that could potentially make weakly￾absorbing semiconductors (that is, Si in the visible) absorb much stronger. The goal
here is to make a thin (although not necessari ly a very sub-wavelength) absorber
backed up by a sheet of CMMs which would prevent reflections and result in a very high
absorption. Applications that are considered are essentially the same as for the
"perfect" absorbers described above. For example, satellites can use the Earth glow for
nighttime battery recharging. The collected power is quite high; 1 m2 of black surface at
23
UNCLASSIFIED/ {fQR OFEICl.t.ls: 1.181!! 8flti
8

[Page 28]
UNCLASSIFIED/;'fOll Offl@lsltt HS! OHLY
room temperature radiates 460 W. Earth-based powerful mid-infrared sources can be
used for nighttime powering of airborne platforms.
All these applications would benefit from the following components: (a) perfect
absorbers of infrared radiation that can be installed on the receiving platforms, (b)
efficient sources of thermal mid-infrared radiation. These two components are related
to each other. Therefore, developing an ultra-thin perfect absorber of infrared radiation
would be highly desirable. The ultra-thin aspect is important because it enhances the
radiation-to-electricity conversion efficiency. For example, it is well known that carrier
separation-collection efficiency in a solar cell improves as the cell gets thinner. The
challenge is to combine this carrier separation-collection efficiency with sufficient
absorption. Unfortunately, the absorption length of many semiconductors in the
infrared is fairly small. Recent experiments provide the new metamaterials-based
concept for increasing the absorptivity of otherwise semi-transparent materials. Below
some of the (still unpublished) experiments and theoretical developments that might
result in new metamaterials-based perfect absorbers are described.
Figure 20 (left) indicates a very instructive experimental result: reflectivity R from an
ultra-thin (500 nm) SiC film backed up by a metal mirror. At w = 762 cm- 1 (or 'A = 13.1
µm) reflectivity from the structure is less than 3 percent. That implies 97 percent
absorption in a film of thickness d = 'A/25 . This remarkable absorptivity can be
explained using the well-known microwave concept: the Salisbury screen. It turns out
that at 'A = 13.1 µm film thickness is d = 'A/4n, where n = n,.e + in;111 is the complex
refractive index of SiC. A simple formula for the reflectivity from a metal-backed thin
film can be derived:
2 r, _ e2;0
R - 0 _1.....::....--2;,5-1 (5) 1-r0e
where r0 = n - l is the reflection coefficient from the air/SiC interface and 5 =nf<od is the
n+l
complex phase shift across the film which includes losses. Fixing the laser frequency
w =cf<o and the sample's thickness d, we can plot the reflectivity as a function of re(n)
and im(n). As can be clearly seen from Figure 20 (right), there is a "sweet spot"
corresponding to specific values of re(n) and im(n) that results in vanishing reflectivity
(or perfect absorption). R vanishes when the quarter-wavelength condition is
approximately satisfied:
re(n)k0d =(2m+l)/2 (6)
where mis an integer. Finite reflection and imperfect absorption result from lower (or
higher) values of im(n), Note that, coincidentally, for the case of heavily doped SiC
predicted reflection is only 3 percent. However, for most materials (that is, Si for visible
light) absorption is too low for perfect absorption. Therefore, a question is posed: Can
one modify the structure of the metal screen to enhance absorption? It is CM Ms that
enable such functionality?
UNCLASSIFIED//FOR QFFI€ililik HS! OHL I
24

[Page 29]
..
UNCLASSIFIED/ (FOR OFEICI0k YSE 8Htt
Specifically, it has been found that by making the mirror slightly leaky, we can actually
increase absorption. If the reflection coefficient of a mirror is given by r2 , then the
reflection/transmission coefficients r ,t through the structure are given by:
(7)
where t2 = 1+ r2 and t0 = l + r0 • Note that Equation 7 turns into Equation 6 if
r2 = -1 (perfectly reflecting mirror). From Equation 7 it follows that it may be possible to
engineer the reflectivity 'i in such a way that minimizes reflection Ir12 while keeping
transmission It 12 small. The remainder of the energy is guaranteed to be absorbed by
the quarter-wavelength thick absorber.
1,-----.-----.------.------,------, 1,-----.----....-----.-----,---,
. ' 0.8 · - v ········ --·---.---------------'-···--· . 0.8 - H
C ~ 0_6 . -s~ooth Au ........................
a.
... -
0
•
·····••·
Bao 700 760
Cl) 0
~ ~ 0.4 ,------'-----'-,..............,......... 0.4
' ' ' ' ' ' ' '
.2 0. 6....._____.
<( 0:: - v - H 0.2 0.2 -smooth Au
Bao 700
' . ' . ------ ---- ----'-- ----- ------ ---'---
760
Figure 22. Preliminary Attempts to Design a Better Absorber Using Complementary MetaMaterials {U￾shaped CMM). Note that only 40 percent absorptivity is possible with a smooth gold film . Paradoxically, this
absorptivity increases to 75 percent when the metal mirror is made "leaky" by perforating it with an array of CMMs
(left panel) .
The design process for engineering r1 using the simplest CMMs, U-shaped apertures,
has been started. Some of the preliminary results are shown in Figure 22. Figure 22
illustrates how the (relatively low) 40 percent absorptivity of the SiC film covered by a
smooth Au mirror (black line) can be boosted up to 75 percent by patterning the mirror
using CMMs. We call such a "leaky mirror" patterned by CMMs a MetaMirror. It is clear
from Figure 23 that a MetaMirror can be used for making absorptivity polarization￾dependent (if that is desirable for applications demanding a reflector-polarizer).
MetaMirror can also be used for shifting the absorption wavelength which would be
highly desirable for developing broadband absorbers. We have found that there are two
mechanisms capable of making MetaMirrors: (a) excitation of the Long Range Surface
Plasmon Polaritons (LR-SPPs) on the patterned MetaMirror, and (b) excitation of highly￾localized (shape-dependent but period-independent) SPPs. An example of the
mechanism (a) is shown in Figure 23, but we also have preliminary results indicating
that both mechanisms can be operational in the same MetaMirror for close-by
frequencies resulting in multiple dips of the reflectivity coefficient I r2 1- By comparing
UNCLASSIFIED/,<FOA 8FFIOIAL tt91!! er,tt
25

[Page 30]
UNCLASSIFIED/ (FOR OFEICI0k YSE 8Htt
Figure 23 with Figure 22, it is observed that the dips correlate with drops of the total
reflectivity and increases of the total absorption of the absorber/MetaMirror structure.
The MetaMirror approach to infrared energy harvesting is one of the very promising
applications of metamaterials. A number of aspects of MetaMirrors must be investigated
and several important questions must be answered before practical applications can be
pursued. Some of those questions are:
• What is the angular dependence of absorptivity, and can it be made wide-angle as
we have recently demonstrated in Reference 20 for negative-index metamaterials?
• Can absorptivity be made broad-bandwidth by combining localized resonances with
the LR-SPPs? That could be potentially accomplished by using U-shapes with
different geometries, yet spaced in a regular periodic pattern, or by using quasi￾periodic arrangements of CM Ms shapes.
• What are the most promising polarization-independent unit cells of CMMs that result
in enhanced absorptivity?
• Is it possible to apply the MetaMirror concept in the visible and contribute to solar
energy harvesting?
As more researchers are investigating energy-harvesting applications of CMMs (or
MetaMirrors), it is believed that these questions will be answered very soon.
Absorbing ll r2
Material
lr0
--N ...
-G)
"' (ti
.s::.
Q.
N
---phase(r2) V
---phase(r2) H
1
-=- 0.5 -
Bso 700 760
Figure 23. Engineering the Complex Reflectivity Coefficient r2 Defined on the Left Panel Using the
Concept of a MetaMirror. Dips of I r2 I shown in the right panel correspond to reflection dips (and absorption
peaks) in Figure 2. The physical reason for these dips is the excitation of long-range SPPs on the MetaMirror
surface. Inset: Fabricated MetaMirror.
UNCLASSIFIED/ {EAR OFFICI.IJ.k Y81!!! tJflti
26

[Page 31]
UNCLASSIFIED/ /fOR. Offl@IAL WS& 9Nk¥
Nonlinear Non-Reciprocal Chiral Metamaterials: For
Developing Novel Optical Isolators and "One-Way"
Microwave Mirrors
Optical isolators play a pivotal role in fiber-optic communication systems by protecting
their active components ( for example, optical amplifiers) from unwanted reflected
signals that could potentially destabilize them. Such protection is especially important in
the context of advanced aerospace platforms, where repairs must be avoided at all
costs . At the core of isolator design is an element which provides non-reciprocity by
breaking time reversal symmetry. Non-reciprocity can only be caused by magnetic
fields or nonlinearities. The most common approach using magnetic Faraday rotators
results in a rather bulky implementation of an isolator. It is believed that metamaterials
are uniquely positioned to enhance the other approach of breaking non-reciprocity: use
of nonlinear effects. It is very natural to use metamaterial in the context of enhancing
nonlinearity. As was explained previously, metamaterials can be used to slow down
light and, therefore, compress electromagnetic energy. Any intensity enhancement
increases nonlinear effects, and larger nonlinear effects translate into more compact
devices. Another aspect that makes metamaterials very appealing for non-reciprocal
applications is the ability to make their properties tunable to almost any frequency
range.
One concept that is being explored (still unpublished) relies on the nonlinearity and
several other aspects of engineered chiral metamaterials. A novel type of a nonlinear
optical isolator based on adiabatic time-irreversible mode conversion (ATIMC) between
two electromagnetic modes supported by the chiral metamaterial is envisioned. As an
example of such metamaterial, a twisted optical fiber shown in Figure 24 is used. It
supports a tightly-confined core mode (CoM) which can be coupled to/converted into a
loosely confined cladding mode (CIM) of the same fiber. Coupling and conversion
between the core and cladding modes is accomplished by twisting the fiber with a
variable pitch A(z) =2,r/ /3,,. Time irreversibility is achieved due to the combination of
the Kerr nonlinearity of the core material (resulting in the intensity-dependent
propagation constant of the CoM) and small but finite loss of the CIM. As a result, the
CoM, when injected in the forward direction, passes through the isolator with a
negligible conversion into the CIM. If subsequently reflected back into the isolator (this
is equivalent to time reversal), it gets entirely converted into the CIM and subsequently
damped as illustrated by Figure 25. Preliminary simulations indicate that, for sufficiently
large nonlinearity, one can find the loss rate a for the CIM such that two conditions are
satisfied: (a) a is small enough so that virtually no power is lost in the forward
direction, and (b) a is large enough so that the time-reversal is strongly violated,
resulting in near-perfect optical isolation.
UNCLASSIFIED/ {EAR OFEICl.t.k W81!! 8flti
27

[Page 32]
UNCLASSIFIED/ ( FOR OFFIClt.k YSE 8Htt
➔
Figure 24. Example of a Generic Chiral Metamaterial: An Optical Fiber with a Rectangular Cross Section Core
Twisted During the Drawing Process Forms a Double Helix. If the core index is nonlinear, then one can engineer a
variable helix pitch in such a way that the core (localized) modes can be selectively coupled to cladding modes
depending on the direction of propagation.
Under a high ly simplified assumption of just two interacting mode (core and cladding),
we have developed a coupled-mode theory describing the evolution of the mode
amplitudes a,0 and ac1 along the fiber axis z. The set of the generic equations for a,0 and
act is given by:
a;; 0 - i(/Jo +rI aw 1
2 -8 I 2)a,·o = iWad,
(8)
aac1 - i(/30 +<5 I 2)ac1 = iW* ac0
ar
where/30 =c(f3co +f3c1)1 2wis the average normalized propagation constant,
o(r) = c(/3co - f3c1 + 2/3,,)I ()) is the distance-dependent mode detuning, r is the
nonlinearity coefficient, Wis the coupling strength between the modes, and r =wz/ c is
the normalized propagation distance.
UNCLASSIFIED/ {fQR OFEICl.t.ls: W81!! 8flti
28

[Page 33]
UNCLASSIFIED/ (fQR OFFIClt.k YSE 8HLI
1.------r----"T""---11111111111:r-------r-----,
0.8
0.6
0.4
0.2
, ... , ' ,. '
,- ' .,. , , ., '
1, I
'
100
I ~
' , '
• I
'
•
'
200 300 400 500
Fiber length [1n1n]
Figure 25. Example of Time-Irreversibility of Light Propagation Inside the Twisted Fiber Core: the core
mode propagates with almost no loss from left to right (purple solid line), reflects back, and gets dissipated/mode
converted on its way back (red line). Input mode is assumed to be right-hand circularly polarized (RCP). Mode
conversion: into LCP cladding mode (dashed line). Propagation from left to right is represented by the red lines,
from right to left: by the purple lines.
As an example, we have used a Chiral Fiber (CF) with the following properties: a 2 µm
x 1.8 µm elliptical core with refractive index of nco =2.2 surrounded by a round cladding
with radius R =20 µm and refractive index nc1 =2.15. The helical pitch is assumed to
linearly vary over /,mx = 500 mm by 6 percent around A= 166 µm. The assumed r
corresponds to the nonlinear refractive index m = 5.4 x10-16 m2/W at the operating
vacuum wavelength>-. = 1.5 µm and the peak power P= 3.5 W. The cladding mode was
assumed to be lossy with the loss coefficient a= 10 dB/m . Results are shown in Figure
25. A core mode injected from the left end of the fiber (z = 0) propagates through the
fiber without converting into the cladding mode (purple solid line) with minimal losses.
After getting reflected at z = 500 mm, the principal core mode (red solid line) gets
converted into the delocalized cladding mode (red dashed line) and damped out. This
example clearly demonstrates that t he interplay between mode-coupling, nonlinearity,
and losses can result in the dramatic loss of time-reversal.
Future research will be looking at other metamaterial systems that support two distinct
modes (one with a strongly nonlinear response and strong spatial localization, the other
essentially linear and delocalized), orthogonal polarizations, and investigate non￾reciprocal wave propagation in such metamaterials. Structures from the previous
UNCLASSIFIED/ {fQR OFEICl.t.ls: W81!! 8flti
29

[Page 34]
UNCLASSIFIED/:£FQB OFEICI\k 1!18!! eNtf
sections, such as shown in Figures 15 and 16, will be primary candidates for
implementing optical and microwave non-reciprocity. Such metamaterials would be
comprised of a unit cell containing a non-radiative element (that is, a two-strip
capacitor-loaded antenna supporting a "dark" magnetic mode) and a single "bright"
dipole antenna. Such a system exhibits EIT when the frequencies of the "dark" and
"bright" resonances coincide. EIT results in energy compression and enhanced
nonlinearity. The source of the nonlinearity could be, for example, a variable
capacitance diode (varactor) used as a capacitive load of the double-strip antenna. The
second (linear) mode could have an orthogonal polarization, and the coupl ing between
the two could be accomplished via spatially-periodic displacement of the single-strip
and double-strip antennas with respect to each other.
Tunable Switchable Metamaterials
Electromagnetic properties of most metamaterials are "hard-wired", meaning they are
determined during fabrication. That can be a serious impediment to using them in the
context of space exploration. Being able to change optical/electromagnetic properties of
a metamaterials-based device without having to re-manufacture it would be highly
desirable. Therefore, this survey is concluded by describing some of the recent progress
in making reconfigurable/switchable metamaterials. This is a new exciting area of
metamaterials research that is worth watching for applications. One of the first
electrically-controllable THz metamaterials has been reported in Reference 36, where
resonant properties of the electric split ring were controlled by applying reverse bias
between metal and highly-doped in GaAs layer. The schematic of the experiment is
shown in Figure 25. Without reverse bias there is no resonant response of the split ring
to incident THz pulse because highly-conductive electrons of the n-GaAs layer are
shorting the gap of the resonant split ring as schematically indicated in Figure 26(b).
With the applied reverse bias, electron density is depleted inside the gap. The resulting
transmission spectrum shows spectral dips which were converted into the effective
dielectric permittivity &eff (w) that exhibited resonant peaks. The strongest of the peaks
corresponded to the Inductance-Capacitance (LC) resonance of the split ring. One
possible application of such electrically tunable metamaterial suggested in Reference 36
was a modulator. The authors claim that the performance of their device as a THz
modulator already exceeds current state-of-the-art electrical THz modulators (based on
semiconductor structures) by one order of magnitude on resonance. Moreover, their
device operates at room temperature. Needless to say, this metamaterial-based
modulator can be improved. For example, configurations exploiting EIT could result in
stronger modulation strength.
Another interesting possibility for tuning microwave metamaterials has been suggested
in Reference 37. Ferroelectrics (such as BST) can be tuned by applying DC voltage
which changes their dielectric permittivity. This property of BST was utilized to develop
frequency tunable magnetic metamaterials using metallic split rings loaded with
barium-strontium titanate thin fi lm capacitors. The resonant frequency of this medium
is voltage tunable across a 140 MHz band centered at 1. 75 GHz. The effective relative
permeability of the slab was shown to have Lorentzian shape that reaches minimum
values between -2 and -3 for biases from Oto 5 V. Therefore, permeability of the slab
can tune between positive and negative values, making it useful in applications
requiring a state switchable magnetic permeability.
UNCLASSIFIED/ {EAR OEEICl.t.ls: 1!181!! eNtf
30

[Page 35]
UNCLASSIFIED/ (EOR OFFICit.k W&E 8Htt
a C e
Ohmic Schottky
d Split gap
Transmitted
L
SI-GaAs
L --, I
'>,f
, ,~ Rd
I
I
Figure 26. THz Properties of an Electric Split Ring Resonator. (a) Are controlled by applying voltage between
Schottky and Ohmic contacts (c,d). (b) Schematic of circuit with inductance. Applied voltage controls charge
density inside the split gap (d). The structure is investigated using a single-cycle THz pulse (e). (Reference 36)
Summary and Conclusions
While it is difficult to pinpoint the exact applications that metamaterials will find in
advanced aerospace industry, metamaterials possess several features that uniquely suit
them for aerospace applications. First, the enable miniaturization of a variety of o tical
components. Making space-born devices small and light-weight is essential. These
opportunities have been covered in detail. Second, metamaterials enable new
modalities for sub-diffraction imaging: super-lenses, hyperlenses, and far-field
superlenses. Those modalities dispense with the near-field scanning microscopes, which
are complex, slow-scanning, large devices that are not appropriate for advanced
aerospace platforms. Harvesting infrared photons, whether from coherent laser sources
on Earth (for guidance, energy recharging, and so forth), from thermal Earth glow, or
from the stars, is likely to be important for aerospace platforms. Metamaterials offer
unique opportunities for making efficient wavelength-tunable, wide-angle absorbers. As
discussed in the numerous examples in this report, metamaterials are going to
revolutionize the way light is captured, manipulated, and used for imaging. Although
metamaterials are still an academic area of research, these examples illustrate that
there is great potential for practical applications.
References
[1] Smith D R, Padilla W J, Vier DC, Nemat-Nasser SC, Schultz S 2000 PRL 84 4184.
[2] J. B. Pendry, "A Chiral Route to Negative Refraction", Science 306, 1353 (2004).
[3] D. Schurig and D. R. Smith, "Spatial filtering using media with indefinite permittivity
and permeabil ity tensors", Appl. Phys. Lett., 82, 2215 (2003).
[4) D. R. Smith and D. Schurig, "Electromagnetic wave propagation in media with
indefinite permittivity and permeability tensors", Phys. Rev. Lett., 90, 77405 (2003)
UNCLASSIFIED/ {EAR OFFICIAk W81!!! Bflti
31

[Page 36: illegible]

[Page 37: illegible]

[Page 38: illegible]
