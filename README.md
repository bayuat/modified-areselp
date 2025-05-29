A modified version of MATLAB packages for the original version of the ice layer annotation technique that was published in "Xiong S, Muller JP, Carretero RC. A new method for automatically tracing englacial layers from MCoRDS data in NW Greenland. Remote Sensing. 2017 Dec 27;10(1):43."
Several modifications include the following main aspects:
- Peak detection strategy
- Seed points selection using image processing techniques
- New validation metrics

MLT folder contains the main implementation (in MATLAB) of the MorphoLayerTrace (MLT) algorithm, while layer_validation folder contains the implementation of new validation approach such as Multi-Frame Layer Consistency (𝑀𝐹𝐿𝐶) metric.

To run MLT, please follow the steps provided by the original ARESELP repo.
To run MFLC in the find_unique_layers_across_multiple_radargrams.ipynb, please [download the annotation data](https://drive.google.com/drive/folders/1Q5u3kZcc0PDiepq4_ifrYfwUzrMYDjmg?usp=sharing) and copy them to the respected folders. 
All packages in the NDH_Tools folder are written by Nick Holschuh and are publicly available [here](https://github.com/nholschuh/NDH_PythonTools).  
Expert annotation data is provided by Nick Holschuh and Joseph A MacGregor.

Please cite the following paper if you find this repo useful:
Tama, Bayu Adhi, Sanjay Purushotham, and Vandana Janeja. "MorphoLayerTrace (MLT): A Modified Automated Radio-Echo Sounding Englacial Layer-tracing Algorithm for Englacial Layer Annotation in Ice Penetrating Radar Data." In _Proceedings of the 40th ACM/SIGAPP Symposium on Applied Computing, pp. 605-612. 2025_.
