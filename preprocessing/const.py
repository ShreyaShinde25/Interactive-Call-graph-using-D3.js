# Directory names
OUT_DIR = "out" # directory where all outputs are saved to
PLOT_DIR = 'plots' # directory where all plotting outputs are saved to
# Misc
DISTRIB_BOUNDS = (1, 2, 5, 10, 20, 50, 100) # upper bounds used to group frequency distribution

# Method data keys
ME_KEY_ID = "id" # unique id for each method based on signature
ME_KEY_CLASS_NAME = "className" # name of the class a method belongs to
ME_KEY_METHOD_NAME = "methodName" # name of the method
ME_KEY_METHOD_DESCRIPTOR = "methodDescriptor" # the input type and return type of the method
ME_KEY_METRICS = "metrics" # metrics list

# Stats data keys
STATS_KEY_METHODS = "methods" # list of ALL methods executed during program run (includes lambda and reflection generated)
STATS_KEY_EXEC_TYPES = "execTypeDistrib" # execution type distribution
STATS_KEY_INVOKES = "invokes" # list of caller-callee relationships
STATS_KEY_ROOTS = "roots" 
STATS_KEY_LAMBDAS = "lambdaMethods"  # list of lambda methods executed during program run
STATS_KEY_REFLECT_METHODS = "reflectionMethods" # list of reflection generated methods executed during program run
STATS_KEY_LAMBDA_COUNT = "lambdaMethodCount" # count of unique lambda methods executed during program run
STATS_KEY_REFLECT_METHOD_COUNT = "relectionMethodCount" # count of unique reflection generated methods executed during program run
STATS_KEY_LAMBDA_FREQ_COUNT = "lambdaMethodFreqCount" # count of frequencies for all lambda methods executed during program run
STATS_KEY_REFLECT_METHOD_FREQ_COUNT = "reflectMethodFreqCount" # count of frequencies for all refleciton genereated methods during program run
STATS_KEY_METHOD_COUNT = "methodCount" # count of methods executed during program run
STATS_KEY_METHOD_FREQ_COUNT = "methodFreqCount" # count of frequencies for ALL methods executed during program run
STATS_KEY_INVOKE_COUNT = "invokeCount" # count of unique invocations during program run
STATS_KEY_INVOKE_FREQ_COUNT = "inovkeFreqCount" # count of frequencies for ALL invocations during program run


# Diff data keys
DIFF_KEY_FILE_NAME_1 = "file1" # file name of first diff file
DIFF_KEY_FILE_NAME_2 = "file2" # file name of second diff file
DIFF_KEY_SHARED_METHODS = "sharedMethods" # list of shared methods between program runs
DIFF_KEY_SHARED_METHOD_COUNT = "sharedMethodCount" # count of shared methods (1 method => 1 count) between program runs

DIFF_KEY_F1_ONLY_METHODS = "f1OnlyMethods" # list of methods ONLY found in file1
DIFF_KEY_F2_ONLY_METHODS = "f2OnlyMethods" # list of methods ONLY found in file2
DIFF_KEY_F1_ONLY_METHOD_COUNT = "f1OnlyMethodCount" # count of methods ONLY found in file1
DIFF_KEY_F2_ONLY_METHOD_COUNT = "f2OnlyMethodCount" # count of methods ONLY found in file2
DIFF_KEY_F1_ONLY_METHOD_FREQ_COUNT = "f1OnlyMethodFreqCount" # count of frequencies for methods ONLY found in file1
DIFF_KEY_F2_ONLY_METHOD_FREQ_COUNT = "f2OnlyMethodFreqCount" # count of frequencies for methods ONLY found in file2
DIFF_KEY_F1_METHOD_COUNT = "f1MethodCount" # count of ALL methods found in file1
DIFF_KEY_F2_METHOD_COUNT = "f2MethodCount" # count of ALL methods found in file2
DIFF_KEY_F1_METHOD_FREQ_COUNT = "f1MethodFreqCount" # count of frequencies for ALL methods found in file1
DIFF_KEY_F2_METHOD_FREQ_COUNT = "f2MethodFreqCount" # count of frequencies for ALL methods found in file2
DIFF_KEY_F1_ONLY_METHOD_FREQ_DISTRIB = "f1OnlyMethodFreqDistrib" # distribution of frequencies (based on upper bound buckets) for methods ONLY found in file1
DIFF_KEY_F2_ONLY_METHOD_FREQ_DISTRIB = "f2OnlyMethodFreqDistrib" # distribution of frequencies (based on upper bound buckets) for methods ONLY found in file1

DIFF_KEY_F1_ONLY_LAMBDA_METHODS = "f1OnlyLambdaMethods" # list of lambda methods ONLY found in file1
DIFF_KEY_F1_ONLY_LAMBDA_METHOD_COUNT = "f1OnlyLambdaMethodCount" # count of lambda methods ONLY found in file1
DIFF_KEY_F1_ONLY_LAMBDA_METHOD_FREQ_COUNT = "f1OnlyLambdaMethodFreqCount" # count of frequencies for lambda methods ONLY found in file1
DIFF_KEY_F2_ONLY_LAMBDA_METHODS = "f2OnlyLambdaMethods" # list of lambda methods ONLY found in file2
DIFF_KEY_F2_ONLY_LAMBDA_METHOD_COUNT = "f2OnlyLambdaMethodCount" # count of lambda methods ONLY found in file2
DIFF_KEY_F2_ONLY_LAMBDA_METHOD_FREQ_COUNT = "f2OnlyLambdaMethodFreqCount" # count of frequencies for lambda methods ONLY found in file2

