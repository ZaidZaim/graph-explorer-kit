# Historical Document: DOW-UAP-D127_AAWSAP-DIRD-An-Introduction-to-the-Statistical-Drake-Equation-March-11-2010

## Source Metadata

- Original file: `DOW-UAP-D127_AAWSAP-DIRD-An-Introduction-to-the-Statistical-Drake-Equation-March-11-2010.pdf`
- Pages: 55 (50 from text layer, 4 OCR, 1 illegible)
- OCR language: `eng`
- Processed at: `2026-09-23T18:09:31.415989+00:00`
- Processing pipeline: `pypdfium2 text layer + Tesseract OCR → Markdown → neo4j-graphrag SimpleKGPipeline`

## Text

[Page 1]
UNCLASSIFIED / / FOR“OFFTCGEE-USE-ONE
Ky Defense
ey: Intelligence
oss) Reference
— Document
yr ti‘éCsS’ Acquisition Threat Support
11 March 2010
ICOD: 1 December 2009
An Introduction to the
Statistical Drake Equation
UNCLASSIFIED / / F@R-OFEIGLALIWSE-ONLY..

[Page 2]
UNCLASSIFIED//P81t 8FFIEIAL Y&E &ttbl/
An Introduction to the Statistical Drake Equation
Prepared by:
Acquisition Support Division (DW0-3)
Defense Warning Office
Directorate for Analysis
Defense Intelligence Agency
Author:
AAP Person 80
Administrative Note
COPYRIGHT WARNING: Further dissemination of the photographs in this publication is not authorized.
This product is one in a series of advanced technology reports produced in FY 2009
under the Defense Intelligence Agency, Defense Warning Office's Advanced Aerospace
Weapon System Applications (AAWSA) Program. Comments or questions pertaining to
this document should be addressed t o !AAP Person 1 ~ AAWSA Program
Manager, Defense Intelligence Agency, ATTN: CLAR/DWO-3, Bldg 6000, Washington,
DC 20340-5100.
UNCLASSIFIED//F8R 8FFl61tlib Wlilli Qtlb¥
ii

[Page 3]
UNCLASSIFIED/ /POil OFFl@IAL WSli 0Nk¥
Contents
1. Introduction .......................................................................................................iv
2. The Key Question: How Far are They ? .............................................................. 4
3. Computing N By Virtue of the Drake Equation (1961) ........................................ 7
4. The Drake Equation is Over-Simplified ............................................................. 10
5. The Statistical Drake Equation ......................................................................... 11
6. Solving the Statistical Drake Equation By Virtue of the Central Limit Theorem
(CLT) of Statistics .......................................................... , .................................... 13
7. An Example Explaining the Statistical Drake Equation ..................................... 15
8. Finding the Probability Distribution of the Et-Distance By Virtue of the Statistical
Drake Equation................................................................................................. 18
9. The "Data Enrichment Principle" as the Best CLT Consequence Upon the
Statistical Drake Equation (Any Number of Factors Allowed) ........................... 23
10. Conclusions .................................................................................................... 23
Appendix A: Proof of Shannon's 1948 Theorem Stating That the Uniform
Distribution is the "Most Uncertain" One Over a Finite Range of
Appendix B: Original Text of the Author's Paper #IAC-08-A4.1.4 Entitled the
Values ............................................................................................. 25
Statistical Drake Equation ............................................................... 28
References ........................................................................................................... 55
UNCLASSIFIED/fEOR OFFICIO! 11SF ON! X
iii

[Page 4]
UNCLASSIFIED/ /POil OFFl@IAI:: WSli 0Nk¥
An Introduction to the Statistical Drake Equation
1. Introduction
SETI (an acronym for "Search for Extraterrestrial Intelligence") is a relatively
new branch of scientific research, having begun only in 1959. Its goal is to
ascertain whether alien civilizations exist in the universe, how far from us
they exist, and possibly how much more advanced than us they may be.
As of 2009, the only physical tools we know that could help us get in touch
with aliens are the electromagnetic waves an alien civilization could emit and
we could detect. This forces us to use the largest radiotelescopes on Earth for
SETI research, because the higher our collecting area of electromagnetic
radiation is, the higher our sensitivity is (that is, the farther in space we can
probe). Yet, even by using the largest radiotelescopes on Earth (the 310-meter
dish at Arecibo, for instance), we cannot search for aliens beyond, say, a few
hundred light years away. This is a very, very small amount of space around us
within our galaxy, the Milky Way, that is about 100,000 light years in diameter.
Thus, current SETI can cover only a very tiny fraction of the galaxy, and it is
not surprising that in the past 50 years of SETI searches, NO extraterrestrial
civilization was discovered. Quite simply, we did not get far enough!
This demands the construction of much more powerful and radically new
radiotelescopes. Rather than big and heavy metal dishes, whose mechanical
problems hamper SETI research too much, we are now turning to "software
radiotelescopes," where a large number of small dishes (ATA = Allen
Telescope Array, and ALMA= Atacama Large Millimeter/submillimeter Array)
or even just of simple dipoles (LOFAR = Low Frequency Array) using state-of￾the-art electronics and very-high-speed computing can outperform the
classical radiotelescopes in many regards. The final dream in this field is the
SKA ( = Square Kilometer Array), currently being designed and expected to be
completed around 2020.
2. The Key Question: How Far are They?
But still, the key question remains: how far are they?
Or, more correctly, how far do we expect the NEAREST extraterrestrial civilization to be
from t he Solar System in the galaxy?
This question was first faced in a scientific manner back in 1961 by the same scientist
who also was t he first experimental SETI rad io astronomer ever: the American, Frank
Donald Drake (born 1930). He first considered the shape and size of the galaxy where
we are living: the Milky Way. This is a spiral galaxy measuring some 100,000 light
years in diameter and some 16,000 light years in thickness of the Galactic Disk at half￾way from its center. That is:
The diameter of the galaxy is (about) 100,000 light years, (abbreviated ly) i.e., its
radius, R Gala.1y , is about 50,000 ly.
UNCLASSIFIED/ /FOR OFFI&IJ.k Wili Ql'II.¥
iv

[Page 5]
UNCLASSIFIED/ /fOR OFFI&IAk Wlii QPU,¥
The thickness of the Galactic Disk at half-way from its center, h a " 1t'-'Y ' is about 16,000 ly.
The volume of the galaxy may then be approximated as the volume of the
corresponding cylinder, i.e.
(1)
Now consider the sphere around us having a radius r. The volume of such a sphere is
4 ( Ef Distance ) 3
Vo ur _Sphere = 3n - (2) 2
In the last equation, we had to divide the distance "ET _Distance" between ourselves
and the nearest ET civilization by 2 because we are now going to make the
unwarranted assumption that all ET civilizations are equally spaced from each
other in the galaxy! This is a crazy assumption, clearly, and should be replaced by
more scientifically-grounded assumptions as soon as we know more about our Galactic
Neighborhood. At the moment, however, this is the best guess that we can make, and
so we shall take it for granted, although we are aware that this is a weak point in the
reasoning.
Furthermore, let us denote by N the total number of civilizations now living in the
galaxy, including ourselves. Of course, this number N is unknown. We only know that
N ~ 1 since one civilization does at least exist!
Having thus assumed that ET civilizations are UNIFORMLY SPACED IN THE GALAXY, we
can then write down the proportion:
Va a/a.,y Vo ,,r_Sphere --= -~- (3) N
That is, upon replacing both (1) and (2) into (3):
3 4 ( Ef- Dis lance ) 2 - i'l" _ ___
i'l" RGa/axy h = 3 2 (4) N 1
The last equation contains two unknowns: N and ET_Distance, and so we don't know
which one it is better to solve for.
However, we may suppose that, by resorting to the (rather uncertain) knowledge that
we have about the Evolution of the galaxy through the last 10 billion years or so, we
might somehow compute an approximate value for N.
Then, we may solve (4) for ET_Distance thus obtaining the (AVERAGE) DISTANCE
BETWEEN ANY PAIR OF NEIGHBORING CIVILIZATIONS IN THE GALAXY (DISTANCE
LAW)
UNCLASSIFIED/;'FQA QFFICiIPL. !Iii 011! Y
5

[Page 6]
UNCLASSIFIED/ /fOR OFFI&IAk Wlii QPU,¥
3 6 R2 h Ef ff (N) Ca!a,y _ ,stance = VN C (5) VN
where the positive constant C is defined by
C =V6 R ~ala.,y h ca/axy ,., 28845 light years . (6)
Equations (5) and (6) are the starting point to understand the origin of the Drake
equation that we discuss in detail in Section 3 of this paper.
Let us just complete this section by pointing out three different numerical cases of the
distance law (5):
• We know that we exist, so N may not be smaller than 1, i.e., N ~ 1. Suppose then
that we are alone in the galaxy, i.e., that N=l. Then the distance law (5) yields as
distance to the nearest civilization from us just the constant C, i.e., 28,845 light
years. This is about the distance in between ourselves and the center of the galaxy
(i. e. the Galactic Bulge) . Thus, this result seems to suggest that, if we do not find
any extraterrestrial civilization around us in these outskirts of the galaxy where we
live, we should look around the Galactic Center first. And this is indeed what is
happening, i.e., many SETI searches are actually pointing the antennas towards the
Galactic Center, looking for beacons (see, for instance ref. [1]).
• Suppose next that N=l000, i.e. there are about a thousand extraterrestrial
communicating civilizations in the whole galaxy right now. Then the distance law (5)
yields an average distance of 2,885 light years. This is a distance that most
radiotelescopes in Earth may not reach for SETI searches right now: hence the need
to build larger radiotelescopes, like ALMA, LOFAR and the SKA.
• Suppose finally that N=l00000O, i.e., there are a million communicating civilizations
now in the galaxy. Then the distance law (5) yields an average distance of 288 light
years. This is within the (upper) range of distances that our current radiotelescopes
may reach for SETI searches, and that justifies all SETI searches that have been
done so far in the first fifty years of SETI (1960-2010).
In conclusion, interpolating the above three special cases of N, we may say that the
distance law (5) yields t he following key diagram of the average ET distance vs. the
assumed number of communicating civilizations, N, in the galaxy right now (Figure 1):
UNCLASSIFIED/ J'FOA. OFlilCI0 I. P !SE ON! X
6

