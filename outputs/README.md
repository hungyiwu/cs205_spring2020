Property output files from step 6 and to be consumed by step 7.

We now have both Spark and non-Spark based post-processing.

The non-Spark post-processing is minimal, as it is only meant to serve as a development/exploration tool. It is object-oriented and located in the file "postprocessing.py" and demonstrated in the file "postprocessing_tests.py".

The Spark post-processing is in "postprocessing_spark.py" and demonstrated in "postprocessing_spark_tests.py". It tries to make the most out of Spark with small files (not an easy task) by combining all of the small files to be processed (either bands or dos, depending) into one larger RDD.