DIFF_KEY_F1_ONLY_REFLECT_METHODS = "f1OnlyReflectMethods" # list of reflection generated methods ONLY found in file1
DIFF_KEY_F1_ONLY_REFLECT_METHOD_COUNT = "f1OnlyReflectMethodCount" # count of reflection generated methods ONLY found in file1
DIFF_KEY_F1_ONLY_REFLECT_METHOD_FREQ_COUNT = "f1OnlyReflectMethodFreqCount" # count of frequencies for reflection generated methods ONLY found in file1
DIFF_KEY_F2_ONLY_REFLECT_METHODS = "f2OnlyReflectMethods" # list of reflection generated methods ONLY found in file2
DIFF_KEY_F2_ONLY_REFLECT_METHOD_COUNT = "f2OnlyReflectMethodCount" # count of reflection generated methods ONLY found in file2
DIFF_KEY_F2_ONLY_REFLECT_METHOD_FREQ_COUNT = "f2OnlyReflectMethodFreqCount" # count of frequencies for reflection generated methods ONLY found in file2


DIFF_KEY_SHARED_INVOKES = "sharedInvokes" # list of shared invocations between program runs
DIFF_KEY_SHARED_INVOKE_COUNT = "sharedInvokeCount" # count of shared invocations (1 invocation => 1 count) between program runs 
DIFF_KEY_F1_ONLY_INVOKES = "f1OnlyInvokes" # list of invocations ONLY found in file1
DIFF_KEY_F2_ONLY_INVOKES = "f2OnlyInvokes" # list of invocations ONLY found in file2
DIFF_KEY_F1_ONLY_INVOKE_COUNT = "f1OnlyInvokeCount" # count of invocations ONLY found in file1
DIFF_KEY_F2_ONLY_INVOKE_COUNT = "f2OnlyInvokeCount" # count of invocations ONLY found in file2
DIFF_KEY_F1_ONLY_INVOKE_FREQ_COUNT = "f1OnlyInvokeFreqCount" # count of frequencies for invocations ONLY found in file1
DIFF_KEY_F2_ONLY_INVOKE_FREQ_COUNT = "f2OnlyInvokeFreqCount" # count of frequencies for invocations ONLY found in file2
DIFF_KEY_F1_INVOKE_COUNT = "f1InvokeCount" # count of ALL invocations found in file1
DIFF_KEY_F2_INVOKE_COUNT = "f2InvokeCount" # count of ALL invocations found in file2
DIFF_KEY_F1_INVOKE_FREQ_COUNT = "f1InvokeFreqCount" # count of frequencies for ALL invocations found in file1
DIFF_KEY_F2_INVOKE_FREQ_COUNT = "f2InvokeFreqCount" # count of frequencies for ALL invocations found in file2
DIFF_KEY_F1_ONLY_INVOKE_FREQ_DISTRIB = "f1OnlyInvokeCountDistrib" # distribution of frequencies (based on upper bound buckets) for invocations ONLY found in file1
DIFF_KEY_F2_ONLY_INVOKE_FREQ_DISTRIB = "f2OnlyInvokeCountDistrib" # distribution of frequencies (based on upper bound buckets) for invocations ONLY found in file1


DIFF_KEY_F1_ONLY_LAMBDA_INVOKES = "f1OnlyLambdaInvokes" # list of lambda-related invocations ONLY found in file1
DIFF_KEY_F2_ONLY_LAMBDA_INVOKES = "f2OnlyLambdaInvokes" # list of lambda-related invocations ONLY found in file2
DIFF_KEY_F1_ONLY_LAMBDA_INVOKE_COUNT = "f1OnlyLambdaInvokeCount" # count of lambda-related invocations ONLY found in file1
DIFF_KEY_F2_ONLY_LAMBDA_INVOKE_COUNT = "f2OnlyLambdaInvokeCount" # count of lambda-related invocations ONLY found in file2
DIFF_KEY_F1_ONLY_LAMBDA_INVOKE_FREQ_COUNT = "f1OnlyLambdaInvokeFreqCount" # count of frequencies for lambda-related invocations ONLY found in file1
DIFF_KEY_F2_ONLY_LAMBDA_INVOKE_FREQ_COUNT = "f2OnlyLambdaInvokeFreqCount" # count of frequencies for lambda-related invocations ONLY found in file2

DIFF_KEY_F1_ONLY_REFLECT_INVOKES = "f1OnlyReflectInvokes" # list of reflection generated invocations ONLY found in file1
DIFF_KEY_F2_ONLY_REFLECT_INVOKES = "f2OnlyReflectInvokes" # list of reflection generated invocations ONLY found in file2
DIFF_KEY_F1_ONLY_REFLECT_INVOKE_COUNT = "f1OnlyReflectInvokeCount" # count of reflection generated invocations ONLY found in file1
DIFF_KEY_F2_ONLY_REFLECT_INVOKE_COUNT = "f2OnlyReflectInvokeCount" # count of reflection generated invocations ONLY found in file2
DIFF_KEY_F1_ONLY_REFLECT_INVOKE_FREQ_COUNT = "f1OnlyReflectInvokeFreqCount" # count of frequencies for reflection generated invocations ONLY found in file1
DIFF_KEY_F2_ONLY_REFLECT_INVOKE_FREQ_COUNT = "f2OnlyReflectInvokeFreqCount" # count of frequencies for reflection generated invocations ONLY found in file2