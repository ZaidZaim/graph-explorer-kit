# Historical Document: DOW-UAP-D130_AAWSAP-DIRD-Technological-Approaches-to-Controlling-External-Devices-March-23-2010

## Source Metadata

- Original file: `DOW-UAP-D130_AAWSAP-DIRD-Technological-Approaches-to-Controlling-External-Devices-March-23-2010.pdf`
- Pages: 36 (34 from text layer, 0 OCR, 2 illegible)
- OCR language: `eng`
- Processed at: `2026-09-23T18:09:09.486307+00:00`
- Processing pipeline: `pypdfium2 text layer + Tesseract OCR → Markdown → neo4j-graphrag SimpleKGPipeline`

## Text

[Page 1]
UNCLASSIFIED / /FOTOFFECEAEUSE-ONEE-
iia Defense
Intelligence
Aws// Reference
“= Document
yF ti‘ ‘C;éC;éCOS? Acquisition Threat Support
23 March 2010
ICOD: 1 December 2009
DIA-08-1003-012
Technological Approaches to
Controlling External Devices in
the Absence of Limb-Operated
Interfaces
UNCLASSIFIED / /FOR-OFFTGH-USE-OALY

[Page 2]
UNCLASSIFIED//F8R 8FFl6i,t.k Miili Ot!P X
Technological Approaches to Controlling External Devices
in the Absence of Limb-Operated Interfaces
Prepared by:
Acquisition Support Division (DW0-3)
Defense Warning Office
Directorate for Analysis
Defense Intelligence Agency
Author:
AAP Person 73
Administrative Note
COPYRIGHT WARN ING: Further dissemination of the photographs in this publication is not authorized.
This product is one in a series of advanced technology reports produced in FY 2009
under the Defense Intelligence Agency, Defense Warning Office's Advanced Aerospace
Weapon System Applications (AAWSA) Program. Comments or questions pertaining to
this document should be addressed to !AAP Person 1 l AAWSA Program
Manager, Defense Intelligence Agency, ATTN: CLAR/DWO-3, Bldg 6000, Washington,
DC 20340-5100.
UNCLASSIFIED//FQA &FFIGIAk Wiili ,u11a¥
ii

[Page 3]
UNCLASSIFIED/ /FOlil OFFI&I.t.k WIiii 8Plklf
Contents
Introduction ............................................................................................................v
Direct Neural Signals.............................................................................................. 1
Indirect Neuronal Signals - The BOLD Effect.......................................................... 3
Control of External Devices .................................................................................... 4
Noninvasive Technologies ...................................................................................... 6
EEG ..................................................................................................................... 7
MEG .................................................................................................................... 8
EMG .................................................................................................................... 9
MRI and fMRI ..................................................................................................... 9
NIRS.................................................................................................................... 10
Invasive Technologies.......................................................................................... 10
Open-Loop Direct Cortical Array Algorithm Modeling ....................................... 11
Closed-Loop Peripheral Arrays Utilizing Visual Feedback ................................. 13
MEMS, ECoG, and PSoC Circuitry ...................................................................... 14
Chronic Neural Implants and fMRI ................................................................... 16
New Electrode Designs ..................................................................................... 18
Hybrid Neuro-Robotic Systems for True Closed-Loop BMI ................................ 20
Trials Using Human Subjects ............................................................................ 22
Optical Stimulation of Action Potentials ........................................................... 23
Discussion ............................................................................................................ 23
Noninvasive Electrical Devices ......................................................................... 24
Noninvasive BOLD-Based devices..................................................................... 25
Noninvasive Magnetic Devices ......................................................................... 26
Invasive Technologies - General, Optical, and Ex-Vivo Engineering................. 26
Implantable Chips, Ladders, and Arrays ........................................................... 27
UNCLASSIFIED/ /rOR: orr1e1J1ct U91!! OHL¥
iii

[Page 4]
UNCLASSIFIED/,'FOR: 8ffl@IJllt t:191!! l>flt I
Conclusions .......................................................................................................... 27
Figures
Figure 1. Simplified Rendering of a Neuron ............................................................ 1
Figure 4. Experimental Overview of Brain-Controlled Robot in a Closed Loop
Figure 9. Image Distortion and Custom Microwire Electrode Assembly to
Figure 11. T2 Value Analysis Summary of T2 Values in All the Image Slices That
Figure 2. The General Layout of a Closed-Loop Control Interface........................... 5
Figure 3. Two Commercially Available EEG Sensors................................................ 8
With Visual Feedback Experiment ......................................................... 13
Figure s. Schematic of the Neurochip Functional Blocks ...................................... 15
Figure 6. Implant Location ................................................................................... 16
Figure 7. Histology and Electrode Tracks ............................................................. 17
Figure 8. The Michigan Electrodes ........................................................................ 18
Improve It............................................................................................. 19
Figure 10. Example of T2 Variability..................................................................... 19
Spanned the Electrode Arrays in All Animals ....................................... 20
Figure 12. A Hybrid Neuro-Robotic System .......................................................... 21
Figure 13. Experimental Arrangements ................................................................ 21
UNCLASSIFIED/ /FOil Offl@IJllL YSIE 8Htlf
iv