[Page 7]
0
l
\
' "-- ~
UNCLASSIFIED/ /FOR OFFIEiIAk Wlii QPU,¥
Av erage DIST A CE of the nearest ET c iviliza tion vs. the ASSUMED NUMBffi of ET c ivilizations in the Gah
Cl)
0:::
<(
UJ
>­
!­
:I:
:i
.!::
!'.l
g
~
!'l=
200
175
150
125
100
750
500
25 0
0
0 I 00000 200000 300000 400000 500000 600000 700000 800000 900000 I 000000
ASS MED NUMBER of civiliz ations in the Galaxy (that is, Nin the Drake equation)
Figure 1. DISTANCE LAW; i.e., the Average Distance (plot along the ver-1:ical axis in light years) Versus
the NUMBER of Communicating Civilizations ASSUMED to Exist in the Galaxy Right Now
3. Computing N By Virtue of the Drake Equation (1961)
In the previous section, the problem of finding how close the nearest ET civilization may
be was "solved" by reducing it to the computation of N, the total number of
extraterrestrial civilizations now existing in this galaxy. In this section the famous
Drake equation is described, that was proposed back in 1961 by Frank Donald Drake
(born 1930) to estimate the numerical value of N. We believe that no better
introductory description of the Drake equations exists other than the one given by Carl
Sagan in his 1983 book "Cosmos" (ref. [2]), in its turn based on the famous TV series
"Cosmos." So, in this paragraph we report Carl Sagan's description of the Drake
equation unabridged.
"But is there anyone out there to talk to? With a third or a half a trillion stars in our
Milky Way galaxy alone, could ours be the only one accompanied by an inhabited
planet? How much more likely it is that technical civilizations are a cosmic
commonplace, that the galaxy is pulsing and humming with advanced societies, and,
therefore, that the nearest such culture is not so very far away - perhaps transmitting
from antennas established on a planet of a naked-eye star just next door. Perhaps
when we look up at the sky at night, near one of those faint pinpoints of light is a world
on which someone quite different from us is then glancing id ly at a star we call the Sun
and entertaining, for just a moment, an outrageous speculation.
UNCLASSIFIED//FOR OFFIEiIAk Wlii QPllsV
7

[Page 8]
UNCLASSIFIED/ /fOR OFFI&IAk Wlii QPU,¥
It is very hard to be sure. There may be several impediments to the evolution of a
technical civilization. Planets may be rarer than we think. Perhaps the origin of life is
not so easy as our laboratory experiments suggest. Perhaps the evolution of advanced
life forms is improbable. Or it may be that complex life forms evolve more readily, but
intelligence and technical societies require an unlikely set of coincidences - just as the
evolution of the human species depended on the demise of the dinosaurs and the ice￾age recession of the forests in whose trees our ancestors screeched and dimly
wondered. Or perhaps civilizations arise repeatedly, inexorably, on innumerable planets
in the Milky Way, but are generally unstable; so all but a tiny fraction are unable to
survive their technology and succumb to greed and ignorance, pollution and nuclear
war.
It is possible to explore this great issue further and make a crude estimate of N, the
number of advanced civilizations in the galaxy. We define an advanced civilization as
one capable of radio astronomy. This is, of course, a parochial if essential definition.
There may be countless worlds on which the inhabitants are accomplished linguists or
superb poets but indifferent radio astronomers. We will not hear from them. N can be
written as the product or multiplication of a number of factors, each a kind of filter,
every one of which must be sizable for there to be a large number of civilizations:
• Ns, the number of stars in the Milky Way galaxy.
• fp, the fraction of stars that have planetary systems.
• ne, the number of planets in a given system that are ecologically suitable for life.
• fl, the fraction of otherwise suitable planets on which life actually arises.
• fi, the fraction of inhabited planets on which an intelligent form of life evolves.
• fc, the fraction of planets inhabited by intelligent beings on which a communicative
technical civilization develops.
• fl, the fraction of planetary lifetime graced by a technical civilization.
Written out, the equation reads
N =Ns •jjJ •ne •fl ·ft ·Jc· fL (7)
All of the f's are fractions, having values between Oand 1; they will pare down the
large value of Ns.
To derive N we must estimate each of these quantities. We know a fair amount about
the early factors in the equation, the number of stars and planetary systems. We know
very little about the later factors, concerning the evolution of intelligence or the lifetime
of technical societies. In these cases our estimates will be little better than guesses. I
invite you, if you disagree with my estimates below, make your own choices and see
what implications your alternative suggestions have for the number of advanced
civilizations in the galaxy. One of the great virtues of this equation, due to Frank Drake
of Cornell, is that it involves subjects ranging from stellar and planetary astronomy to
organic chemistry, evolutionary biology, history, politics and abnormal psychology.
Much of the Cosmos is in the span of the Drake equation.
UNCLASSIFIED//FQA QFFICiIPL. !Iii 011! Y
8

[Page 9]
UNCLASSIFIED/ /fOR OFFI&IAk Wlii QPU,¥
We know Ns, the number of stars in the Milky Way galaxy, fairly well, by careful counts
of stars in a small but representative region of the sky. It is a few hundred billion; some
recent estimates place it at 4 x 1011 . Very few of these stars are of the massive short￾lived variety that squander their reserves of thermonuclear fuel. The great majority
have lifetimes of billions or more years in which they are shining stably, providing a
suitable energy source for the energy and evolution of life on nearby planets.
There is evidence that planets are a frequent accompaniment of star formation: in the
satellite systems of Jupiter, Saturn and Uranus, which are like miniature solar systems;
in theories of the origin of the planets; in studies of double stars; in observations of
accretion disks around stars; and is some preliminary investigations of gravitational
perturbations of nearby stars. 1 Many, perhaps even most, stars may have planets. We
take the fraction of stars that have planets, fp, as roughly equal to 1/3. Then the total
number of planetary systems in the galaxy would be Ns fp ~1.3 x 1011 (the symbol ~
means "approximately equal to"). If each system were to have about ten planets, as
ours does, the total number of worlds in the galaxy would be more than a trillion, a vast
arena for the cosmic drama.
In our own solar system there are several bodies that may be suitable for life of some
sort: the Earth certainly, and perhaps Mars, Titan and Jupiter. Once life originates, it
tends to be very adaptable and tenacious. There must be many different environments
suitable for life in a given planetary system. But conservatively we choose ne=2. Then
the number of planets in the galaxy suitable for life becomes Ns fp ne ~3 x 1011 .
Experiments show that under the most common cosmic conditions the molecular basis
of life is readily made, the building blocks of molecules able to make copies of
themselves. We are now on less certain grounds; there may, for example, be
impediments in the evolution of the genetic code, although I think this is unlikely over
billions of years of primeval chemistry. We choose fl~ 1/3, implying a total number of
planets in the Milky Way on which life has arisen at least once as Ns fp ne fl~ 1 x 1011 ,
a hundred billion inhabited worlds . That in itself is a remarkable conclusion. But we are
not yet finished.
The choices of fi and fc are more difficult. On the one hand, many individually unlikely
steps had to occur in biological evolution and human history for our present intelligence
and technology to develop. On the other hand, there must be quite different pathways
to an advanced civilization of specified capabilities. Considering the apparent difficulty
in the evolution of large organisms, represented by the Cambrian explosion, let us
choose fix fc = 1/100, meaning that only 1 per cent of planets on wh ich life arises
actually produce a technical civilization. This estimate represents some middle ground
among the varying scientific options. Some think that the equivalent of the step from
the emergence of trilobites to the domestication of fire goes like a shot in all planetary
systems; others think that, even given ten or fifteen billion years, the evolution of a
technical civi lization is unlikely. This is not a subject on wh ich we can do much
experimentation as long as our investigations are limited to a single planet. Multiplying
1 Carl Sagan was writings these lines back in the 1970's, when no extrasolar planets had been discovered yet. The
first such discovery occurred in 1995, when Michel Mayor and Didier Queloz, working at the "Observatoire de Haute
Provence" in France, discovered the first extrasolar planet orbiting the nearby star 51 Peg. This first extrasolar
planet was hence named 51 Peg B. Many more extrasolar planets were discovered around nearby stars ever since.
As of Apri l 2009, 347 extrasolar planets (exoplanets) are listed in the Extrasolar Planets Encyclopaedia.
UNCLASSIFIED/ /POil Offl@IAL W&i 9Nls¥
9

[Page 10]
UNCLASSIFIED/ /FOR OFFIEiIAk Wlii QPU,¥
these factors together, we find Ns fp ne fl fi fc ~ 1 x 109, a billion planets on which
technical civilizations have arisen at least once. But that is very different from saying
that there are a billion planets on which technical civilizations now exist. For this we
must also estimate fl.
What percentage of the lifetime of a planet is marked by a technical civil ization? The
Earth has harbored a technical civilization characterized by radio astronomy for only a
few decades out of a lifetime of a few billion years. So far, then, for our planet fl is less
than 1/108 , a millionth of a percent. And it is hardly out of the question that we might
destroy ourselves tomorrow. Suppose this were a typical case, and the destruction so
complete that no other technical civilization - of the human or any other species - were
able to emerge in the five or so billion years remaining before the Sun dies. Then Ns fp
ne fl fi fc fl ~10, and, at a given time there would be only a tiny smattering, a handful,
a pitiful few technical civilizations in the galaxy, the steady state number maintained as
emerging societies replace those recently self-immolated. The number N might be even
as small as 1 if civilizations tend to destroy themselves soon after reaching a
technological phase; there might be no one for us to talk with but ourselves. And that
we do but poorly. Civilizations would take billions of years of tortuous evolution, and
then snuff themselves out in an instant of unforgivable neglect.
But consider the alternative, the prospect that at least some civilizations learn to live
with technology; that the contradictions posed by the vagaries of past brain evolution
are consciously resolved and do not lead to self destruction; or that, even if major
disturbances occur, they are reveres in the subsequent billions of years of biological
evolution. Such societies might live to a prosperous old age, their lifetimes measured
perhaps on geological or stellar evolutionary time scales. If 1 percent of civilizations can
survive technological adolescence, take the proper fork at this critical historical branch
point and achieve maturity, then fl ~1/100, N ~ 107 , and the number of extant
civilizations in the galaxy is in the millions. Thus, for all our concern about the possible
unrel iabi lity of our estimates of the early factors in the Drake equation, which involve
astronomy, organic chemistry and evolutionary biology, the principal uncertainty comes
to economics and politics and what, on Earth, we call human nature. It seems fairly
clear that if self-destruction is not the overwhelmingly preponderant fate of galactic
civilizations, then the sky is softly humming with messages from the stars.
These estimates are stirring . They suggest that the receipt of a message from space is,
even before we decode it, a profoundly hopeful sign. It means that someone has
learned to live with high technology; that it is possible to survive technological
adolescence. This alone, quite apart from the contents of the message, provides a
powerful justification for the search for other civilizations.
4. The Drake Equation is Over-Simplified
In the nearly fifty years (1961-2009) elapsed since Frank Drake proposed his equation,
a number of scientists and writers tried to find out which numerical values of its seven
independent variables are more real istic in agreement with our present-day knowledge.
Thus there is a considerable amount of literature about the Drake equation nowadays,
and, as one can easily imagine, the results obtained by the various authors largely
differ from one another. In other words, the value of N, that various authors obtained
by different assumptions about the astronomy, the biology and the sociology implied by
the Drake equation, may range from a few tens (in the pessimist's view) to some
UNCLASSIFIED//FOR OFFIEiIAk Wlii QPII.¥
10

[Page 11]
UNCLASSIFIED/ /FOR OFFIEil.t.k W~i Q~lls¥
million or even billions in the optimist's opinion. A lot of uncertainty is thus affecting our
knowledge of N as of 2010. In all cases, however, the final result about N has always
been a sheer number, i.e., a positive integer number ranging from 1 to millions or
billions. This is precisely the aspect of the Drake equation that this author regarded as
"too simplistic" and improved mathematically in his paper #IAC-08-A4.1.4, entitled
"The Statistical Drake Equation" and presented on October 1st , 2008, at the 59th
International Astronautical Congress (IAC) held in Glasgow, Scotland, UK, September
29th thru October 3rd, 2008. That paper is attached herewith as Appendix B. Newcomers
to SETI and to the Drake equation, however, may find that paper too difficult to be
understood mathematically at a first reading. Thus, I shall now explain the content of
that paper "by speaking easily." I thank the reader for his or her attention .
5. The Statistical Drake Equation
We start by an example.
Consider the first independent variable in the Drake equation (7), i.e., Ns, the number
of stars in the Milky Way galaxy. Astronomers tell us that approximately there should
be about 350 millions stars in the galaxy. Of course, nobody has counted (or even seen
in the photographic plates) all the stars in the galaxy! There are too many practical
difficulties preventing us from doing so: just to name one, the dust clouds that don't
allow us to see even the Galactic Bulge (i.e. the central region of the galaxy) in the
visible light (although we may "see it" at radio frequencies like the famous neutral
hydrogen line at 1420 MHz). So, it doesn't make any sense to say that Ns = 350 x 106,
or, say (even worse) that the number of stars in the galaxy is (say) 354,233,321, or
similar fanciful exact integer numbers. That is just silly and non-scientific. Much more
scientific, on the contrary, is to say that the number of stars in the galaxy is 350 million
plus or minus, say, 50 millions (or whatever values the astronomers may regard as
more appropriate, since this is just an example to let the reader understand the
difficulty).
Thus, it makes sense to REPLACE each of the seven independent variables in the Drake
equation (7) by a MEAN VALUE (350 millions, in the above example) PLUS OR MINUS A
CERTAIN STANDARD DEVIATION (SO millions, in the above example).
By doing so, we have made a great step ahead: we have abandoned the too-simplistic
equation (7) and replaced it by something more sophisticated and scientifically more
serious: the STATISTICAL Drake equation. In other words, we have transformed the
classical and simplistic Drake equation (7) into an advanced statistical tool for the
investigation of a host of facts hardly known to us in detail. In other words still:
• We replace each independent variable in (7) by a RANDOM VARIABLE, labeled
D, (from Drake).
• We assume that the MEAN VALUE of each D, is the same numerical value previously
attributed to the corresponding independent variable in (7).
• But now we also ADD A STANDARD DEVIATION cr0; on each side of the mean value,
that is provided by the knowledge gathered by scientists in each discipline
encompassed by each D,.
UNCLASSIFIED//FQA QFFICilOL. !!ii ONI X
11

[Page 12]
UNCLASSIFIED/ /fOR OFFI&IAk Wlii QPU,¥
Having so done, the next question is:
How can we find out the PROBABILITY DISTRIBUTION for each D; ?
For instance, shall that be a Gaussian, or what?
This is a difficult question, for nobody knows, for instance, the probability distribution of
the number of stars in the galaxy, not to mention the probability distribution of the
other six variables in the Drake equation (7).
There is a brilliant way to get around this difficulty, though.
We start by excluding the Gaussian because each variable in the Drake equation is a
POSITIVE (or, more precisely, a non-negative) random variable, while the Gaussian
applies to REAL random variables only. So, the Gaussian is out. Then, one might
consider the large class of well-studied and positive probability densities called "the
gamma distributions," but it is then unclear why one should adopt the gamma
distributions and not any other. The solution to this apparent conundrum comes from
Shannon's Information Theory and a theorem that he proved in 1948: "The probability
distribution having maximum entropy ( = uncertainty) over any FINITE range of real
values is the UNIFORM distribution over that range," This is proven in Appendix A of the
present document.
So, at this point, we assume that each of the seven D; in (7) is a UNIFORM random
variable, whose mean value and standard deviation is known by the scientists working
in the respective field (let it be astronomy, or biology, or sociology). Notice that, for
such a uniform distribution, the knowledge of the mean value Po; and of the standard
deviation u 0, automatically determines the RANGE of that random variable in between
its lower (called a;) and upper (called b;) limits: in fact these limits are given by the
equations
(8)
(the "surprising" factor 3 in the above equations comes from the definitions of mean
value and standard deviation: please see equations (12), (15) and (17) in Appendix B
for the relevant proof). So the uniform distribution of each random variable D; is
perfectly determined by its mean value and standard deviation, and so are all its other
properties.
The next problem is the following:
OK, since we now know everything about each uniformly distributed D;, what is the
probability distribution of N, given that N is the product (7) of all the D1 ?
In other words, not only do we want to find the analytical expression of the probability
density function of N, but we also want to relate its mean value f-lN to all mean values
µ 0
, of the D;, and its standard deviation u N to all standard deviations u
0
, of the D;.
12
UNCLASSIFIED/fFOR: QFFICiIO L. lalii ODIL.¥

[Page 13]
UNCLASSIFIED/ /FOR OFFI&I.t.k W~i Q~lk¥
This is a difficult problem.
It occupied the author's mind for no less than about ten years (1997-2007).
It is actually an ANALYTICALLY UNSOLVABLE problem, in that, to the best of this
author's knowledge, it is IMPOSSIBLE to find an analytic expression for any FINITE
PRODUCT of uniform random variablesD; . This result is proven in Sections 2 thru 3.3 of
Appendix B (unfortunately!) .
6. Solving the Statistical Drake Equation By Virtue of the
Central Limit Theorem (CLT) of Statistics
The solution to the problem of finding the analytical expression for the probability
density function of N in the statistical Drake equation was found by this author in
September 2007. The key steps are the following:
• Take the natural logs of both sides of the statistical Drake equation (7). This
changes the product into a sum.
• The mean values and standard deviations of the logs of the random variables D;
may all be expressed analytically in terms of the mean values and standard
deviations of the D; .
• Recall the Central Limit Theorem (CLT) of statistics, stating that (loosely speaking) if
you have a SUM of independent random variables, each of which is ARBITRARILY
DISTRIBUTED (hence, also including uniformly distributed), then, when the number
of terms in the sum increases indefinitely (i.e. for a sum of random variables
infinitely long) .. . the SUM RANDOM VARIABLE TENDS TO A GAUSSIAN.
• Thus, the natural log of N tends to a Gaussian.
• Thus, N tends to the LOGNORMAL DISTRIBUTION.
• The mean value and standard deviations of this lognormal distribution of N may all
be expressed analytically in terms of the mean values and standard deviations of
the logs of the D, already found previously.
This result is fundamental.
All the relevant equations are summarized in the following Table 1. This table is actually
the same as Table 2 of the author's original paper IAC-08-A4.1.4, entitled "The
Statistical Drake Equation" and presented by him at the International Astronautical
Congress (IAC) held in Glasgow, UK, on October l5t, 2008. This original paper is
reproduced in Appendix B.
To sum up, not only is it found that N approaches the completely known lognormal
distribution for an INFINITY of factors in the statistical Drake equation (7), but the way
is paved to further applications by removing the condition that the number of terms in
the product (7) must be FINITE.
UNCLASSIFIED/ /FOR 8FFI&l.t.k Wii QNk¥
13

[Page 14]
UNCLASSIFIED/ /fOR OFFI&IAk Wlii QPU,¥
This possibility of ADDING ANY NUMBER OF FACTORS IN THE DRAKE EQUATION (7)
was not envisaged, of course, by Frank Drake back in 1961, when "summarizing" the
evolution of life in the galaxy in SEVEN simple STEPS. But today, the number of factors
in the Drake equation should already be increased: for instance, there is no mention in
the original Drake equation of the possibility that asteroidal impacts might destroy the
life on Earth at any time, and this is because the demise of the dinosaurs at the K/T
impact had not been yet understood by scientists in 1961, and was so only in 1980!
In practice, the number of factors should INCREASE as much as necessary in order to
get better and better estimates of N as long as our scientific knowledge increases. This
is called the "Data Enrichment Principle" and believe should be the next important goal
in the study of the statistical Drake equation.
Finally, a numerical example explaining how the statistical Drake equation works in the
practice will be given in the next section.
UNCLASSIFIED/ /rOR orr1e1At HSE OrtLY
14

[Page 15]
UNCLASSIFIED/ /FOR OFFIEiIAk Wlii QPU,¥
Table 1. Summary of the Properties of the Lognormal Distribution That Applies
to the Random Variable N = Number of ET Communicating Civilizations in the
Galaxy
Random variable N = number of communicating ET
civilizations in galaxy
Probability distribution Loqnormal
Probability density function (1n(11h,J'
1 1 -~
(n ;::-: 0)
n 27!<:T
JN (n)= - · & e
Mean value a'
-
(N )= eµe 2
Variance a 1 = e2µ ea' (ea' - I)
a'
a N = eµ e 2 .Jea2 - 1
Standard deviation
All the moments, i.e. k-th moment 2 a' k ·-
(Nk)= ekµ e 2
_ _ ~I - a- Mode 2 (= abscissa of the log normal peak) n nnde = npeak - e e
a'
f ( )
Value of the Mode Peak 1 -p 2 N n lTl)dc = & ·e ·e 2,r (l
Median (= fifty-fifty probability value for rred ian =m =e"
N)
Skewness K ( , ) e-6pe-3a' _ 3_ = ea + 2
(K4)¾ ., k' - lne3a2 + 3e2a' +6ea' +61
Kurtosis K ,, ., ., "} _ 4_ = e4a- + 2 e3a- + 3 e-u- - 6
(K2)2
Expression of 1-1 in terms of the lower (a;) µ = ± (Y;) =± b;[in(b;) - 1]- a;[in (a;)-1]
and upper (b;) limits of the Drake i=I i= I b; - a; uniform input random variables 0 ;
Expression of <:T 2 in terms of the lower (a;) 7 7
a;b;[ln (b; )- in(a;)f a 2 =La~ = L l- and upper (b;) limits of the Drake (b;-a} i= I i=I uniform input random variables 0 ;
7. An Example Explaining the Statistical Drake Equation
To understand how things work in practice for the statistical Drake equation, please
consider the following table 2. It is made up of three columns:
• The first column on the left lists the seven input sheer numbers that also become
• The mean values (middle column).
• Finally the last column on the right lists the seven input standard deviations.
UNCLASSIFIED/1re1t OFFl@IAL WSE 9Nk¥
15

[Page 16]
UNCLASSIFIED/ /FOR OFFIEil.t.k W&i Q~lls¥
The bottom line is the classical Drake equation (7). We see that, for this particular set
of seven inputs, the classical Drake equation (i.e. the product of the seven numbers)
yields a total of 3500 communicating extraterrestrial civilizations existing in the galaxy
right now.
rs := 350 -109 s := s
0 10
µfp := fp fp := 100 ofp := 100
l ne := 1 µne := ne crne := -
/3
0 fl := - µfl := fl crfl := ~ 100 100
fi :=~ µfi := fi on := ~ 100 100
0 fc:= - µfc := fc crfc := ~ 100 100
fL := 10000 crtL := 1000 µfl. := tL
1010 1010
_ 1 := Ks-fp -ne-fl-fi.fc .ff, = 3500
Table 2. Input Values (i.e. mean values and standard deviations) for the Seven Drake Uniform Random
Variables Di . The first column on the left lists the seven input sheer numbers that also become the mean values
(middle column). Finally the last column on the right lists the seven input standard deviations. The bottom line is
the classical Drake equation (7).
The statistical Drake equation, however, provides a much more articulated answer than
just the above sheer number N = 3500. In fact, a MathCad code written by this author
and capable of performing all t he numerical calculations required by the statistical
Drake equation for a given set of seven input mean values plus seven input standard
deviations, yields for N the lognormal distribution (thin curve) plotted in Figure 2. We
see immediately that the peak of this thin curve (i.e. the mode) falls at about
n rmde;;;; npeak = eµ e-a' ""250 (this is equation (99) of Appendix B), while the median (fifty￾fifty value splitting the lognormal density in two parts with equal undergoing areas) falls
at about nm,dian;;;; eµ ""1740 . These seem to be smaller values than N = 3500 provided by
the classical Drake equations, but it's a wrong impression due to a poor "intuitive"
understanding of what statistics is! In fact, neither the mode nor the median are the
" really important" values: the really important value for N is the MEAN VALUE! Now if
you look at t he thin curve in Figure 2 below (i.e. the lognorma l distribution arising from
the Central Limit Theorem), you see that this curve has a LONG TAIL ON THE RIGHT! In
other words, it does NOT immediately go down to nearly zero beyond the peak of the
mode. Thus, when you actually compute the mean value, you should not be too
UNCLASSIFIED// POR OPPICll<L ti.!! er~LV
16

[Page 17]
UNCLASSIFIED/ /FOR OFFI&IAk Wlii QPU,¥
(]''
surprised to find out that it equals (N) = e11 e2 ::::: 4589 .559 ~4590 communicating
civilizations now in the galaxy. This is the important number, and it is HIGHER than the
3500 provided by the classical Drake equation. Thus, in conclusion, THE STATISTICAL
EXTENSION of the classical Drake equation INCREASES OUR HOPES to find an
extraterrestriaI civiIization !
PROBABILITY DENSITY FUNCTION OF N
1000 2000 3000 4000
N = Number of ET Civilizations in Galaxy
Figure 2. Comparing the Two Probability Density Functions of the Random Variable N Found (1)
Without Resorting to the CLT at All (thick curve) and (2) Using the CLT and the Relevant Lognormal
Approximation (thin curve).
Even more so our hopes are increased when we go on to consider the standard
deviation associated with the mean value 4590. In fact, the standard deviation is given ,,.,
by equation (97) of Appendix B. This yields er"' = e11 e2 e"2 -1 =11195 and so the
expected number of N may actually be even much higher than the 4590 provided by
the mean value alone! The "upper limit of the one-sigma confidence interval" (as
statisticians call it), i.e. the sum 4590+11195 = 15,785, yields a higher number still!
(Note: the "lower limit of the one-sigma confidence interval is ZERO because the
lognormal distribution is POSITIVE (or, more correctly, non-negative)). Finally, the
reader should note that the thick curve depicted in Figure 2 is just the NUMERICAL
solution of the statistical Drake equation for a FINITE number of 7 input factors. Figure
2 actually shows that this curve "is well interpolated" by the lognormal distribution (thin
curve), i.e., by the neat analytical expression provided by the Central Limit Theorem for
an INFINITE number of factors in the Drake equation. That is, in conclusion, Figure 2
visually shows that taking 7 factors or an infinity of factors "is almost the same thing"
already for a value as small as 7.
UNCLASSIFIED/ /FOil OFFI@IAb W&i QNI.¥
17

[Page 18]
UNCLASSIFIED/ /FOR OFFIEil.t.k Wii Q~lls¥
8. Finding the Probability Distribution of the Et-Distance By
Virtue of the Statistical Drake Equation
Having solved the statistical Drake equation by finding the lognormal distribution, we
are now in a position to solve the ET-DISTANCE problem by resorting to statistics again,
rather than just to the purely deterministic Distance Law (5), as we did in Section 2.
This is "scientifically more serious" than just the purely deterministic Distance Law (5)
inasmuch as the new statistical Distance Law will yield a PROBABILITY DENSITY for the
Distance, with the relevant mean value and standard deviation. In other words, the
Distance Law (5) itself becomes a random variable whose probability distribution, mean
value and standard deviation must be computed by "replacing" into (5) the fact that N
is now known to follow the lognormal distribution. This is mathematically described in
detail in Section 7 of Appendix A.
The important new result is the PROBABILITY DENSITY FOR THE DISTANCE, the
equation of which is
(9)
holding for r ;,: O. This is equation (114) of Appendix B.
Starting from this equation, the MEAN VALUE OF THE random variable ET_DISTANCE is
computed as
J.I cr2
(Er_Distance) =Ce3 e""jg (10)
which is equation (119) of Appendix B, and finally the ET_DISTANCE STANDARD
DEVIATION
_!!. a2Kr2 - 3 18 9 CJ ET_Distanu: - Ce e e - l (11)
which is equation ( 123) of Appendix B. Of course, all other descriptive statistical
quantities, such as moments, cumulants etc. can be computed upon starting from the
probability density (9), and the result is Table two hereafter, that is Table 3 of Appendix
B.
Finally, to complete this section, as well as this "introduction to the statistical Drake
equation," the numerical values that equations (10) and (11) yield for the Input Table 1
are determined. They are, respectively:
_}!_ CTl
r,11ea11 _ m lue =Ce 3 e 18 ;::: 2,670 light years (12)
UNCLASSIFIED/ /FOR OFFIEil.t.k Wii QNls¥
18

[Page 19]
UNCLASSIFIED / / FOR-OFFIGRAL-U65-ONLY
which is equation (153) of Appendix B, and
awe | cam
gr pisine =Ce 2 e!8 Ve % —1 1,309 light years (13)
which is equation (154) of Appendix B.
19
UNCLASSIFIED/ }-FOR-OFFIGTAL-UGE-ONLY

[Page 20]
UNCLASSIFIED / / FOR-OFFEGHH-USE-OAL
Table 2. Summary of the Properties of the Probability Distribution That Applies
to the Random Variable ET_Distance Yielding the (average) Distance Between
Any Two Neighboring Communicating Civilizations in the Galaxy
Random variable ET_Distance between any two neighboring
ET civilizations in galaxy assuming they are
UNIFORMLY distributed throughout the
whole galaxy volume.
Probability distribution
Probability density function f i: Haag }
Recta heater |,
os tg 207
Set pistane(") + \tno re;
Mean value we
(ET_Distance) =Ce 3 e!8
Variance 2, 2f a
zr Distme =C’e} e%/e% -1
Standard deviation uwele
Ort pistane = Ce Biers Viesh
All the moments, i.e. k-th moment eh Be
(ET_Distance*) = c* e je 18
Mode (= abscissa of the lognormal peak) woe
Trode = "peak =C ne ®
Value of the Mode Peak Peak Value of fer pistane(") =
3 iio
= fer pistane (mde ) ae nes
Median (= fifty-fifty probability value for N) aH
median = m=Ce 3
Skewness e Sa? a
ele? -3e18 +26
K3
ooo,
(K,)2 8 so@ to? wt a? 2
Cle® -4e% -3e 9 +12¢3 -6e 9
Kurtosis K 4a? o 20
a4 =e 9 +2e3 43¢9 -6
(K2)
Expression of “in terms of the lower (ai) a Zp [in(b,)—1]-a,[in(a,)—1]
and upper (bi) limits of the Drake uniform x= Di= > Bia
input random variables Di i = oe
Expression of in terms of the lower (ai) Py Si => alin) P
and upper (bi) limits of the Drake uniform ah e (,-4,
input random variables Di
20
UNCLASSIFIED / 4-@R-OFFIGIAL-US5E-ODLY.

[Page 21: illegible]

[Page 22]
UNCLASSIFIED/ /fOR OFFI&IAk Wlii QPU,¥
It is clarifying to draw the graph of the ET_Distance probability density (9):
DISTANCE OF NEAREST Ef_CIVILIZA TION
5.63 ·10-20
500 1000 1500 2000 2500 3000 3500 4000 4500 5000
ET _Distance from Earth (light years)
Figure 3. The Probability of Finding the Nearest Extraterrestrial Civilization at the distance r From Earth
(in light years) if the Values Assumed in the Drake Equation are Those Shown in Input Table 1. The
relevant probability density function fET_Disian.,( r) is given by equation (9). Its mode (peak abscissa) equals 1933
light years, but its mean value is higher since the curve has a long tail on the right: the mean value equals in fact
2670 light years. Finally, the standard deviation equals 1309 light years: THIS IS GOOD NEWS FOR SETI,
inasmuch as the nearest ET galaxy civilization might lie at just 1 sigma = 2670-1309 = 1361 light years from us.
From Figure 3 we see that the probability of finding extraterrestrials is practically zero
up to a distance of about 500 light years from Earth. Then it starts increasing with the
increasing distance from Earth, and reaches its maximum at
_l!_ ~
r=de =r peak =Ce 3 e 9 :::: 1,933 light years. (14)
This is the MOST LIKELY VALUE of the distance at which we can expect to find the
nearest extraterrestrial civilization.
It is not the mean value of the probability distribution (9) for fET_Distan.,( r). In fact, the
probability density (9) has an infinite tail on the right, as clearly shown in Figure 3, and
hence its mean value must be higher than its peak value. As given by (10) and (12), its
....!:!.. 0'2
mean value is r,,,en,,_mlue = Ce 3 e 18 c::,2670 light years. This is the MEAN (value of the)
DISTANCE at which we can expect to find extraterrestrials.
UNCLASSIFIED/ ;'FQA QFFICiIPL. !Iii 011! Y
22

[Page 23]
UNCLASSIFIED/ /FOR OFFIEiIAk Wlii QPU,¥
After having found the above two distances (1933 and 2670 light years, respectively),
the next natural question that arises is: "what is the range, back and forth around the
mean value of the distance, within which we can expect to find extraterrestrials with
"the highest hopes?" The answer to this question is given by the notion of standard
deviation that we already found to be given by (11) and (13),
I' 0'2 ~
CTET_Distance = Ce 3 e •8 Ve 9 -1 ""1309 light years .
More precisely, this is the so-called 1-sigma (distance) level. Probability theory then
shows that the nearest extraterrestrial civilization is expected to be located within this
range, i.e. within the two distances of (2670-1309) = 1361 light years and
(2670+1309) = 3979 light years, with probability given by the integral of fET_oistance(r)
taken in between these two lower and upper limits, that is:
i
3979 1igh1 years
fET Disiance (r) dr:::: 0.75 = 75 % (15)
l36 1 ligbtycars -
In plain words: with 75 percent probability, the nearest extraterrestrial civilization is
located in between the distances of 1361 and 3979 light years from us, having assumed
the input values to the Drake Equation given by table 1. If we change those input
values, then all the numbers change again, of course.
9. The "Data Enrichment Principle" as the Best CLT
Consequence Upon the Statistical Drake Equation (Any
Number of Factors Allowed)
As a fitting climax to all the statistical equations developed so far, let us now state our
"DATA ENRICHMENT PRINCIPLE." It simply states that "The Higher the Number of
Factors in the Statistical Drake equation, The Better."
Put in this simple way, it simply looks like a new way of saying that the CLT lets the
random variable Y approach the normal distribution when the number of terms in the
sum (4) approaches infinity. And this is the case, indeed.
10. Conclusions
We have sought to extend the classical Drake equation to let it encompass Statistics
and Probability.
This approach appears to pave the way to future, more profound investigations
intended not only to associate "error bars" to each factor in the Drake equation, but
especially to increase the number of factors themselves. In fact, this seems to be the
only way to incorporate into the Drake equation more and more new scientific
information as soon as it becomes available. In the long run, the Statistical Drake
equation might just become a huge computer code, growing in size and especially in
the depth of the scientific information it contains. It would thus be Humanity's first
"Encyclopaedia Galactica."
UNCLASSIFIED/ /FOR OFFIEiIAk Wlii QPlls¥
23

[Page 24]
UNCLASSIFIED/ /fOR OFFI&IAk Wlii QPU,¥
Unfortunately, to extend the Drake equation to Statistics, it was necessary to use a
mathematical apparatus that is more sophisticated than just the simple product of
seven numbers.
UNCLASSIFIED/ /FOR 8FFIGl.t.k W&i QPII.¥
24

[Page 25]
1
UNCLASSIFIED/ /FOR OFFIEil.t.k W~i Q~lls¥
Appendix A: Proof of Shannon's 1948 Theorem Stating
That the Uniform Distribution is the "Most Uncertain" One
Over a Finite Range of Values
Information Theory was initiated by Claude Shannon (1916-2001) in his well-known
1948 two papers:
Rqrutted mm commi:ms from B •1-S,'l•st Ii •ral Jour:!li,
\ GI. 1 . pp. 9--!13 , 62J..,iS , July, Occober. I
A Mathematical Theory of Communication
By C. E SHANNO
In this Appendix, we wish to draw attention to a couple of theorems that Shannon
proves on pages 36 and 37 of his work, and read, respectively (note that Shannon
omits the upper and lower limits of all integrals in the first theorem: they are minus
infinity and plus infinity, respectively):
5. Letp(x) bea one-dimensionaldis :i ti The onno p(x) ginng ammcimumentropy 1:.ubjec-tto the
c dition tha e dan:l devia on ofx be fixed at a i- G ian. To show this we must maximize
H(x) = - fp x)logp(x)d
<T- =j p x- dx and 1 =/ p x)dx
as cons •. This requi~ . by calculu~ of variations maxunizing
/ [- p x)logp(x) >.p(x 1p(x)] dx.
e condition or lus is
- 1- logp(x
•ng the constllllf5 to sat' the
and
UNCLASSIFIED/ /FOR: QFFIGI0ls Uii 0111 X
25

[Page 26]
UNCLASSIFIED/ /fOR OFFI&IAk Wlii QPU,¥
7. Ifx is limited to a half line (p(x) = 0 for x <0) and the fin.t moment ofx is ihted at a:
a = f p(x dx
then the maximwn en opy OCCW1! when
p(x) =,! - f.r/al a
and 1s equal to logea.
Now, we wish to point out that there is a third possible case, other than the two given
by Shannon. This is the case when the probability density function p(x) is limited to a
FINITE INTERVAL a::; x::; b. This is obviously the case with any physical POSITIVE
random variable, such as a distance, or the number N of extraterrestrial communicating
civilizations in the,". And it is easy to prove that for any such finite random variable the
maximum entropy distribution is the UNIFORM distribution over a -5, x -5, b. Shannon did
not bother to prove this simple theorem in his 1948 papers since he probably regarded
it as too trivial. But we prefer to point out this theorem since, in the language of the
statistical Drake equation, it sounds like:
"Since we don't know what the probability distribution of any one of the Drake random
variables D; is, it is safer to assume that each of them has the maximum possible
entropy over a; -5,x-5, h;, i.e., that D; is UNIFORMLY distributed there.
The proof of this theorem is along the same lines as for the previous two cases
discussed by Shannon:
We start by assuming that a; -5, x -5, b; .
We then form the linear combination of the entropy integral plus the normalization
condition for D;
where i is a Lagrange multiplier.
Performing the variation, one finds
- Iogp(x)- 1+1 = 0 that is: p(x)= e ,1,- i .
Applying the normalization condition (constraint) to the last expression for p(x) yields
b, ( ) f. b; ,l,-1 2-1 f.b; ,1,-1 ( ) I = f. p x dx = e dx = e dx = e b; - a,. a1 a1 a1
that yields
,l,-1 1
e = --
h; - a;
UNCLASSIFIED/ /POlt Offl@IAL WSi 9Nk¥
26

[Page 27]
UNCLASSIFIED/ /FOR OFFI&IAk Wlii QPU,¥
and finally
p(x) = - 1- with a; s x s b;
b; - a;
showing that the maximum-entropy probability distribution over any FINITE interval
a; sxsb; is the UNIFORM distribution .
UNCLASSIFIED/ /FOR OFFI&IAk Wlii QNk¥
27

[Page 28]
UNCLASSIFIED/ /FOR OFFIEil.t.k W&i Q~lls¥
Appendix B: Original Text of the Author's Paper #IAC-08-
A4.1.4 Titled the Statistical Drake Equation
IAC-08-A4.1.4
THE STATISTICAL DRAKE EQUATION
Claudio Maccone
Co-Vice Chair, SETI Permanent Study Group, International Academy ofAstronautics
Address: Via Martorelli, 43 - Torino (Turin) 10155 - Italy
URL: http://www.maccone.com/ - E-mail: clmaccon@libero.it
ABSTRACT. We provide th statistical generalization of the Drake equation.
From a simple product of seven positive numbers, the Drake equation is now turned into the product of seven
positive random variables. We call this "the Statistical Drake Equation," The mathematical consequences of
this transformation are then derived. The proof of our results is based on the Central Limit Theorem (CL T) of
Statistics. In loose terms, the CLT states that the sum of any number of independent random variables, each of
which may be ARBITRARILY distributed, approaches a Gaussian (i.e. u01mal) random variable. This is called
the Lyapunov Form of the CLT, or the Lindeberg Form of th CLT, depending on the mathematical constraints
assumed on the third moments of the various probability distributions. In conclusion, we show that:
l) The new random variable N, yielding the number of communicating civilizations in the Galaxy, follows the
LOGNORMAL distribution. Then, as a consequence, the mean value of this lognormal distribution is the
ordinary Nin the Drake equation. The standard deviation, mode, and all the moments of this lognormal N
are found also.
2) The seven factors in the ordinary Drake equation now become seven positive random variables. The
probability distribution of each random variable may be ARBITRARY. The CLT in the so-called
Lyapunov or Lindeberg forms (that both do not assume the factors to be identically distributed) allows for
that. In other words the CLT "translates" into our statistical Drake equation by allowing an arbitrary
probability distribution for each factor. This is both physically realistic and practicalJ y very useful, of
course.
3) An application of our statistical Drake equation then follows. The (average) DISTANCE between any two
neighboring and communicating civilizations in the Galaxy may be shown to be inversely proportional to
the cubic root of N. Then, in our approach, this distance becomes a new random variable. We derive the
relevant probability density function , apparently previously unknown and dubbed "Maccone distribution"
by Paul Davies.
4) DATA ENRICHMENT PRINCIPLE. It should be noticed that ANY positive number of random vai'iables
in the Statistical Drake Equation is compatible with the CLT. So, our generalization allows for many more
factors to be added in the future as long as more refined scientific knowledge about each factor will be
known to the scientists. This capability to make room for more future factors in the statistical Drake
equation we call the "Data Enrichment Principle", and we regard it as the key to more profound future
results in the fields of Astrobiology and SETI.
Finally, a practical example is given of how our statistical Drake equation works numerically. We work out in
detail the case where each of the seven random variables is uniformly distributed around its own mean value
and has a given standard deviation. For instance, the number of stars in the Galaxy is assumed to be uniformly
distributed around (say) 350 billions with a standard deviation of (say) I billion. Then, the resulting lognormal
distribution of N is computed numerically by virtue of a MathCad file that the author has written. This shows
UNCLASSIFIED/; P"OR OP"P"lelltt li!I! er•tv
28

