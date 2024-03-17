# Directory names
OUT_DIR = "out" # directory where all outputs are saved to
PLOT_DIR = 'plots' # directory where all plotting outputs are saved to
# Misc
DISTRIB_BOUNDS = [1, 2, 5, 10, 50, float('inf')] # upper bounds used to group frequency distribution
LAMBDA_TOKEN = "$$Lambda$"
REFLECT_TOKEN = "jdk.internal.reflect.Generated"

# Method data keys
ME_KEY_ID = "id" # unique id for each method based on signature
ME_KEY_CLASS_NAME = "className" # name of the class a method belongs to
ME_KEY_METHOD_NAME = "methodName" # name of the method
ME_KEY_METHOD_DESCRIPTOR = "methodDescriptor" # the input type and return type of the method
ME_KEY_METRICS = "metrics" # metrics list

# Stats data keys
STATS_KEY_ROOTS = "roots" 
STATS_KEY_EXEC_TYPES = "execTypeDistrib" # execution type distribution

STATS_KEY_ALL_METHODS = "allMethods" # list of ALL methods executed during program run (includes lambda and reflection generated)
STATS_KEY_ALL_METHOD_COUNT = "allMethodCount" # count of ALL methods executed during program run
STATS_KEY_ALL_METHOD_FREQ_SUM = "allMethodFreqSum" # sum of frequencies for ALL methods executed during program run
STATS_KEY_ALL_METHOD_FREQ_DISTRIB = "allMethodFreqDistrib" # distribution of frequencies (based on upper bound buckets) for ALL methods

STATS_KEY_DEFAULT_METHODS = "defaultMethods" # list of default methods executed during program run (excludes lambda and reflection generated) 
STATS_KEY_DEFAULT_METHOD_COUNT = "defaultMethodCount" # count of unique default methods executed during program run
STATS_KEY_DEFAULT_METHODS_FREQ_SUM = "defaultMethodFreqSum" # sum of frequencies for all default methods executed during program run
STATS_KEY_DEFAULT_METHOD_FREQ_DISTRIB = "defaultMethodFreqDistrib" # distribution of frequencies (based on upper bound buckets) for default methods

STATS_KEY_LAMBDA_METHODS = "lambdaMethods"  # list of lambda methods executed during program run
STATS_KEY_LAMBDA_METHOD_COUNT = "lambdaMethodCount" # count of unique lambda methods executed during program run
STATS_KEY_LAMBDA_MEHTOD_FREQ_SUM = "lambdaMethodFreqSum" # sum of frequencies for all lambda methods executed during program run
STATS_KEY_LAMBDA_METHOD_FREQ_DISTRIB = "lambdaMethodFreqDistrib" # distribution of frequencies (based on upper bound buckets) for lambda methods

STATS_KEY_REFLECT_METHODS = "reflectionMethods" # list of reflection generated methods executed during program run
STATS_KEY_REFLECT_METHOD_COUNT = "relectionMethodCount" # count of unique reflection generated methods executed during program run
STATS_KEY_REFLECT_METHOD_FREQ_SUM = "reflectMethodFreqSum" # sum of frequencies for all refleciton genereated methods during program run
STATS_KEY_REFLECT_METHOD_FREQ_DISTRIB = "reflectMethodFreqDistrib" # distribution of frequencies (based on upper bound buckets) for reflection generated methods

STATS_KEY_ALL_INVOKES = "allInvokes" # list of caller-callee relationships
STATS_KEY_ALL_INVOKE_COUNT = "allInvokeCount" # count of unique invocations during program run
STATS_KEY_ALL_INVOKE_FREQ_SUM = "allInovkeFreqSum" # sum of frequencies for ALL invocations during program run
STATS_KEY_ALL_INVOKE_FREQ_DISTRIB = "allInvokeFreqDistrib" # distribution of frequencies (based on upper bound buckets) for invocations

STATS_KEY_DEFAULT_INVOKES = "defaultInvokes" # list of default invocations
STATS_KEY_DEFAULT_INVOKE_COUNT = "defaultInvokeCount" # count of unique default invocations during program run
STATS_KEY_DEFAULT_INVOKE_FREQ_SUM = "defaultInovkeFreqSum" # sum of frequencies for default invocations during program run
STATS_KEY_DEFAULT_INVOKE_FREQ_DISTRIB = "defaultInvokeFreqDistrib" # distribution of frequencies (based on upper bound buckets) for default invocations