[Page 5]
UNCLASSIFIED/ /P(Ht err1e1s1tt l!ISI!!! 9HL'I
Technological Approaches to Controlling External Devices
in the Absence of Limb-Operated Interfaces
Introduction
Since the advent of modern interactive control of computers, technologies
have been sought to directly connect the biological and the physical to form a
seamless entity. While science fiction explores the possibilities of shared
consciousness between brains and mainframes, real-life scientists work
toward an equally fantastic but more pedestrian goal of eliminating required
electromechanical human-machine interfaces (HMis). Such technologies
promise integration of thought and computer-controlled action, without the
need for a limb-operated device to translate intent from physiological
networks to physical circuits.
This paper first briefly reviews underlying neural structure, function, and
activity to provide background on the type of signals and the scale of temporal
changes that arise from conscious control within the nervous system. A short
primer on brain-machine interfaces (BMis) is included at the end of the
background material. This is followed by a survey of the state-of-the-art
detection and stimulation technologies available utilizing noninvasive and
invasive methods, including several studies that exemplify research paths
currently being undertaken. Discussion brings together elements of the
technology survey, application limitations, a timeline for useful commercial
deployment, and predicted future research directions. Two technology
research paths are highlighted as the most probable to produce functionally
useful devices (defined as nearly equal or even superior to the control
capabilities of current HMis) in the near and far term.
The technology endpoint this paper seeks is thought-based operation of
remote machinery during normal human activities without mechanical device
interaction-that is, control of external devices without the need to go to a
specified location, such as a shielded room; without the need to remain
perfectly motionless to reduce signal noise; and without the need for
interaction with a normal electro-mechanical device, such as an i-Phone or
other handheld device with buttons and trackballs. Data transfer rates are
sought to exceed 5-10 bits/second to be useful for operation of complex
devices; this rate range and above is referred to as high-bandwidth BMis.
Response time for a 1-of-N selection of commands is targeted at 300
milliseconds or less. These are the operational parameters assumed for final
implementation unless some limitation or supercapability is described.
The paper concludes that noninvasive electrical monitoring of neural activity,
primarily reading combined action of muscles and neurons, is the most
promising commercial technology in the near term. Inherent limitations in the
noninvasive electrical approach require future development of different
research paths. The paper argues, mainly by eliminating other approaches,
that the most probable technology in the long term involves invasive single￾neuron-based direct cortical connections to form a network of high-bandwidth
duplex communication pathways. Currently the most promising technologies
UNCLASSIFIED/ /FOR. OFFIGIAk Uii QPlk¥
V

[Page 6]
UNCLASSIFIED/ /P91t 9Ffl@IAL YSIE 8HLY
for robust construction of such an interface are optical stimulation, gating, and
sensory devices, and chip-based electrode arrays that have been encased in
ex-vivo-engineered neural tissue.
UNCLASSIFIED/ /FOR. orrlEIAL U.!~ Gilt I
vi

[Page 7]
UNCLASSIFIED/ /POR: err1e1At l:191!! er•t I
Direct Neural Signals
The human nervous system has two classes of cells, neurons and glia. Based on all
research to date, it is believed that signals within the network of neurons constitute the
whole of information processing, with gl ial cells playing a purely supporting role. This
neural doctrine has dominated research in BMI until recently and still constitutes the
only major research path in direct technologies. Furthermore, all technologies directly
measuring human neuronal action rely on detecting or influencing electrical activity of
these cells; no current in situ research selectively affects neurotransmitter activity
between local cells for the purpose of information exchange . Therefore, the focus for
the foreseeable future will be on the electrical activity of neurons as the primary target
of BMI.
Neurons consist of four parts: axon, dendrites, cell body or soma, and pre-synaptic
terminals. Electrical information is transmitted to the neuron through the dendrites,
proceeds through the cell body, and leaves the cell through the axon at one or more
pre-synaptic terminals. Neurons have one axon and from one to tens of thousands of
dendrites.
Figure 1. Simplified Rendering of a Neuron. The arrows indicate t he direction in which signals are
conveyed . The single axon conducts signals away from the cell body, while the multiple dendrites receive
signals from the axons of other neurons. The nerve terminals end on the dendrites or cell body of other
neurons or on other cell types, such as muscle or gland cells. (Reference 1)
Chemical details of how the action potentials travel through the cell or are transmitted
across the synapse are not important to the current treatise, other than the distinction
that in these biologically based electrical networks, ions of sodium, potassium, and
chlorine move through the cell membranes perpendicular to the propagation of the
action potential down the axon. This allows information to be transmitted faster than
ions could flow down the axon. The propagation of information is similar to a wave
traveling down a garden hose: quickly move one end of the hose back and forth with
sufficient force, and a wave will travel to the other end of the hose; however, any part
of the hose structure has only moved (nominally) perpendicular to the direction of wave
propagation. In a similar fashion, ions flow through channels across the axon's cell
membrane, changing the local membrane potential and thus propagating the electrical
signal down the axon.
UNCLASSIFIED/;'FOR OFFI&I.t.k Wliliii 8fslk¥
1

[Page 8]
UNCLASSIFIED/;'FOR OFFl&I.t.k Wliliii &NL¥
The signal transmission down the axon of a neuron is an all-or-nothing process. When
the cell body is stimulated above threshold, the axon transmits the same action
potential at the same speed and in the same direction, regardless of the extent above
threshold or duration of the input. Action potentials have durations of 1-10
milliseconds. Input signals can result in transmission of multiple action potentials, and
thus the frequency and number of neuronal firings do vary with the input. Neurons
require some t ime to reset between firings, nominally the duration of the pulse for that
axon, yielding a typical maximum firing rate of between 100 hertz (Hz) and 1 kilohertz
(kHz).
It is instructional at this point to contrast this mechanism with propagation of signals
through a physical electrical circuit, the planned external portion of our BMI. In a
copper wire, electrons carry the signal. Electrons drift along the signal path, but the
signal itself moves as a compression wave rather than a transverse wave as in the
biological system. Going back to our garden hose example, consider the hose now filled
with small marbles: inserting a marble at one end will move each marble in the hose
just a little, but very rapidly the last marble in line will pop out of the far end of the
hose. As with the biological system, the signal is propagated to the far end of the hose
by local actors rather than physical motion of a single ion or electron moving the whole
distance. The underlying physics governing the signal transmission makes metallic and
semimetallic circuits about a million times faster than the biological system.
This difference in the carriers and underlying mechanisms of signal transmission
between biological and physical circuits has so far prevented the invention of a direct
connection between the two disparate systems. Instead, both noninvasive and invasive
direct-detection technologies rely on placing physical sensors or transmitters in close
proximity to the neurons of interest and utilizing classical electrodynamics to govern
signal jump between the systems. Additionally, given the maximum typical firing rate
for neurons of 1 kHz, sampling of action potentials at a few kHz will be fast enough to
detect firing of any individual neuron, though super-sampling above 10 kHz can be used
to reduce noise. Higher sampling frequencies also may be required if multiple neurons
are monitored and quantitative information about their relative firing sequence is
desired . Frequencies of a 1 kHz or below are sufficient to stimulate action potentials,
and again, higher system frequency may be required for multiple neuron sequential
stimulation. Finally, higher frequencies may be required if monitoring or stimulation of
some aspect of signal transmission other than action potentials is sought, such as
monitoring single ion channels. 1 There is currently no evidence that transduction
frequencies above 100 kHz have any advantage in BMis, thus the main challenge is the
connection dynamics, since even this ultra-maximum frequency is easily attainable with
current electronic manufacturing technology.
The human brain doesn't process information as a traditional computer does.
Information is moved around through pathways and at certain neurons it is allowed or
not allowed to pass based on excitory or inhibitory dendritic signals arriving before
triggering of action potentials . Local groups of neurons can act nearly coherently, for
example in volition of motor action like a hand movement. Detecting such coherent
firing at nodes around the brain is robust both noninvasively and invasively, though
1 Technologies that monitor single ion channels on a neuronal membrane are important for research on neural
function and neurotransmitter action. However, these devices are ultra -sensitive to physical motion, and have so
far not proven useful in large scale information transfer required in BMis .
UNCLASSIFIED/ /fOll OFFl@IAl W&lii OPU..¥
2

[Page 9]
UNCLASSIFIED/ /FOR OFFl&IAk le.ISi: OPtklf
noninvasive techniques currently cannot resolve firing sequences of individual neurons
within such groups.
Living neurons in an active tissue fire in the rest state. Changes in the frequency of
these firings imply that a given neuron is currently involved in the processing of
information. Bulk changes in local field potential oscillations imply that several neurons
are active. This is the signal seen in the noninvasive direct-measurement techniques of
electroencephalography (EEG) and magnetoencephalography (MEG).
Movement as simple as an eye blink involves signal communication through a million
neurons. Several locales in the nervous system thus offer the possibility of placement of
an invasive monitoring device for detecting electrical activity associated with an eye
blink or other signal of interest. Many other factors will influence the placement
decision, but considering only catching the signal as an action potential, using any
neuron along the complete pathway is equally as good, assuming detection of individual
neuronal firing can be accomplished.
Considering cortical placement of detection devices, the most common area of activity
under study is the outer covering of gray matter of the cerebral cortex, the neocortex.
The neocortex is about 2. 5 mm thick in humans and follows the ridges and fissures of
the brain (gyri and sucli, respectively, or gyrus and sulcus, if singular). The neocortex is
roughly divided into six layers and different cortical probes can concentrate on activity
in different layers, or just measure the combined activity on the surface of the cortex,
or the combined activity that is detectable noninvasively through the layers of tissue
and bone of the cranium.
Detecting single firings of individual neurons is a difficult process because the signals
are weak to start with, and not isolated from the rest of the electrical activity within the
brain. Large groups of coherent neurons, perhaps a few thousand to tens of thousands
all firing at once in relation to an external event, are the most studied of single firing
signals. 2 One of the most studied signals is the so-called P300 which occurs in many
cognitive tasks (References 2-4).
P300 is a term used to indicate a pulse signal from a large group of neurons that
appears about 300 milliseconds after a stimulus event. Peaks that occur between 200
and 400 milliseconds are commonly grouped into the P300 category. The "P" stands for
a positive measured voltage, while "N" signals are negative. 3 The P300 signal has been
shown to be influenced by top-down executive function and is therefore a prime
candidate for a trainable interface (Reference 5). Earlier signals, like PS0 and Nl00, are
of a greater interest for differential diagnosis of pathology in current research.
The preceding discussion is greatly simplified version of the electrical dynamics of
neuronal firing and does not include differences between axon and dendrite signals, or
the transmission of signals across the synapse. Complete discussion of underlying
electrical signals in the nervous system can be found in (References 6, 7).
Indirect Neuronal Signals - The BOLD Effect
2 Single firing signals here mean a single peak of combined electrical activity relative to an event. This is not
necessarily the same as single firings of each neuron. 3 The literature is not consistent with plotting P signals up, and N signals down; however, P peaks are always in the
opposite direction of N peaks.
UNCLASSIFIED/ /POil OPPl@IAL liSI!! 8HLY
3

[Page 10]
UNCLASSIFIED/ /EOR OlifilEIAk W&li (UtLY
The brain activity mentioned above is a complex chain of ionic motion within the central
nervous system. Ionic production, release, and movement within and between cells all
consume energy. This energy is supplied by the conversion of blood-borne
oxyhemoglobin to deoxyhemoglobin. The rate of oxygen consumption in a localized
volume varies based on local neural activity. The circulatory system compensates for
changes in energy demand by increasing or decreasing both the flow rate and volume
of blood, regionally and locally. Local energy demand, expressed in the capillary beds,
will alter the rate at which oxygen is metabolized, called the cerebral rate of oxygen
metabolism, abbreviated CMRO2. When brai n activity increases in a region, the
circulatory response, called the hemodynamic response, will be increases in flow and
volume, while the local areas increase CMRO2.
The hemodynamic response consistently provides an excess of oxygen over what is
required, and this results in some oxyhemoglobin traveling through the capillary bed
and local venous structure without being converted into deoxyhemoglobin. Oxy- and
deoxyhemoglobin have different magnetic susceptibilities, and different infrared
spectra. The hemodynamic response, by changing the net ratio of oxy- to
deoxyhemoglobin in the local venous structure, thus changes the local magnetic
susceptibility and local infrared resonance spectra around focused brain activity. This
complex chain reaction is called the Blood Oxygen Level Dependent, or BOLD effect
(Reference 8). The BOLD effect leads to a method to indirectly measure the local brain
activity by monitoring the hemodynamic response using Magnetic Resonance Imaging
(MRI) or Near Infrared Spectroscopy (NIRS).
The BOLD response to any event peaks about 4-6 seconds a~er the event occurs,
limiting the applications for which monitoring these signals and their associated delay
may be useful, given the BMI operating parameters defined above Furthermore, person
to person variation in distributed signals show significant differences in regions
activated (Reference 9), though there is evidence that these inter-subject variations are
stable intra-subject over time (Reference 10).
Control of External Devices
In general, there are two types of BMI design called open-loop and closed-loop. Open
loop designs, those either detecting activity or providing stimulation, are important for
BMI research and application other than the practical control of an external device.
Closed-loop systems include both output signals from the brain to effect a change in the
state of a device, and a stimulation channel, which can be used as feedback. In some
system designs, the feedback can be via visual cues such as watching a display
(Reference 11). Open-loop systems are important for BMI research and have
application in sense replacement such as artificial hearing, or when extensive output
signal processing is combined with external device state feedback (see remote robot
operation below). For learning and fine, efficient control of external devices without
significant external processing, closed-loop systems are typically needed .
Several components constitute a general BMI system for control of an external device
(Figure 2). As mentioned in the previous section, the interfaces where the information
signal makes the jump between biological and physical pathways are the most
challenging part of the system. These connections can be placed to stimulate or read
peripheral or cerebral neurons. The processing step could be as simple as amplification
UNCLASSIFIED/ /FOR OFFl@IAL Y!H! 8HL1/
4

[Page 11]
UNCLASSIFIED/ /FOR: 8Ffl@IJltt t:191!! er•t I
of a spiking train to trigger a switch, or as complex as decoding signal from noise
utilizing a 300-channel EEG cap.
~-------------------------,
: Additional sensory :
I ---1 -------------------'
~
Brain
Output
interface
,----1 Input
interface
Output
signal
processing
Components of a
Closed-loop BMI
Control System
Input
signal
processing
External
Device
Figure 2. The General Layout of a Closed-Loop Control Interface. The input and output interfaces can attach
to read or affect activity of cerebral or peripheral neurons. Additional sensory feedback channels such as visual
displays, audio tones, or haptic feedback are possible. In some system designs, especially noninvasive types, these
sensory feedback channels replace stimulation inputs. In an open-loop interface, either the input or output signal
paths are absent.
One consideration in developing a BMI control system is the utility of the application:
does it make sense to directly tie these controls to neural activity? The bulk of research
in direct neural interfaces is toward the goal of restoring mechanical capabilities to
those individuals who have either lost limbs or lost control of limbs through central
nervous system injury or disease. In these cases it is of obvious utility to produce a
system that moves a cursor across screen to select an item over the course of several
seconds; however, for a healthy individual, it is far more practical to execute a hand
movement to control a mechanical device4 to achieve the same goal.
An exception to consider is the case of applications where the subject's hands or feet
are already occupied with other essential tasks in the overall application. A research
question for any such application is whether training a subject to uti lize a BMI is
advantageous over a more complex mechanical interface. Furthermore, whether
training on a new BMI affects learning/retaining proficiency with similar BMis is an
additional concern.
Moreover, for any BMI, one can quantitatively describe the information transfer in
controlling the magnitude of human motor action (Reference 12). Since the advent of
digital control of external devices, this information is expressed in equivalent bits per
4 Mechanical device as used here represents any limb-operated interface, such as a mouse or touchscreen.
UNCLASSIFIED/ /FOR OFFI&IAk W&E 8Ptk¥
5

[Page 12]
UNCLASSIFIED/ /POil 8ffl61Al W&li 0NL¥
second transferred. Higher bit rates equate to more efficient interfaces . Baseline
examples of performance include finger pointing, which can convey 14 bits/s of
information (Reference 13), operation of a mouse about 8 bits/s (Reference 14), while
stylus tapping a soft QWERTY keyboard on a PDA has a lower rate, around 5 bits/s
(Reference 15).
Once these questions are researched and answered for a given application, the design
choice should be made whether a new mechanical interface, or an optical interface that
tracking detailed motion of the eyes, body and limbs, may be the optimum solution
rather than a BMI. 5
Another consideration in developing a BMI control system is the cognitive limit of
supervisory control of external devices. The current state of the art for human
interfaces involves volition of control, meaning that there is some executive
supervision, typically involving the pre-frontal cortex, active during the control process.
Recent studies relating to control of semiautonomous vehicles show that there are
significant limits on the number of supervisory activities that can be undertaken
simultaneously (Reference 16). In response to these limits, one can consider utilization
of nonsupervised brain networks in control of external devices, similar to those brain
systems that initiate very complex muscle coordination activity such as martial arts or
playing a musical instrument, or systems like those that are responsible for autonomic
function. Application from such research is long term, but there are current studies that
show BMI training of at least one spinal cord patient exhibited differential activity in the
cerebellum, owing to extraordinary plasticity (Reference 17). It is therefore not out of
the realm of possibility that sufficient input and output interfaces that include neural
pathways through the cerebellum could result in over-learning a BMI application to the
point that supervisory control is developed and thus significant cognitive effort is not
required.
Noninvasive Technologies
There are four noninvasive technologies currently in widespread use in monitoring brain
activity. The two direct-measure technologies involve detecting surface currents from
the relative voltage changes at or just below the scalp, electroencephalography (EEG),
and detection of near scalp magnetic fields associated with neural pathway current flow,
magnetoencephalography (MEG). The remaining two indirect measures involve
monitoring BOLD response through rapid successions of whole brain MRI (functional
MRI or fMRI), and near-infrared spectroscopy (NIRS). 6
The primary technology used for BMI is also the oldest. EEG was first described in 1929
(Reference 18) and now exists in several derivative forms. Traditional EEG uses
electrodes at the surface of the scalp to measure and amplify potential differences
between points above the cortical surface and a fixed reference such as the average
reading from the earlobes. Traditional EEG data is analyzed by breaking up the power
spectrum into several bands between 0.5 and 100 Hz. A derivative form of EEG
developed about 10 years later is called event-related potentials, or ERP. In ERP, scalp
5 There is a valid argument to be made that optical tracking and analysis, especially of the eyes, is a BMI
technology as defined in the current treatise. It is excluded as one merely by fiat. 6 NIRS is occasionally referred to as functional NIRS or fNIRS. NIRS using multiple sources to produce 3D images of
internal changes in blood flow is occasionally called diffuse optical tomography (DOT). DOT is a more general
technology that can also refer methods such as to visible-light laser excitation of tissue.
UNCLASSIFIED/ /FOil OFFl61Al WSE OHlY
6

[Page 13]
UNCLASSIFIED/ j POI\ OFFICIAL l:ISE 8Ptllf
data is averaged over several electrodes time-locked to a stimulus (Reference 19). Both
the previous methods record summed electrical activity of nominally 50,000 local
neurons, thus large coherent group spiking activity7 is required to produce appreciable
signal.
EEG
EEG-based BMI systems use pattern recognition among the several electrodes to
transmit information. In closed-loop systems, audio or visual feedback is utilized.
Training on the system and adaptation by the processing software can increase target
detection efficiency, though some recent work shows that systems can be produced
that nearly work right out of the box. Blankertz demonstrated a system that required
only 20 minutes of training on naNe subjects (Reference 20).
Development is partially being driven by the need to provide a means of communication
or action on the environment to patients that have lost control of their body. Much of
this clinically-orientated research has focused on 'locked-in' patients, who suffer from
total paralysis following brainstem stroke or degenerative diseases such as amyotrophic
lateral sclerosis (ALS) (Reference 21). The goal has been to extract control signals
either from surface EEG signals or from electrodes implanted near or within the cerebral
cortex: ECoG (see next section on invasive technologies for details on ECoG). ALS
deteriorates peripheral motor function before progression to cognitive areas. This
greatly reduces a primary source of bioelectric noise, cranial and facial muscle action,
and thus provides a reduced signal processing problem to decode neural signals.
Successful communication has been established via EEG BMI in several studies based
on both spiking activity and P300 signals (References 22-25). The response time to
execute a command using these systems is measured in seconds. The results from ALS
patients represent a best-case scenario for what could be accomplished using EEG-only
sensors in a normal, healthy human who would have significant muscle noise to sift
through.
The number of electrodes and the time-consuming application of conducting gel make
EEG arrays bulky and slow to put on. An improvement would be a reduction in the
number of electrodes, typically a few dozen for traditional EEG, and electrodes that
could operate without conducting gel. Commercial versions of dry-electrode devices are
being released on the market from companies such as Neurosky, OCZ Technology, and
Emotiv.8 The Neurosky and Emotive systems claim proprietary processing algorithms,
lack peer-reviewed literature supporting their claims, and even discuss using facial
muscle movement to send signals (References 26, 27), raising doubt about whether
neural signals are being measured at all. The NIA, for Neural Impulse Actuator, from
OCZ clearly states that the electrodes pick up a combination of EEG, EMG, and EOG, 9
and that the algorithm is only interpreting the net signal patterns instead of trying to
sort out the EEG component.
7 Spiking activity is the term used for recognition of action potentials. Spikes are fast and easy to recognize with
electronic triggering circuits, while more complex waveforms require additional processing .
8 Websites www.emotiv.com, www.ocztechnology .com, and www.neurosky .com, last accessed 12 May 2009. 9 The electrco-myogram (EMG) reads signals from muscle activity, in this case facial muscles. The electro￾oculogram (EOG) measures electrical signals arising from muscles associated with the eyes.
7
UNCLASSIFIED/fFOR OFFI&I.t.L W&E 8Pttlf

[Page 14]
UNCLASSIFIED/ /FOR OFFI@Il.tk WSI: Ortklf
Commercial EEG sensors
Mindset, by NeuroSky nia, by OCZ Technology
Figure 3. Two Commercially Available EEG Sensors. The Mindset utilizes two sensors, one in the right
earphone and one for placement on the forehead (what looks like a microphone arm is to be pressed against the
forehead). The nia records signals from three sensors on the forehead .
In a documented and peer-reviewed study, Popescu and colleagues have shown a
system that uses 6 dry electrodes and is 90 percent accurate in operation of a 1-D
cursor by untrained subjects. Additionally, a measurement of error rates as a function
of number of electrodes show that an increase to 12 electrodes could drop the error
rate to around 5 percent, but that additional electrodes much beyond a dozen do not
significantly improve the accuracy of their algorithm (Reference 28).
MEG
MEG-based BMI systems have been shown to be feasible utilizing a subject imagining
limb movements for binary decisions (References 29, 30). Future work could improve
the methodology to parallel that achieved with EEG; however, there are significant
technological hurdles to a field deployment of MEG. The magnetic fields from neural
activity are detected with very sensitive devices called superconducting quantum
interference devices, or SQUIDs. These detectors are sensitive to the neural activity
induced 100 fT (femtoTesla) changes near the scalp. SQUIDs only operate at very low
temperatures thus requiring a cryogenic system as well significant detection and
amplification electronics. The availability of a cold sink and high vacuum, such as in a
space-based application, could reduce the support system overhead, but there is still
the matter of the weakness of the signals. Even if future detector development like
atomic magnetometers would solve the equipment overhead issue for Earthbound
application, the fact that 100 fT is about 100 million times smaller than the Earth's
magnetic field will prove an insurmountable barrier to sifting signal from noise in
anything but a heavily-shielded, metal-free environment. Attempts have been made to
use High-Tc superconductors as a shielding material with some success (Reference 31),
but significant further development is needed.
UNCLASSIFIED/ /FOR OFFIEiIAk WSIE 8HL1/
8

[Page 15]
UNCLASSIFIED/ /FOA OFFIEill.tL l::181: 8HLY
EMG
Instead of measuring nerve impulses and amplifying them, one can design a system
that monitors muscle movement in a hands-free approach to a mechanical interface,
essentially using the muscles as a biological amplifier of neural signals. One may close
the feedback loop using a heads-up display, monocle, or other visual device, or another
traditional sensory feedback. The advantage of such a design is that controls may be
actuated through a lightweight wireless system, effectively providing control stations
anywhere such a wireless system would work. Such a system could be used to untie a
pilot from the cockpit. Recent work has shown that performance of 1-2 bits/s is possible
with minimal training, about four times the current performance of a comparison EEG
forehead sensor (Reference 14).
MRI AND FMRI
Magnetic Resonance Imaging (MRI) works by a simple excitation and relaxation of spin
states. When molecules containing hydrogen are placed in a strong static magnetic
field, a small but detectable number of hydrogen protons align their intrinsic spins along
the direction of the external field. An applied radiofrequency (RF) pulse near the proton
resonant frequency, 42.6 MHz/Tesla or 128 MHz at 3 Tesla, knocks the spins
perpendicular to the field and the relaxation back to ground state releases RF energy in
patterns that can be reconstructed to show both composition and distribution of any
hydrogen-rich materiel. The resonant frequency is a direct function of the local
magnetic field defined by the Larmor relation: c.o = y B; where c.o is the frequency of
precession, B is the local magnetic field, and y is a constant of the material, 42.6
MHz/Tesla for bare protons as mentioned above.
Small perturbations to the static field will change the resonant frequency. By applying a
small gradient to the static field, for example 100 milliTesla/meter along the z-axis, and
limiting the bandwidth of the RF excitation signal to 8ro, one may select a slice of the
brain perpendicular to the z-axis for excitation to 82. A change in the gradient field will
change the position of the excited slice for the next excitation. Similar gradients in the
x and y directions can limit the excitation to a single small volume of brain tissue. In
current MRis, these gradient fields are produced with electromagnets, and the series of
time-dependent imaging gradient manipulations is called the scan sequence.
Free hydrogen (H) would produce a resonant signal slightly different than the bare
proton due to the local field changes induced by its valance electron. Hydrogen gas (H2)
would produce a still different frequency since the local field around each proton is
altered by the two shared electrons. Water molecules (H2O) contain two hydrogen
atoms and an entirely different "electron shield" than either H or H2 and thus shows still
another slightly different resonant frequency. Fat and other lipid molecules, important
cell structure building blocks, have long chains of hydrocarbons, and the resulting
ensemble of electron screening produces a wide peak that is substantially shifted10
from that of water.
Brain gray matter and white matter have different macroscopic lipid content and are
thus able to be differentiated in an MRI scan. Different signals also arise in bone,
1° Frequency detection sensitivities in MRI are very good, and "su bstantial" here means about 3 parts per million.
The frequency shifts caused by imaging gradients ranges in the parts per thousand.
UNCLASSIFIED/f FOA OFFIEiIAL l::ISE 8PtLY
9

[Page 16]
UNCLASSIFIED/ /P91t 9Ffl@IAL YSIE 8HLY
cerebral-spinal fluid (CSF), and internal tissue structures of various other organs. Unlike
x-ray based technologies, MRI scans can be optimized to contrast any of the many
parts of the physics signal: total density of protons, water content, lipid content, and
even particle motion in advanced techniques involving diffusion or spin label ing. Using
such scans sequences that take several minutes, one can construct very high resolution
images of gray and white matter structure for comparison with, and also mapping onto
a "standard brain" template.
In addition to electron screening, macroscopic susceptibility will also change the local
response to RF stimulation. The presence of even a small amount of metal, say as small
as a hairpin, will greatly distort the reconstructed images. Indeed, the usual effect is a
shift of frequency completely outside the sensitivity of the machine RF receiver in what
is known as "drop-out." Smaller changes in local susceptibility, like produced in the
BOLD effect, are measureable.
A series of fast scan sequences, typically collecting an entire brain volume at a
resolution of 3 mm3 in 2 seconds, that are calibrated to optimize detection of the BOLD
signal will show the dynamics of brain function under the specific internal or applied
conditions; this is known as a functional MRI, or simply fMRI. 11 The major advantages
of fMRI are unmatched 3D spatial resolution, compared to other noninvasive imaging
methods, and complete skull penetration, making it the only imaging modality to
unambiguously detect limbic activations important for determining emotionally-laden
neuropsychological states. The main disadvantage for BMI is that the BOLD signal is
detected several seconds after the neuronal firing takes place, making fMRI
inappropriate for many naturalistic applications.
A long term prospect, likely in the 20- to 40-year timeframe, is that combined low-field
MRI and MEG technology could detect neuronal firing deep in the brain and with high
temporal accuracy. Initial experiments indicate some level of feasibi lity, but there is
substantial development work required in room temperature low field magnetic field
detection devices, such as atomic magnetometers, and signal processing algorithms to
sift through the substantial electromagnetic background (References 32, 33).
NIRS
Near-infrared spectroscopy is an additional technology to monitor the BOLD effect
noninvasively. Studies have shown it correlates well with the fMRI signal in animal
models, although with reduced coverage and lower resolution (Reference 34). This
lowered resolution greatly affects the accuracy of the technique, with recent work
involving single trials and a decision attaining only 80 percent accuracy (Reference 35).
Invasive Technologies
The most prolific invasive BMI for use in humans is the cochlear implant (Reference
36), a sensory neuroprosthesis designed to aid in hearing for deaf individuals. This
device, under continued development and refinement for more than 30 years, consists
of a microphone, sound processor, and a receiver t hat is attached to an array of
11 Specifically this is T2* Echo-Planar Imaging, also cal led BOLD EPI, Gradient Echo EPI, or BOLD fMRI. This
approach is used in well over 95 percent of published functional studies, though there are more advanced
techniques that concentrate on smaller portions of the hemodynamic signal. For example, Spin-Echo EPI will
provide a higher localization within the gray matter, but the cost is a loss of 90 percent of the signal amplitude.
UNCLASSIFIED/ /FOR OFFI&Il.tk WSE 8Hk¥
10

[Page 17]
UNCLASSIFIED/ /FOR 8FFI€iIAL YSE 8,.LV
currently 22 electrodes directly implanted into the cochlea of the inner ear. The
microphone and sound processor replaces the outer and middle ear, while the
electrodes replace the frequency selective hair fibers of the inner ear that normally
would transmit electrical signals to the cochlea. The quality of the sound is much less
than natural hearing, but the only option for patients who have lost hearing or were
born deaf. It has been estimated that 100,000 cochlear implants provide sound to users
worldwide (Reference 37). The cochlear implant is an open loop stimulation system that
provides complex signals to the nervous system through a peripheral connection.
BMI technologies have evolved from assistive technology devices solely targeted for the
healthcare industry, into apparatuses designed for intracortical microstimulation to
deliver sensory feedback. Such systems allow the simultaneous recording and
microstimulation of neuronal and behavioral events. The primary device that has
emerged leading this technological transformation is the direct cortical array containing
either surface or neocortex penetrating electrodes. The direct cortical array is implanted
on the surface of the brain near the functional area of interest, and then the connection
is reverse-engineered: individual electrodes are tested to determine if they should be
assigned as input, output, or neither. 12 These devices are designed to fuse neural
signaling pathways with external machinery into a 3D control system, such as those
apparatuses designed to modulate the movement of appendages (e.g. robotic arms),
though the signals could be used for control of any complex machine. The control
circuits on these systems are intricate and often bulky, and they can be designed with
either open- or closed-loop sensory feedback.
An additional device is the penetrating cortical electrode. These electrodes contain a
ladder of input/output probes and can be selected to transmit or receive signals in any
layer of the neocortex. Research is ongoing regarding the optimal layer with which to
place an interface. When using penetrating electrodes, tissue response is an additional
challenge as these devices frequently cause scarring. Animal studies are in progress to
quantify this effect.
Technological challenges in development of all types of invasive BMI devices include
signal decoding/stimulation algorithms, and localization of brain activation near the
implant. Functional MRI (fMRI) is utilized in conjunction with the invasive implants to
confirm additional neural network activity during interface tasks. Modifications in the
design of electrodes is necessary for experiments involving fMRI (Reference 38). 13
The majority of invasive experiments to date use animal or even tissue models, though
a few human trials have been conducted (with the exception of the cochlear implant
described above) .
OPEN-LOOP DIRECT CORTICAL ARRAY ALGORITHM MODELING
In traditional open loop experiments, eye movement systems are utilized to develop a
linear model for a physiological system. 14 In such experiments, invasive signals are
recorded from the cortex and the motion of the eye is recorded in tandem. The location
t i This procedure eliminates the need to directly locate the neuron(s) of interest during implantation.
13 Field potentials at the points of metal electrodes cause concentration of RF energy from the excitation pulses of
the MRI. This effect is used in a similar setup for tissue ablation therapy; however, such energy concentration is
undesirable in the studies at hand .
1• These techniques may be generally applied to any motor control systems.
UNCLASSIFIED/ /FOR. 8fPltlAL U.91!! f>flt I
11

[Page 18]
UNCLASSIFIED/ /P91t 9Ffl@IAL YSIE 8HLY
on the cortex to implant cortical arrays is determined from previous experiments in
fMRI (References 39, 40). In this way, a map is constructed correlating electrical neural
activity with muscle movement. The goal of this exercise is to develop an algorithm that
will predict which muscles move based on reading the neural activity alone. The reading
of the neural activity for eye movement can then be used to move a device such as a
camera lens.
There are two main models of fine motor control, one where the cortical motor areas
perform all of the control functions and receive all sensory feedback, and a second
where the cortical areas direct the function and receive interpreted feedback through
sub-cortical or even peripheral networks. For open-loop invasive BMI applications, this
is an academic question since peripheral interfaces would receive and send the same
signals in both models, and cortical interfaces would blindly adapt external decoding
algorithms based on the signals present regardless of model.
There have been numerous demonstrations of nonhuman primates controlling robots or
graphical cursors in real-time through signals collected from cortical areas that employ
open loop experimentation (References 41, 42). Kim, et al. conducted experiments
where monkeys are trained on tasks prior to implantation, and then the tasks are
repeated multiple times while muscle action and cortical activity are monitored
(Reference 42). In these trials, shoulder and elbow torque were measured while the
arm itself was constrained in an exoskeleton such that the hand would only move in a
plane axial to the monkey's torso. A visual cursor was introduced and projected on a
screen above the monkeys hand to follow the 2-D motion from the center starting point
to the various task targets, which are also projected on the screen. The shoulder and
elbow position recorded the state of flexation of 6 sets of muscle groups, collectively
called the musculoskeletal arm model (MAM). Relating the spiking activity from
implanted arrays to even this simplified 2-D MAM motion proved quite complex, and no
fit correlating the observed movements and neural activity could be obtained with a
linear model when kinematic impedance was considered. 15
Even considering the six inputs, the 2-D problem is essentially a computer cursor
control and therefore a relatively simple device, fully specified by a Cartesian coordinate
system. The ultimate goal of these control systems is to manipulate something much
more complex, like an arm, which may have many more degrees of freedom organized
in a completely different coordinate system. For these tests a more elaborate "tracking
system" may be utilized in teaching a primate to feed itself16 using a directly observed
cortically controlled robotic arm.
Open-loop control systems have an inherent drawback in cases where cortical activity
controls movement directly via an adaptive algorithm. Training the algorithm is the
critical part of interface development. The adaptive algorithms use an iterative process
to create a brain-to-cursor motion decoding scheme based on how the neurons fire
when different targets are presented and therefore rely on previous normal feedback
training - the brain knows how to move an arm because it has been moving an arm for
most of its life.
15 Impedance to motion is essential for realistic operation of artificial limbs. 16 Food in this experiment is used as a reward.
UNCLASSIFIED/ /F8R 8FFI&I.t.k Y&liii 8,.kY
12

[Page 19]
UNCLASSIFIED/ /FOR OFFI@Il.tk WSI: Ortklf
An issue develops when an entirely new device is considered. The form of the
movement control algorithm is similar to a population vector in that movement at each
time step is determined by a vector sum of the neurons' normalized firing rates
multiplied by a set of linear coefficients. Modern neuroscience has proven that tens of
thousands, even up to millions of neurons fire in concert to perform even the most
mundane of movements. These extended neural pathways developed through full￾duplex closed loop training. It will thus be quite an issue in an open-loop design to
develop an algorithm that can decode control signals for a system the brain has never
controlled before, say a 12-direction rocket stabilization system. 17 This places another
limitation on the open-loop model, even using complex nonlinear fitting, and has driven
development of the closed-loop model.
CLOSED-LOOP PERIPHERAL ARRAYS UTILIZING VISUAL FEEDBACK
In a closed-loop system that provides feedback to a control system, the differences
between the two models of movement become apparent. Sensory feedback within the
system is used for error correction of fine motor control, such as balance - without fine
motor control and error correction for balance, the human body could not stand up. In
the model with abstract cortical control, feedback corrections are processed externally
to the BMI and sensory feedback to the brain is usually limited to observation. This is a
subtle distinction between open-loop with visual feedback and closed-loop abstract
control that includes visual feedback. In the former, the visual feedback is intended to
show success of a control command being sent by the brain, whereas in the latter,
visual feedback is showing success of supervisory function of a semiautonomous
mechanical device.
eural Recording
JAPAN
Figure 4. Experimental Overview of Brain-Controlled Robot in a Closed-Loop With Visual Feedback
Experiment. After decoding walking-related Information from a monkey's brain activity while walking on a
treadmill, these data were relayed from Duke University in USA to the Advanced Telecommunication Research in
17 Twelve directions are the minimum number of positive controls commands to +/- x, y, and z thrust, as well as
increasing or decreasing roll, pitch, and yaw. These are six degrees of freedom but as far as a BMI control system
is concerned, increasing x and decreasing x are separate commands to decode.
UNCLASSIFIED/ /iiiOlil OiiiiiilCI0ls !lili OPII.¥
13

[Page 20]
UNCLASSIFIED/ /P91t 9FFl@IAL YSIE 8HLY
Japan in real time. Using visual feedback to the monkey via live streaming video, the humanoid robot in Japan was
shown to execute locomotion-like movements in a similar manner as the monkey . (Reference 43)
An example of a closed loop peripheral system is the creation of the humanoid robot
called CB-i (Computational Brain Interface) . This system is illustrated in Figure 4. In a
recent experiment, CB-i successfully mimicked the physical actions being performed by
a monkey that was positioned in a remote location (Reference 43).
MEMS, ECOG, AND PSOC CIRCUITRY
To address the issue of signal interface between the biological and physical systems,
development has focused on hybrid devices that are created by fusing together
biomolecules, cells, and other tissues, with innovative micro-size current sensors using
Micro Electro Mechanical Systems (MEMS). These systems often employ the use of
biomaterials and functional high polymer materials that enable the device to sense
information about the human body and the environment with greater speed and
sensitivity than conventional metallic sensors. These devices are built from materials
and mechanisms that are compatible with the human body, and they are proving to be
powerful tools for interfacing between the human body and machines.
The emergence of MEMS biotechnology has motivated various strategies to detect
electrical signals generated from a stimulated region within the brain into a captured
electrical response that is translated to a machine interface. One advantage of these
devices is that the fusing of biological to physical circuitry is performed external to the
body and the interface connection of the implants is thus biological to biological. This
avoids a natural reaction of the nervous system to form scar tissue around penetrating
chronic physical probes. 18 Scar tissue leads to degradation of proximal signal transfer
over time. These neural-tissue encapsulated chips offer significant advantages over
other technologies because of their ability to be rapidly integrated into the biological
environment.
Noninvasive EEG platforms often utilize a cap that covers the skull and reads the
electrical signals generated from the brain on the surface of the skin atop the head.
However, a technical limitation in the bandwidth of EEG-based methods often provides
low information rates. Currently EEG methods are limited to 20-30 bits/min ( < 0.5
bits/s). This drawback has prompted the use of a more accurate and speedy recording
method based on invasive techniques such as the electrocorticogram (ECoG), where
electrode arrays are placed on top of the cortex, but electrode penetration into brain
tissue is minimal. ECoGs have become synonymous with the pre-surgical monitoring of
epileptic seizure foci (Reference 45). Valuable insights can be gained by combining both
invasive and noninvasive schemes. For example, combining functional MRI (fMRI) and
intracortical recording has yielded important information about metabolic mechanisms
that are most highly correlated with recorded neural activity. Microelectric neurochip
developments seek to combine signal sensing and processing for bidirectional BMI
systems.
Studies in the feasibility of using adaptive input-output models for reconstructing hand
trajectories have recently been published. These studies have focused on the
18 Chronic devices are intended for long-duration implant, in contrast with acute implanted devices, which are
utilized for a short duration and then removed . Formation of scar tissue is dependent on the material used for the
electrodes.
UNCLASSIFIED/ /FOA OFFI&IAk YSIE 8HL'I
14

[Page 21]
UNCLASSIFIED/,SfOR 8FFI€il.t.k Wlili QPIIL¥
microelectric design of chronic neural implants. In 2006, Fetz et al. illustrated an
intracranial operated neural implant that could function as neural prosthetic to assist
upper limb movement for individuals that suffered from spinal cord injuries. The
intriguing part of the Fetz design is its ability to function as an autonomous battery
operated device. This is a departure from traditional BMI devices that are cumbersome
and difficult to operate. Clearly this is a step forward in the development of microwire
electrode design applications (Reference 44). Figure 5 illustrates the schematic flow
chart of the Fetz MEMS neurochip, also called a programmable system-on-chip (PSoC)
architecture.
Programmable System on Chip Architecture
(1R module) ( eITM>ry) ( MeITM>ry)
t t l
Prim ry ( Secondary ( PSoC ) PSoC J
l ! l
o
:5"' ~wE;;:,
r.n
lf n
M icrowire e lectrodes EMG ecllod s
Figure 5. Schematic of the Neurochip Functional Blocks. Parallel PSoC microcontrollers record neural and
muscle signals to independent memory modules. Primary PSoC also controls a constant-current stimulator circuit
and communicates via IR to a PC or hand-held PDA. (Reference 44)
Traditional PSoC designs operate on a high power consumption and short battery life of
radiotelemetry systems (Reference 46). In the Fetz study, researchers implanted
electronic devices that collected data in unrestrained monkeys. The system operated
without the power limiting and cumbersome restraints exhibited by these previous
systems . For this design, an onboard spike processing and a stimulator circuit were
employed to allow for real-time bidirectional interface with the nervous system. After
several modifications, Fetz et al. successfully created a device that was able to
simultaneously record electromyogram (EMG) activity and neural activity at the
implant. The lithium battery operated power source and electronic data systems were
skillfully packaged within a compact percutaneous (inner skin) titanium casing that was
attached to a monkey's skull; the entire implant weighed only 56 g. Neural data was
acquired from 12 microwire electrodes chronically implanted in the primary motor
cortex. Leads run subcutaneously from the head casing to a connector on the monkey's
back. Two pairs of stainless-steel wires were inserted percutaneously into the forearm
muscles where they were attached to an EMG signal recorder (Reference 44).
UNCLASSIFIED/lf81l OfPltlJlcL U:!I! f>flt I
15

[Page 22]
UNCLASSIFIED/ /FOR: orr1e1J1tt Y!H: e ..tv
CHRONIC NEURAL IMPLANTS AND FMRI
While developing microelectric neural chips for functional studies appears revolutionary
on the surface, it only presents a piece to the greater puzzle of understanding the
feasibility between neuroprosthetic chips and BMI development. For a BMI system to
succeed, researchers must understand the brain, its regions of activity and how those
area correlate to real time stimulation and neural responses, and how the brain may
evolve with training on use of the BMI. This will require the employment of sensitive
neural mapping devices such as fMRI.
~ II {
I
! Ill
t,
i:
0
..J
04-1.eft
Figure 6. Implant Location. Cartoon shows location and orientation of the different electrode sites in the various
layers of an animal's neocortical implant (layer thicknesses are approximately scaled). The gray band is the 200µm
separation region between the upper and lower layers of the neocortex.
To address this question, studies performed by Parikh et al., have targeted tissue￾specific layers within the motor cortex region, essentially a modified ECoG, where
penetrating microelectrodes exhibit the greatest functionality in cortical prosthetic
design (Reference 47). The interesting parameter of this experimental design is its
ability to successfully employ a behavioral task paradigm where electrodes could
accurately record brain activity and animal response based on audible and visual cues.
With this information the researchers discovered that the lower layers of the cortex are
more likely to encode directional information as compared to units in the upper layers.
This understanding has prompted the use of prosthetic neural implants as critical
instruments for developing accurate BMI models and the mapping all neurological
(brain triggered) responses.
For these experiments, accurate measurement of responses was placed solely into the
unique design of chronic implantable neural prosthetic devices. These devices enabled
investigation of activity in the upper or lower brain tissue layers, including whether
either had a preference for ipsilateral (same body side) versus contralateral (opposite
side of body) movement. In addition, chronic neural implants provided an innovative
method to target isolated brain regions. During this experiment a craniotomy was
performed over the target cortical area. In this procedure, a 2 mm diameter hole is
made into the skull to expose the dura mater. This dura matter is then removed to
reveal the cortical surface. An electrode scaffold array is inserted by hand with the use
of fine PTFE-coated forceps into the target cortical area. Typically, the electrode will be
UNCLASSIFIED/ /F8R 8FFl@IJltL Y!H! 8,.L'I
16

[Page 23]
UNCLASSIFIED/,'FOR: 8Ffl@IJltt t:191!! er•t I
loca lized in a manner where the top site will be below t he cortical surface. The electrode
assembly was then wrapped with Gel Foam (Pfizer, I nc. , New York) and then cemented
with dental acrylic (Reference 47). Once the experiment was concluded, precise location
of the cortical arrays was obtained by passing currents t hough the electrodes to cause
micro-lesioning, then post-mortem examination of brain slices could locate the lesions
and reconstruct the precise 3-D position of the electrodes (Figure 7). This test provided
an initial understa nding of brain activity and the ability to utilize microelectrodes to
loca lize specific neu ral regions.
Sample slices from all implants
IOOOl)m
Multipl sllces from 04 Left
Figure 7. Histology and Electrode Tracks. The left panel shows Nissl-stained coronal sections of sample slices
from all animals D1-D4 showing electrode tracks or lesion marks for all seven implantations. The black line marks
the boundary between the upper and lower layers. The right panel shows seven coronal sections arranged rostro￾caudally, as indicated by the schematic, for one implant (D4Leh) showing alternating lesions and electrode tracks
which were used to reconstruct site locations. (Reference 47)
UNCLASSIFIED//EAR AfifilCl.\k Wlilii o ..tv
17

[Page 24]
UNCLASSIFIED/ /P91t 9ffl@IAL YSE &P•tlf
NEW ELECTRODE DESIGNS
Building upon studies like Parikh et al., designs look toward invasive systems capable of
pinpointing cortical regions and monitoring their neural activity at or near single neuron
resolution. Clement et al. employed microwire neural implants to combine fMRI and
intracortical recordings to yield important information about metabolic mechanisms that
correlate with neural activity. While modeling studies have been conducted in numerous
experiments, they served as a baseline to understand the potential dangers associated
with the strong static magnetic field alone or while exposed to typical MRI protocols on
the surrounding tissue and the design of an MRI compatible electrical array (References
48, 49). On the surface this may seem a trivial task, however the study shows this is
not only a challenging design detail, but decisive in the resulting recorded data of
neural activity. Examples of the electrode designs are shown in Figure 8.
Figure 8. The Michigan Electrodes. Left: A variety of different silicon probes have been placed on the back of a
U.S. penny . The copper scaffold in the background is the array of columns on the Lincoln Memorial. Right: Four 64-
site probes have been assembled into a three-dimensional structure. (Reference 49)
Previous work addressed important issues related to short-term compatibility of silicon
microelectrodes. In that report, identification and replacement of appropriate
components of a silicon microelectrode system resulted in virtually artifact-free MR
images and stable recordings of motor unit activity, although chronic studies were not
performed (Reference 50). By utilizing this knowledge the authors designed a microwire
electrode array capable of surviving the strong magnetic fluctuations exhibited from an
fMRI. Figure 9 shows the device and its related connective components (Reference 51).
Figure 10 shows the before and after MR images when connectors and structural screws
compatible with MR are employed as well as the compatible electrodes.
UNCLASSIFIED/ /f91t 9ffl@IAL Y§E 8Htlf
18

[Page 25]
UNCLASSIFIED/ /FOR OFFI@Il.tk WSI: Ortklf
Figure 9. Image Distortion and Custom Microwire Electrode Assembly to Improve It. (A) Image distortion
induced by metallic bone screws and connectors. No feature can be identified. Spin echo sequence: TR=ls,
TE=6.75ms, NT=4, Matrix=128x128. FOV=60x60mm2 . Experiment time=512 s. (B) (Top) Microelectrode array
used in the study. (Bottom) Close-up of the connector piece that was constructed for multiple
connection/disconnection cycles. Interface piece to connect the nano-miniature Omnetics connector of the head
stage with the head-cap-embedded custom connector for extracellular multiunit activity monitoring. (C)
Improvement in image quality after replacement of bone screws and connectors with compatible equivalents.
TR=3500ms, TE=20ms, averages=2, acquisition matrix=128x96, FOV=21x21mm2, slice thickness=0.4mm, total
acquisition time (TA)=672sec, resolutlon=164µmx220µm. (Reference 51)
With this system, the authors successfully recorded spontaneous extracellular multiunit
neural activity in 16 electrodes (four in each animal) for 6 weeks post-implant. Of those
16 electrodes, 12 registered data verifying distinct neural activity prior to MR exposure.
To determine the overall effectiveness and feasibility of th is procedure, a tissues
damage assessment associated with the MRI was conducted by utilizing T2 maps from
tissue dissections (Figure 10). Thorough examination of the electrode location and
resultant tissue survivability revealed little damage from the operation of t he BMI. The
locations of t he microwires are visible as dark lines in the image (indicated by ovals).
$
009
0011
007
006
005
0 04
003
002
0,01
0
Figure 10. Example of T2 Variability, (A) T2 maps from MRI rat 16 at day 7 post-implant show elevated values
proximal to the Implant location (circled). (B) T2 maps from MRI rat 18 at day 30 post-implant shows no difference
between the implant and control hemispheres. TR=3500ms, TE=l0, 20, 30, 40, 50, 60ms, averages=2, acquisition
matrix=128x96, FOV=21x21mm2, slice thickness= 0.4mm, TA=75mins, resolution=164µmx220µm. The ovals
indicate the site of electrodes . (Reference 51)
UNCLASSIFIED/ /fiOlil OfifilCIOP l!SE AN! X
19

[Page 26]
UNCLASSIFIED/ / POI\ OPPlelAL l:l§li &Pn,¥
The results of statistical analysis are
shown in Figure 11 comparing the T2
values obtained in the implanted
hemisphere versus those in the
contralateral (unimplanted) hemisphere.
There was no significant difference in T2
values between the two hemispheres.
These results prove the feasibility of
fMRI neural tracking and the use of
microelectrode arrays. With these
findings the use of microelectrical
implants and fMRI will become a vital
instrument in understanding neural
activity in invasive BMI. With the
growing use of chronic microelectric
implants for neurophysiological mapping
studies, future studies will be able to
explore a new realm of possibilities in
BM! applications.
Figure 11. T2 Value Analysis Summary of T2 Values
in All the Image Slices That Spanned the Electrode
Arrays in All Animals. There was no significant
difference between the implanted and contralateral control
hemispheres in the susceptibility-free regions proximal to
electrodes. p-values (one-sided student t-test assuming
equal variance): day0 : 0.2, day7: 0.7, day14: 0.4, day28 :
0.8, day42: 0.4. Combining all imaging sessions for all
animals: p=0.
60
.-. 50 "' §_ 40
:l 30
~ .. 20
I- 10
0 0 7 1 28 42
nmePosl-lmplant( Days)
HYBRID NEURO-ROBOTIC SYSTEMS FOR TRUE CLOSED-LOOP BMI
While many innovations have been seen in BMI technologies that detect neural
stimulation from direct cortical regions of monkeys and rats, another approach has
been pursued through the use of lamprey eels. Chordates, like the lamprey are ideally
suited for neurological studies because of their distinct and readily accessible hollow
dorsal nerve cord or brain stem. In the realm of neuroscience the brain stem is often
regarded as the most primitive region of the human brain. In one study, Mussa-Ivaldi
et al. (References 28, 29) investigated the possibility of using the feedback from a BMI
for inducing controlled plastic changes at specific synapses. Figure 12 shows the
bidirectional connections between a mobile robotic device and a lamprey brain stem
that has been used to investigate the repertoire of operations carried out by neurons in
the reticular formation. Signals generated by the two optical sensors of the robot were
translated into electrical stimuli and applied to the vestibular pathways, and to two
populations of reticular neurons. The resulting discharge frequency of the reticular
neurons commanded the right and left wheels of the robot. In this simple arrangement,
the reticular neurons acted as a processing element that determined the closed-loop
response of the neuro-robotic system to a source of light. These studies revealed that:
• Different behaviors can be generated with different electrode locations.
• The input-output relationship of the reticular synapses is well approximated by
simple linear models with a recurrent dynamic component.
• The prolonged suppression of one input channel leads to altered responsiveness
long after it has been restored in the variable frequency pulse generator.
The results of this lamprey study hints that cerebellar connections in mammals could
provide excellent plastic interface points for full closed loop technologies .
UNCLASSIFIED/,'FOR OFFl@IAL l:l!H! 8HL1/
20

[Page 27]
I
I
,
UNCLASSIFIED/ /P91t 9FFl@IAL YSIE 8HLY
Lamp1 y
bramstem
V Amplifiers ldoog
A
c=:;)> Recording
,'I •
. ,
I
,
I
,
I
Spike de ecttt>n
rreq --rt11and low-pass pulse fill r
ge ' omoor
.,_crualC!fs
Additional studies utilizing neurological signals generated from the lamprey have been
equally promising in eliciting cognitive responses that translate a controlled response
into a machine's activity. In a similar experiment, Deliagina, and coworkers (Reference
30) used the activity of reticulospinal neurons recorded from a swimming lamprey to
Figure 12. A Hybrid Neuro-Robotic System. Signals
from the optical sensors of a Khepera (K-team) mobile
robot (bottom) are encoded by the interface into
electrical stimulations, the frequency of which depends
linearly on the light intensity. These stimuli are delivered
by tungsten microelectrodes to the right and left
vestibular pathways of a lamprey brainstem (top) that is
immersed in artificial cerebrospinal fluid within a
recording chamber. The electrical stimuli are delivered to
the axons of the intermediate and posterior octavomotor
nuclei (nOMI and nOMP, respectively). Glass
microelectrodes record extracellular responses to the
stimuli from the posterior rhombencephalic neurons
(PRRN). Recorded signals from right and left PRRN are
decoded by the interface. First, the electric artifacts
generated by the stimulation impulses are removed.
Then, population spikes are detected. The resulting spike
train is passed through a low-pass filter, which calculates
an average firing rate over a 300-millisecond firing
window. The average firing rate detected from each
electrode is translated into a command to the
corresponding wheel of the robot. The angular velocity of
the wheel is set to be proportional to this average rate.
Figure 13. Experimental Arrangements. (A) :
arrangement for simultaneous recordings of neuronal
activity, electromyograms (EMGs), and movements in the
freely behaving animal. Electrophysiological recordings
and the video recordings were synchronized by pulses (1
Hz) recorded simultaneously by both systems (Synchro).
(B) : arrangement for recording vestibular responses fn
RS neurons du ring swimming . Central, denervated region
of the body was fixed in the experimental device.
Lamprey could perform locomotor-like undulatory
movements by its anterior and posterior body parts
(indicated by arrows). Device could be rotated manually
(a, roll ti lt angle).
UNCLASSIFIED/ /F8R. 8FFI&iIAk Uili QNL¥
Variable
ncy
rator
___________
21

[Page 28]
UNCLASSIFIED/ /POR: err1e1At l:191!! er•t I
rotate the platform supporting the fish. The lamprey was able to stabilize the hybrid
system, and this compensatory effect was most efficient in combination with undulating
swimming motions. The experimental setup is seen in Figure 13. These studies
demonstrate the feasibility of closed-loop interactions between a specific region of the
nervous system and an artificial device. Closed-loop brain-machine interfaces offer an
unparalleled opportunity to investigate how plastic changes can be guided by
modulating the input signals of the neurons based on the behaviors generated by the
output of the same neurons. Furthermore, in such hybrid systems it is possible to
replace the neural tissue with a computational model, thus providing a direct means for
testing the predictions of specific hypotheses about neural information processing.
Adaptation to the variable dynamics of the limbs and of the limb environment has
generated an increasing volume of research that is relevant to brain-machine
interfaces.
TRIALS USING HUMAN SUBJECTS
Testing BMis on normal human subjects presents ethical dilemma since any volunteer
outside of the research team itself would likely have difficulty understanding all of the
risks involved in neural implantation. Even well-known volunteers such as Jans
Naumann now admit they truly did not understand the risks involved and are
considering having chronic implants removed. 19 Not all human trials have produced
such poor results.
Significant ECoG arrays are implanted in epileptic patients prior to surgery to provide
high resolution spatial localization of seizure activity (Reference 45). In these clinical
tests, the arrays are implanted in the patient and then monitored until seizures takes
place. This procedure can take more than a week and the patient has little to do
between random onsets of seizure activity. Epilepsy is generally considered a localized
pathology, almost always lateralized to the right or left lobe. The remaining brain
networks, especially from the nonseizure half of the brain, are generally normal. This
provides an opportunity for cohort cognitive studies since they represent minimal
additional risk for volunteers undergoing the procedure as a medical necessity. Blakely
et al. utilized such a patient to decode brain network patterns associated with different
English phonemes (Reference 52). Mapping all of the phonemes could constitute an
open-loop technology to communicate without speaking using normal language instead
of learned motor patterns. Schalk and colleagues utilized a sample of five pre-surgical
epileptics to demonstrate ECoG to control one- and two-dimensional cursor movement.
Movement times to target were on the order of 1-2 seconds with up to 75 percent
accuracy with training time on the order of 30 minutes or less (Reference 53).
Spinal cord injury (SCI) is another clinical condition where the normal brain is intact
and ECoG arrays may be implanted for testing a neuroprosthetic. Researchers in
Toronto recently reported good hand movement and grasping control using ECoG
arrays (Reference 54). Similarly, Hochberg showed good results in 2-D cursor control,
but still seconds or more slower than a mouse control, even after 90 days of training. A
following task was more successful, though the accuracy for use in fine manipulations
needs improvement (Reference 55).
19 Jans Naumann was the first recipient of a second-generation artificial vision system (AVS) designed by the
Dobelle Institute. The AVS project was based in New York, but the procedures themselves were conducted in
Lisbon, Portugal, to avoid U.S. prohibitions against implant surgery.
UNCLASSIFIED/ /POR: err1e1At 0!11!! OHLI
22

[Page 29]
UNCLASSIFIED//POlt OPPIEIAL U.!I! 01\LI
EMG interfaces for limb amputees have advanced dramatically in the last several years,
with several devices controlled by remain ing muscles that have been implanted with
otherwise unused nerves in an invasive process called reinnervation (References 56,
57). Twelve electrode pairs were utilized in the recording of intended arm motion . The
classifier algorithm used to determine hand control was able to provide a new prediction
10 times a second, and for controls, a motion selection from 1 of 10 possibilities could
be achieved in less than 170 milliseconds. Interesting with this procedure is that a
direct biological amplification of the neuronal signal is achieved by connecting it to a
muscle. The amplified signal is then read by a noninvasive EMG probe. Although not yet
approaching normal, the speed and dexterity of these artificial limbs is impressive.
Finally, one trial utilizing a normal, healthy human self-experimenter in 2002 showed
that sensation and control is possible through a peripheral array implant in the median
nerve of the left arm. This trial lasted 3 months before the physical connection between
the nerve and the microarray deteriorated beyond use. Subsequent examination and
testing has revealed no long-term damage at the implant site (Reference 58).
OPTICAL STIMULATION OF ACTION POTENTIALS
A final invasive technology that utilizes light to gate action potentials shows promise
(Reference 59). In this technology, the biological switch is controlled by a locally
inserted LED and possibly guided using optical fibers, but there is no contact between
the physical circuits and neurons, thus avoiding the issue of scar tissue caused by
operation of invasive probes. Application to artificial vision have already interesting pre￾clinical results in rat brain tissue (Reference 60).
Discussion
Any successful BMI hardware technology relies on at least one, and in most cases all, of
the following three essential elements: brain plasticity through user training, neural
decoding by a machine learning algorithm, and neuroscience knowledge. Advances in
the latter two will help all BMI research paths, but the former element is the most
research path dependent since different technologies have different training limitations
such as the inherent visual feedback delay of a noninvasive BOLD monitor.
One approach to the training issue is to greatly simplify the control information
bandwidth required. Research here has placed a focus on scenario-based controlling
that is not from millisecond-to-millisecond updating of some 3-D trajectory like a full￾duplex BMI specified in the introduction would perform, but rather is controlled by high
level commands from the user in a low-bandwidth supervisory mode. It is conceivably
useful to tell a wheelchair to "Go Left," "Stop," or "Veer Right," and let sensors and
actuators on the wheelchair work out the trajectory details, as opposed to constantly
setting and resetting the trajectory of the wheelchair. In this manner, much of the
feedback error-correction is done in the physical circuit. This approach can be viewed as
a series of simple asynchronous decisions, and relies on the artificial intelligence of the
execution algorithms rather than tapping the general adaptability of mammalian brain
architecture. Mention is made of this research path because it is important to the
advancement of the field as a whole, though the concentration in this treatise is on
tapping the plasticity of neural systems rather than creating a program to imitate them .
UNCLASSIFIED/ ,'FOR OFFI@IAl WSE OHlY
23

[Page 30]
UNCLASSIFIED/ /FOR: orr1e1J1tt Y!H: e ..tv
The remainder of discussion concentrates on the surveyed studies into five technology
areas, and listing their advantages and disadvantages, as well as their critical barriers
to further development and likely future paths of research.
NONINVASIVE ELECTRICAL DEVICES
The current state-of-the-art BMI devices that have shown the most promise in the near
term utilize muscle amplification of the neural signal. This is the result of commercial
investment in development. These primarily EMG based systems are noninvasive
connections to existing or constructed nerve-muscle pairs. Neurally operated
prosthetics have been demonstrated such as the artificial hand. Decoding algorithms
are nearly as fast as muscle response itself at selecting 1 of 10 actions. Commercial
products for entertainment are available for normal, healthy consumers. These
entertainment devices contain few sensors but make use of more complex decoding
algorithms. All sensors don't just turn on and off, rather they can relay amplitude,
polarity, and frequency of muscle action, as well as detect underlying spiking signals
from neurons. This combination, along with algorithms developed from a support vector
machine, will allow device selection of many more actions than the simple binary
combinatorics of the number of sensors. The gaming market will drive this noninvasive
technology in the next 5 years with advances in signal processing from current sensors.
The EMG based systems can be scaled to a large number of sensors for a more complex
control task. It has been demonstrated with amputees the feasibility to move existing
nerves around to control existing muscles. There has not been a study yet to explore
how many nerve-muscle pairs may be available for such use in a normal human, with
or without reinnervation. Such a study could be done theoretically based on current and
near term work with patients. The longer term for EMG will likely evolve toward very
small, wireless chronic implants that operate near the skin surface and are easy to
install and remove.
Devices based solely on noninvasive detection of EEG signals from the cortex in normal,
healthy individuals are unlikely in the next 5 years. This is primarily because of muscle
noise filtering issues which will need to be solved through development of better EMG
sensors and detection algorithms mentioned above. Even though such devices have
been shown to work in laboratory settings, moving them to the arbitrary conditions in
naturalistic settings introduces significant complication to signal detection and filtering
that greatly limits the information transfer bandwidth to a fraction of the target 5
bits/sec. Also an issue is the origin of surface EEG signals, which are still under
theoretical study even after 80 years. Some of the frequency bands directly related to
spiking activity in axons are somewhat understood, but the whole of the signals contain
many transients that are likely the more interesting and possibly more robust parts of
brain activity. In the medium to long term, many applications are envisioned in surface
or near surface detection of cortical spiking activity or ERP, once the background
separation issue in naturalistic environments is addressed . However, these signals still
require localized coherent firing of tens of thousands of neurons, a biological
requirement that has limited the information transfer rates of these techniques to 1
bit/sec or less, which is well below target rates but could be useful for some
applications.
One can suppose an ultra-high density EEG, thousands of sensors with wireless micro
probes embedded subcutaneously that track electrical activity and relative location
UNCLASSIFIED/ /FOR. 8FFI@IJltL Y9I!! 9Htl"
24

[Page 31]
UNCLASSIFIED/ /POlt err1e1J1tt U.!I! er\tt I
based on skin movement using technology similar to the operation of GPS. This system
would have the same inherent problem of signal conduction through tissue from all
directions. The key indicator of a future advance in EEG technology would be a study
showing noninvasive spiking or ERP signal detection from a coherent group of less than
10,000 neurons. Until progress in localization on this order is demonstrated, EEG-only
devices will remain low bit rate application technologies.
EEG-only sensor control of devices has been pursued with the supposition that signal
transmission directly from the motor cortex will outperform conventional mechanical
operation because the signal transmission delay between the neocortex and muscles in
the extremities will be augmented via a physical circuit. While this is true, the inherent
assumption that complex mechanical interface operation can be replaced with a 1
bit/second low-delay control pathway is incorrect for naturalistic environments. The
millions of channels of two-way communication between the extremities and the brain
naturally present will control naturalistic mechanical devices far better, and provides
the ability to react to an ever-changing environment. Adding significant computer
control and relegating the motor cortex to a supervisory role of low data bandwidth
could have benefits and is a possible path to real-world improved reaction time
application. Also beneficial to reaction time is the combined EMG EEG devices
mentioned above since the pathways between the brain and facial muscles are far
shorter than those to the extremities.
NONINVASIVE BOLD- BASED DEVICES
The detection resolution of hemodynamic responses using fMRI and NIRS type
technologies is expected to improve in the near, medium, and far terms. NIRS has been
deployed in naturalistic experiments, specifically, automobile driving, and it is
reasonable to envision such systems becoming small enough to wear in the medium to
far term. The limiting issue with BOLD technologies is that the detectable response is
delayed several seconds from neuronal firing, greatly limiting the cognitive control
applications available to these technologies. Progress in localization to below 0.5 mm3
in a mobile device could indicate the possibility of high bit transfer rates with the use of
state vector machines, albeit with the inherent delay of the physiology. Until the
localization and portability issues are addressed in tandem, BOLD-only devices are
unlikely to be used for commercial cognitive control interfaces.
The vast majority of experiments in fMRI utilize the General Linear Model (GLM) and
something akin to a canonical hemodynamic response. There exists significant
physiological noise in these data analyses that are traditionally filtered out. The
differential results from Independent Component Analysis (ICA) and GLM analysis of the
same data sets indicate that there may be additional circulatory response mechanisms
with faster onsets than typical BOLD. Future studies indicating that filtering or analysis
methods may be ignoring important detectable signals that have inherently faster
response times would provide a breakthrough path for hemodynamic response
technologies. The current research to monitor on this matter is the technology known
as Inverse MRI which can capture high temporal resolution (100 frames a second for
single slices) T2* variations.
UNCLASSIFIED/ /POil Offl@IAL YSIE 8Htlf
25

[Page 32]
UNCLASSIFIED/fFOlil OFFI&I.t.k WIiii 8Plklf
NONINVASIVE MAGNETIC DEVICES
Detection of magnetic fields arising from neural activity using MEG or a future
technology have the same inherent limitations as EEG-only noninvasive sensors.
Resolving these signals from background in any naturalistic environment will not occur
without the development of a disruptive technology in shielding that is portable and
lightweight enough to be worn comfortably on the head, and will attenuate background
amplitude nearly 10 orders of magnitude across the entire range of neural signal
frequencies, and the entire range of frequencies where the detection electronics may be
sensitive. Body-temperature superconducting materials may accomplish the shielding if
engineering development continues, and these could be combined with atomic
magnetometer technology to produce a portable system, though the inherent
limitations of the method will still be present.
INVASIVE TECHNOLOGIES - GENERAL, OPTICAL, AND EX-VIVO
ENGINEERING
All invasive technologies will have to undergo substantial rigorous testing to determine
the long-term side-effects of implantation and operation, as well as drift in the
operational performance with extended use. Several pre-clinical devices detailed above
and discussed below show promise, but the handful of human trials show that direct
interface technologies based on proximal action potential stimulation and detection are
still a long way off from practical application since the trials themselves in duplex
operation show functional failure after only a matter of weeks. The mammalian auditory
system is well studied, and the cochlear implant has been in use and continued
development for more than 30 years, and there is yet to be any practical application for
implanting a cochlear device into a normal healthy individual. Proximal electrode
interfaces do not appear to be the answer for high bandwidth BMI, and further
development in the machine-biology contact is required. If the 30-year advancement of
cochlear is a realistic guide of innovation, the proximal electrical technology path to
success is 30-40 years off save for a disruptive advance in the development of
penetrating electrodes.
Two invasive research paths that are promising are optical stimulation and gating, and
ex-vivo growth of neural cells on physical circuits.
The advantage of optical stimulation and gating is that one could theoretically design an
optical link to act as a connected input dendrite on a single neuron. Theoretically, one
should also be able to use spectroscopic sampling to determine if an action potential is
progressing down an axon, thus providing a single neuron output (read or monitor)
capability as well. This invasive but noncontact full-duplex information channel would
effectively hook-up the physical computer seamlessly to the network structure of the
brain. Proof of principle studies in this technology could emerge at any time, and given
the demonstrated plasticity of neural networks in both closed-loop visual feedback and
lamprey experiments, could provide a disruptive path for advancement of BMI.
The ex-vivo growth of neural tissue on electrode arrays provides a controlled platform
for:
• Testing long-term effects of electrode use on proximal neural tissue.
UNCLASSIFIED/ /FOlil OFFI€llAL 1:181! 8Htl"
26

[Page 33]
UNCLASSIFIED/ /POI': OPFIClltt U.!I! Oflt I
• Developing complex neural networks on top of chips prior to implant.
• Development of chronic electrode materials such as biopolymers that may be
suitable for implant without an ex-vivo grown sheath.
• Creating a biological to biological interface upon implant.
This technology does still rely on proximal sensing and stimulation of action potentials,
but the neural tissue at the biological to physical interface is engineered rather than
native, thus providing the opportunity to develop an effective bridging network to
seamlessly integrate between the two systems. Development of such chronic implant
capability could make feasible the nondestructive addition of cerebellar pathways for
control activity that incorporates the huge potential of brain plasticity without adding
significant cognitive burden on the prefrontal cortex. This would effectively turn the
controlled device into part of the body as far as the brain is concerned.
IMPLANTABLE CHIPS, LADDERS AND ARRAYS
Research utilizing ECoG or neocortical ladder array technology is the state of the art in
neural communication. However, stimulating nerves or peripheral pathways in this
matter without damage to the receiving cells has proven difficult. Even in cochlear
arrays, normal functioning of the surrounding tissue is lost and only a fraction of the
quality of natural stimulation is available. Locating single neurons has also been
challenging, though new electrode designs are being developed. These devices will
continue to be useful for research applications such as better understanding of network
structure and network function in conjunction with fMRI. BMI application will continue in
the foreseeable future to be lim ited to instances where closed-loop with visual or other
traditional sensory feedback is sufficient. Until new electrode designs develop a robust
method of two-way communication with single neurons, they will not be the dominant
BMI technology for use in normal, healthy individuals.
Conclusions
The gamut of modern technologies that connect neural systems to physical systems has
been surveyed, with attention to the underlying physiological signals. Many examples
have been presented of studies illustrating the different research paths under way. Two
of these technologies show the most promise of near term and long term successful
high-bandwidth integration of brain and external systems.
In the near term, noninvasive electrical sensors that primarily rely on EMG signals, but
also include those weaker signals directly from neuronal firing, are expected to
dominate real-world applications. The decoding of these signals from just a handful of
dry sensors can produce a large combination of on-off and variable strength control
commands that should surpass the information capability of traditional electro￾mechanical interfaces in the next 5 years. This technology is limited, however, by the
number of available EMG sites and the required coherent firing of very large numbers of
neurons. To surpass these limitations, technologies capable of connections to individual
neurons on a large scale will be necessary.
In the far term, an invasive approach to establish high-bandwidth duplex
communication networks, 5-20 bits/second, using interfaces with single neurons
UNCLASSIFIED/ /P91l err1e1Jct U.!I! or•t I
27

[Page 34]
UNCLASSIFIED/,'FOR OFFl&IAk le.ISi: OPtklf
directly in the cortex or cerebellum can take the fullest advantage of neural training and
processing capability. Two research paths currently showing the most promise are
optical interfaces and ex-vivo preparation of electrode arrays encased in engineered
neural tissue. New electrode designs that could establish two-way communication with
single neurons are also promising. The cerebellar connection point is extremely
interesting to perhaps provide a connection that would effectively make the external
device a part of the body as far as the brain is concerned.
The current state of the art using metal electrode arrays for proximal stimulation and
sensing does not appear to be advancing toward long duration viability as a commercial
BMI without some unforeseen advance in two-way communication. Peripheral
connections have some theoretical promise, but an example of such an implant in a
human trial did not shown terrific success over several weeks it functioned.
Implantation of cortical arrays in human trials has not been conducted on a wide scale
for durations longer than a few weeks, and two-way electrical communication has yet to
be realistically demonstrated, limiting the possible commercial application portfolio for
this technology.
Many possible research directions for disruptive advances have been presented. These
areas and the physiological-physical interconnection field of study as a whole should be
monitored regularly for advances, as well as the ancillary technology areas of brain
plasticity, neural signal decoding, and general basic neuroscience. Advances in any and
all of these areas could alter the future landscape of commercial applications and
dramatically alter our understanding of what is possible through thought-directed
control.
1 Alberts B. Molecular biology of the cell. 4th ed. New York : Garland Science; 2002. 2 Polich J. Updating P300 : an integrative theory of P3a and P3b. Clin Neurophysiol 2007 Oct;118(10) :2128-48.
3 Ravden D, Polich J. On P300 measurement stability: habituation, intra-trial block variation, and ultradian
rhythms . Biol Psychol 1999 Oct;51(1):59-76 .
4 Sutton S, Braren M, Zubin J, John ER. Evoked-potential correlates of stimulus uncertainty. Science 1965 Nov
26; 150(700): 1187-8.
5 Sawaki R, Katayama J. Top-down directed attention to stimulus features and attentional allocation to bottom -up
deviations. J Vis 2008;8(15):4 1-8.
6 Huettel SA, Song AW, McCarthy G. Functional magnetic resonance imag ing. Sunderland, Mass. : Sinauer
Associates, Publishers; 2004. 7 Kandel ER, Schwartz JH, Jessell TM. Principles of neural science. 4th ed. New York: McGraw-Hill, Health
Professions Division; 2000. 8 Ogawa 5, Tank DW, Menon R, Ellermann JM, Kim SG , Merkle H, et al. Intrinsic signal changes accompanying
sensory stimulation : functional brain mapping with magnetic resonance imaging. Proc Natl Acad Sci US A 1992 Jul
1;89(13):5951 -5.
9 Emerging Cognitive Neuroscience and Related Technologies. Washington DC: National Research Council of the
National Academies; 2008. 10 Miller MB, Van Horn JD, Wolford GL, Handy TC, Valsangkar-Smyth M, Inati S, et al. Extensive individual
differences in brain activations associated with episodic retrieval are reliable over time. J Cogn Neurosci 2002 Nov
15; 14(8): 1200-14.
11 Hatsopoulos NG, Donoghue JP. The Science of Neural Interface Systems. Annu Rev Neurosci 2009 Mar 24. 12 Fitts PM. The information capacity of the human motor system in controlling the amplitude of movement. J Exp
Psychol 1954 Jun;47(6):381 -91.
' 3 Drury CG, Hoffmann ER. A model for movement time on data-entry keyboards. Ergonomics 1992;35(2):129 -
47 . 14 Choi C, Micera S, Carpaneto J, Kim J. Development and quantitative performance evaluation of a noninvasive
EMG computer interface. IEEE Trans Biomed Eng 2009 Jan;56(1):188-91. 15 Soukoreff RW, MacKenzie IS. Theoretical upper and lower bounds on typing speed using a stylus and soft
keyboard. Behaviour & Information Technology 1995;14(6):370-9.
UNCLASSIFIED/ /FOR OFFI@IAL 1:191!!! 9Htl"
28

[Page 35: illegible]

[Page 36: illegible]