[Page 29]
UNCLASSIFIED/ /fOR OFFI&IAk Wlii QPU,¥
that the mean value of the lognormal random variable N is actually of the same order as the classical N given
by the ordinary Drake equation, as one might expect from a good statistical generalization.
1. INTRODUCTION
The Drake equation is a now famous result
(see ref. [1] for the Wikipedia summary) in the
fields of SETI (the Search for ExtraTetTestial
Intelligence, see ref. [2]) and Astrobiology (see ref.
[3]). Devised in l 960, the Drake equation was the
first scientific attempt to estimate the number N of
ExtraTerrestrial civilizations in the Galaxy with
which we might come in contact. Frank D. Drake
(see ref. [4]) proposed it as the product of seven
factors:
N=Ns-fp-ne·fl·fi·fc·fL. (1)
Where:
I) Ns is the estimated number of stars in our
Galaxy.
2) fp is the fraction (= percentage) of such stars
that have planets.
3) ne is the number "Earth-type" such planets
around the given star; in other words, ne is
number of planets, in a given stellar system,
on which the chemical conditions exist for life
to begin its course: they are "ready for life,"
4) fl is fraction(= percentage) of such "ready for
life" planets on which life actually starts and
grows up (but not yet to the "intelligence"
level).
5) fl is the fraction (= percentage) of such
"planets with life fom1S" that actually evolve
until some form of "intelligent civilization"
emerges (like the first, historic human
civilizations on Earth).
6) Jc is the fraction (= percentage) of such
"planets with civilizations" where the
civilizations evolve to the point of being able
to communicate across the interstellar
distances with other (at least) similarly
evolved civilizations. As far as we know in
2008, this means that they must be aware of
the Maxwell equations governing radio waves,
as well as of computers and radioastronomy
(at least).
7) fl is the fraction of galactic civilizations alive
at the time when we, poor humans, attempt to
pick up their radio signals (that they throw out
into space just as we have done since l 900,
when Marconi started the transatlantic
transmissions). In other words, fl is the
number of civilizations now transmitting and
receiving, and this implies an estimate of"how
long will a technological civilization live?"
that nobody can make at the moment. Also,
are they going to destroy themselves in a
nuclear war, and thus live only a few decades
of technological civilization? Or are they
slowly becoming wiser, reject war, speak a
single language (like English today), and
merge into a single "nation", thus living in
peace for ages? Or will robots take over one
day making "flesh animals" disappear forever
(the so-called "post-biological universe")?
No one knows ...
But let us go back to the Drake equation (1).
In the fifty years of its existence, a number of
suggestions have been put forward about the
different numeric values of its seven factors. Of
course, every different set of these seven input
numbers yields a different value for N, and we can
endlessly play that way. But we claim that these
are like ... children plays!
We claim the classical Drake equation (1), as
we shall call it from now on to distinguish it from
our statistical Drake equation to be introduced in
the coming sections, well, the classical Drake
equation is scientifically inadequate in one regard
at least: it just handles sheer numbers and does not
associate an error bar to each of its seven factors.
At the very least, we want to associate an error
bar to each D;.
Well, we have thus reached STEP ONE in our
improvement of the classical Drake equation:
replace each sheer number by a probability
distribution!
The reader is now asked to look at the flow
chart in the next page as a guide to this paper,
please.
2. STEP 1: LETTING EACH FACTOR
BECOME A RANDOM VARIABLE
In this paper we adopt the notations of the
great book "Probability, Random Variables and
Stochastic Processes" by Athanasios Papoulis
(1921-2002), now re-published as Papoulis-Pillai,
UNCLASSIFIED/ ,'FOR: QFFIGI CL. Wii ODIL:¥
29