# Diff data keys
DIFF_KEY_FILE_NAME_1 = "file1" # file name of first diff file
DIFF_KEY_FILE_NAME_2 = "file2" # file name of second diff file
DIFF_KEY_SHARED_METHODS = "sharedMethods" # list of shared methods between program runs
DIFF_KEY_SHARED_METHOD_COUNT = "sharedMethodCount" # count of shared methods (1 method => 1 count) between program runs

DIFF_KEY_F1_ONLY_DEFAULT_METHODS = "f1OnlyDefaultMethods" # list of methods ONLY found in file1
DIFF_KEY_F2_ONLY_DEFAULT_METHODS = "f2OnlyDefaultMethods" # list of methods ONLY found in file2
DIFF_KEY_F1_ONLY_DEFAULT_METHOD_COUNT = "f1OnlyDefaultMethodCount" # count of methods ONLY found in file1
DIFF_KEY_F2_ONLY_DEFAULT_METHOD_COUNT = "f2OnlyDefaultMethodCount" # count of methods ONLY found in file2
DIFF_KEY_F1_ONLY_DEFAULT_METHOD_FREQ_SUM = "f1OnlyDefualtMethodFreqSum" # sum of frequencies for methods ONLY found in file1
DIFF_KEY_F2_ONLY_DEFAULT_METHOD_FREQ_SUM = "f2OnlyDefaultMethodFreqSum" # sum of frequencies for methods ONLY found in file2
DIFF_KEY_F1_ALL_METHOD_COUNT = "f1AllMethodCount" # count of ALL methods found in file1
DIFF_KEY_F2_ALL_METHOD_COUNT = "f2AllMethodCount" # count of ALL methods found in file2
DIFF_KEY_F1_ALL_METHOD_FREQ_SUM = "f1AllMethodFreqSum" # sum of frequencies for ALL methods found in file1
DIFF_KEY_F2_ALL_METHOD_FREQ_SUM = "f2AllMethodFreqSum" # sum of frequencies for ALL methods found in file2
DIFF_KEY_F1_ONLY_DEFAULT_METHOD_FREQ_DISTRIB = "f1OnlyDefaultMethodFreqDistrib" # distribution of frequencies (based on upper bound buckets) for methods ONLY found in file1
DIFF_KEY_F2_ONLY_DEFAULT_METHOD_FREQ_DISTRIB = "f2OnlyDefaultMethodFreqDistrib" # distribution of frequencies (based on upper bound buckets) for methods ONLY found in file1

DIFF_KEY_F1_ONLY_LAMBDA_METHODS = "f1OnlyLambdaMethods" # list of lambda methods ONLY found in file1
DIFF_KEY_F1_ONLY_LAMBDA_METHOD_COUNT = "f1OnlyLambdaMethodCount" # count of lambda methods ONLY found in file1
DIFF_KEY_F1_ONLY_LAMBDA_METHOD_FREQ_SUM = "f1OnlyLambdaMethodFreqSum" # sum of frequencies for lambda methods ONLY found in file1
DIFF_KEY_F2_ONLY_LAMBDA_METHODS = "f2OnlyLambdaMethods" # list of lambda methods ONLY found in file2
DIFF_KEY_F2_ONLY_LAMBDA_METHOD_COUNT = "f2OnlyLambdaMethodCount" # count of lambda methods ONLY found in file2
DIFF_KEY_F2_ONLY_LAMBDA_METHOD_FREQ_SUM = "f2OnlyLambdaMethodFreqSum" # sum of frequencies for lambda methods ONLY found in file2

DIFF_KEY_F1_ONLY_REFLECT_METHODS = "f1OnlyReflectMethods" # list of reflection generated methods ONLY found in file1
DIFF_KEY_F1_ONLY_REFLECT_METHOD_COUNT = "f1OnlyReflectMethodCount" # count of reflection generated methods ONLY found in file1
DIFF_KEY_F1_ONLY_REFLECT_METHOD_FREQ_SUM = "f1OnlyReflectMethodFreqSum" # sum of frequencies for reflection generated methods ONLY found in file1
DIFF_KEY_F2_ONLY_REFLECT_METHODS = "f2OnlyReflectMethods" # list of reflection generated methods ONLY found in file2
DIFF_KEY_F2_ONLY_REFLECT_METHOD_COUNT = "f2OnlyReflectMethodCount" # count of reflection generated methods ONLY found in file2
DIFF_KEY_F2_ONLY_REFLECT_METHOD_FREQ_SUM = "f2OnlyReflectMethodFreqSum" # sum of frequencies for reflection generated methods ONLY found in file2


