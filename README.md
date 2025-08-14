IConFuzz Artifact
========

[IConFuzz](https://github.com/infosec-sogang/IConFuzz) is a grey-box fuzzer for
Ethereum smart contracts. This repository contains artifacts for the
experiments in our paper.

# Structure

We run all our experiments in a dockerized environment. In
[docker-setup](./docker-setup), we provide various files required to build the
docker image. The [benchmarks](./benchmarks) directory contains benchmarks we
used for the experiments. In [scripts](./scripts), you can find scripts to run
the experiments and analyze their results.

# Setup

We assume that your system has Docker installed. Also, you should be able to run
the `docker` command without `sudo`. The following command will build the
docker image name 'iconfuzz-artifact', using our [Dockerfile](./Dockerfile).

```
$ ./build.sh
```

Next, check the `MAX_INSTANCE_NUM` configuration parameter in
[scripts/run\_experiment.py](./scripts/run_experiment.py) script, which decides
the number of containers to run in parallel.  Currently, this parameter is set
to 60. Make sure that this parameter value is lower than the number of cores in
your machine.

# Comparison between IConFuzz and other tools

You can use the following scripts to reproduce the experiment in our paper,
which compares IConFuzz against other testing tools.

```
$ ./scripts/test_ELSC_compare.sh 5
$ ./scripts/test_IO_compare.sh 5
```

Then, you will get the raw data under `output/result-ELSC-compare` and
`output/result-IO-compare`.

```
$ ls output/result-IO-compare/
IConFuzz smartian SmarTest
$ ls output/result-ELSC-compare/
IConFuzz smartian SmarTest rlf
```

To obtain the results in our paper, you may refer to the following commands.
```
$ python scripts/plot_IO_cve.py output/result-IO-compare/IConFuzz/*
$ python scripts/median_IO_cve.py output/result-IO-compare/IConFuzz/*

$ python scripts/plot_ELSC_bug.py output/result-ELSC-compare/IConFuzz/*
$ python scripts/median_ELSC_bug.py output/result-ELSC-compare/IConFuzz/*
```

# Hyperparameter (random mutation rate) experiment
You can use the following script to reproduce the experiment in our paper,
which analyzes the impact of random mutation rate on IConFuzz.
```
$ ./scripts/test_parameter.sh
```

Then, you will get the raw data under `output/result-parameter`.
```
$ ls output/result-parameter/
B-IO_5 B-IO_10 B-IO_20 B-IO_40 B-ELSC_5 B-ELSС_10 B-ELSС_20 B-ELSС_40
```

To obtain the results in our paper, you may refer to the following commands.
```
$ python scripts/median_IO_cve.py output/result-parameter/B-IO_5/*
$ python scripts/median_IO_cve.py output/result-parameter/B-IO_10/*
$ python scripts/median_IO_cve.py output/result-parameter/B-IO_20/*
$ python scripts/median_IO_cve.py output/result-parameter/B-IO_40/*

$ python scripts/median_ELSC_bug.py output/result-parameter/B-ELSC_5/*
$ python scripts/median_ELSC_bug.py output/result-parameter/B-ELSС_10/*
$ python scripts/median_ELSC_bug.py output/result-parameter/B-ELSС_20/*
$ python scripts/median_ELSC_bug.py output/result-parameter/B-ELSС_40/*
```