[Page 30]
UNCLASSIFIED/ /fOR OFFI&IAk Wlii QPU,¥
ref. [5]. The advantage of this notation is that it
makes a neat distinction between probabilistic ( or
statistical: it's the same thing here) variables,
always denoted by capitals, from non-probabilistic
(or "detenninistic") variables, always denoted by
lower-case letters. Adopting the Papoulis notation
also is a tribute to him by this author, who was a
Fulbright Grantee in the United States with him at
the Polytechnic [nstitute (now Polytechnic
University) of New York in the years 1977-78-79.
We thus introduce seven new (positive)
random variables D; ("D" from "Drake") defined
as
D1 = Ns
D2 =fp
D3 =ne
D4 = fl (2)
Ds =fl
D6 =Jc
D7 =fL
so that our STATISTICAL Drake equation may be
simply rewritten as
(3)
Of course, N now becomes a (positive) random
variable too, having its own (positive) mean value
and standard deviation. Just as each of the D; has its
own (positive) mean value and standard deviation ...
... the natural question then arises: how are the seven
mean values on the right related to the mean value on
the left?
... and how are the seven standard deviations on the
right related to the standard deviation on the left?
Just take the next step ...
3. STEP 2: INTRODUCING LOGS TO
CHANGE THE PRODUCT INTO A SUM
Products of random variables are not easy to
handle in probability theory. It is actually much
easier to handle sums of random variables, rather
than products, because:
1) The probability density of the sum of two or
more independent random variables is the
convolution of the relevant probabifay
densities (worry not about the equations,
right now).
2) The Fourier transform of the convolution
simply is the product of the Fourier
transforms (again, worry not about the
equations, at this point)
UNCLASSIFIED//EOR OFFICIO! !!SF ON! X
30

[Page 31]
UNCLASSIFIED/ /fOR OFFI&IAk Wlii QPU,¥
I
1. Introduction I
I
2. Step 1: Letting each factor become a random
I
2.1. Step 2: Introducing logs to change the product into a I
I
2.2. Step 3: The transformation law of random variables. I
I
3. Step 4: Assuming the easiest input distribution for
each D1: the uniform distribution.
I
3.1. Step 5: A numerical example of the Statistical Drake equation
with uniform distributions for the Drake random
variables 0 ;.
I
3.2. Step 6: Computing the logs of the
7 uniformly distributed
Drake random variables
O; .
I
3.3. Step 7: Finding the probability
I
density function of N, but
only numerically not
analytically.
I
DEAD END! I 4. The Central Limit Theorem (CLT) of Statistics.
I
s. LOGNORMAL distribution as the probability
distribution of the number N of
communicating ExtraTerrestrial Civilizations
in the Galaxy.
I
6. Comparing the CLT r esults with the Non- CLT
results, and discarding the Non-CLT approach.
7. DISTANCE to the nearest ExtraTerrestriai
Civilization as a probability distribution ( Paul
Davies dubbed that the Maccone distribution).
I
7.1 Classical, non-probabilistic derivation of the
Distance to the nearest ET Civilization.
7.2 Probabilistic derivation of probability density
function for nearest ET Civilization Distance.
7.3 Statistical properties of the distribution.
7.4 Numerical example of the distribution.
I
8. DATA ENRICHMENT PRINCIPLE as the best
CLT consequence upon the Drake equation:
;mx number of factors allowed for.
UNCLASSIFIED/ ;'FQA QFFICilPL. PP&i ODI! Y
31

