# Historical Document: DOW-UAP-D148_AAWSAP-DIRD-Detection-and-High-Resolution-Tracking-of-Vehicles-at-Hypersonic-Velocities-November-20-2010

## Source Metadata

- Original file: `DOW-UAP-D148_AAWSAP-DIRD-Detection-and-High-Resolution-Tracking-of-Vehicles-at-Hypersonic-Velocities-November-20-2010.pdf`
- Pages: 46 (39 from text layer, 5 OCR, 2 illegible)
- OCR language: `eng`
- Processed at: `2026-09-23T18:09:05.020739+00:00`
- Processing pipeline: `pypdfium2 text layer + Tesseract OCR → Markdown → neo4j-graphrag SimpleKGPipeline`

## Text

[Page 1]
UNCLASSIFIED #+F@R-OFFIGEAL-USE—
cam, Defense
Ay Intelligence
AS) Reference
“ee Document
HS (Defense Futures
20 November 2010
ICOD: 30 August 2010
-08-1012-001
Detection and High
Resolution Tracking of
Vehicles at Hypersonic
Velocities
UNCLASSIFIED £4502-0551-65A-US Ef

[Page 2]
UNCLASSIFIED//F8R: &FFIGl,liaL Mii QtPP X
Detection and High Resolution Tracking of Vehicles at
Hypersonic Velocities
The Defense Intelligence Reference Document provides nonsubstantive but
authoritative reference information related to iutelli ence to ics or methodolo ies.
Prepared by:
Technology Warning Division (DW0-4)
Defense Warning Office
Directorate for Analysis
Defense Intelligence Agency
Author:
AAP Person 83
{U) COPYRIGHT WARNING: Further dissemination of the photographs in this publication is not authorized.
This product is one of a series of advanced technology reports produced in FY 2010 under the
Defense Intelligence Agency, Defense Warning Office's Advanced Aerospace Weapons System
Applications (AAWSA) Program. Comments or questions pertaining to this document should be
addressed to !AAP Person 1 f AWSA Program Manager, Defense Intelligence Agency,
ATTN: JUIAF - 01/DWO-3, Bldg 6000, Washington D.C. 20340-5100
UNCLASSIFIED.'/FOR OliliiliGiliiliaL W&& 8HLV

[Page 3]
UNCLASSIFIED/fFOR. QFFIEl .t.L: Uii QD:I! X
Contents
Introduct ion ........... .. ...... .. .............. ...... .. ............. .. ..... ...... ......... ... .... ...... ......... ...... .... 1
Chapter 1: Theory Governing Objects in Flight ...... .... ........ .. .... .. .... ................................. 3
Subsonic Flow and Drag ............ ............ .......... ............ ........... ....... .......................... 3
Supersonic Flow .. ......... ............. .. ..................................... .... ... ... ...... ......... ... ...... .... 6
Chapter 2: Hypersonic Com pressible Flow Theory .... .. ........ ...................... .. ........ .. .. ...... . 10
Chapter 3: Detection Technologies .... ..... ... ...... ....... ... ....... ..... ......... ... ..... ..... .......... ..... 11
Electromagnetic Methods .. ......... ... ... .. .. .. .. ....... .. .. .. .. ... .. ......... ..... .... .......... .... .......... 13
RADAR (Reflected Energy) ....... .. ...... .. ............ ...... ..... .. ............ ... ..... .... .......... ..... . 13
Doppler RADAR .. ...... .. .............. ...... .. .... .......... ...... ..... .... ...... ... .... .... ........... ...... .. 14
Ra dio Reflection Detection ...... .. ......... .. .......... ... ....... .... ................... ... ................. 15
Optical Methods ................................................................................................... 16
Sky Cameras and Photographic Methods ............................................................... 16
Infrared Detection ............................................................................................. 17
LIDAR .............................................................................................................. 23
Acoustic and Seismic Methods ................................................................................ 25
Recommendation #1 - Build a Database of the Wake Characteristics for Existing Aircraft
Recommendation #2 - Exploit the Detectability of Hypersonic Aircraft Based on the
Recommendation #3 - Explore the Detection of Vehicles Designed To Be Undetectable30
Infrasound ....................................................................................................... 25
Seismic ............................................................................................................ 27
Chapter 4: Vision of Progress Over the Next 30 Years ................................................... 28
Detectability of New Hypersonic Aircraft ................................................................... 29
...................................................................................................................... 29
Features That Allow Them To Fly Efficiently at High Speeds ..................................... 30
Recommendation #4 - Explore the Development of Novel Detectors ......................... 31
Summary ............................................................................................................ 31
UNCLASSIFIED//EQA: QlililEl.t.L: W&&: O,.L'l
iii

[Page 4]
UNCLASSIFIED/fFOR. QFFIEl.t.L: Uii QD:I! X
Figures
Figure 1. Boundary Layer Development in Subsonic Flow about a Projectile........................ 4
Figure 2. Subsonic Flow Past a Projectile....................................................................... 5
Figure 3. Strauhal Frequency as a Function of Reynolds Number for Flow over a
Circular Cylinder .. .............. ............................ .. ............................................. 6
Figure 4. Supersonic Flow Past a Wedge-Shaped Body .................................................... 8
Figure 5. Supersonic Flow Past a Blunt Body (Spheroid) .................................................. 8
Figure 6. Ratios of Mach Number, Temperature, and Pressure Across a Normal Shock .... ... 10
Figure 7. Hypersonic Vehicle Detection Techniques ....................................................... 11
Figure 8. Laser-Based Chronograph ... ......... ............. ................................................... 12
Figure 9. Electromagnetic Spectrum as a Function of Wavelength ................................... 13
Figure 10. Schematic of a RADAR System................................................................... 14
Figure 11. Radio Reflection Detector................ .. ......................................................... 16
Figure 12. Energy Spectrum of t he Sun at 5,778 K....................................................... 19
Figure 13. Hypersonic Flow Past a Sphere... ................................................................ 20
Figure 14. Infrared Energy Spectra for Mach 3 and Mach 3.5 ......................................... 21
Figure 15. Peak Wavelength of the Infrared Radiation Emitted by Hypersonic Objects ........ 22
Figure 16. Peak Shock Layer Temperature for Hypersonic Objects .................................. 22
Figure 17. Schematic of a Pulsed LIDAR System ........................................................... 24
Figure 18. Mach Cone Generated by a Supersonic Object .............................................. 26
Figure 19. Comparison of Detection Technology for Hypersonic Objects ........................... 32
Tables
Table 1: Normal Shock Values for Mach 3 Flow ...............................................................9
UNCLASSIFIED//EQA: QlililEl.t.L: W&&: O,.L'l
iv

[Page 5]
UNCLASSIFIED/fFOR. QFFIEl.t.L: Uii QD:I! X
Introduction
An object is supersonic when its speed through the atmosphere is greater than the local
speed of sound . The Mach number is defined as the speed of the object divided by the local
speed of sound . For Mach numbers greater than 1 (supersonic flow), shock waves develop in
the flowfield and near the surface of the object due to the air's compressibility. Traditionally,
the lower Mach number limit for the so-called hypersonic speed regime is about Mach 5 (1. 7
km/sec). "Low hypersonic" values range between Mach 5 to about Mach 10, while "high
hypersonic" values range between approximately Mach 10 to Mach 30 or above. Mach 30
(10 km/s), for example, is close to Space Shuttle reentry velocity . Few objects can travel at
hypersonic velocities. The most common object that we see moving at these speeds are
meteors entering the Earth's atmosphere. As meteors fall to the Earth's surface, their
velocities may reach 30 miles per second (48 km/s), 1 and their corresponding Mach number
as they enter the upper layers of the atmosphere will exceed 150. Meteors are preceded by
a bow shockwave as they compress the air immediately in their path. Temperatures and
pressures increase dramatically across the shockwave to a point where the gases in air ionize
and disassociate, leading to the emission of visible light and radio waves. These conditions
also lead to rapid heating of the meteor surface causing them to fracture and break up as
they enter the atmosphere. Optical and RADAR-based surveillance systems are now used to
scan outer space to detect asteroids and other objects with orbits that may lead them to
collide with Earth.
A second class of hypersonic objects includes reentry vehicles moving into the Earth's
atmosphere from orbit. In the case of a reentry vehicle returning from low-Earth orbit at
100 km altitude, the velocity of the vehicle will reach 8 km/s (about 5 miles per second).
The Mach number of this vehicle will exceed 26.5 in the upper atmosphere. As the vehicle
moves through the atmosphere, flow-induced drag forces will slow down the vehicle; if the
vehicle has sufficient thermal protection, it can survive reentry and be recovered.
A third class of hypersonic vehicles includes the reentry payload used in ICBMs
(intercontinental ballistic missiles). The payload in these missiles is launched using a rocket
that boosts them above the atmosphere to a suborbital velocity. The payload velocity may
exceed 7 km/s as they reenter the atmosphere, equating to M > 23. The coupled high
velocity and high kinetic energy of these objects creates an ionized wake and shock wave
that can be used to detect their position and to determine their velocity. This information,
along with their ballistic trajectory, is used to locate their target and the time to impact.
A fourth class of hypersonic vehicles includes manned and unmanned rockets and aircraft.
The North American X-15, for example, exceeded a speed of 7,274 km/hr in 1964, equating
to about M = 6.5. This aircraft also exceeded 100 km in altitude on two occasions, qualifying
the X-15 as a spacecraft. The SR-71 Blackbird, an air-breathing strategic reconnaissance
aircraft, has exceeded Mach 3.2 at 80,000-ft altitude, and its actual maximum speed may
have reached into the hypersonic flow regime. Other real and conceptual aircraft capable of
reaching hypersonic speeds include the alleged Aurora SR-91 (Mach 4 to 6), the Boeing X￾51, an unmanned Mach 6 scramjet, the HTV-2 from the DARPA Falcon project (designed for
M=20 flight to low-Earth orbit), the HyperSoar (M = 12), the Russian Leninetz Ayaks, and
the Skylon (designed for single-stage-to-orbit flights). Certain rockets are also designed to
travel at hypersonic speeds. The Patriot missile, for example, travels at Mach 5, a high
speed necessary for it to be able to intercept and destroy other missiles while they are in
flight.
UNCLASSIFIED//EQA: QlililEl.t.L: W&&: O,.L'l
1

[Page 6]
UNCLASSIFIED/fFOR. QFFIEl.t.L: Uii QD:I! X
There are a number of different techniques available to detect hypersonic objects and to
determine their position, velocity, and trajectory. These detection methods can be broadly
divided into electromagnetic, optical, and acoustic/seismic methods. Each method relies on
the properties of the surface of the object to reflect incident radiation or upon the properties
of the hot ionized gases caused by the bow shock and entrained into the object's wake. The
theory of external fluid flow around objects in subsonic, supersonic, and hypersonic regimes
will be reviewed and various detection methods will be compared in this report.
UNCLASSIFIED//EQA: QlililEl.t.L: W&&: O,.L'l
2

[Page 7]
UNCLASSIFIED/fFOR. QFFIEl.t.L: Uii QD:I! X
Chapter 1: Theory Governing Objects in Flight
Many of the detection technologies for hypersonic aircraft are based on the properties of the
air flow around the object. The fluid mechanics affecting supersonic and hypersonic aircraft
are well described in textbooks on compressible flow by J.D. Anderson;2•3 subsonic flow,
including the affect of boundary layers, is covered in the textbook by F. M. White. 4
Hypersonic flow usually refers to the regime where objects are moving faster than Mach 5,
but technically refers to the Mach range where pressure, temperature, and density ratios
across shock waves reach constant values, and this does happen at about Mach 5. Fluid flow
changes dramatically at Mach 1 defined at the point where the velocity of a projectile, V,
equals the local speed of sound, a, in the atmosphere:
M ='!_ (1)
a
Flow regimes are defined by the following:
• M < 1, subsonic flow
• M = 1, sonic flow
• M > 1, supersonic flow
• M > 5, hypersonic flow
The speed of sound varies with temperature and with t he type of gases in the atmosphere. A
simple equation for the speed of sound includes the ratio of specific heats, y, the gas
constant, R, and the temperature, T:
a=.JyRT (2)
For air at room temperature, y = 1.4, R = 287 J/kg -K, and T = 20° C or 293 K. The
subsequent speed of sound is 343 m/s (1,125 ft/s or 767 mph). It is easier for a projectile
to exceed the speed of sound at higher elevations since the temperature of the atmosphere
is lower, reducing the speed of sound and the subsequent velocity necessary to break the
sound barrier.
The viscosity of the fluid flowing around an object induces drag and retards its forward
motion. Supersonic flow has some of the viscous characteristics of subsonic flow, but adds in
the complication of shock waves. To understand the nature of how a projectile affects the
flow of fluid around it, consider the case of a subsonic projectile.
SUBSONIC FLOW AND DRAG
Subsonic flows, such as the flow shown in Figure 1, are heavily influenced by collisions
between molecules of air and the surface of the projectile. The equations for this interaction
were first developed by Sir Isaac Newton in the seventeenth century, where he determined
that fluids have a property called "viscosity" that is the cause of drag on projectiles. The key
parameter that affects subsonic fluid flow is the ratio of viscous forces to inertial forces,
where inertial forces are associated with the tendency for a moving fluid to keep moving in
the same direction. The ratio of these two forces is defined as the Reynolds Number, Re.
UNCLASSIFIED//FQA: QlililEl.t.L: W&li ONL'l
3

[Page 8]
UNCLASSIFIED/fFOR. QFFIEIA.L: Ulii Qt!! X
Re = viscous forces= VD (3) inertial forces v
In this expression, V is the velocity of the projectile, D is its effective diameter, and v is the
kinematic viscosity of the fluid. As flow passes over the projectile in Figure 1, viscous forces
are especially strong near the surface where the velocity changes from zero at the surface of
the projectile to the free stream velocity.
Direction of Flow
.---- Streamlines
<- ________ Velocity D ibution within
Boundary Layer -- - - - - - the Bounda ayer
-------,,,
' ' ' ' \
\
\
\
I
I
Figure 1. Boundary Layer Development in Subsonic Flow About a Projectile.
The region where this transition in velocity occurs is called a "boundary layer," which grows
in thickness as flow moves along the surface from the nose to the rear of the projectile.
The boundary layer forms around the surface of the projectile and "separates" from the
surface at the back end of the projectile. Pockets of fluid spill off of the back end of the
projectile and form rotating pockets of fluid called Strauhal eddies or vortices. These eddies
"shed" from the surface at a rate that is strongly dependent upon the Reynolds number in
the flow. Figure 2 demonstrates that these eddies form a "wake" downstream of the
projectile that can extend far into the fluid.
UNCLASSIFIED//EQA: QlililEl.t.L: W&&: O,.L'l
4

[Page 9]
UNCLASSIFIED/fFOR. QFFIEl .t.L: Uii QD:I! X
Boundary Layers
Strouhal Eddies or Streamlines
Vortices
Direction of Flow
Projectile
Figure 2. Subsonic Flow Past a Projectile.
Visible examples of a "wake" are the contrails observed in the upper atmosphere when water
vapor in the exhaust of jet aircraft freezes into ice crystals, highlighting the wake generated
by the aircraft and its engines. In still air, the wake can be visible for many miles behind the
aircraft.
The wake rapidly becomes turbulent as it extends downstream. The Strauhal eddies are
detectable and have a shedding frequency that is expressed in terms of the Strauhal
number, St = f D/V, where f is the Strauhal shedding frequency (hz), D is the diameter (m)
of the projectile, and V is its velocity (m/s) through the air. The Strauhal number is a
function of Reynolds number, as shown in Figure 3. By measuring the Strauhal frequency,
the velocity of the projectile can be determined with moderate accuracy.
At low speeds, and corresponding low Reynolds numbers, the flow is "laminar" where
streamlines move in smooth "laminae" or layers over projectiles. At high Reynolds numbers,
the fluid flow becomes unstable and forms a widely distributed set of small eddies defined as
"turbulence." In turbulent flow, rapid mixing of the flow in the wake, even in the boundary
layers, will occur.
UNCLASSIFIED//EQA: QlililEl.t.L: W&&: O,.L'l
5

[Page 10]
UNCLASSIFIED/fFOR. QFFIEl.t.L: Uii QD:I! X
St= 10/V
0 -~~----+--~............f--~~-~f--..........-~~-+---~~......
1.E+0l 1.E+02 1.E+03 1.E+04 1.E+05 1.E+06 1.H07
Re 0 =VD/v
Figure 3. Strouhal Frequency as a Function of Reynolds Number for
Flow Over a Circular Cylinder.
The high velocities present in the wake generate low pressures on the downstream side of
the projectile that pull the projectile backwards into the wake. This is defined as "wake" or
"form" drag and is a predominant cause of drag forces on aircraft or on any obj ect moving
through the atmosphere. The viscous forces that create the boundary layers on the surface
of a projectile also contribute a small amount of drag, usually referred to as "skin friction."
Boundary layers and wakes also affect supersonic flow, but the effect of shock waves tends
to be the predominant mechanism affecting flow around supersonic projecti les. Total drag
force, Fo, exerted on projectiles or aircraft is usually summarized by this equation:
(4)
The drag force is dependent upon the density of the air, p, the frontal area of the aircraft, Ar,
the aircraft velocity, V, and the drag coefficient, Co. The drag coefficient is a function of the
geometry of the aircraft and the two "dimensionless" groups, Mach number, M, and Reynolds
number, Reo, that relate inertial, viscous, and elastic forces in the flow:
C0 =f (Re 0 , M , geoniet ry) (5)
Drag coefficients for various types of aircraft and projectiles are obtained from theory, from
computational fluid mechanics, or, most commonly, from experiments in wind tunnels.
These coefficients are usually presented in tables or in graphical form. 5, 6, 7
SUPERSONIC FLOW
Air is predominantly made up of molecules of nitrogen (78%) and oxygen (21%). At room
temperature, air behaves as an ideal gas where the density, p, the pressure, p, and the
temperature, T, are related through a gas constant, R, which is a property of the air. The
ideal gas law gives the relationship between these values. The gas constant for air is
R = 287 J/kg-K.
UNCLASSIFIED//FOR QlililEl.t.L: W&li ONL'l
6

[Page 11]
UNCLASSIFIED/,SFOR. QFFIElal L: 1!ii 011! X
p = pRT (6)
It is possible to statistically model the motion of the molecules of oxygen and nitrogen in air,
and their kinetic energy, KE, can be determined based on the mass, m, of each molecule and
the temperature of the gas.
KE =_!.mV 2 ='i kT
2 2 (7)
In this equation, k is the Boltzmann constant (1.3807 x 10-23 J/K). We can calculate the
velocity of air molecules based on the temperature of the air.
(8)
Or, for the average velocity of a molecule:
V= 8=T (9)
For air near sea level (p = 101,320 Pa, T = 293 K) the average velocity of molecules in air is
463 m/s or 1,035 MPH. This value is just a little higher than the speed of sound in air (343
m/s or 767 MPH) as computed earlier. These molecules only travel a short distance before
they collide with each other. This distance is defined as the "mean free path" given by the
symbol A.
(10)
In this expression, d is the diameter of a molecule, which is approximately 0.3 nanometers.
For air at 20° C and 101,325 Pa, the mean free path (A) is approximately 100 nanometers or
about 333 molecular diameters.
When the supersonic projectile in Figure 4 moves through the air, molecules of nitrogen and
oxygen in the air bounce off the vehicle's surface and collide with other molecules of air a
short distance away. At the speed of sound, these molecules are not moving fast enough to
get out of the way and a large number of molecules pile up along a straight line that
emanates from the nose or leading edge of the projectile as a "shock wave."
Supersonic flow in the atmosphere labeled as region 1 passes through the shock and moves
parallel to the surface of the body. The flow "expands" through a Prandtl-Meyer expansion
fan at the end of the airfoil and speeds back up to its original Mach number. Flow in the
boundary layer separates from the end of the airfoil and forms a highly turbulent wake
downstream of the airfoil. The wake is also composed of Strouhal eddies that can subsist in
the air long after the airfoil has passed by. The flow density, pressure, and temperature
increases dramatically across the bow shockwave and returns to the original Mach number
downstream of the airfoil.
For a blunt-nosed object, as shown in Figure 5, the magnitude of the impact that the
shockwave has on the flow is easier to explain. For a blunt object, the shock detaches from
the surface of the object into the freestream in front of the object. Since the original flow
moving at M1 is traveling at 90° with respect to the shock near the nose of the object, the
shock in this region is referred to as a "normal" shock. The properties across a normal shock
UNCLASSIFIED//FOR 0661El.t.L: W&&: OttLY
7

[Page 12]
Expansion Fan
UNCLASSIFIED/fFOR. QFFIEl.t.L: U&i QD:I! X
are described by the Rankine-Hugoniot equations, which yield the ratio of certain
thermodynamic properties.
Bow Shockwave
Region 1
Figure 4. Supersonic Flow Past a Wedge-Shaped Body.
Expansion Fans
Turbulent Wake Detached Shock
Blunt Body
Figure 5. Supersonic Flow Past a Blunt Body (Spheroid).
UNCLASSIFIED//FQlil QlifilEIAL: Wlili O,.L'l
8

[Page 13]
UNCLASSIFIED/fFOR. QFFIEIA.L: Ulii Qt!! X
These equations can be expressed in a form where the ratio of density, temperature, and
pressure across the normal shock are a function of the upstream Mach number, M1.
(11)
(12)
Pz = 1+ ~(M12 - 1) (13)
P1 r+ 1
Pi <r + t) M 12 = ----- (14)
Pi 2 + (y - 1) M i2
As an example, if the object shown in figure 4 is traveling at Mach 3 through air at sea level,
the pressure in the region between the nose of the object and the shock changes as shown in
the following table:
Table 1: Normal Shock Values for Mach 3 Flow
Freestream Ratio of Values
Values Properties Downstream
Across the of the
Normal Shock Normal Shock
M1 =3 M2/M1 = 0.158 M2 = 0.475
p1 = 101,325 Pa p/p1 = 10.333 p2 = 1,047,000 Pa
T1 = 293 K Ti/T1 = 2.679 T2 = 785.0 K
= (2o·q = (s12·q
p1 = 1.293 kg/m3 p/p1 = 3.857 p2 = 4.976 kg/m3
For a normal shock, the Mach number on the downstream side of the shock is always
subsonic, and in this example, the Mach number abru ptly drops from M1 = 3 to M2 = 0.475.
The temperature always increases across a shock, and for a Mach 3 flow, the temperature
rises from room temperature at 20° C up to 512° C. It is apparent that, for supersonic
aircraft traveling at this speed, the fuselage and wings will need to be made of materials that
can withstand the high temperatures and the dramatic pressure increase of 10.333. Shocks
are always accompanied by significant increases in pressure, temperature, and density in the
flow across the shock.
Flow about an Ogive or wedge-shaped airfoil as shown in Figure 4 can be analyzed in a
similar fashion; however, the wall deflection angle, e, will affect the flow and the formation of
the oblique shock wave that surrounds the airfoil.
UNCLASSIFIED//EQA: QlililEl.t.L: W&&: O,.L'l
9

[Page 14]
UNCLASSIFIED/fFOR. QFFIEl.t.L: Uii QD:I! X
Chapter 2: Hypersonic Compressible Flow Theory
Hypersonic flow is typically assumed to apply to objects traveling at M > 5. Figure 6 shows
that, for Mach numbers above 5, the ratio of Mach numbers across the shock approaches a
constant value of 0.378, although temperature and pressure ratios continue to increase. In
hypersonic flow, the bow shock, or Mach angle, /3, approaches the half-angle, 0, of slender
airfoils and the drag coefficient reaches a constant value that does not change with Mach
number. The drag coefficient actually becomes a simple function of the half-angle of the
airfoil, and the boundary layer is squeezed between the shockwave and the airfoil surface.
150
•
I
• -
' -
-~..-+---+----+-----ie-----+---+----+----+--'---l-
' -
.. • ..... -
·--.. , ·-···-·•--1111--- .. .. • • • • • "' • • • • • • • • • .-
-
:::::::::l:±::t::c J-
-
OL J d
09
0.8
0.7 100
06
Tnllio(M )
0.5 M z( M )
P,mio(M ) ... 0.4
50
03
0.2
.-~-. -;;; -·· -~·--~----~·-····-,~· o.J
I 2 3 4 5 6 7 9 1S
M
Figure 6. Ratios of Mach Number, Temperature, and Pressure Across a Normal Shock
In hypersonic flow, the Rankine-Hugoniot equations, which are based on the perfect gas law
(p = pRT), fail to predict the real behavior of air at extremely high temperatures. Equation
12, for example, predicts a temperature of 29, 787° C in the air near the surface of a blunt
obj ect traveling at the reentry Mach number of 26.5, while the actual temperature only
reaches 7,600° C. The reason for this discrepancy is due to ionization of molecules of air as
electrons are stripped away by the high temperatures that exist across the shock. Some
energy is used to produce this ionization, and above temperatures of 550° C, equation 15
does not accurately predict air temperatures due to shocks. Ionization is responsible for the
glowing wake that follows reentry vehicles and meteors as electrons rush to recombine with
ions releasing x-rays and visible light. The ionization also interferes with radio transmissions,
but provides a convenient way to identify hypersonic objects due to the emitted light. A
"rule of thumb" is that the peak shock layer temperature in degrees kelvin is 1,000 times
larger than the aircraft speed in km/s. By this standard, a reentry vehicle at 8 km/s
(Mach 26.5) would have a maximum shock layer temperature of 8,000 K. At temperatures
above 2,000 K, nitrogen and oxygen gas in the form of 02 and N2 will disassociate into
individual ions, consuming more energy from the flow.
UNCLASSIFIED//EQA: QlililEl.t.L: W&&: O,.L'l
10

[Page 15]
UNCLASSIFIED/fFOR. QFFIEl.t.L: Uii QD:I! X
Chapter 3: Detection Technologies
Hypersonic objects passing through the Earth's atmosphere leave traces that can be
observed using a number of detection methods. The bow shock introduced by such objects
reflects and refracts radio waves, RADAR pulses, and visible light. The ionized air
surrounding the object also creates electromagnetic interference that is visible on RADAR and
the emitted visible light in the wake is observable in photographs. The shock and turbulent
wake also create low frequency sound that can be sensed by ground-based sensors. These
detection methods can be characterized as electromagnetic, optical, and acoustic and seismic
as shown in Figure 7. Each method will be discussed along with the limitations and
advantages for the detection of hypersonic objects passing through the atmosphere.
Electromagnetic
RADAR
Energy Reflection
Doppler RADAR
Radio Reflection Detection
Optical
Sky Cameras and Photographic Methods
Infrared Detection
LIDAR
Chronograph
Acoustic and Seismic
Infrasound
Seismic
Figure 7. Hypersonic Vehicle Detection Techniques.
One of the fundamental tools for detecting the velocity of high-speed objects is the
chronograph. These devices are used to measure the velocity of automobiles using
pneumatic tubes, and simple systems using laser diodes or LEDs are used to measure the
velocity of bullets. Figure 8 outlines a laser-based chronograph that is commercially
available for measuring the velocity of projectiles in two-stage gas guns capable of speeds in
a vacuum of 12 km/h, or approximately Mach 36 if the projectile passed through air. As a
high-speed object passes through the first laser beam followed rapidly by the second,
photodetectors sense the change in intensity of the laser beam and send these signals to a
storage oscilloscope or to a counter. The time delay between the two signals, Lit, is used to
find the velocity of the object based on the distance between the two photodetectors, L.
Digital clocks are capable of accurately measuring time delays to within a fraction of a
nanosecond (10·9 seconds), so chronographs are capable of very high accuracy in
determining the velocity of objects. As noted earlier, their use at gun ranges or in high￾speed gas guns requires that the path of the hypersonic object must pass through the laser
beams for the chronograph to be effective, which limits their usage for the detection of
hypersonic aircraft except at instrumented test ranges.
UNCLASSIFIED//EQA: QlililEl.t.L: W&&: O,.L'l
11

[Page 16]
UNCLASSIFIED/fFOR. QFFIEl.t.L: Uii QD:I! X
Storage
Oscillo­
~ l
:
scope
Hypersonic
~--- : Photodetectors
--~
Aircraft
c===-
' ' ' ' '
' ' '
'
Test Range llL: .. 111:
~Laser / 1 lit
D
Velocity= L/llt
~~~ams /~
Lasers
Figure 8. Laser-Based Chronograph.
Currently, the best devices for the detection of hypersonic vehicles are based on the
reflection of radio and microwave radiation through RADAR and upon the detection of
infrared energy emitted by the ionized gases surrounding high-speed vehicles and in their
wake. Optical and RADAR methods are also based on electromagnetic energy, yet make use
of different parts of the electromagnetic spectrum as shown in Figure 9. Longer wavelength
photons, or quanta of electromagnetic energy, have less energy than short wavelength
photons. As a result, detection of short wavelength radiation tends to be more line-of-sight
as in infrared or other optical methods. Longer wavelengths, used in RADAR, tend to bend
around the Earth and can provide over-the-horizon detection of ICBMs, reentry vehicles, and
other hypersonic vehicles.
UNCLASSIFIED//EQA: QlililEl.t.L: W&&: O,.L'l
12

[Page 17]
UNCLASSIFIED/fFOR. QFFIEl.t.L: Uii QD:I! X
Electromagnetic Spectrum
Wavelength Type of
Radiation
1nm x-rays
10nm
100nm Ultraviolet (UV)
lµm Visible Light {0.4 to 0.7 µm)
l0µm Near Infrared
lOOµm Thermal Infrared
1mm Far Infrared
10mm Microwaves
100mm Radar
lm Rad io Waves
10m
100m AM Radio
Figure 9. Electromagnetic Spectrum as a Function of Wavelength.
ELECTROMAGNETIC METHODS
RADAR (Reflected Energy)
RADAR, or "radio detection and ranging," has been heavily used since World War II for the
detection of aircraft and sea vessels. First patented by Christian Hulsmeyer in 1904, this
technique was first demonstrated by Nikola Tesla in 1917; RADAR was exploited in the
defense of Britain through the Chain Home RADAR network initiated in the late 1930s.8
RADAR uses an antenna or a dish to transmit pulses of microwaves or radio waves toward a
potential target. Energy reflected from the target is collected by the antenna and the time of
flight of the transmitted and reflected signals yields the distance to the target. Early RADAR
systems emitted radiation in the high-frequency band (HF) from about 10 to 30 MHz.
Modern systems can operate well above 300 GHz.
As a single pulse travels at the speed of light toward a target, the time delay between the
generation of the pulse and the time that its echo is received is 2L/c where L is the distance
to the target and c is the speed of light. For a target located 30 km from the source, the
time delay is 200 microseconds, an easily measurable delay. By using microwave radiation
emitted from a dish, target distance and bearing can both be measured.
While it was possible to use low-frequency radio waves (~30 MHz) for RADAR systems in the
1940s, the wavelength of these waves (100 meters) made it difficult to resolve small targets,
including aircraft. This made it desirable to develop systems that could operate at higher
frequencies. UHF energy (300 to 1,000 GHz, 0.3- to 1-meter wavelength) radiation is used
for long-range surveillance, includi ng the detection of intercontinental ballistic missi les . Air
traffic control uses the L band (1 to 2 GHz, 0.15- to 0.3-meter wavelength). X-band (8 to
12 GHz, 25- to 37-millimeter wavelength) energy is now used for airport RADAR where the
range to aircraft is short. Higher frequency radiation is used for imaging systems and for
meteorological data acquisition.
UNCLASSIFIED//EQA: QlililEl.t.L: W&&: O,.L'l
13

[Page 18]
UNCLASSIFIED/fFOR. QFFIEIA.L: Ulii Qt!! X
RADAR systems are widely used for aircraft surveillance and can detect the distance to
objects and the position of an object (through triangulation); with Doppler RADAR, the
velocity can be directly measured. RADAR does have limitations. While low-frequency
RADAR systems are capable of following the curvature of the earth, the long wavelength of
this energy makes it difficult to resolve small objects. Higher frequency RADAR tends to be
more "line of sight." Since it depends upon reflected energy, several problems are
highlighted by the RADAR Equation:
p . = P,,·ansmilld GA a F4
(15) rece,ved ( 4 1r)2 R/ R,2
In this equation, Ptransmitted represents the transmitted power, Preceived the received power, G
the transmitting antenna gain, A the aperture area of the receiving antenna, a the RADAR
cross section, F the pattern propagation factor, and Rt and Rr are the distance from the
transmitter to the target and the target to the receiver, respectively. If the RADAR
transmitter and receiver are in the same unit, the power returned as a reflection from a
target decreases as R4 . This means that energy received in reflected energy decreases by
94% every time the distance to the target is doubled.
RADAR depends upon the reflection of electromagnetic waves off of a target's surface,
thereby making objects with a small RADAR cross section difficult to detect (e.g., stealth
aircraft). Atmospheric phenomenon, including inversions and turbulence, can lead to
interference with RADAR reflections. Even with these limitations, RADAR is widely used to
monitor high-speed aircraft, meteors, and man-made objects reentering the atmosphere
from Earth orbit.
Velocity Vector
Radar Dish
Hypersonic Vehicle
Radial direction I Rotat
Pedei
Reflected Energy Transmitted Energy
R= radial distance
Figure 10. Schematic of a RADAR System.
Doppler RADAR
Doppler RADAR systems yield velocity data for a target. Pulsed RADAR systems send out a
short burst of high-frequency radiation that is reflected from a target. The RADAR unit
processes the delay time between the transmitted pulse and the received echo to determine
the range or distance to the target. The energy reflected from the target is, however,
14
UNCLASSIFIED//FQR QfifilEIA.k W&lii O,.L\f

[Page 19]
UNCLASSIFIED/fFOR. QFFIEIA.L: Ulii Qt!! X
Doppler-shifted from its original frequency due to its velocity toward or away from the
RADAR transmitter. 9 The frequency shift, /J.f, is given by the following equation:
!).j' _ + _ + _ ~ + ~ 2VJ,rasnmi11d (16) - J ref7e,·ted J transmitld - V J transmi11d ,...,,, • C - C
In this equation, c is the speed of light, and V is the target speed in the direction toward or
away from the RADAR transmitter. The frequency shift is typically small since V << c, but
the shift is easily observable due to "beating" between the transmitted and reflected signals.
The development of fast Fourier transforms {FFTs) greatly increased the rate that Doppler
reflections could be processed to compute target velocity. By triangulating between two
RADAR transmitters, the position of a target can be determined along with its velocity and
direction of travel. Doppler RADAR systems are used for monitoring high-speed aircraft,
turbulence and shear in meteorology, and even in hand-held police RADAR guns.
RADAR technology has been used for the detection of missiles, reentry vehicles, and space
objects near the Earth since the 1960s. On 9 September 1961, for example, a Naval
Research Laboratory RADAR installation at the Chesapeake Bay Annex was used to detect a
Mercury/Atlas flight during its launch phase. 10 The RADAR system sensed the range to the
rocket, its rate of climb, and the range of its exhaust plume. This RADAR system worked
"over the horizon" and demonstrated that a RADAR system could be used to identify targets
and compute their trajectory.
A wide range of RADAR systems are now available to monitor the Earth and space for high￾speed objects in the atmosphere. 11 Cobra Dane and Cobra Judy, L-band phased-array
RADAR systems located on land (Alaska) and on ships (X- and S-band), are used for the
detection of reentry vehicles above 35 km. RADAR systems in Florida and Massachusetts are
capable of monitoring objects in space at a distance of 5,000 km to yield data on their size
and shape. Ballistic missile early warning systems still operate in Alaska, Great Britain, and
in Greenland to detect and track missile launches. On Kwajalein Atoll in the Pacific Ocean,
Altar tracks reentry vehicles at distances of up to 2,500 km with high resolution using a 100-
kW, millimeter-wave RADAR system. TRADEX, a multitarget tracking system using L- and S￾band RADAR was developed in 1963 to track missile signatures at a distance of up to 1,400
km. The venerable RC-137 (converted Boeing 707) can also be deployed with onboard
RADAR and optical systems that can track missile launches and reentry vehicles.
Radio Reflection Detection
This method can be used to detect meteors or any other object entering the Earth's
atmosphere during the day or night. The principle of this method is based on passive
electromagnetic energy emitted from the Earth's surface in the form of radio or television
signals. If these signals are relatively high frequency, the signal is line of sight and cannot
normally be received over the horizon. A radio or television located over the horizon and
tuned into the signal frequency will only detect static or hiss. When a meteor or other object
enters the Earth's atmosphere, its bow shock and turbulent wake containing ionized air
reflects radio signals causing an over-the-horizon receiver to hear pings and whistles that
change pitch as the meteor passes by and breaks up in the atmosphere. 12 It is possible to
receive reflections off of the surface of the hypersonic meteor in addition to the wake and the
shock. Sound files from the Aurigid Meteor Shower caused by radio echoes are available13
with data obtained from a directional antenna at 61 MHz and 217 MHz. The data
demonstrates that it is possible to differentiate reflections from the bow shock and the
UNCLASSIFIED//FQR QliliiliEiliA.L: W&lii O,.L\f
15

[Page 20]
UNCLASSIFIED/fFOR. QFFIEl.t.L: U&i QD:I! X
ionized wake. This technique for detecting hypersonic meteors is not fully developed and
appears to be employed only by hobbyists.
Since a receiver can be tuned to a specific over-the-horizon transmitter, it may be possible to
develop a network of rad io receivers to provide information on high-speed objects in t he
atmosphere. Multiple stations would allow triangulation of t he object to determine velocity
and position as a function of time, i.e., tracking and pat h prediction. The sound files also
contain information that could provide information on the hypersonic object. Detection of the
shock provides information on the position of the object while t he transient "whistles"
reflected from the ionized wake may provide information on the Strouhal eddy frequency that
could directly infer the object's velocity. This detection technology should be further
developed.
Hypersonic Aircraft
Radio Receiver The radio receiver is not in
line-of-sight with the
transmitter, yet receives
reflected energy from t he Transmitter
transmitter by the aircraft.
Figure 11. Radio Reflection Detector.
OPTICAL METHODS
Sky Cameras and Photographic Methods
A classic example of a hypersonic object passing through t he Earth's atmosphere is a
meteor. Meteorite hunters and astrophysicists have worked to develop methods to detect
these object s as they fa ll to the Earth. Motion-detection video systems provide information
on location and direction of meteors passing t hrough the atmosphere by detecting their
visible wake. The El Paso All Sky Camera proj ect14 is one example and even provides live
st reaming video of meteoric events.
Photographs of objects in orbit with diameters ranging from 0.1 meter to several meters
have been used to determine t heir expected trajectory as meteors as they entered and fell
through the Earth's atmosphere. 15 This technique was first used to monitor the Pribram
meteorite simultaneously by several observatories in 1959. This techn ique was even used to
locate a 1. 75-kg enstatite chondrite meteorite called Neuschwanstein reported in 2003. The
UNCLASSIFIED//FQlil QlifilEIAL: Wlili O,.L'l
16

[Page 21]
UNCLASSIFIED/fFOR. QFFIEIA.L: Ulii Qt!! X
European Fireball Network16 uses cameras at several stations separated by distances of
about 100 km and covering an area of about 1,000,000 km2 . Fisheye lenses allow each
station to observe the sky every night to monitor meteors and other nebular objects. The
network is operated by the German Aerospace Center (DLR) and the Institute of Planetary
Research in Prague.17 Other networks include the Meteorite Observation and Recovery
Project (MORP) in Canada and the Prairie Network in the United States; all have been in
operation since the 1960s and 70s.
Another recent meteorite recovery was made when asteroid 2008 TC3 entered the Earth's
atmosphere on 7 October 2008 over Sudan .18 The meteor's path left a wake that was visible
through dawn. A total of 280 fragments weighing 11 pounds were collected in the Sudanese
desert. The photographic evidence of this hypersonic reentry was interesting. The 4.2-
meter William Herschel Telescope in the Canary Islands optically recorded the spectrum of
this asteroid 2 hours before it burned up in the Earth's atmosphere. This information can be
used to identify the chemical makeup of the surface of the object or of the vaporized
products in its wake. A sequence of photographs taken at 4-second intervals over a period
of about 50 seconds provided information on its velocity as it reentered the atmosphere and
its brightness as a function of time.
Although these photographic methods have been applied to meteors, data from the European
Fireball Network and similar camera systems can be used to monitor the flight of hypersonic
aircraft that produce a visible wake through the ionization of air. The photograph ic methods
described here are limited to nighttime use. Multiple stations recording the same event have
been used to measure both position and velocity of objects moving at hypersonic velocities
through the Earth's atmosphere and the computed trajectories have been used to
successfully predict meteorite impact points on at least two occasions.
Optical systems are constantly monitoring the Earth for possible missile launches. Two KH -11
satellites are constantly in orbit 250 to 500 km above the Earth's surface with multispectral
cameras that resolve objects to within 2 to 3 meters. Big-Bird, at an orbit 160 to 280 km
above the Earth, can take video or photographs with a resolution of 250 mm. The photos
must be sent back to Earth for processing. Close-Look, operating from 130 to 300 km, has
a resolution of 50 to 150 mm. Landsat, with an orbit of 800 km, can transmit multispectral
video of the Earth with a resolution of 20 to 30 meters. The space shuttle, the U-2 aircraft,
and the SR-71 have all been used to provide high-resolution images of objects from high
altitude.
Infrared Detection
Infrared detection of reentry vehicles and ICBMs by satellites has been available since the
early 1960s, with the United States leading the effort through detection of possible missile
launches from the Soviet Union. In addition to RADAR, infrared detection is one of the best
techniques for the detection of hypersonic vehicles.
Theory of Infrared Detection Systems.
All objects emit radiation that is a function of their temperature according to equation 17, the
Stefan-Boltzmann Law: 19
q=BCY AT4 (17)
UNCLASSIFIED//FOR QliliiliEili.t.L: W&li ONL'l
17

[Page 22]
UNCLASSIFIED/,SFOR. QFFIElal L: 1!ii 011! X
In this equation, q represents the amount of radiant energy emitted in watts, E is the
emissivity (a dimensionless quantity that gauges the relative ability of an object's surface to
emit energy by radiation), A is the surface area, a is the Stefan-Boltzmann constant (a
= 5.67 x 10-s J-s-1-m-2-K-4 ), and T is the temperature of the object's surface. A simple
example of emission of heat as radiant energy is an infrared bathroom heater where electric
current is passed through a metallic element that reaches several thousand degrees and
emits considerable thermal radiation.
All objects in the environment exchange radiant heat with each other and seek equilibrium
temperatures. At high temperatures, many objects behave as "black body radiators" defined
by their surface emissivity, E = 1. The surface temperature of an object causes
electromagnetic radiation to be emitted with a spectrum given by Planck's Distribution Law,
equation 18, where the energy density is emitted by the surface of the object per
wavelength per unit volume:
u(A,T) = 8 n h c 5 __1__ (18) A, h e
e AkT - 1
The terms in this equation are as follows:
• c: speed of light, (3 x 108 m/s).
• h: Planck's constant, (6.62 x 10-34 J-s).
• A: wavelength of the emitted radiation, (m).
• k: Boltzmann constant, (1.38 x 10-23 J/K).
• T : surface temperature, (K).
• u(A,T): spectral energy density, (Jm-3-m- 1).
The surface of the sun behaves as a black body radiatora with a surface temperature of
5,778 K. For the sun, the Planck distribution of energy versus wavelength looks like that of
Figure 12. The horizontal axis is the wavelength in units of meters and shows that peak
energy occurs at a wavelength of about 5.02 x 10-7 meters or 0.502 microns (1 micron = 10·6
meters). This falls within the visible band (0.38 microns to 0.65 microns) and corresponds to
the yellow color of our sun. The peak wavelength, equation 19, is given by Wien's
Displacement Law:
A-.rnx = 2.8977685 X 10-3 (m · K) I T (19)
This shows that as the temperature of an object increases, the amount of radiant energy
released by the surface increases and the value of the peak wavelength becomes smaller.
a A black body is an idealized object that absorbs all electromagnetic radiation that falls on it.
Since a black body is a perfect absorber of radiant energy, by the laws of thermodynamics it must
also be a perfect emitter of radiation.
UNCLASSIFIED//FOR 0661El.t.L: W&&: OttLY
18

[Page 23]
UNCLASSIFIED/fFOR. QFFIEl.t.L: Uii QD:I! X
I x I06 i
J \
\
I
u(A, T 2)
I
''!.
\
\
Sx I05 •.
! o~---~----~--------~---~
Figure 12. Energy Spectrum of the Sun at 5,778 K.
Application of Planck's Law to Hypersonic Vehicles.
As described in the theory of hypersonic fluid flow, any object moving through the
atmosphere with an M > 1 will result in a shock wave emanating from the leading edge of
the object. If the object has a blunt nose, such as a meteor entering the atmosphere, the
shock wi ll be detached from the surface. If we consider a spherical object moving through
the atmosphere at hypersonic speed, as shown in Figure 13, the expected spectrum of
emitted radiation can be computed. In this example, the altitude is assumed to be 10 km
above the Earth's surface. At this altitude, the ambient static temperature is 223 K (- 50° C),
the pressure is 26.1 % of sea level atmospheric pressure (see Appendix A for the properties
of the U.S. Standard Atmosphere).
UNCLASSIFIED//EQA: QlililEl.t.L: W&&: O,.L'l
19

[Page 24]
UNCLASSIFIED/fFOR. QFFIEl.t.L: Uii QD:I! X
M1 =5.0
Figure 13. Hypersonic Flow Past a Sphere. '
If the sphere in Figure 13 were traveling through the atmosphere at Mach 3, could we
identify the speed of the sphere by the peak wavelength of the infrared radiation that it
emits? From compressible aerodynamics relationships, conditions behind the bow shock, in
region 2, can be calculated. We find that the peak static temperature would reach 597 K and
the peak wavelength 4.85 microns. Figure 14 shows the expected infrared spectrum. For
comparison, the spectrum for Mach 3.5 is also shown. In the figure, the wavelength has units
of microns (i.e., 10-6 meter) .. As the Mach number increases, the peak temperature also
rises while the peak wavelength decreases (shifts to the left). The higher the Mach number,
the greater the amount of infrared energy emitted. For Mach 3.5, the peak wavelength is
3.92 microns. The energy difference between a Mach 3 and Mach 3.5 aircraft would be
significant enough to detect with an infrared camera or FUR (forward looking infrared)
detector.
UNCLASSIFIED//EQA: QlililEl.t.L: W&&: O,.L'l
20

[Page 25]
UNCLASSIFIED/fFOR. QFFIEl.t.L: Uii QD:I! X
ltO.• nlll'ron.59'7 K l
35 - ----------------1-----,,-------------­
l('II-------<----+-------------,----------~------<
j 2.1---~------+---~-------------------l
2< -~- -----·-'~-t----+---·t------.1--------1--­ U(A•mx:ron.739 K l
15 ·
..... , ..... I
10 12 1-1 16
,. "
Figure 14. Infrared Energy Spectra for Mach 3 (red line) and Mach 3.5 (blue dashed line).
The peak wavelength changes for hypersonic aircraft with speeds that range from Mach 1 to
Mach 100 are included in Figure 15. Satellite systems currently monitor 2.5- to 5-micron IR
emissions and could detect aircraft with speeds as low as Mach 3. While Figure 15 plots the
peak wavelength, aircraft at Mach 5 or higher have lower temperatures in the turbulent wake
that would still be detectable. The peak temperatures are shown in Figure 16. Above 550 K,
the perfect gas law cannot be used to accurately predict the peak temperature due to
ionization and disassociation of molecules in the air. Figure 15 and Figure 16 use the "rule of
thumb" described earlier in the theory of hypersonic vehicle flight to determine peak
temperature and the corresponding wavelength.
Military satellite systems monitor infrared energy emitted by objects on the surface of the
Earth. Kidd and Caldweli 20 reported on the use of IR systems for defense support in 1992
and highlighted the problems in resolving missile launches and wakes from background
"clutter" caused by the infrared emissions from other objects on the surface of the Earth.
Typical satellite IR systems detect energy between 2 and 5 microns. To verify that an object
is an actual missile, the object must be detected in the 2.6- to 3.2-micron band, which
corresponds to the emission from water vapor in the hot exhaust of a rocket. It must
simultaneously be identified in the 4.1- to 4.8-micron range to differentiate the missile from
background clutter. One problem encountered in missile detection involves the "glint" that
occurs as aircraft at high altitude passing over land at night reflects sunlight to an overhead
satellite. Computer software to discriminate signals from background heat combined with
detection in the two different infrared bands helps to identify actual missile launches. FUR
(forward looking infrared) is also now used for atmospheric surveillance to detect objects in
the 3- to 5-micron band and in the 5- to 14-micron band.
UNCLASSIFIED//EQA: QlililEl.t.L: W&&: O,.L'l
21

[Page 26]
UNCLASSIFIED/fFOR. QFFIEl.t.L: U&i QD:I! X
Peak Wavelength of Emitted Radiation
10 ++---+-----+-----+---+-----_._---+-----+---r----+------,
,:f 6 ---+----+----l------1---+----+-----+-----+---+------I
J -----~---------------- Typical SatellitE IR System.5
Me, sure Radia ion from
\ -~----------------
2.5 o 5 micror s. I
----- ----- -----r-----------
\r--._
oL-_L___I===±:::=::±:=======±==:::d::::======h=d 10 20 30 40 50 60 70 80 90 100
Madi Number
Figure 15. Peak Wavelength of the Infrared Radiation Emitted by Hypersonic Objects.
Temperature Downstream of a Normal Shock
35,000
30,000
g
ii
~ 2S,000
1
z
:;
~
20,000
0
~
..
~
~
"5
~
15,000
C
0
&
l!
~
t_ 10,000
E
~
5,000
//
/
V -
Aboye 550 C (8 23 K). loni2ation and
1---f>· , • t · fHI f'-GJ< I .., / - tsapeet;ne · , yge n..
Nitlgen Lead to Lower / / Tern eratures i, the Gases
Do nstrea m o the Bow Snock.
/
V
/ I
/
V /
I 0 10 20 30 40 50 60 70 80 90 100
Mach Number
Figure 16. Peak Shock Layer Temperature for Hypersonic Objects.
UNCLASSIFIED//FQlil QlifilEIAL: Wlili O,.L'l
22

[Page 27]
UNCLASSIFIED/fFOR. QFFIEl.t.L: Uii QD:I! X
Commercial and Governmental IR Systems
There is a long history in the United States of the usage of IR detectors to sense launches
and to track the trajectory of ICBMs.21 ARPA initiated studies of the possible use of IR
detection of aircraft and missiles in the 1950s. Under their Defense Support Program (DSP),
Joseph Knopaw studied the possible use of IR detectors in satellites to detect missiles and
the hot exhaust plumes of ICBMs. Rand Corporation submitted a report in 1955 that outlined
the detection of ICBM launches from satellites in Earth orbit. In 1956, the U.S. Air Force
chose Lockheed as the lead designer with Joseph Knopaw as the project manager for
Subsystem G, ICBM Attack Alarm System (WS-117L) .
By 1958, control of the Air Force system shifted to ARPA (Advanced Research Projects
Agency) as the MIDAS missile defense alarm system. The satellite IR detection system could
alert the Strategic Air Command of possible Soviet missile launches 15 minutes earlier than
the DEW system could . The first successful satellite launch occurred in 1960 with a 300-mile
orbit. In 1963, MIDAS 9 with a 2,250-mile polar orbit succeeded in detecting nine missile
launches using an 8-inch concentric telescope and an Aerojet-General IR detector.
In 1964, the Air Force launched the RJS-2 satellites into geosynchronous orbit over the
equator. The MIDAS system was renamed the Defense Support Program in 1969 and an
agreement between the United States and Australia provided communication to the
constellation of MIDAS satellites from the Overseas Ground Station (OGS) in Australia and
the Continental Ground Station (CGS) at the Buckley Air National Guard Station in the United
States. Four Phase 1 Integrated Missile Early Warning Satellites (!MEWS) were launched
between 1970 and 1973 followed by Phase 2 satellites from 1975 to 1977, the Multi-Orbit
Satellite/Performance Improvement Modification (MOS/PIM) models from 1979 to 1984, two
Sensor Evolutionary Development (SED) satellites from 1984 to 1987, and DSP-1 satellites
since 1989. The DSP satellites are designed for the global monitoring of ICBMs, SLBMs, and
tactical missiles. Their operating life is 5 to 7 years, and they weigh approximately 5,000
lbs. With 6,000 IR telescopic detectors, these satellites monitor IR emissions between 2. 7
and 4.3 microns. The 23rd, and last, DSP satellite was launched in November 2007.
The DSP system is capable of monitoring more than ICBMs. In 1972, the system detected a
large meteor passing over several western states 94 km above the Earth. This meteor,
moving at 18 km/s, was on a trajectory over Salt Lake City that would have done significant
damage if it had impacted the Earth. In 1991, DSP satellites detected the launch of 88 Iraqi
SCUD missiles. The DSP system is currently controlled under the ALERT (attack and launch
early report to theater) system under the ALERT Control Center located at Shriever Air Force
Base in Colorado. The current operational inventory is classified .
Other commercial IR detection equipment includes the Lucid Dimensions Spherical Detection
System (SDS) using a 3D spherical sensor array. 22 This system is designed to track ballistic
missiles, aircraft, and vehicles. Developed under an SBIR, this system can be mounted on
ground-based vehicles, ships, or aircraft.
LIDAR
LIDAR, or "light detection and ranging," uses pulses of laser light directed toward a target.
Reflected light is detected and, through the time of flight of the laser beam, the distance to
the target can be computed. While LIDAR systems are similar in function to RADAR systems,
the highly directional nature of the laser beam permits a very accurate determination of
target distance. As an example, reflected panels left on the moon's surface by the Apollo
astronauts are now used to accurately monitor the distance from the Earth to the moon using
UNCLASSIFIED//FQA: QlililEl.t.L: W&li ONL'l
23

[Page 28]
UNCLASSIFIED/fFOR. QFFIEIA.L: Ulii Qt!! X
LIDAR. By attaching a rotating mirror to vary the direction of the laser beam, it is possible to
traverse the laser across surfaces to develop 3-D maps of objects using "imaging LIDAR." As
an example, during the DARPA challenge held in the Nevada desert in 2005, autonomous
automobiles used LIDAR to build a map of all objects in front of the vehicle and used it for
collision avoidance and navigation. LIDAR systems have also been used to obtain accurate
maps of the surface of mars from the Mars Orbiting Global Surveyer. LIDAR systems for
meteorological studies are often mounted in aircraft and fired from the side of the fuselage to
obtain a two-dimensional horizontal map of the atmospheric conditions.
A measurement technique known as Laser Doppler Velocimetry (LDV) uses the Doppler shift
in the transmitted and reflected laser light to measure the velocity of the target and the
properties of the air along the axis of the laser beam.
LIDAR systems using pulsed YAG lasers are capable of measuring many properties of air
along the path of the laser beam. As shown in Figure 17, if a laser pulse is fired toward a
distant target, light is reflected from particles in the atmosphere and this light is collected
through a beamsplitter and directed to a photodetector. By knowing the time interval
between generation of the laser pulse and the time that each reflected signal is received, the
distance along the beam can be accurately determined for each data set. By recording this
optical information as a function of time, using Raman spectroscopy, particle light scattering,
and absorption theory, multiple properties of the air and particles in the air along the path of
the laser can be measured as a function of distance from the transmitter. Particle density,
velocity, and chemical species can be measured using pulsed LIDAR systems. Concentration
of airborne gas species (oxygen, nitrogen), air temperature, and air velocity can also be
measured in this fashion.
v(x, YI
~
v(x,y)
~ X,Y
v(x.y) ~
v(x,y)
Laser Beam
Supel50fliC
Vehicle and
Turbulent Wake
Figure 17. Schematic of a Pulsed LIDAR System.
UNCLASSIFIED//FQR QfifilEIA.k W&li O,.L\f
24

[Page 29]
UNCLASSIFIED/fFOR. QFFIEIA.L: Ulii Qt!! X
LIDAR can be used to detect and monitor hypersonic objects in several ways. By using a
micropulse laser, a LIDAR system could be used to scan the sky for supersonic airborne
objects. LIDAR can also detect the presence of a hypersonic vehicle by measuring the air
velocities in the long turbulent wakes that they leave in the atmosphere. Electro Optic
Systems in Sydney, Australia, 23 has announced a laser tracking system that can track objects
in low-Earth orbit that are as small as 100 mm (4 inches). These objects pose a risk to
satellites and manned space vehicles due to their high velocities (~ 8 km/s). There are an
estimated 200,000 such objects greater than 10 mm in size currently orbiting the Earth.
In the testing of hypersonic aircraft, a dedicated LIDAR system trained on the turbulent wake
could measure the temperature and velocity distribution within the wake. This information
can be used to design aircraft that would minimize detectability and increase vehicle
rel iability. The U.S. Army, for example, reported on the use of a LIDAR system to monitor
atmospheric particulates from the erosion of nose-cones on Athena-H reentry missions at the
White Sands Missile Range in New Mexico in 1973. 24 The LIDAR system monitored the path
of the reentry vehicles at altitudes of 9.3 km and 14.3 km and determined the concentration
of erosion products and ice particles along the laser beam path.
ACOUSTIC AND SEISMIC METHODS
Infrasound
Microphones can be used as a chronograph to measure the velocity of airborne objects. A
supersonic aircraft generates a three-dimensional bow shock referred to as a "Mach cone ." If
the aircraft's Mach cone, which is actually a pressure pulse, sweeps over two microphones
separated by a distance, the velocity of the aircraft can be measured. In Figure 18, two
microphones can sense the dramatic pressure increase that occurs behind a shock wave and
determine the velocity by dividing the microphone separation distance by the delay time.
Sound waves generated by the aircraft and the shock do not reach a terrestrial microphone
until the Mach cone reaches the detector. The Mach cone has a half angle given by
f3 = arcsin (1/M), and this yields a method of detecting the aircraft altitude, H:
(20)
"Infrasound" refers to subaudible (< 100 Hz) sound waves that are generated by explosions,
sonic booms, and rocket exhaust. I nfrasound can be sensed by pressure transducers t hat
detect the very small changes in atmospheric pressure that are induced by these events.
The U.S. Air Force installed a network of infrasound stations around the country in the 1960s
to detect the detonation of nuclear devices. Each station was composed of multiple pressure
transducers so that the direction of the sound waves could be detected at the location of
each station.
UNCLASSIFIED//EQA: QlililEl.t.L: W&&: O,.L'l
25

[Page 30]
UNCLASSIFIED/fFOR. QFFIEl.t.L: Uii QD:I! X
Mach Cone
H
~ = arcsin(l/M) = Mach Angle
Bow Shock
Acoustic
Detector
D
Figure 18. Mach Cone Generated by a Supersonic Object.
The Los Alamos National Laboratory still operates four of these stations that were installed in
1983 at various locations in the United States. 25 These infrasound detector stations are
relatively inexpensive and are easy to maintain. While they have not yet been used to sense
nuclear detonations, they do detect sonic booms, and they were responsible for identifying
and tracking two large bolides, or brilliant meteors, that entered the Earth's atmosphere in
2000 and 2001. While capable of sensing meteors as small as a baseball, in 2001, a large
bolide entered the Earth's atmosphere over the Pacific Ocean and exploded near Baja
California. The bolide was estimated to have a 3.6-meter diameter and exploded with the
energy of 6,000 tons of TNT.
Even a single infrasound station can track a meteor. On 4 October 1996, a station in
Colorado observed a meteor near Bakersfield, California. 26
Another infrasound station network includes the I nternational Monitoring System, a network
of 321 stations around the world designed to monitor explosions that would represent
violations of the Comprehensive Nuclear Test Ban Treaty. Although this network may be a
useful worldwide resource for the detection of meteors, reentry vehicles, and hypersonic
flights, its use in the detection of nuclear explosions is dubious given the circumstances of
November 1999. During this event, a sonic boom was monitored in the skies above northern
Germany. The information provided by the network could not differentiate between a meteor
and a nuclear explosion.
UNCLASSIFIED//EQA: QlililEl.t.L: W&&: O,.L'l
26

[Page 31]
UNCLASSIFIED/fFOR. QFFIEl.t.L: Uii QD:I! X
Infrasound stations, or observatories, could also be used to monitor the acoustic signature of
meteors or supersonic aircraft based on their shock waves or the disturbances caused by
their turbulent wake. Some meteors, for example, produce subsonic sound from 1 to 5 Hz
for several minutes during their flight through the atmosphere. This data could be developed
to identify the speed, altitude, and type of object moving through the atmosphere.
Seismic
When a sonic boom is generated by a meteor or an aircraft, the sound waves pass through
the atmosphere at the speed of sound in air at about 343 m/s. Infrasound stations pick up
the pressure variations caused by the shock wave many minutes after the event occurred,
depending upon the distance between the supersonic object and the station. When a Mach
cone generated by a shockwave strikes the ground as shown in Figure 18, the pressure pulse
is propagated into the ground and travels as a high-speed N-wave at a velocity far exceeding
the speed of sound in air.
Ground-based vibrations caused by sonic booms have been detected by seismic sensors
originally designed to detect earthquakes as documented by Cates and Sturtevant. 27 Caltech
and the U.S.G.S. operate 200 seismographic stations throughout Southern California as part
of the TERRAscope seismic network. The network employs detectors that can sense ground
vibration between 1 and 20 Hz.
The network was actually used to detect the sonic boom and pressure vibration induced by
the flight of supersonic aircraft and reentry vehicles. On 9 December 1993, the network
successfully detected the flight of an SR-71 flying over Edwards Air Force Base at a
maximum speed of Mach 3.2. On 30 January 1992, the network was also used to detect the
reentry of the space shuttle Discovery, STS-42, over the Pacific Ocean and landing at
Edwards Air Force Base.
Another Discovery landing on the west coast was monitored by 66 seismic stations in
Washington and Oregon. The shuttle was monitored by this seismic network for 500 km of
its trajectory through the atmosphere. The seismic data from these stations showed the
hyperbolic shape of the Mach cone as it impacted the surface of the earth. The angle of the
Mach cone showed that the shuttle was traveling at Mach 14, corresponding to an altitude of
55 km.
One interesting investigation that involved the use of these seismic arrays involved
mysterious sonic booms heard over Southern California in 1991 and 1992. By using data
from the TERRAscope array, the source of these disturbances was traced to two F-4 Phantom
aircraft flying over Edwards Air Force Base at speeds near Mach 1.
Since the TERRAscope array is designed to detect seismic activity, including earthquakes and
volcanoes, the detection of meteors and supersonic aircraft generate unwanted data.
Caltech has been adding atmospheric pressure transducers to its seismic network to detect
and remove airborne signals from the seismic data. Conversely, by combining the infrasound
network data operated by the Los Alamos National Laboratory with data from seismic arrays,
data from explosions, volcanic eruptions, and other terrestrial sources can be eliminated
from infrasound data to better detect the presence of meteors, reentry vehicles, and
supersonic aircraft.
UNCLASSIFIED//EQA: QlililEl.t.L: W&&: O,.L'l
27

[Page 32]
UNCLASSIFIED/fFOR. QFFIEl.t.L: Uii QD:I! X
Chapter 4: Vision of Progress Over the Next 30 Years
While there are several methods that can be used to sense high-speed supersonic objects,
technology changes in aircraft will generate the need for newer detection and tracking
techniques. Listed below are five important categories of objects capable of hypersonic
speeds. Over the next 30 years, the ability to reliably and accurately detect them will be
critical.
• Space Debris - Technology is currently available to detect space debris using RADAR and
cameras. Novel methods using coronographs 28 during daylight have been shown to
detect the reflected light from millimeter-size debris particles in orbit, and existing
telescopes are capable of detecting meteors that pose a risk to Earth. Space debris
reentering the Earth's atmosphere can reach speeds of over 17,000 miles per hour or
Mach 23.
• Reentry Craft - The highest recorded speed for any manmade vehicle was the Apollo 10
reentry capsule in 1969. It reached a velocity of 24,790 mph, or Mach 36. Reentry
vehicles are currently monitored by ground-based telescopes and RADAR and through
satellite imagery.
• Meteors - The systems used to monitor missiles and satellites based on RADAR and
optical devices can currently detect and track meteors entering the Earth's atmosphere.
Further development of acoustic and radio detection techniques should be pursued over
the next 30 years.
• Missiles - The Cold War generated the need for equipment to monitor hostile missile
launches, to track their path, and to estimate the location of their targets based on
ballistic trajectories. The United States Space Surveillance Network, for example, is
composed of a worldwide collection of RADAR, electro-optical detectors, and passive RF
devices that can track satellites, missiles, and aircraft. They maintain an inventory of
satellites in Earth orbit and, through the Space Surveillance Telescope program (SST),
asteroids and other faint objects in space are detected and tracked. GEODSS (Ground￾Based Electro-Optical Deep Space Surveillance) telescopes monitor space at 3 different
locations around the globe with high enough resolution to detect a basketball 20,000
miles from the Earth. Continued vigilance from governments around the world will likely
increase the development of technology to detect and track high-speed objects in the
atmosphere and in space over the next 30 years with an emphasis on RADAR and optical
detection.
• Hypersonic Aircraft - Over the next three decades, hypersonic aircraft development will
likely spur an increased need for new technology to detect their presence. While the X-15
rocket plane exceeded Mach 6 (4,520 mph) as early as 1967, continued development of
high-speed aircraft will continue to meet needs in the following areas:
o SSTO (Single Stage to Orbit) - Long the dream of NASA and space exploration
enthusiasts, technology has been under development to replace the Space Shuttle
using aircraft that can take off from a conventional runway and attain low-Earth
orbit. The X-43A scram jet, part of NASA's Hyper X Program and fueled by
hydrogen fuel was successfully tested in 2004. This aircraft is capable of 7,000
mph or Mach 9.8 flight.
UNCLASSIFIED//EQA: QlililEl.t.L: W&&: O,.L'l
28

[Page 33]
UNCLASSIFIED/fFOR. QFFIEIA.L: Ulii Qt!! X
o Manned military jet fighters - The fastest military jet is the MIG-25 Foxbat at
2,115 mph (M = 3). The fastest U.S. jet is the F-15 at 1,875 mph (Mach 2.6).
Current U.S. efforts are concentrating on unmanned vehicles, such as the X-43A.
o Surveillance aircraft - The SR-71a "Blackbird" achieved 2,056 mph (Mach 3.3) in
1976 using an air-breathing engine. Its rumored replacement, the SR-91 Aurora,
would have been capable of Mach 6. In 2008, the U.S. Air Force entered into an
agreement to design a Mach 6 unmanned "blackswift" aircraft using a scramjet.
o Passenger jets - The current record holder is the Tupolev Tu-144 "charger" at
1,553 mph (Mach 2.15). Reaction Engines Limited has proposed the A2 hypersonic
passenger liner using liquid hydrogen to fuel the aircraft and to cool the wings and
fuselage. This aircraft is expected to achieve Mach 5. In 2000, Russia and the
People's Republic of China entered into a 25-year agreement to develop the
Leninetz AYAKS hypersonic transport plane using kerosene fuel and a variety of
techniques to attain Mach 8 to 10. An MHD (magnetohydrodynamic) engine is
used to further accelerate combustion products produced by the engine. Lasers
and RF generators are employed to disrupt the bow shock, reducing drag and
doubling the velocity of the vehicle.
o Stealth missiles - The USAF Falcon Project planned for building a Mach 6 HTV-3V
"Blackswift" platform but was cancelled in 2008. The NASA X-51 scramjet vehicle
is based on the Falcon scramjet and is scheduled for testing in 2010. This vehicle
is capable of Mach 7+.
DETECTABILITY OF NEW HYPERSONIC AIRCRAFT
While conventional RADAR and optical systems may be able to track existing vehicles, future
aircraft capable of Mach 8 and above are now being designed and tested. New propulsion
technology and drag reduction techniques also offer new ways to detect such aircraft. Based
on a review of hypersonic vehicle detection and tracking, four recommendations are made for
research and technology development over the next 30 years to increase the detectability of
hypersonic objects passing through the Earth's atmosphere.
Recommendation #1 - Build a Database of the Wake Characteristics for
Existing Aircraft
There is considerable information about the aircraft contained within the turbulent wake that
trails it. The wake provides an indication of the vehicle's path and its current bearing. By
analyzing the Strouhal eddy formation, it is possible to ascertain its velocity and hydraulic
diameter. The wake can also provide information on the chemical combustion products that
can be obtained through LIDAR and can indicate the fuel used by the aircraft. Some aircraft,
such as the X-43A and the proposed Reaction Engines Limited A2, use hydrogen as the fuel,
so the absence of carbon molecules in their turbulent wakes could aid in their identification.
Authors Mark Garnet and Aaron Altman from the University of Dayton29 proposed the
development of a database of turbulent wake data for conventional aircraft to allow their
identification. They point out that, although the aircraft may be designed for stealth, their
wakes cannot be hidden. They presented data on the unique characteristics that can be used
to identify the wakes generated by the F-15, F-16, F-18, and B-52. They also point out the
UNCLASSIFIED//FQR QfifilEIA.k W&lii O,.L\f
29

[Page 34]
UNCLASSIFIED/fFOR. QFFIEl.t.L: Uii QD:I! X
need for computational modeling of hypersonic wakes to predict the characteristic signature
of new, unknown aircraft.
A hypersonic vehicle database of wake characteristics for existing aircraft should be
developed based on optical and Doppler RADAR data. Doppler RADAR provides information
on turbulent intensities and eddy formation within the wake. Computational fluid mechanics
models of hypersonic wakes have been done since the early 1960s, such as the work done by
Zieberg and Bleich. 30 Such modeling work should continue capitalizing on the increasing
computer performance that will be available during the next 30 years.
Recommendation #2 - Exploit the Detectability of Hypersonic Aircraft
Based on the Features That Allow Them To Fly Efficiently at High Speeds
Several new propulsion systems for hypersonic aircraft will be tested over the next 30 years.
These include pulsed detonation engines (PDE) successfully tested in 2008 by the Air Force
Research Laboratory and Innovative Scientific Solutions, Inc. over the Mojave Desert. While
these engines are capable of Mach > 6, they have one characteristic that makes them very
detectable. The pulsed detonation of combustible fuel creates a wake with periodic bulges
referred to as "donuts on a rope." As mentioned earlier, measurements of the turbulent
wake behind hypersonic aircraft can be used for detection, identification, and tracking.
The AYAKS hypersonic transport plane under development in Russia uses an MHD engine,
lasers, and RF generators to decrease aircraft drag. The lasers and RF ionize the air ahead of
the aircraft, creating a plasma to disrupt the bow shock and significantly reduce aerodynamic
drag. Drag reduction allows the aircraft to double its maximum speed. The RF and laser
emissions from this aircraft can possibly be used to detect the aircraft in flight from ground￾based antenna or telescopes or from satellites. The MHD engine also generates
electromagnetic radiation that can possibly be detected.
Every new propulsion or drag reduction system under development will have some
characteristic that may make it more detectable from the ground or from satellite. The
Aerospike engine proposed for the SSTO and under development by Rocketdyne and Garvey
Spacecraft involves the use of a novel virtual Laval nozzle that is external to the engine. The
IR emissions from an Aerospike engine may increase its detectability.
Recommendation #3 - Explore the Detection of Vehicles Designed To Be
Undetectable
Over the next 30 years, hypersonic cruise missiles will have the ability to travel at speeds of
up to Mach 8 decreasing the chances of being detected or defeated by antimissiles. The
unmanned NASA X-51 tested in 2010 is capable of greater than Mach 7 (over 4,000 mph),
for example, and is designed to be launched from a B-52. The DARPA/USAF Falcon Project
has resulted in the testing of the HTV-2 at Mach 6. 7 over the Pacific Ocean, designed as a
hypersonic cruise vehicle.
Efforts to disguise aircraft through the use of novel vehicle shapes and stealth materials can
also increase their detectability in other ways. Golovitichev and Hansson presented a paper
in 199931 that stated the following:
"The concentrated energy drag reduction concept has proven to be effective for the
cruise range vehicles, preventing the missile deceleration with the benefit that the
spike "products" could envelope the missile in a film of ionized gas which would be
impervious to RADAR pulses, thereby rendering it electronically "invisible". The infra￾UNCLASSIFIED//EQA: QlililEl.t.L: W&&: O,.L'l
30

[Page 35]
UNCLASSIFIED/fFOR. QFFIEl.t.L: Uii QD:I! X
red penalty at close range would be significantly offset by the high speed of the
flight."
This discussion about the AJAX engine concerned the generation of ion combustion products
that would be further accelerated by an MHD (magnetohydrodynamic drive) . The increased
number of various carbon -based molecules in the wake of this aircraft could be detected
using LIDAR. The increased temperature near the surface of this aircraft would also increase
its detectabi lity due to increased emission of infrared radiation. For AJAX (AYAK) vehicles,
development of enhanced LIDAR systems and IR detectors should proceed over the next 30
years to increase their detection and tracking.
Recommendation #4 - Explore the Development of Novel Detectors
One characteristic of hypersonic flight (M > 5) is the ionization of air in the region
downstream of the bow shock and the disassociation of oxygen and nitrogen at very high
speeds. When electrons recombine with ions generated by the shock, they emit
electromagnetic radiation that can be detected. This radiation extends from the visible
range, as evidenced by the glowing trail left by meteors entering the Earth's atmosphere, but
the emitted radiation also extends into the ultraviolet and x-ray range. Although such
electro-optical sensors are likely part of the existing DARPA/USAF space surveillance system,
telescope systems that monitor the UV range should be developed, along with x-ray
detectors capable of monitoring the atmosphere.
Hypersonic objects passing through the atmosphere disassociate nitrogen and oxygen which
recombine in the object's turbulent wake. During recombination, new molecules are created,
including NO, NO2, ionized O and N, and combustion products. 32 LIDAR can detect the
presence and concentration of these compounds in vehicle wakes and improved LIDAR
systems should be a priority.
As hypersonic objects pass through the atmosphere, the object becomes ionized with a
significant positive charge. Technology should be developed to sense the flight of objects
with an electrostatic charge as they pass through the atmosphere.
SUMMARY
Each detection system discussed in the previous section has both benefits and problems. A
comparison of the various detection techniques is shown in Figure 19 based on their ability to
detect specific properties, relative cost, and accuracy.
Infrared detection systems and multispectral cameras installed on satellites, such as the KH￾11, provide surveillance of large portions of the Earth for possible missile launches, reentry
vehicle trajectories, meteor wakes, and hypersonic vehicles. RADAR systems based on
satellites, ships, and aircraft can detect the position and velocity of such hypersonic objects
at varying range. AWACS, for example, can detect objects at up to 370 km with a resolution
of 0.5 meters. TRADEX can track up to six objects at a distance of 1,400 km with an
accuracy of 3 meters and a velocity resolution of 0.01 m/s.
UNCLASSIFIED//EQA: QlililEl.t.L: W&&: O,.L'l
31

[Page 36]
UNCLASSIFIED/fFOR. QFFIEl.t.L: Uii QD:I! X
Detection Method Properties Detected Availability Useful for Detection of:
I Distance Velocity Altitude Whole Sky Commercially Existing Expense Meteor Reentry Aircraft
I To Target Or Directed Available Network Detection Vehicles
Electromagnetic
Radar I X X X Both X X Modest X X X
Radio Reflection Detection Whole Sky X Low X X
I
Optical I
Sky Cameras, Photographic Whole Sky X X Low X X X
Infrared I possible Both X Modest X X X
Lidar I X X Directed X Medium X X X
Chronograph X Directted low
I
Acoustic and Seismic
lnfrasound X X Whole Sky X X low X X X
Seismic I X X Whole Sky X Modest X X X
I
Figure 19. Comparison of Detection Technology for Hypersonic Objects.
LIDAR systems provide detailed information on velocity, temperature, particle velocity, and
atmospheric composition along the path of the laser beam that can be used to interrogate
vehicle wakes and exhaust plumes. Seismic and infrasound systems continuously operate
and can provide information on the path followed by a high-speed aircra~ or object by
tracking its sonic boom and low-frequency acoustic signature. Finally, optical cameras
aimed toward the Earth provide valuable information on hypersonic object tracks by
recording their tracks. Aimed toward space, optical cameras are tracking asteroids and other
spaceborne objects that may enter the atmosphere as a meteor posing a risk.
UNCLASSIFIED//EQA: QlililEl.t.L: W&&: O,.L'l
32

[Page 37]
UNCLASSIFIED/fFOR. QFFIEl.t.L: U&i QD:I! X
Appendix A: MathCad Program Used To Estimate Hypersonic
Vehicle Surface Temperature
Modeling of the Thermodynamic Properties
Of Airflow about Hypersonic Vehicles
I Purpose: Compute the properties across the bow shock of a hypersonic vehicle moving
through the earth's atmosphere.
A. Define the Aircraft Velocity
.- 3300· .fi>H ,Wv Vehicle Velocity.
H := 10-km Vehicle Altitute. NW
Note that the Karman Level corresponds to 100 km altitude
where the atmosphere essentially ends.
8 . Compute the Mach number for the Vehicle
Tatm(H) = 222.986K
a = 2993:16~ s
C. Compute the Stagnation Properties Upstream of the Bow Shock
I I = -21.986K
I ot = l-~'06 103K
P1 := Pa1In(H) Pt = 0.l6t -a1m
1
Pol :=p1 {t + = 1·- i2) i - l Pot = l.26.9 ·atrn
UNCLASSIFIED//FQlil QlifilEIAL: Wlili O,.L'l
33

[Page 38]
UNCLASSIFIED &+F@R-OFFIGEAL-USE-ONLY.
D. Compute the Properties on the Downstream Side of the Bow Shock at the Nose
1. The following functions describe the change in properties across a normal shock.
= 2
1+ om? (y + 1)-My
M,(M,) = |———_— Prato(Ma) = 2
M2 (y =D) 2+ (y -1)-My
(hi == >
2
27 2 1
Pratio( M =1+2(m -1) Unstiog( My) = ——
Rati 1) ytl 1 ae | 1) Pratio(M1)
2+(y -)-M,
27 2 cia |
Tratio(M) -[1 + ar (um = i} —_—
(y + My
a. Stagnation temperature and pressure ratios.
Ty ratio(M1) = 10
ae
y-l
Pol 2
[1 ontn)y|
Po.atio1) = Prati)" —
wii, at
(: + tm’)
2
2. Compute the properties across a normal shock for this problem.
Mar M,(Mj) My = 0416
Ty= Ty-Tratio(M1) Tp = 1.263 x 10°K
5
P2= PPratio(M) Po = 7.447 x 10° Pa
= M = 3.624 10°Pa
Po2 = PorPratiol 1) Rod nce
34
UNCLASSIFIED £4502.0551601-U5E-ONEY=

[Page 39]
UNCLASSIFIED &*+F@R-OFFIGLAL-USE-ONLY..
T.2* Tor Tratio(Mi) Typ = 7.396 x 10°K
5 1
Bs ose SO This is the Mach angle for a blunt-nosed object.
E. Compute the Peak Wavelength of Emitted Infrared Energy
1. Using Wien's Displacement Law, compute the peak wavelength of emitted radiation.
b= 2.8977685:10 *.mK
b 3
hmax*= max = 2295 x 10°-nm
2
Imax = 2-295-micron
— 6
Iemax = 2-295 10 °'m
2. Using Planck's Law, compute the distribution of emitted energy with wavelength.
ae 8-n-h-e 5
ee 5 | he Spectral Energy Density for a Black Body
a ra Radiator in energy per unit volume per unit
“kT
é -1 wavelength.
35
UNCLASSIFIED L4502..05516041-U5E-ONE-

[Page 40]
UNCLASSIFIED #}F@R-OFFIGEAL-USE-ONLY.
600
ee ee ee ee ee
oi _| | | |
a se ee ee
a
ee
a ee ee ee
| =| | |
je ee ee ee
2x10~° 4xio"° 6x10~° ax10-® 1x107>
a
36
UNCLASSIFIED L4502.055167FA1-U6E-ONE-

[Page 41]
UNCLASSIFIED/,SFOR. QFFIElal L: 1!ii 011! X
II. Definition of Units
mile MPH = ­
hr
- 34 h =6.62606896 10 •J-s Plane k '.s Constant.
- 23 J k =1.380650410 · - Boltzmann Constant. K
8 m C =2.99792458- 10 ·­
S Speed of light in a vacuum.
Ill. Properties of Atmospheric Air
A. Fundamental properties.
'Y = 1.4 Ratio of specific heats for air.
J
R · =287--- a tr kg -K Gas constant for air.
B. U.S. Standard Atmosphere
1. The raw data is included in the matrix "data."
2. Functions will be de\€1oped from a cubic spline interpolation of the data
data = cs 01t(data,0)
3 )(o) ( height = 10 data -m
3 )( 1) ( press ure = 10 data -Pa
('}) temperature= data · K
. (3) kg density= data ·-
3 m
press urefit = cs plin e(heigh t, press ure)
UNCLASSIFIED//FOR 0661El.t.L: W&&: OttLY
37

[Page 42: illegible]

[Page 43]
UNCLASSIFIED &*+F@R-OFFIGTAL-USE-ONLY.
temperatures, = cspline(height, temperature)
dens itys, = cspline(height, dens ity)
3. These functions provide atmospheric pressure, temperature, and density for the U.S.
Standard Atmosphere from 0 to 100 km in height.
Patm(h) = interp(press ureg, height, press ure, h) Pres sure (Pa).
Tatm(h) = interp(temperatureg,, height, temperature, h) Temperature (K).
Patm(h) = interp(dens ity gy-height, density,h) Density (kg/m‘3).
: | ft | ft
+o
6x10"
"| Ab Ef
™ Lai
0 2x10" 4xio* 6x10" sxio* 1x10"
height
39
UNCLASSIFIED L4502.-055160i-USE-ONEY=

[Page 44: illegible]

[Page 45]
UNCLASSIFIED/,SFOR. QFFIElal L: 1!ii 011! X
1 Dyrud, L. P., et al, "Meteor velocity determination with plasma physics," Atmospheric Chemistry and Physics, 4, pp. 817-
824, 2004.
2 Anderson, John D., Modern Compressible Flow, 3rd ed., McGraw-Hill, 2003.
3 Anderson, John D., Fundamentals of Aerodynamics, 5th ed., McGraw-Hill, 2007.
4 White, Frank M., Fluid Mechanics, 7th ed ., McGraw-Hill, 2003.
5 White, Frank M., Fluid Mechanics, 7th ed ., McGraw-Hill, 2003.
6 Carter, R. T., et al, "Estimating the Drag Coefficients of Meteorites for All Mach Number Regimes," 40th Lunar and
Planetary Science Conference, pp. 2059-2060, 2009.
7 Macrossan, M. N., "Scaling parameters for hypersonic flow: correlation of sphere drag data," Center for Hypersonics,
University of Queensland, Brisbane, Australia.
8 Brown, Louis, A RADAR History of World War II, Institute of Physics Publishing, Bristol, England, 1999 (ISBN 0-7503-
0659-9).
9 Luck, David G., Frequency Modulated RADAR, RCA Labs, McGraw-Hill, 1949.
10 Headrick, J.M., et al, "A MADRE ICBM Detection : Some Trajectory Parameter Determinations when Employing
Ionospheric Refraction," Naval Research Laboratory Report, AD596673, December 1, 1961 .
11 "Technical Verification Systems, Detection of Reentry Vehicles," Bulletin of the Atomic Scientists, Vol. 41, No 1, p. 39,
January, 1985.
12 West, Adrian, "Detecting Meteors using Radio,"
http://newburyas.wordpress.com/2009/12/12/detecting-meteors-usi ng-radio/, 7/15/2010.
13 Barricklow, Sam, "Aurigid Meteor Shower Radio Echoes, September 1, 2007," http://www.k5kj.net/Aurigid_2007.htm,
7/15/2010.
14 Gamble, Jim, http://elpallskycamera.us, 2010.
15 P. Spurny, J. Oberst, D. Heinlein (2003) . "Photographic observations of Neuschwanstein, a second meteorite from the
orbit of the Pribram chondrite" . Nature 423 (6936) : 151-153.
16 Oberst, J.; Molau, 5.; Heinlein, D.; Gritzner, C.; Schindler, M.; Spurny, P.; Ceplecha, Z.; Rendtel, J.; Betlem, H.. "The
"European Fireball Network" : Current status and future prospects" . Meteoritics & Planetary Science 33 (1) : 49, 1998.
17 http://www. rcktmom .com/njlworks/MeteorTrackingPpr. html
18 Beatty, Kelly, " Meteorites Found from Asteroid 2008 TC3,
http://www.skyandtelescope.com/community/skyblog/newsblog/41873107 .html, retrieved 7/10/2010.
19 Bird, R. B., Steward, W., Lightfoot, E., Transport Phenomenon, John Wiley & Sons, p. 432, 1960.
2°Kidd, J., and Caldwell, H, USAF, "Defense Support Programs to Support a Changing World," AIAA Space Programs and
Technologies Conference, Huntsville, AL, March 24, 1992.
21 Bayne, Walter J., Air Warfare: An International Encyclopedia,Volume 1, ABC-CLIO, Inc., Santa Barbara, CA, pp. 169 -
172, 2002.
22 " Lucid Dimensions Spherical Detection Systems (SDS) 3D Passive Infrared (IR)", http://www.defensereview.com/lucid￾dimensions-spherical-detection-sds-3d-passive-system, downloaded 7/14/2010.
23 "Australian laser system to track space junk,"
http://news.yahoo.com/s/afp/20100720/sc_afp/technologyaustraliasciencespacelaser_2010, 7/20/2010.
41
UNCLASSIFIED,','FQR. QFFIEl.t.L: Wii Qf!IL:¥

[Page 46]
UNCLASSIFIED/,SFOR. QFFIElal L: 1!ii 011! X
24 Roberto, Rubio, "LI DAR Detection of Subvisible Reentry Vehicle Erosive Atmospheric Material," Army Electronics
Command, Fort Monmouth, New Jersey, DTIC Number ADA041085, March, 1977.
25 Britt, Robert Roy, "Listening for Nukes: A Meteor Detection Project,"
http://www.space.com/scienceastronomy/solarsystem/nuke_meteor _010524.html, May 24, 2001.
26 Bedard, A. J., "Infrasonic and Near Infrasonic Atmospheric Sounding and Imaging," U.S. Department of Commerce,
http://www.esrl.noaa. gov /psd/programs/infrasound/infrasound . html, 7/15/2010.
27 Cates, Joseph E., and Sturtevant, Bradford, "Seismic detection of sonic booms, " Journal of the Acoustic Society of
America, vol. 111, no 1, part 2, pp. 614 - 628, January, 2002.
28 Koutchmy, S. and Nitshelm, C., "Optical Detection of Space Debris using a Large Achromatic Coronograph,"
Astrophysics and Space Science, vol. 143, pp. 45-49, 1988.
29 Garnet, M., and Altman, A., "Identification of Any Aircraft by Its Unique Turbulent Wake Signature," AIAA, Journal of
Aircraft, vol. 46, no 1, pp. 263-268, 2009.
30 Zeiberg, S. and Bleich, G., "Finite-Difference Calculation of Hypersonic Wakes," AIAA Journal, vol 2, no 8, pp. 1396,
1964.
31 Golovitchev, V. I., and Hansson, J., "Some Trends in Improving Hypersonic Vehicles' Aerodynamics and Propulsion
(Fundamentals of AJAX Project)," XIV ISABE Conference, September 5-10, 1999, Florence Italy.
32 Stepanov, M., "Study of Thermochemical Nonequilibrium in Hypersonic Far Wakes in the Atmosphere," Fluid Dynamics,
vol. 37, no 1, pp. 138-146, 2002.
UNCLASSIFIED,','FQR. QFFIEl.t.L: Wii Qf!IL:¥
42
