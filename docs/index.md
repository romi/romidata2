


### Tasks output files


Conventions:

* The log file of a task can be obtained using zone.get_files_by_source(task.short_name, task.id, "log")

* The list of output files of a task indicate the short names of the output files. The IFile objects can be obtained using zone.get_files_by_source(task.short_name, task.id, output_files[i])