[Page 32]
UNCLASSIFIED/ /FOR OFFI&IAk Wlii QPU,¥
So, let us take the natural logs of both sides of the
Statistical Drake equation (3) and change it into a
sum:
It is now convenient to introduce eight new (positive)
random variables defined as follows:
Y=ln(N) { (5) Y;=ln(D;) i=l,...,7.
Upon inversion, the first equation of (5) yields the
important equation, that will be used in the sequel
(6)
We are now ready to take STEP THREE.
STEP 3: THE TRANSFORMATION LAW
OF RANDOM VARIABLES
So far we did not mention at all the problem:
"which probability disttibution shall we attach to
each of the seven (positive) random variables D; ?"
It is not easy to answer this question because we
do not have the least scientific clue to what
probability distributions fit at best to each of the
seven points listed in Section 1.
Yet, at least one trivial error must be avoided:
claiming that each of those seven random variables
must have a Gaussian (i.e. normal) distribution. In
fact, the Gaussian distribution, having the well￾known bell-shaped probability density function
(a ;,: o) (7)
has its independent variable y ranging between --oo
and oo and so it can apply to a real random variable
Y only, and never to positive random variables like
those in the statistical Drake equation (3). Period.
Searching again for probability density functions
that represent positive random variables, an obvious
choice would be the gamma distributions (see, for
instance, ref. [6]). However, we discarded this choice
too because of a different reason: please keep in mind
that, according to (5), once we selected a particular
type of probability density function (pdt) for the last
seven of equations (5), then we must compute the
(new and different) pdf of the logs of such random
variables. And the pdf of these logs certainly is not
gamma-type any more.
It is high time now to remind the reader of a
certain theorem that is proved in probability courses,
but, unfortunately, does not seem to have a specific
name. It is the transformation law (so we shall call
it, see, for instance, ref. [5]) allowing us to compute
the pdf of a certain new random variable Y that is a
known function Y=g(X) of another random
variable X having a known pdf. In other words, if the
pdf fx (x) of a certain random variable X is known,
then the pdf fr(Y) of the new random variable Y,
related to X by the functional relationship
y = g(X) (8)
can be calculated according to this rule:
1) First invert the corresponding non-probabilistic
equation y =g(x) and denote by X; (y) the
various real roots resulting from the this
inversion.
2) Second, take notice whether these real roots may
be either finitely- or infinitely-many, according
to the nature of the function y = g(x).
3) Third, the probability density function of Y is
then given by the (finite or infinite) sum
(9)
where the summation extends to all roots x;(Y) and
lg' (x; (y)~ is the absolute value of the first
derivative of g(x) where the i-th root x;(Y) has
been replaced instead of x.
Since we must use this transformation law to transfer
from the D; to the Y; =ln(D;), it is clear that we
need to start from a D; pdf that is as simple as
possible. The gamma pdf is not responding to this
need because the analytic expression of the
transformed pdf is very complicated (or, at least, it
looked so to this author in the first instance). Also,
the gamma distribution has two free parameters in it,
and this "complicates" its application to the various
meanings of the Drake equation. Tn conclusion, we
discarded the gamma distributions and confined
UNCLASSIFIED/ /FOil OFFI@IAb W&i! QNI.¥
32

