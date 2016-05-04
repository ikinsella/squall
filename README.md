# Motivation

Functional Magnetic Resonance Imaging (fMRI) provides a means to record neural activity in human subjects, providing a means for basic and medical science researchers to investigate new and exciting avenues. However, the complexity of this data poses many challenges to meaningful interpretation, thereby motivating the development of novel analysis techniques that leverage statistical machine learning methods. Unfortunately, there exists a high degree of variability in how these types of analyses are conducted across the neuroimaging literature, and the interpretation of fMRI data can vary significantly depending on which analysis methods are used. With a vast array of machine learning tools to choose from and few direct comparisons between them, there does not exist a consensus on how or when to use a particular method. Consequently, these factors make it difficult to compare results across different studies, assess competing models of neural activity, and reproduce previous findings. 

Our clients, seek to address these problems by carrying out large scale studies, but the amount of computational power needed to do so makes single-workstation and single-cluster workflows infeasible. To overcome these limitations, the UW-Madison Center for High-Throughput Computing (CHTC) has provided access to large pools of distributed computing resources, but the process of maintaining workflows on these resources is often cumbersome and restrictively time consuming. As a result, the bottleneck in the research pipeline had shifted from the availability of computing resources to the user’s ability to conduct computational workflows.

# What is Squall? 

In response to the aforementioned obstacles, we have designed an application, Squall, to facilitate the use of distributed computing resources for fMRI analysis. The system consists of a ‘front-end’ web application to gather user input, ‘back-end’ web server to automate the process of deploying workflows, and a database to organize and facilitate examination of the results returned by completed analyses. As a whole, Squall alleviates the previously mentioned bottlenecks by providing a means to manage more scalable workflows on distributed computing resources.

The web application consists of a number of forms used to collect the information needed to run computation on [HTCondor](https://github.com/ikinsella/squall/wiki/Glossary#htcondor) [execute nodes](https://github.com/ikinsella/squall/wiki/Glossary#execute-nodes) such as URLs to [code](https://github.com/ikinsella/squall/wiki/Glossary#implementation) and [data](https://github.com/ikinsella/squall/wiki/Glossary#data-set), executables, and system requirements (memory, disk, space, ect.). Additionally, the application collects metadata used to organize the results returned by these computations. Squall uses this information to generate a file structures consisting of [DAGs](https://github.com/ikinsella/squall/wiki/Glossary#dag), [Submit Files](https://github.com/ikinsella/squall/wiki/Glossary#submit-file), [Wrapper Scripts](https://github.com/ikinsella/squall/wiki/Glossary#wrapper-script), and [Pre/Post Scripts](https://github.com/ikinsella/squall/wiki/Glossary#pre-&-post-scripts) that are used to deploy [Parameter Sweeps](https://github.com/ikinsella/squall/wiki/Glossary#workflow) using [HTCondor](https://github.com/ikinsella/squall/wiki/Glossary#htcondor). The results from completed [Parameter Sweeps](https://github.com/ikinsella/squall/wiki/Glossary#workflow) are returned to the web application for organization and storage. These results (and the meta-data associated with them) are collected in [MongoDB](https://github.com/ikinsella/squall/wiki/Glossary#mongodb) (a document based database) where they are easily accesible to the user for exploration, analysis, and visualization via any number of extensions.

# Use Case

While Squall was inspired by challenges faced in fMRI analysis, there is nothing domain specific about it. More generally, Squall is a web application which can be used facilitate use of the [HTCondor](https://github.com/ikinsella/squall/wiki/Glossary#htcondor) job scheduler for computationally intensive [workflows](https://github.com/ikinsella/squall/wiki/Glossary#workflow) that fit a particular formula (presented below). As a result, it can be applied by researchers in countless other domains employing similarly structured computational workflows (Biomedical Informatics, Optimization, ect.).  

1. Sweep: This phase consists of the deployment of hundred or thousands of [Jobs](https://github.com/ikinsella/squall/wiki/Glossary#job) of the same computation (same [Implementation](https://github.com/ikinsella/squall/wiki/Glossary#implementation) run with the same [Data Set](https://github.com/ikinsella/squall/wiki/Glossary#data-set)), each which are each fed a different permutation of [Parameters](https://github.com/ikinsella/squall/wiki/Glossary#parameter). This style of mass deployment allows the researcher to explore vast spaces of tuning [Parameters](https://github.com/ikinsella/squall/wiki/Glossary#parameter) in order to find an optimal set, perform repeated simulations with different random seeds, or even perform model validation procedures such as [Cross Validation](https://en.wikipedia.org/wiki/Cross-validation_(statistics)) or [Permutation Testing](https://en.wikipedia.org/wiki/Resampling_(statistics)).

2. Summarize: In this phase, the researcher must aggregate and explore the results of the [Parameter](https://github.com/ikinsella/squall/wiki/Glossary#parameter) Sweep performed in step 1 to determine what the next steps are (ie. run more simulations, explore a different [Parameter](https://github.com/ikinsella/squall/wiki/Glossary#parameter) spaces, fit a final model with the set of [Parameters](https://github.com/ikinsella/squall/wiki/Glossary#) chosen via Cross Validation, or calculate summary statistics of the results to determine an effect size).

3. Final Fit: The information gained in step 2 is acted upon which may require additional computation or analysis.

![](https://github.com/ikinsella/squall/blob/master/images/WorkflowDiagram.png)

**For more information on the [HTCondor](https://research.cs.wisc.edu/htcondor/) job scheduler and obtaining access to [High Throughput Computing](https://en.wikipedia.org/wiki/High-throughput_computing) resources that can support the above workflow, please see the [Center for High Throughput Computing](http://chtc.cs.wisc.edu/) (CHTC) and [Open Science Grid](http://www.opensciencegrid.org/) (OSG) websites.**
