# icom-modeling

This project contains a framework for running parflow against the icom domain

# Prepping a run
To prep a run (create all the parflow inputs in the right place) execute

```prep_run.sh -n YOUR_RUN_NAME```

This will create a folder named appropriately under the runs directory with necessary input files. The actual parflow run name will be icom.

Behind the scenes generate_run_files is doing all the heavy lifting, prep_run.sh only exists to work around some oddities in how parflow handles relative and absolute paths

# Executing a run on local
To execute a run navigate into the directory of the run and run
```parflow icom```
If you prepped the run inside a docker container you will also need to execcute it inside a docker container opened at the project root.

Note that you might need to edit generate_run_file.py first to use less cores, which might also involve redistributing the forcing files

# Executing a run on CORI
To submit a run on cori navigate into the run folder and submit one of the project batch jobs e.g.
```sbatch ../../run_debug_job```


# Redistributing forcing data
You can use distribute_forcing.py to do this. Right now it is very much a work in progress though and will only redistribute the first forcing file