[Page 33]
I
UNCLASSIFIED/ /fOR OFFI&IAk Wlii QPU,¥
ourselves to the simpler uniform distribution instead,
as shown in the nest section.
4. STEP 4: ASSUMING THE EASIEST
PUT DISTRIBUTION FOR EACH D; :
THE U IFORM DISTRIBUTION
Let us now suppose that each of the seven D; is
distributed UNIFORMLY in the interval ranging
from the lower limit a; ~ 0 to the upper limit
b; ~a;·
This is the same as saying that the probability
density function of each of the seven Drake random
variables D; has the equation
1 funi rom, o. (x) = - - with O::; a; s; x s; b; (10) - ' h;-a;
as it follows at once from the normalization condition
b
f, funi rol'TlLD-(x )dx = 1. (11) ti; I
Let us now consider the mean value of such
uniform D; defined by
b; 1 f b' (unifom'LD;)= f xfunibniLo, (x)dx=--- xdx ai b; -a; a;
2 ]b; 2 2 = --1- .::._ = b; - a; = a; +b; [
b; - a; 2 a; 2 (b; - a;) 2 •
By words (as it is intuitively obvious): the mean
value of the uniform distribution simply is the mean
of the lower plus upper limit of the variable range
a -+b. (unifonn_D; ) = -'--' . (12) 2
In order to find the variance of the uniform
distribution, we first need finding the second moment
• 2) fb; 2 ( ) ( uniform_Di = X fun ibrnLD, X dx 0 1
I ", , l x 3 ]b; h3
- - a.
3
[ = b-a. Lx-dx = b. -a. 3 = 3(b. -;,.) I I I I I <l; I I
_ (b; -a;)(a; +a;b; +b; ) _ a; +a;b; +b;
- 3 (b; - a;) - 3
The second moment of the uniform distribution is
thus
D 2) a; +a;b; +b; ( unitiorm . = ---'---'-'-----'- (13) - I 3
From (12 and (13) we may now derive the variance
of the uniform distribution
c:r~n ifi>rnLD; = ( uniform_D ; 2)-(uniform_D;) 2
a; ? + a;b; +b;2
= ( 14) 3 4 12
Upon taking the square root of both sides of ( 14 ), we
finally obtain the sta11dard deviation of the u11iform
distribution :
We now wish to perform a calculation that is
mathematically trivial, but rather unexpected from
the intuitive point of view, and very important for our
applications to the statistical Drake equation. Just
consider the two simultaneous equations ( 12) and
(15)
a. +b- ) l( uniform_Di =~
(16) (T __b,
--
__a,
uniIDTITLD; - 3 •
Upon inverting this trivial linear system, one finds
fa; = (uniform_D; )- 3 (Tuni DnTLD; (17)
lb; = ( uniform_D;) + 3 c:runifom1..D, •
This is of paramount importance for our application
the Statistical Drake equation inasmuch as it shows
that:
if one (scientifically) assigns the mean value and
standard deviation of a certai11 Drake random
variable D;, then. the lower a11d upper limits of the
relevant uniform distribution are given by the two
equations (17), respectively.
UNCLASSIFIED/ /POlt 9Pfl@IAL H§E 8Nk¥
33

[Page 34]
UNCLASSIFIED/ /FOR OFFI&IAk Wlii QPU,¥
In other words, there is a factor of 3 =1.732
included in the two equations (17) that is not obvious
at all to human intuition, and must indeed be taken
into account.
The application of this result to the Statistical Drake
equation is discussed in the next section.
3.1 STEP 5: A NUMERICAL EXAMPLE
OF THE STATISTICAL DRAKE
EQUATION WITH UNIFORM
DISTRIBUTIO S FOR THE DRAKE
RANDOM VARIABLES D;
The first variable Ns in the classical Drake
equation (1) is the number of stars in our Galaxy.
Nobody knows how many they are exactly (!). Only
statistical estimates can be made by astronomers, and
they oscillate (say) around a mean value of 350
billions (if this value is indeed correct!). This being
the situation, we assume that our uniformly
distributed random variable Ns has a mean value of
350 billions minus or plus a standard deviation of
(say) one billion (we don't care whether this number
is scientifically the best estimate as of August 2008:
we just want to set up a numerical example of our
Statistical Drake equation). ln other words, we now
assume that one has:
(uniform_D1) =350 ~109
{ (18)
a unilomLD, =l • 10 •
Therefore, according to equations (17) the lower and
upper limit of our uniform distribution for the
random variable Ns=D1 are, respectively
aNs uniform_D 3auni "'" rm O = 348.3-109
{ \ . ,v - I 9 ( ( 9)
bNs =(umform_D 1) + ,fj aunii:>rTTLD, =351.7 -10
Similarly we proceed for all the other six random
variables in the Statistical Drake equation (3).
For instance, we assume that the fraction of stars
that have planets is 50%, i.e. 50/100, and this will be
the mean value of the random variable fp=D2. We
also assume that the relevant standard deviation will
be 10%, i. e. that a fr =10 /100 . Therefore, the
relevant lower and upper limits for the uniform
distribution offp=D2 tum out to be
a fp : ( un~orm_D2 )-,fj a unitbrnLD2 : 0.327 (20) {
b.fp - ( uniform_D 2 ) + ,fj a unitomLD2 - 0.673
The next Drake random variable is the number
ne of "Earth-type" planets in a given star system.
Taking example from the Solar System, since only
the Earth is truly "Earth-type", the mean value of ne
is clearly I, but the standard deviation is not zero if
we assume that Mars also may be regarded as Earth￾type. Since there are thus two Earth-type planets in
the Solar System, we must assume a standard
deviation of 1 / ,fj =0.577 to compensate the ,fj
appearing in (17) in order to finally yield two "Earth￾type" planets (Earth and Mars) for the upper limit of
the random variable ne. In other words, we assume
that
The next four Drake random variables have even
more "arbitrarily" assumed values that we simply
assume for the sake of making up a numerical
example of our Statistical Drake equation with
uniform entry distributions. So, we really make no
assumption about the astronomy, or the biology, or
the sociology of the Drake equation: we just care
about its mathematics.
All our assumed entries are given in Table l.
Please notice that, had we assumed all the
standard deviations to equal zero in Table I, then our
Statistical Drake equation (3) would have obviously
reduced to the classical Drake equation (1), and the
resulting number of civilizations in the Galaxy would
have turned out to be 3500:
IN =3500 1. (22)
This is the important deterministic number that we
will use in the sequel of this paper for comparison
with our statistical results on the mean value of N,
i.e. (N). This will be explained in Sections 3.3 and 5.
UNCLASSIFIED// POil OFFI@IAb W&i 01'11.¥
34

[Page 35]
=
UNCLASSIFIED/ /FOR OFFIEil.t.k W&i Q~lls¥
1s := 3 · o-109 s := -s cr s := 1-109
·o 10
µfp := fp fp := 100 crfp := 100
1
ne := 1 µne := ne crne := -
,/3
fl :=~
100 µfl := fl crt1 = ~ 100
fi := 20 µfi := fi crfi := ~ 100 100
fc := 20
-
100 µfc := fc
10 crfc := -
100
10000 fl. :=-- µfl. := fl.
1000
crfl. := -- 1010 101 0
s-fp -ne-fl-fi.fc .fl. - = 3500
Table 1. Input values (i.e. mean values and standard devi ations) for the seven Drake uniform random variables D;.
The fi rst column on the left lists the seven input sheer numbers that also become the mean values (middle column).
Finally the last column on the right lists the seven input standard deviations. The bottom line is the cl assical Drake
equation (1).
3.2 STEP 6: COMPUTING THE LOGS
OF THE 7 UNIFORMY
DISTRIBUTED DRAKE RANDOM
VARIABLES D;
Intuiti vely speakiJ1g, the natural log of a
unifonnly disuibuted random vari able may not be
another uniformly distributed random variable! This
is obvious from the tri vial diagram of y =ln (x)
shown below:
Natural logarithm of x
-
_,,,,,,,,_,,. ~
r
2 3 4 5
POSITIVE independent variable x
Figure 1. The simple function y = ln(x).
So, if we have a unifo rml y distributed random
variable D; with lower limit a;and upper limit b;, the
random variable
Y; =ln(D;) i = l,...,7 (23)
must have its range limited in between the lower limit
l11 (a;) and the upper limi t ln(b,). In other words, this
are the lower and upper limits of the relevant
probability density functio n fr;(y). But what is the
actual analytic expression of such a pdf/. To find it,
we must resort to the general transformation law for
random variables, defined by equation (9). Here we
obviously have
y =g(x) =ln(x) (24)
That, upon inversion, yields the single root
(25)
On the other hand, differentiating (24) one gets
UNCLASSIFIED//FOR OFFIEil.t.k W&i QNls¥
35

[Page 36]
• •
UNCLASSIFIED/ /fOR OFFI&IAk Wlii QPU,¥
where (25) was already used in the last step. By
virtue of the uniform probability density function
(I 0) and of (26), the general transformation law (9)
finally yields
1n other words, the requested pdf of Y; is
eY ,--,---,,-----,-.,..,
fr,(y) =-- i = l, ...,7 lm(a;) :,;y:,;in(b;)I (28) b; - a;
Probability density functions of the natural logs of
all the uniformly distributed Drake random
variables D; .
This is indeed a positive function of y over the
interval !n(a;):,; y:,; ln(b;) , as for every pdf, and it is
easy to see that its normalization condition is
fulfilled:
... (29)
Next we want to find the mean value and
standard deviation of Y; , since these play a crucial
role for future developments. The mean value (Y;) is
given by
!n(b;) ( ) s.•n(b;) y,eY (Y.) = J. Y· fr y dy = --dy 1 Jn(a,) ' !n(a,)b; -a;
b; [in(b; )-1]- a,-[in(a; )-1] = --'-''----''--'--'--=--'-"-"--'-'---= (30)
This is thus the mean value of the natural log of all
the uniformly distributed Drake random variables
D;
In order to find the variance also, we must first
compute the mean value of the square of Y;, that is
( 2) J.in(b.) 2 { .) J.!n(/J.) y2 •e Y Y; = y ·fry dy= --dy
h1(<1;) ' !n(a;) b; - Cl;
= b; ~ 2 (b; )- 21n(b; )+ 2]- a; [ln 2 (a; )- 2ln(a; )+ 2)
b; - a;
... (32)
The variance of Y; = ln(D;) is now given by (32)
minus the square of (31), that, after a few reductions,
yield:
2 2 a .b.[ln(b.)- ln(a .)]2
a - a _ 1_ , , , , (33) r, - In(o,) - (b; _ a;)2
Whence the corresponding standard deviation
1 _ a;b; [in(b;)- in(a;)]2
(34)
(b; - a;)2
Let us now turn to another topic: the use of
Fourier transforms, that, in probability theory, are
called "characteristic functions," Following again the
notations of Papoulis (ref. [5]) we call "characteristic
function", <Dy, (s) , of an assigned probability
distribution Y; , the Fourier transform of the relevant
probability density function, that is (with j = ~)
The use of characteristic functions simplifies things
greatly. For instance, the calculation of all moments
of a known pdf becomes trivial if the relevant
characteristic function is known, and greatly
simplified also are the proofs of important theorems
of statistics, like the Central Limit Theorem that we
will use in Section 4. Another important result is that
the characteristic function of the sum of a finite
number of independent random variables is simply
given by the product of the corresponding
characteristic functions. This is just the case we are
facing in the Statistical Drake equation (3) and so we
are now led to find the characteristic function of the
random variable Y; , i.e.
UNCLASSIFIED/,'FOA OFlilCI0 I. P !SE ON! X
36

[Page 37]
UNCLASSIFIED/ /fOR OFFI&IAk Wlii QPU,¥
(36)
Thus, the characteristic function of the natural log
ofthe Drake uniform random variable D; is given by
3.3 STEP 7: FINDING THE
PROBABILITY DENSITY
FUNCTION OF N, BUT ONLY
NUMERICALLY NOT
ANALYTICALLY
Having found the characteristic functions
<l>y/s) of the logs of the seven input random
variables D; , we can now immediately find the
characteristic fu ctio □ of the random variable Y =
ln(N) defined by (5). 1n fact, by virtue of (4), of the
well-known Fourier transform property stating that
"the Fourier transform of a convolution is the product
of the Fourier transforms", and of (37), it
immediately follows that <l>y(() equals the product
of the seven Cf> y1 (s):
The next step is to invert this Fourier transform in
order to get the probability density function of the
random variable Y = ln(N). In other words, we must
compute the following inverse Fourier transform
-oo
oo [ 7 bl+)( i+ j( l = - 1 fe -i(y IT ;_ - a;_ dc;'.(39)
2n - co i= I (b; a;)(l+ Js)
This author regrets that he was unable to compute the
last integral analytically. He had to compute it
numerically for the particular values of the 14 a; and
b; that follow from Table 1 and equations 17. The
result was the probability density function for Y =
ln(N) plotted in the following Figure 2.
...
>- PROB. DENSITY FUNCTION OF Y=ln(N) 0 0.4 C
0
·.:::,
..2
Q 0.3
-f 0.2
ii
~ "' 0.1
:z;
..8
•
~I....-,
/
I
'
\
\
e O O I 2 3 4 5 6 7 8 9 10 11 12 ll,
Independent variable Y = ln(N)
Figure 2. Probability density function of Y = ln(N)
computed numericaJly by virtue of the integral (39).
The two "funny gaps" in the curve are due to the
numeric limitations in the MathCad numeric solver
that the author used for this numeric computation.
We are now just one more step from finding the
probability density of N, the number of
ExtraTerrestrial Civilizations in the Galaxy predicted
by our Statistical Drake equation (3). The point here
is to transfer from the probability density function of
Y to that of N, knowing that Y = ln(N) , or
alternatively, that N=exp(Y), as stated by (6). We
must thus resort to the transformation law of random
variables (9) by setting
(40)
This, upon inversion, yields the single root
(41)
On the other hand, differentiating ( 40) one gets
(42)
where (41) was already used in the last step. The
general transformation law (9) finally yields
UNCLASSIFIED/ /EAR AFFJCJA 1 1!SF QN 1Y
37

[Page 38]
UNCLASSIFIED/ /fOR OFFI&IAk Wlii QPU,¥
This probability density function f N (y) was
computed numerically by using (43) and the numeric
curve given by (39), and the result is shown in Figure
3.
Z 4 · l 0
-4PROBA BILITY DENSITY FUNCTIO OF N
.....
0
.g3·10-4 {)
C:
..: 2·10-4
·i
~ 1 ·10-4
1000 2000 3000 4000
N = umber of ET Civilizations in Galaxy
Figure 3. The numeric (and not analytic) probability
density function curve f N (y) of the number N of
ExtraTerrestrial Civilizations in the Galaxy according
to the Statistical Drake equation (3). We see that the
curve peak (i.e. the mode) is very close to low values
of N, but the tail on the right is high, meaning that the
resulting mean value (N) is of the order of
thousands.
We now want to compute the mean value (N)
of the probability density (43). Clearly, it is given by
(N) =f
00
y J,v(y)dy. (44)
0
This integral too was computed numerically, and the
result was a perfect match with N=3500 of (22), that
is
(N) = 3499.99880 177509 + 0.OOCXX:XH2 4914686i (45)
Note that this result was computed numerically in the
complex domain because of the Fourier transforms,
and that the real part is virtually 3500 (as expected)
while the imaginary part is virtually zero because of
the rounding errors. So, this result is excellent, and
proves that the theory presented so far is
mathematically correct.
Finally we want to consider the standard
deviation. This also had to be computed numerically,
resulting in
uN =3953.42910 143389 +o.cx:x:x:x:x:m 28CXXJ58i . (46)
This standard deviation, higher than the mean value,
implies that N might range in between 0 and 7453.
This completes our study of the probability
density function of N if the seven uniform Drake
input random variable D; have the mean values and
standard deviations listed in Table I .
We conclude that, unfortunately, even under the
simplifying assumptions that the D; be 11nifor111ly
distributed, it is impossible to solve the full problem
a11alytically, since all calculations beyond equation
(38) had to be performed numerically.
This is no good.
Shall we thus loose faith, and declare "impossible"
the task of finding an analytic expression for the
probability density function f N (y) ?
Rather surprisingly, the answer is "no", and there
is indeed a way out of this dead-end, as we shall see
in the next section.
5. THE CENTRAL LIMIT THEOREM (CLT)
OF STATISTICS
Indeed there is a good, approximating analytical
expression for ftv (y) , and this is the following
lognormal probability density Junction
To understand why, we must resort to what is
perhaps the most beautiful theorem of Statistics:
the Central Limit Theorem (abbreviated CLT).
Historically, the CLT was in fact proven first in
190 I by the Russian mathematician Alexandr
Lyapunov (1857-1918), and later (1920) by the
Finnish mathematician Jar! Waldemar Lindeberg
(1876-1932) under weaker conditions. These
conditions are certainly fulfilled in the context of
the Drake equation because of the "reality" of the
astronomy, biology and sociology involved with it,
and we are not going to discuss this point any
further here. A good, synthetic description of the
Central Limit Theorem (CLT) of Statistics is found
at the Wikipedia site (ref. (7)) to which the reader
is refetTed for more details, such as the equations
for the Lyapunov and the Lindeberg conditions,
making the theorem "rigorously" valid.
UNCLASSIFIED/ J'FQA QFFICiIPL. !Iii 011! X
38

[Page 39]
UNCLASSIFIED/ /fOR OFFI&IAk Wlii QPU,¥
Put in loose terms, the CLT states that, if one
has a sum of random variables eve11 NOT
identically distributed, this sum tends to a normal
distribution whe11 the 11umber of tenns maki11g up
the sum te11ds to infinity. Also, the normal
distribution mean value is the sum of the mean
values of the addend random variables, and the
normal distribution variance is the sum of the
variances ofthe addend random variables.
Let us now write down the equations of the CLT
in the form needed to apply it to our Statistical Drake
equation (3). The idea is to apply the CLT to the sum
of random variables given by (4) and (5) whatever
their probability distributions ca11 possibly be. Tn
other words, the CL T applied to the Statistical Drake
equation (3) leads immediately to the following three
equations:
I) The sum of the (arbitrarily distributed)
independent random variables Y; makes up
the new random variable Y.
2) The sum of their mean values makes up the
new mean value of Y.
3) The sum of their variances makes up the
new variance of Y.
In equations:
7
y = :~::vi i =I
7
(Y) = I(Y; ) (48)
i=I
7
O'y 2 ="' L..Jo-r2,
i= I
This completes our synthetic description of the CL T
for sw11s of random variables.
6. THE LOGNORMAL DISTRIBTIO IS
THE DISTRIBUTION OF THE NUMBER
N OF EXTRATERRESTRIAL
CIVILIZATIONS IN THE GALAXY
The CLT may of course be exte11ded to products
of random variables upon taki11g the logs of both
sides, just as we did in equatio11 (3). It then follows
that the exponent random variable, like Y i11 (6),
tends to a 11ormal random variable, and, as a
co11 seque11 ce, it follows that the base random
variable, like N i11 (6), te11ds to a lognormal random
variable.
To understand this fact better in mathematical
terms consider again of the transformation law (9) of
random variables. The question is: what is the
probability density function of the random variable N
in equation (6), that is, what is the probability density
function of the lognormal distribution? To find it, set
(49)
This, upon inversion, yields the single root
x1(y) =x(y) =!n(y). (50)
On the other hand, differentiating (49) one gets
where (50) was already used in the last step. The
general transformation law (9) finally yields
( ) "' fx(x;(y)) 1 ( ( )) fNY= L..J i '( ()~=-/ylny • (52)
i g X; )' ~ 11y
Therefore, replacing the probability density on the
right by virtue of the well-known normal (or
Gaussian) distribution given by equation (7), the
lognormal distribution of equation (47) is found , and
the derivation of the lognormal distribution from the
normal distribution is proved.
In view of future calculations, it is also useful to
point out the so-called "Gaussian integral", that is:
B2
f"' e - Ax2 e 8 ·x dx = ~ •e 4 A A> 0 B =real. (53) L., VA ' '
This follows immediately from the normalization
condition of the Gaussian (7), that is
oo (x- pf 1 -- ,- J-- e lu· dx=l (54) &a- ' --Oj
just upon expanding the square at the exponent and
making the two replacements (we skip all steps)
l A= -->0, 2 2a- l (55)
B = ; 2 = real.
UNCLASSIFIED/ /FOR 8FFIGl.t.k W&i ,n11.¥
39

[Page 40]
UNCLASSIFIED/ /fOR OFFI&IAk Wlii QPU,¥
In the sequel of this paper we shall denote the
independent variable of the lognormal distribution
(47) by a lower case letter n to remind the reader that
corresponding random variable N is the positive
integer number of ExtraTerrestriaJ Civilizations in
the Galaxy. In other words, n will be treated as a
positive real number in all calculations to follow
because it is a "large" number (i.e. a continuous
variable) compared to the only civilization that we
know of, i.e. ourselves. In conclusion, from 110w 011
the log11or111al probability density f11nction of N will
be written as
(1n(11}--µ)2
1 1 -~ ( ) (56)
n v2na
IN n =-· r;:;- e (n~ O)
Having so said, we now turn to the statistical
properties of the lognormal distribution (55), i.e. to
the statistical properties that describe the number N
of ExtraTerrestrial Civilizations in the Galaxy.
Our first goal is to prove an equation yielding all
the moments of the lognormal distribution (56), that
is, for every non-negative integer k = 0, I, 2, . . . one
has
(57)
The relevant proof starts with the definition of the k￾d1 moment
(111[11 ]-p)'
k I I -~
= rn •~ •.Ji;a •e dn 0
One then transforms the above integral by
virtue of the substitution
In[n]= z. (58)
The new integral in z is then seen to
reduce to the Gaussian integral (53)
(we skip all steps here) and (57)
follows
Upon setting k =0 into (56), the
normalization condition for f N (n) follows
Upon setting k =1 into (56), the important
mean value ofthe ra11dom variable N is found
(60)
Upon setting k =2 into (56), the mean value
of the square of the random variable N is found
/N2) - 211 2a2 \ -e e . (61)
The variance of N now follows from the last two
formulae:
(62)
The square root of this is the important standard
deviation f onnula for the N random variable
(63)
The third moment is obtained upon setting
k =3 into (56)
(64)
Finally, upon setting k =4, the fourth moment
of N is found
(65)
Our next goal is to find the cumulants of N. In
principle, we could compute all the cumulants K;
from the generic i-th moment p; by virtue of the
recursion formula (see ref. [8])
• i- 1 (i - 1) . K; =A-L (66) k-1 K k f.l11 -k·
k=i
UNCLASSIFIED/ /rOR orrl@IAL HSE O,.LY
40

[Page 41]
UNCLASSIFIED/ /fOR OFFI&IAk WliF QPU,¥
In practice, however, here we shall confine
ourselves to the computation of the first four
cumulants only because they only are required to
find the skewness and kurtosis of the distribution.
Then, the first four cumulants in terms of the first
four moments read:
These equations yield, respectively:
(68)
(69)
(70)
From these we derive the skewness
(72)
and the kurtosis
(73)
Finally, we want to find the mode of the
lognormal probability density function, i.e. the
abscissa of its peak. To do so, we must first
compute the derivative of the probability density
function f N (n) of equation (56), and then set it
equal to zero. This derivative is actually the
derivative of the ratio of two functions of n, as it
plainly appears from (57). Thus, let us set for a
moment
E(n) =(1n [n] - ,u)2 (74)
2a 2
where "E" stands for "exponent," Upon
differentiating this, one gets
E 1 ' (n) = - - • 2(In [n] - ,u)· _!_ . (75)
2a2 n
But the lognormal probability density function (56),
by virtue of (74), now reads
(76)
So that its derivative is
dfET_Dis1ana,' (r) - e- E(" )E' (n )· n-1 · e- E(")
dr .Ji;a • n2
I -e-E(")[E'(n)·n + i] (77) = &a. n2
Setting this derivative equal to zero means setting
E'(n) ·n+l=O (78)
That is, upon replacing (75),
~ -(In[n]- µ)+1 =0. (79) a
Rean-anging, this becomes
In[n]- µ+a2 = 0 (80)
and finally
I 11 _ _fl - a ' I ntJde = 11pcak - e e (81)
This is the most likely number of ExtraTerrestrial
Civilizations i11 the Galaxy.
How likely? To find the value of the probability
density function f N (n) corresponding to this
value of the mode, we must obviously replace (81)
into (56). After a few rearrangements, one then
gets
UNCLASSIFIED/ ;'FOA OlililCil0 L. P!SF ON! Y
41

[Page 42]
UNCLASSIFIED/ /fOR OFFI&IAk Wlii QPU,¥
(82) 2 fx ' erf(x)= r e-:-dz (85)
This is "how likely" the most likely number of
ExtraTerrestrial Civilizations in the Galaxy is, i.e.
it is the peak height in the lognormal probability
density function f N(n) .
Next to the mode, the median m (ref. (9)) is one
more statistical number used to characterize any
probability distribution. It is defined as the
independent variable abscissa m such that a
realization of the random variable will take up a
value lower than m with 50% probability or a value
higher than m with 50% probability again. In other
words, the median m splits up our probability
density in exactly two equally probable parts. Since
the probability of occurrence of the random event
equals the area under its density curve (i.e. the
definite integral under its density curve) then the
median m (of the lognormal distribution, in this
case) is defined as the integral upper limit m:
(111(11 )-,,1)2
f
111 JN(n)dn = f"'_!__ rd- e---;;;;r- == (83)
Jo Jo n v 2na 2
In order to find m , we may not differentiate (83) with
respect to m , since the "precise" factor ½ on the
right would then disappear into a zero. On the
contrary, we may try to perform the obvious
substitution
zzO (84)
into the integral (83) to reduce it to the following
integral defining the error function erf(z)
-,/ Ji 0
Then, after a few reductions that we skip for the sake
of brevity, the full equation (83) is turned into
(86)
that is
e,f[ln(m) - p) == 0 (87) 2a
Since from the definition (85) one obviously has
erf(0)=0, (87) becomes
ln(m)- µ == 0 (88) 2a
whence finally
Irredian = m =e" I. (89)
This is the median of the lognormal distribution of
N. In other words, this is the number of
ExtraTerrestrial civilizations in the Galaxy such
that, with 50% probability the actual value of N will
be lower than this median, and with 50% probability
it will be higher.
ln conclusion, we feel useful to summarize all the
equations that we derived about the random variable
N in the following Table 2.
Random variable
Probability distribution
Probability density function
N =number of communicating ET civilizations in Galaxy
Lognormal
(111(11}--p)'
1 1 ---;;;;r- fN(n) =-· ..n,; e (n z O) n 2na
Mean value
(T2
-
(N) =e" e 2
Variance a1 =e2" ea2 (ea2 -1)
Standard deviation
a'
a N =e" e2 .Jea' -1
UNCLASSIFIED/ /fOR OFfl&IAk Wlii QNls¥
42

[Page 43]
UNCLASSIFIED/ /fOR OFFI&IAk Wlii QPU,¥
All the moments, i.e. k-th moment
Mode(= abscissa of the lognormal peak)
Value of the Mode Peak
Median(= fifty-fifty probability value for N)
Skewness
Kurtosis
Expression of µ in terms of the lower (a;) and upper
(b;) limits of the Drake uniform input random
variables D;
Expression of a 2 in terms of the lower (a;) and upper
(b;) limits of the Drake uniform input random
variables D;
- - JI -a2
nnnde = npeak - e e
a l
I - 11 , f ( ) N nTIDde = ~ •e •e - -,121r a
Table 2. Summary of the properties of the lognormal distribution that applies to the random variable N = number of
ET communicating civilizations in the Galaxy.
We want to complete this section about the
lognormal probability density function (56) by
finding out its numeric values for the inputs to the
Statistical Drake equation (3) listed in Table I.
According to the CLT, the mean value µ to be
inserted into the lognormal density (56) is given
(according to the second equation (48)) by the sum of
all the mean values (Y;), that is, by virtue of (31 ), by:
Upon replacing the 14 a; and b; listed in Table 1
into (90), the following 11umeric mea11 value µ is
found
1µ,,,7.462116 1 (91)
Similarly, to get the numeric variance a 2 one
must resort to the last of equations (48) and to (33):
(92)
yielding a 2 the following numeric varia11ce to be
inserted into the lognormal pdf (56)
la2 ,,, 1.938725 1 (93)
whence the numeric standard deviation a
1 a ,,, 1.392381 t- (94)
Upon replacing these two numeric values (84)
and (86) into the lognormal pdf (56), the latter is
perfectly determined. It is plotted in Figure 4
hereafter as the thin curve.
In other words, Figure 4 shows the lognormal
distribution for the number N of ExtraTerrestrial
Civilizations in the Galaxy derived from the Central
Limit Theorem as applied to the Drake equation
(with the input data listed i11 Table 1).
We now like to point out the most important
statistical properties of this lognormal pdf:
1) Mean Value of N. This is given by equation (60)
with µ and a given by (91) and (94), respectively:
UNCLASSIFIED/ /FOR OFFICIO! !!SF ON! X
43

[Page 44]
UNCLASSIFIED/ /FOR OFFIEiIAk Wlii QPU,¥
(N) =eµ e 2 "'4589 .559 . (95)
In other words, there are 4590 ET Civilizatio11s in
the Galaxy according the Central Limit Theorem of
Statistics with the inputs of Table 1. This ,mmber
4590 is HIGHER than the 3500 foreseen by the
classical Drake equation working with sheer
numbers only, rather than with probability
distributions. Thus equation (95) IS GOOD FOR
NEWS FOR SETI, since it shows that the expected
number of ETs is HIGHER with an adequate
statistical treatment than just with the too simple
Drake sheer numbers of(1).
2) Variance of N. The variance of the Iognormal
distribution is given by (62) and turns out to be a
huge number:
3) Standard deviation of N. The standard deviation
of the lognormal distribution is given by (63) and
turns out to be:
(97)
Again, this is GOOD NEWS FOR SETI. In fact,
such a high standard deviation means that N may
range from very low values (zero, theoretically, and
one since Humanity exists) up to tens of thousands
(4590+11195=15785 is (95)+(97)).
4) Mode of N. The mode (= peak abscissa) of the
lognormal distribution of N is given by (81 ), and has
a surprisingly low numeric value:
This is well shown in Figure 4: the mode peak is very
pronounced and close to the origin, but the right tail
is high, and this means that the mean value of the
distribution is much higher than the mode:
4590»250.
5) Median of N. The median (= fifty -fifty abscissa,
splitting the pdf in two exactly equi-probable parts)
of the lognormal distribution of N is given by (89),
and has the numeric value:
(99)
Tn words, assuming the input values listed in Table 1,
we have exactly a 50% probability that the actual
value of N is lower than 1740, and 50% that it is
higher than 1740.
7. COMPARING THE CLT RESULTS
WITH THE NON-CLT RESULTS
The time is now ripe to compare the CLT￾based results about the lognormal distribution of N,
just described in Section 5, against the Non-CLT￾based results obtained numerically in Section 3.3
To do so in a simple, visual way, let us plot on
the same diagram two curves:
1) The numeric curves appearing in Figure 2
and obtained after laborious Fourier
transform calculations in the complex
domain, and
2) The lognormal distribution (56) with
numeric µ and a given by (91) and (94)
respectively.
We see that the two curves are virtually coincident
for values of N larger than 1500. This is a
consequence of the law of large numbers, of which
the CLT is just one ofthe 111a11y facets.
Similarly it happens for natural log of N, i.e. the
random variable Y of (5), that is plotted in Figure 5
both in its normal curve version (thin curve) and in
its numeric version, obtained via Fourier transforms
and already shown in Figure 2.
The conclusion is simple: from now 011 we shall
discard forever the 1111meric calc11lations a11d we'll
stick only to the equations derived by virtue of the
CLT, i.e. to the lognormal (56) and its
co11seque11ces.
UNCLASSIFIED//509 OFFICIO! 11SF QN 1X
44

[Page 45]
UNCLASSIFIED/ /fOR OFFI&IAk WliF QPU,¥
6 ·10-4
1000 2000 3000 4000
N = Number of ET Civilizations in Galaxy
Figure 4. Comparing the two probability density functions of the random variable N found:
1) At the end of Section 3.3. in a purely numeric way and without resorting to the CLT at all (thick curve) and
2) AnalyticaJly by using the CLT and the relevant lognormal approximation (thin curve).
PROBABILITY DENSITY FUNCTION OF Y=ln(N)
0.5
>- 0.4 .....
0
g
.B
§ 0.3 .....
•~
5
"O 0.2 _q
]
" .D
e 0.1 0..
00 2 3 12
Independent variable Y = ln(N )
Figure 5. Comparing the two probability density functions of the random variable Y=ln(N) found:
I) At the end of Section 3.3. in a purely numeric way and without resorting to the CL Tat all (thick curve) and
2) Analytically by using the CL T and the relevant normal (Gaussian) approximation (thin Gaussian curve).
8. DISTANCE OF THE NEAREST and in several web sites, the solution to this
EXTRA TERRESTRIAL CIVILIZATION problem is reported with only slight differences in
AS A PROBABILITY DISTRIBUTION the mathematical proofs among the various authors.
In the first of the coming two sections (section 7 .1 )
As an application of the Statistical Drake we derive the expression for this "ET_Distance"
Equation developed in the previous sections of this (as we like to denote it) in the classical, non￾paper, we now want to consider the problem of probabilistic way: in other words, this is the
estimating the distance of the ExtraTerrestrial classical, deterministic derivation. In the second
Civilization nearest to us in the Galaxy. In all section (7.2) we provide the probabilistic
Astrobiology textbooks (see, for instance, ref. [10)) derivation, arising from our Statistical Drake
UNCLASSIFIED/}FOA OlililCil0L. 1155 ON!¥
45

