# Nordhavn Terminals — Operations Note

Nordhavn Terminals operates container terminals in Aarhus, Denmark and Rotterdam,
Netherlands. It is the connective tissue in this corpus: both Meridian Robotics and
Kestrel Automation count Nordhavn as a partner, which is why questions about the
sector are hard to answer from any single document.

## People

Lars Andersen is the Chief Operating Officer at Nordhavn Terminals. He signed off on
the Atlas pilot in Aarhus and on the Harbourmaster rollout in Rotterdam.

Mette Sørensen is Head of Automation. She reports on both vendor relationships and
has publicly described the combination of Meridian hardware and Kestrel software as
the terminal's target architecture.

## Deployments

The Aarhus terminal runs Atlas Yard Mover units on the container yard, scheduled by
Harbourmaster. This is the only site where both vendors' systems run together.

The Rotterdam terminal runs Harbourmaster against third-party equipment. Nordhavn
has not committed to Meridian hardware there.

## Technology notes

Nordhavn's internal telemetry platform, **Fjord**, aggregates equipment data from
both vendors. Fjord uses an event streaming architecture and feeds a predictive
maintenance model that flags crane faults before they cause downtime.
