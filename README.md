A modified version of MATLAB packages for the original version of the ice layer annotation technique that was published in "Xiong S, Muller JP, Carretero RC. A new method for automatically tracing englacial layers from MCoRDS data in NW Greenland. Remote Sensing. 2017 Dec 27;10(1):43."
Several modifications include the following main aspects:
- Peak detection strategy
- Seed points selection using image processing techniques
- New validation metrics

MLT folder contains the main implementation (in MATLAB) of the MorphoLayerTrace (MLT) algorithm, while layer_validation folder contains the implementation of new validation approach such as Multi-Frame Layer Consistency (𝑀𝐹𝐿𝐶) metric.

Please cite the following paper if you find this repo useful:
Tama, Bayu Adhi, Sanjay Purushotham, and Vandana Janeja. "MorphoLayerTrace (MLT): A Modified Automated Radio-Echo Sounding Englacial Layer-tracing Algorithm for Englacial Layer Annotation in Ice Penetrating Radar Data." In _Proceedings of the 40th ACM/SIGAPP Symposium on Applied Computing, pp. 605-612. 2025_.