[Page 46]
UNCLASSIFIED/ /fOR OFFI&Ial.k Wlili QPU,¥
Equation, of the corresponding probability density
function fET_Distance(r) : here r is the distance
between us and the nearest ET civilization
assumed as the independent variable of its own
prob~bility density function. The ensuing sections
provide more mathematical details about this
.firr_oistana, (r) such as its mean value, variance,
standard deviation, all central moments, mode,
median, cumulants, skewness and kurtosis.
CLASSICAL, NON-PROBABILISTIC
DERIVATION OF THE DISTANCE OF THE
NEAREST ET CIVILIZATION
Consider the Galactic Disk and assume that:
1) The diameter of the Galaxy is (about) 100,000
light years, (abbreviated ly) i.e. its radius,
R calaxy• is about 50,000 ly.
2) The thickness of the Galactic Disk at half-way
from its center, hcalaxy , is about 16,000 ly.
Then
3) The volume of the Galaxy may be
approximated as the volume of the
corresponding cylinder, i.e.
V Gal«ry - R1 h (100) - 1l Ga/,uy
4) Now consider the sphere around us having a
radius r. The volume of such as sphere is
4 (Er Distance) 3
VOw·_ Sphere =31l' 2 (101)
In the last equation, we had to divide the distance
"ET_Distance" between ourselves and the nearest
ET Civilization by 2 because we are now going to
make the unwarranted assumption that all ET
Civilizations are equally space from each other in
the Galaxy! This is a crazy assumption, clearly,
and should be replaced by more scientifically￾grounded assumptions as soon as we know more
about our Galactic Neighbourhood. At the moment,
however, this is the best guess that we can make,
and so we shall take it for granted, although we are
aware that this is weak point in the reasoning.
Having thus assumed that ET Civilizations
are UNIFORMLY SPACED IN THE GALAXY' we can write down this proportion:
Vcal<Lry = Vo11r_ Sphere (102)
N
That is, upon replacing both (100) and (101) into
(102):
4 (Er Distance ) 3
1l RJalaxy h = 3" ---=- 2-- (103) N I
The only unknown in the last equation is
ET _Distance, and so we may solve for it, thus
getting the:
(A VERA GE) DISTANCE BETWEEN ANY PAIR
OF NEIGHBOURING CIVILIZATIONS IN
THE GALAXY
116 R 2 h Er D. _ V Galaxy C istance - (104) 1 ,.--; = - - tN ifii
where the positive constant C is defined by
C =3 6 Ria1a.,y h calcuy ""28845 light years . ( l 05)
Equations (104) and (105) are the starting point for
our first application of the Statistical Drake
equation, that we discuss in detail in the coming
sections of this paper.
PROBABILISTIC DERIVATION OF THE
PROBABILITY DE SITY FUNCTION FOR
ET_DISTA CE
~he probability density function (pdt) yielding
the distance of the ET Civilization nearest to us in
the Galaxy and pre ented in this section, was
discovered by this author on September 5th' 2007.
He did not disclose it to other scientists until the
SETI meeting run by the famous mathematical
physicist and popular science author, Paul Davies,
at the "Beyond" Center of the University of
Arizona at Phoenix, on February 5-6-7-8, 2008.
This meeting was also attended by SETI Institute
experts Jill Tarter, Seth Shostak, Doug Vakoch,
Tom Pierson and others. During this author's talk,
Paul Davies suggested to call "the Maccone
distribution" the new probability density function
that yields the ET_Distance and is derived in this
section.
UNCLASSIFIED/ ffOR OFFI&Ial.L Wlili QPII..¥
46