DIFF_KEY_SHARED_INVOKES = "sharedInvokes" # list of shared invocations between program runs
DIFF_KEY_SHARED_INVOKE_COUNT = "sharedInvokeCount" # count of shared invocations (1 invocation => 1 count) between program runs 
DIFF_KEY_F1_ONLY_INVOKES = "f1OnlyInvokes" # list of invocations ONLY found in file1
DIFF_KEY_F2_ONLY_INVOKES = "f2OnlyInvokes" # list of invocations ONLY found in file2
DIFF_KEY_F1_ONLY_INVOKE_COUNT = "f1OnlyInvokeCount" # count of invocations ONLY found in file1
DIFF_KEY_F2_ONLY_INVOKE_COUNT = "f2OnlyInvokeCount" # count of invocations ONLY found in file2
DIFF_KEY_F1_ONLY_INVOKE_FREQ_SUM = "f1OnlyInvokeFreqSum" # sum of frequencies for invocations ONLY found in file1
DIFF_KEY_F2_ONLY_INVOKE_FREQ_SUM = "f2OnlyInvokeFreqSum" # sum of frequencies for invocations ONLY found in file2
DIFF_KEY_F1_INVOKE_COUNT = "f1InvokeCount" # count of ALL invocations found in file1
DIFF_KEY_F2_INVOKE_COUNT = "f2InvokeCount" # count of ALL invocations found in file2
DIFF_KEY_F1_INVOKE_FREQ_SUM = "f1InvokeFreqSum" # sum of frequencies for ALL invocations found in file1
DIFF_KEY_F2_INVOKE_FREQ_SUM = "f2InvokeFreqSum" # sum of frequencies for ALL invocations found in file2
DIFF_KEY_F1_ONLY_INVOKE_FREQ_DISTRIB = "f1OnlyInvokeCountDistrib" # distribution of frequencies (based on upper bound buckets) for invocations ONLY found in file1
DIFF_KEY_F2_ONLY_INVOKE_FREQ_DISTRIB = "f2OnlyInvokeCountDistrib" # distribution of frequencies (based on upper bound buckets) for invocations ONLY found in file1

DIFF_KEY_F1_ONLY_LAMBDA_INVOKES = "f1OnlyLambdaInvokes" # list of lambda-related invocations ONLY found in file1
DIFF_KEY_F2_ONLY_LAMBDA_INVOKES = "f2OnlyLambdaInvokes" # list of lambda-related invocations ONLY found in file2
DIFF_KEY_F1_ONLY_LAMBDA_INVOKE_COUNT = "f1OnlyLambdaInvokeCount" # count of lambda-related invocations ONLY found in file1
DIFF_KEY_F2_ONLY_LAMBDA_INVOKE_COUNT = "f2OnlyLambdaInvokeCount" # count of lambda-related invocations ONLY found in file2
DIFF_KEY_F1_ONLY_LAMBDA_INVOKE_FREQ_SUM = "f1OnlyLambdaInvokeFreqSum" # sum of frequencies for lambda-related invocations ONLY found in file1
DIFF_KEY_F2_ONLY_LAMBDA_INVOKE_FREQ_SUM = "f2OnlyLambdaInvokeFreqSum" # sum of frequencies for lambda-related invocations ONLY found in file2

DIFF_KEY_F1_ONLY_REFLECT_INVOKES = "f1OnlyReflectInvokes" # list of reflection generated invocations ONLY found in file1
DIFF_KEY_F2_ONLY_REFLECT_INVOKES = "f2OnlyReflectInvokes" # list of reflection generated invocations ONLY found in file2
DIFF_KEY_F1_ONLY_REFLECT_INVOKE_COUNT = "f1OnlyReflectInvokeCount" # count of reflection generated invocations ONLY found in file1
DIFF_KEY_F2_ONLY_REFLECT_INVOKE_COUNT = "f2OnlyReflectInvokeCount" # count of reflection generated invocations ONLY found in file2
DIFF_KEY_F1_ONLY_REFLECT_INVOKE_FREQ_SUM = "f1OnlyReflectInvokeFreqSum" # sum of frequencies for reflection generated invocations ONLY found in file1
DIFF_KEY_F2_ONLY_REFLECT_INVOKE_FREQ_SUM = "f2OnlyReflectInvokeFreqSum" # sum of frequencies for reflection generated invocations ONLY found in file2