# Third-party provenance and exclusions

## CAD tooling

The historical engineering files were produced with FreeCAD / Open CASCADE. Sixteen ISO 4762 screw representations were generated using [FreeCAD Fasteners Workbench](https://github.com/shaise/FreeCAD_FastenersWB), commit `79a06dc067b57ebc89532be835704eb2af5da96c` (ScrewMaker: Ulrich Brammer; workbench wrapper: Shai Seger and contributors).

The upstream workbench [declares GPLv2](https://github.com/shaise/FreeCAD_FastenersWB/blob/79a06dc067b57ebc89532be835704eb2af5da96c/LICENSE). Its program source, icons and distributions are **not bundled or relicensed as MIT here**. The native files contain generated shapes, module/class references and serialized parameter data, not a vendored workbench implementation. Project licence grants are limited to project-controlled design rights; use of a GPL tool does not itself establish that every generated output is GPL-licensed. See upstream terms for the tool. No general legal clearance opinion is made.

Other development plugins, workstation-specific validator implementations and detailed historical test reports are not redistributed. Tool references in the assembly documentation are attribution, not endorsement of this project by those developers.

## Purchased components and standards

Ensinger, igus, Lee Spring, Bossard, TE Connectivity and Outokumpu names identify proposed materials or publicly documented components. They remain their owners' names and marks. No manufacturer has certified this assembly through this publication. Availability, price, exact screw order codes and suitability require independent confirmation.

Spring envelopes, installed bush dimensions and terminal tongues are project-made simplified representations, **not downloaded manufacturer CAD**. They omit physical details and are not production models for those purchased parts.

The repository links to public catalogue/standards sources in [sources.json](manufacturing/sources.json) and the assembly manual. It does not distribute supplier PDF originals, proprietary CAD downloads, ISO/SEMI standard texts, private quotations, supplier contact lists or internal budgets. Dimensions and factual source references do not grant rights to copy the linked documents.