[Page 47]
UNCLASSIFIED/ /fOR OFFI&IAk Wlii QPU,¥
Let us go back to equation (104). Since N is
now a random variable ( obeying the lognorma1
distribution), it follows that the ET _Distance must
be a random variable as well. Hence it must have
some unknown probability density function that
we denote by
(106) f ET_Di stana, (r)
where r is the new independent variable of such a
probability distribution (it is denoted by r to
remind the reader that it expresses the three￾dimensional radial distance separating us from the
nearest ET civilization in a full spherical symmetry
of the space around us).
The question then is: what is the unknown
probability distribution (106) of the ET_Distance?
We can answer this question upon making the two
formal substitutions
{ (107) Er_distance ➔ y
into the transformation law (8) for random
variables. As a consequence, ( I 04) takes form
I C - y = g(x) = -,- = C • x 3 . (108) v;;
In order to find the unknown probability density
f ET_Di stru,., (r) , we now to apply the rule (9) to
(108). First, notice that (108), when inverted to
yield the various roots x; (y), yields a single real
root only
(109)
Then, the summation in (9) reduces to one term
only.
Second, differentiating (108) one finds
4 C -- g'(x) =--·x 3 . (110) 3
Thus, the relevant absolute value reads
(111)
Upon replacing (111) into (9), we then find
This is the denominator of (9). The numerator
simply is the lognormal probability density
function (56) where the old independent variable x
must now be re-written in terms of the new
independent variable y by virtue of (109). By
doing so, we finally an-ive at the new probability
density function f y (y)
Rearranging and replacing y by r, the final form
is:
2
(In[~]-11]
3 1 - 2u'
f ET_distana, (r) = - • ~ •e (113) 2 r 'I/ L.Jr a￾Now, just replace C in ( 113) by virtue of ( 105).
Then:
We have discovered the probability density
function yielding the probability of finding the
nearest ExtraTerrestrial Civilization in the
Galaxy in the spherical shell between the
distances r and r+dr from Earth:
(,{ 6 Ri.t11a~~ hc0 1a.Q}l'r
3 l 2 0-l
fET_DistanaJr)=-· ~ ·e 2 r "1.,1r a
(114)
holding for r .:: 0 .
STA TISTICAL PROPERTIES OF THIS
DISTRIBUTION
UNCLASSIFIED/ /FOR &FFIGIAk lalii ODIL:¥
47

[Page 48]
UNCLASSIFIED/ /fOR OFFI&IAk Wlii QPU,¥
We now want to study this probability
distribution in detail. Our next questions are:
l) What is its mean value?
2) What are its variance and standard
deviation?
3) What are its moments to any higher order?
4) What are its cumulants?
5) What are its skewness and kurtosis?
6) What are the coordinates of its peak, i.e.
the mode (peak abscissa) and its ordinate?
7) What is its median?
The first three points in the list are all covered
by the following theorem: all the moments of ( 113)
are given by (here k is the generic and non￾negative integer exponent, i.e. k = 0, I, 2, 3, ... ~ 0)
(Er_Distance*) = f' / ·f ET_Distana,(r)dr
(1n[ ~ ]-µr
=fr*-r~(T dr -e
(115)
To prove this result, one first transforms the above
integral by virtue of the substitution
(116)
Then the new integral in z is then seen to reduce to
the known Gaussian integral (53) and, after several
reductions that we skip for the sake of brevity,
(115) follows from (53). In other words, we have
proven that
µ 2 (J2
(Er_Distancek) = Ck e - k3 / •18 . (117)
Upon setting k = 0 into (117), the
normalization condition for f ET_Distan"' (r) follows
if ET Distame(r)dr = l . (118) 0 -
Upon setting k = l into (117), the important
mean val11e of the random variable ET_Distance
isfo1111d
f.-l a z
(Ef_Distance) =Ce3 e18 . (119)
Upon setting k = 2 into (l 17), the mean value of
the square of the random variable ET _Distance is
found
2 2 2 - p - (1 (Ef_Distance2 ) = C2 e 3 e 9 (120)
The variance of ET_Distance now follows from
the last two formulae with a few reductions:
CT~T_Distan"' = (Ef_Distance2 )-(Ef_Distance)2
(121)
So, the variance ofET_Distance is
(122)
The square root of this is the important
standard deviation of the ET_Distance random
variable
_f!_ (11 ,-;i-- (TET_Di S(ana, =C e 3 e• 8 ~e9 -1 . (123)
The third moment is obtained upon setting
k = 3 into ( 117)
(12
(Er_Distance 3 ) = C3 e-p e2 (124)
Finally, upon setting k =4 into ( 117), the fourth
moment of ET _Distance is found
4 8 l
(Er_Distance4 )=C4 e3 -µ e9(1 (125)
UNCLASSIFIED//POR 9Pfl@IAL H§E 8PUs:¥
48

[Page 49]
3
UNCLASSIFIED/ /FOR OFFI&IAk Wlii QPU,¥
a 2 5,,.2 a'] Our next goal is to find the cumulants of the e- P[ e 2 - 3 e 18 + 2 e 6
ET _Di stance. 1n principle, we could compute all
the cumulants K; from the generic i-th moment
µ; by virtue of the recursion formula (see ref. [8])
' i- 1 ( i -1) ' (126)
k=i k - 1
K; = JI; -z: Kk J.111 -k ·
ln practice, however, here we shall confine
ourselves to the computation of the fust four
cumulants because they only are required to find
the skewness and kurtosis of the distribution ( 113).
Then, the first four cumulants in terms of the first
four moments read:
These equations yield, respectively:
_!!_ a 2
K .=Ce3el8_ (128)
(129)
(130)
Sa ' 5a2 4a2 a 2 2a2 ]2 C3 [ e- 9- -4e9 -3e9 +12 e3 -6e_9_
... (132)
and the kurtosis
4 0"2 2 a 2
K - (K 4
)2 =e 9 +2e 3 +3e 9 -6 . (133)
2
Next we want to find the mode of this
distribution, i.e. the abscissa of its peak. To do so,
we must fust compute the derivative of the
probability density function fET_Oistame(r) of (113),
and then set it equal to zero. This derivative is
actually the derivative of the ratio of two functions
of r, as its plainly appears from (113). Thus, let us
set for a moment
(134)
where "E" stands for "exponent," Upon
differentiating,
one gets
(13 1) = - 1 •[ln[£.] - µ)·(- 3).!.. (135) c,2 ,-3 ,.
2 4a2 4p [ sa 5a2 a ' 2a'] =C4 e-3 e- 9- -4 e- 9- - 3e_9_ + 12 e3 - 6e_9_
But the probability density function (113) now
reads
3 e-E(r) From these we derive the skewness fET Distana:(r)= ~ ·-- (136) - ..,;2,rc, r
So that its derivative is
dfET_Disiana:, (r) 3 -e- E(r) E' (r)· r-1 ·e- E(r)
dr = &a. ,.2
UNCLASSIFIED//POil OFFI@IAb W&I! 91'11.¥
49

[Page 50]
UNCLASSIFIED/ /FOR OFFI&IAk Wlii QPU,¥
3 -e-£(,-)[E '(,}r+l] (137) .Ji;a . ,.2
Setting this derivative equal to zero means setting
E'(r)·r+l=O (138)
That is, upon replacing (l 35) into (138), we get
Rearranging, this becomes
that is
(141)
whence
In[£] =!!_+ i!_ (142) r 3 9
and finally
_!:!_ 0'"2
r;mde"',.peak=Ce 3e 9 (143)
This is the most likely ET_Distance/rom Earth.
How likely?
To find the value of the probability density
function f ET_Disim,"' (r) corresponding to this value
of the mode, we must obviously replace () into ().
After a few rearrangements, which we skip for the
sake of brevity, one gets
Peak Value of fET_Distana,(r) = fET_Distana,(1rroctcl
... (144)
This is the peak height in the pdf f ET_Dist"""' (r) •
Next to the mode, the median m (ref. [9]) is one
more statistical number used to characterize any
probability distribution. It is defined as the
independent variable abscissa m such that a
realization of the random variable will take up a
value lower than m with 50% probability or a value
higher than m with 50% probability again. In other
words, the median m splits up our probability
density in exactly two equally probable parts. Since
the probability of occurrence of the random event
equals the area under its density curve (i.e. the
definite integral under its density curve) then the
median m (of the lognormal distribution, in this
case) is defined as the integral upper limit m:
J,"' I (145) fET Distanu,(r)dr=- 0 - 2
Upon replacing ( 113), this becomes
(146)
2
In order to find m, we may not differentiate ( 146)
with respect to m, since the "precise" factor ½ on the
right would then disappear into a zero. On the
contrary, we may try to perform the obvious
substitution
(147)
into the integral (146) to reduce it to the following
integral (85) defining the error function erf(z). Then,
after a few reductions that we leave to the reader as
an exercise, the full equation (145), defining the
median, is turned into the corresponding equation
involving the error function erj{x) as defined by (85):
UNCLASSIFIED/ /FOR OFFI&IAk Wlii ,un.¥
50

[Page 51]
UNCLASSIFIED / / FOR-OFFEGHH-USE-OA
ET_Distance between any two neighboring ET
Random variable Civilizations in Galaxy assuming they are UNIFORMLY
distributed throughout the whole Galaxy volume.
Probability distribution Unnamed (Paul Davies suggested “Maccone distribution”
[xfetees=]
Probability density function 3 1 — COC
Ser _pistane(") =—-7=—-e 20
r \2r0
(Defining the positive numeric constant C) C= alo Re salaxy "Galaxy ¥ 28845 light years
we
Mean value (ET_Distance) =Ce 3 e!8
2, 22
Variance Oar pistne =C’€ 3? €%|e% -1
a7 ko | ions
Standard deviation Cr pinicat Ce 3e)8Ve® -1
apf Be
All the moments, i.e. k-th moment (ET_Distance" ) =Cke 3¢ 38
St aoe
Mode (= abscissa of the ms density function Tande ™ Tpeak = Ce 3¢@ 9
pe
Peak Value of fpr pistane(") =
2
Value of the Mode Peak Se a 5 ai elf
ET_Distane \"mde Cc de
BT Distance ala ita oe
ET_Distance) megan Ce
e so oF
ele? -3e!8 +2e6
Skewness K; = ee ee
3 3
(K,)2 Boh Soh 4 oe 20° \2
Cle® -4e% -3e 9 +12¢3 -6e °
x @ 2 2
Kurtosis 4 se 9 4263439 -6
(kK.
Expression of sin terms of the lower (a;) and upper wis 3 )- x }{in(b,)-1]-a;{In(a,)-1]
(bj) limits of the Drake uniform input random = y = b,-a;
variables Dj a ia
. 2: td 7
Expression of o” in terms of the lower (a;) and upper eae > ales v1 _ Gb; [in )- In(a; i
(bj) limits of the Drake uniform input random = ¥ Ps (, = a;
variables D; _ Z
Table 3. Summary of the properties of the probability distribution that applies to the random variable ET_Distance
yielding the (average) distance between any two neighboring communicating civilizations in the Galaxy.
51
UNCLASSIFIED / /®OR-OBEILGLALUSEONLY.

[Page 52]
UNCLASSIFIED/ /fOR OFFI&IAk Wlii QPU,¥
that is
(148)
(149)
Since from the definition (147) one obviously has
erf(0)=0, (149) yields
This is the median of the lognormal distribution of
N. Ill other words, this is the number of
ExtraTerrestrial civilizatio11s i11 the Galaxy such
that, with 50% probability the actual value of N will
be lower tha11 this median, and with 50% probability
it will be higher.
In conclusion, we feel useful to summarize all the
equations that we derived about the random variable
N in the following Table 2.
NUMERICAL EXAMPLE OF THE
ET_DISTANCE DISTRIBUTION
ln this section we provide a numerical
example of the analytic calculations carried on so
far.
Consider the Drake Equation values reported
(150) in Table 1. Then, the graph of the corresponding
probability density function of the nearest
whence finally ET _Distance, f ET_Distan"' (r), is shown in Figure 6.
Imedian= m= Ce-~ 1. (151)
DISTANCE OF NEAREST Er_CIVILIZA TION
5.63·10-20
500 I000 I500 2000 2500 3000 3500 4000 4500 5000
ET_Distance from Earth (ligJ,t years)
Figure 6. This is the probability of finding the nearest ExtraTerrestrial Civilization at the distance r from
Earth (in light years) if the values assumed in the Drake Equation are those shown in Table I. The relevant
probability density function f ET_Distano:Cr) is given by equation (113). Its mode (peak abscissa) equals 1933
light years, but its mean value is higher since the curve has a high tail on the right: the mean value equals in
UNCLASSIFIED/fFQA QFFICiIPL. PP&i ODI! Y
52

[Page 53]
UNCLASSIFIED/ /fOR OFFI&IAk Wlii QPU,¥
fact 2670 light years. Finally, the standard deviation equals 1309 light years: THIS IS GOOD NEWS FOR
SETI, inasmuch as the nearest ET Civilization might lie at just 1 sigma =2670-1309 =1361 light years
from us.
From Figure 6, we see that the probability of
finding ExtraTenestrials is practically zero up to a
distance of about 500 light years from Earth. Then
it starts increasing with the increasing distance
from Earth, and reaches its maximum at
_fl_ ,?-
rrmde = rpeak = Ce 3 e 9 ~1933 light years. (152)
This is the MOST LIKELY VALUE of the
distance at which we can expect to fi11d the
nearest ExtraTerrestrial civilization.
It is not, however, the mean value of the
probability distribution (113) for .feT_Distana,(r) . In
fact, the probability density (] l 3) has an infinite
tail on the right, as clearly shown in Figure 6, and
hence its mean value must be higher than its peak
value. As given by ( 119), its mean value is
_!!_ 0"2
r,11ea11 l'alue =Ce 3 e 18 ~ 2670 light years. (153)
This is the MEAN (value of the) DISTANCE
at which we can expect to find ExtraTerrestrials.
After having found the above two distances (1933
and 2670 light years, respectively), the next natural
question that arises is: "what is the range, forth and
back around the mean value of the distance, within
which we can expect to find ExtraTenestrials with
"the highest hopes ?," The answer to this question
is given by the notion of standard deviation, that
we already found to be given by (123)
_fl_ 0"2 ~
(TET_Dislana, = Ce 3 e 18 Ve9 - 1 ~1309 light years.
... (154)
More precisely, this is the so called I-sigma
(distance) level. Probability theory then shows that
the nearest ExtraTenestrial civilization is expected
to be located within this range, i.e. within the two
distances of (2670-1309) = 1361 light years and
(2670+ 1309) = 3979 light years, with probability
given by the integral of fET_Distana, (r) taken in
between these two lower and upper limits, that is:
i
39791ightyears
/ET Distana,(r)dr~0.75 = 75% (155) 136 llightyears -
In plain words: with 75% probability, the nearest
ExtraTerrestrial civilization is located in between
the distances of 1361 and 3979 light years from us,
having assumed the input values to the Drake
Equation given by Table 1. If we change those
input values, then all the numbers change again.
9. THE "DATA ENRICHMENT
PRINCIPLE" AS THE BEST CL T
CONSEQUENCE UPON THE
STATISTICAL DRAKE EQUATION
(ANY NUMBER OF FACTORS
ALLOWED)
As a fitting climax to all the statistical
equations developed so far, let us now state our
"DATA ENRICHMENT PRINCIPLE," It simply states that
"The Higher the Number of Factors in the
Statistical Drake equation, The Better,"
Put in this simple way, it simply looks like a
new way of saying that the CL T lets the random
variable Y approach the nonnal distribution when
the number of terms in the sum (4) approaches
infinity. And this is the case, indeed. However, our
"Data Enrichment Principle" has more profound
methodological consequences that we cannot
explain now, but hope to describe more precisely
in one or more coming papers.
CONCLUSIONS
We have sought to extend the classical Drake
equation to let it encompass Statistics and
Probability.
This approach appears to pave the way to
future, more profound investigations intended not
only to associate "enor bars" to each factor in the
Drake equation, but especially to increase the
number of factors themselves. In fact, this seems to
be the only way to incorporate into the Drake
UNCLASSIFIED/ ffOR OFFI&IAk Wlii QPII.¥
53

[Page 54]
UNCLASSIFIED/ /FO R OFFIEil.t.k W&i Q~lls¥
equation more and more new scientific information
as soon as it becomes available. In the long run,
the Statistical Drake equation might just become a
huge computer code, growing up in size and
especially in the depth of the scientific information
it contained. It would thus be Humanity's fast
"Encyclopaedia Galactica,"
Unfortunately, to extend the Drake equation to
Statistics, it was necessary to use a mathematical
apparatus that is more sophisticated than just the
simple product of seven numbers.
When this author had the honour and privilege
to present his results at the SETI Institute on April
lJlh, 2008, in front of an audjence also including
Professor Frank Drake, he felt he had to add these
words: " My apologies, Frank, for disrupting the
beautiful simplicity of your equation,"
ACKNOWLEDGEMENTS
The author is grateful to Drs. Jill Tarter, Paul
Davies, Seth Shostak, Doug Vakoch, Tom Pierson,
Carol Oliver, Paul Shuch and Kathryn Denning for
attending his first presentation ever about these
topics at the "Beyond" Center of the University of
Arizona at Phoenix on February 8th , 2008. He also
would like to thank Dan Werthi.mer and rus School
of SETI young experts for keeping alive the
interplay between experimental and theoretical
SETI. But the greatest "thanks" goes of course to
the Teacher to all of us: Professor Frank D. Drake,
whose equation opened a new way of thinking
about the past and the future of Human in the
Galaxy.
REFERE CES
[I] http://en.wikipedia.org/wiki/Drake equation
[2] http://en.wikipedia.org/wiki/SETI
[3] http://en.wikipedia.org/wiki/ Astrobiology
[4] http://en.wikipedia.org/wiki/Frank Drake
l5J Athanasios Papoulis and S. Unnikrishna Pillai,
"Probability, Random Variables and Stochastic
Processes", Fourth Edition, Tata McGraw-Hill,
ew Delhi, 2002, ISBN 0-07-048658-l.
[6) http://en.wikipedia.org/wiki/Gamma distribution
[7]
http://en.wikipedia.org/wiki/Central limit theore
ill
[8] http://en.wikipedia.org/wiki/Cumulants
(9) http://en.wikipedia.org/wiki/Median
[ I0]Jeffrey Bennett and Seth Shostak, "Life in the
Universe", Second Edition, Pearson - Addison￾Wesley, San Francisco, 2007, ISBN 0-8053-
4753-4. See in particular page 404.
UNCLASSIFIED/ /FOR 8FFI&l.t.k Wii ,>DIis¥
54

[Page 55]
UNCLASSIFIED/ /FOR OFFIEil.t.k W&i Q~lls¥
References
[1] Benford, Gregory, Jim and Dominic, "Cost Optimized Interstellar Beacons: SETI",
arXiv.org web site (22 Oct. 2008).
[2] Carl Sagan, "Cosmos", Random House, New York, 1983. See in particular the pages
298-302.
[3] Bennet, Jeffrey, and Shostak, Seth, "Life in the Universe", second edition, Pearson -
Addison Wesley, San Francisco, 2007. See in particular page 404.
[4] C. Maccone, "The Statistical Drake Equation", paper #IAC-08-A4.1.4 presented on
October 1st, 2008, at the 59th International Astronautical Congress (IAC) held in
Glasgow, Scotland, UK, September 29th thru October 3rd, 2008.
UNCLASSIFIED/ /FOR OFFIEil.t.k W&i QNls¥
55
